import os
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional

import yaml
import requests
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import io
import argparse

FRED_SERIES = ["M2SL", "WALCL", "RRPONTSYD", "PCEPILFE", "BAMLH0A0HYM2"]
YAHOO_TICKERS = {
    "DXY": ["DX-Y.NYB", "DX=F"],
    "TNX": ["^TNX"],  # 10-year yield (percentage)
    "VIX": ["^VIX"],
    "NDX": ["^NDX"],
    "BTCUSD": ["BTC-USD"],
    "GOLD": ["XAUUSD=X", "GC=F"],
}

HISTORY_DAYS = 365 * 5


def load_existing():
    if os.path.exists("data.yml"):
        with open("data.yml", "r") as f:
            data = yaml.safe_load(f) or []
        # migrate old dict format to list
        if isinstance(data, dict):
            data = [data]
        return data
    return []

def _to_date_index(df: pd.DataFrame, date_col: str = None) -> pd.DataFrame:
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col]).dt.tz_localize(None)
        df = df.set_index(date_col)
    df.index = pd.to_datetime(df.index).tz_localize(None)
    # normalize to date (no time)
    df.index = df.index.normalize()
    return df

def get_fred(series_id):
    try:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        df = pd.read_csv(url)
        col = df.columns[-1]
        return float(df.iloc[-1][col])
    except Exception:
        return None

def get_fred_history(series_id: str, start: date) -> Optional[pd.Series]:
    try:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        res = requests.get(url, timeout=20)
        res.raise_for_status()
        # Some environments return bytes; decode to text
        text = res.text
        df = pd.read_csv(io.StringIO(text))
        col = df.columns[-1]
        # FRED returns either 'DATE' or 'observation_date'
        date_col = "DATE" if "DATE" in df.columns else ("observation_date" if "observation_date" in df.columns else None)
        if date_col is None:
            return None
        df = _to_date_index(df, date_col)
        # coerce numeric, drop missing
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        s = s[s.index.date >= start]
        return s
    except Exception:
        return None

def get_yahoo(symbols):
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            return float(hist["Close"].iloc[-1])
        except Exception:
            try:
                url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
                res = requests.get(url, timeout=10)
                res.raise_for_status()
                j = res.json()
                return float(j["quoteResponse"]["result"][0]["regularMarketPrice"])
            except Exception:
                continue
    return None

def get_yahoo_history(symbols: List[str], period: str = "5y") -> Optional[pd.Series]:
    # Try yfinance first for each candidate symbol, return first non-empty Series
    for symbol in symbols:
        try:
            t = yf.Ticker(symbol)
            hist = t.history(period=period, interval="1d")
            if not hist.empty and "Close" in hist:
                s = hist["Close"].copy()
                s = _to_date_index(s.to_frame()).iloc[:, 0]
                return s
        except Exception:
            continue
    # Fallback: none
    return None

def trim_history(records):
    cutoff = datetime.utcnow() - timedelta(days=HISTORY_DAYS)
    trimmed = [r for r in records if datetime.fromisoformat(r["timestamp"].replace("Z", "")) >= cutoff]
    return trimmed


def save_history(records):
    with open("data.yml", "w") as f:
        yaml.safe_dump(records, f, sort_keys=False)


def plot_history(records):
    df = pd.DataFrame(records)
    if "M2SL" not in df or df.get("M2SL") is None or pd.Series(df["M2SL"]).dropna().empty:
        return
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df.set_index("timestamp", inplace=True)
    plt.figure(figsize=(10, 6))
    plt.fill_between(df.index, df["M2SL"], color="skyblue", alpha=0.5)
    plt.plot(df.index, df["M2SL"], color="steelblue")
    plt.title(f"M2SL (last {HISTORY_DAYS // 365} years)")
    plt.xlabel("Date")
    plt.ylabel("M2SL")
    plt.tight_layout()
    plt.savefig("m2_area.png")
    plt.close()


def backfill_last_5y() -> List[Dict]:
    start = (datetime.utcnow() - timedelta(days=HISTORY_DAYS)).date()
    # Build a daily date index from start to today
    date_index = pd.date_range(start=start, end=datetime.utcnow().date(), freq="D")
    df = pd.DataFrame(index=date_index)

    # FRED series
    for sid in FRED_SERIES:
        s = get_fred_history(sid, start)
        if s is not None and not s.empty:
            df[sid] = s
    # Yahoo series
    for name, symbols in YAHOO_TICKERS.items():
        s = get_yahoo_history(symbols, period="5y")
        if s is None or s.empty:
            continue
        if name == "TNX":
            s = s / 10.0
        df[name] = s

    # Sort columns for stability
    df = df.sort_index()
    # Ensure all expected columns exist so schema is stable
    for sid in FRED_SERIES:
        if sid not in df.columns:
            df[sid] = pd.Series(index=df.index, dtype=float)
    for name in YAHOO_TICKERS.keys():
        if name not in df.columns:
            df[name] = pd.Series(index=df.index, dtype=float)

    # Forward-fill to daily frequency where needed, then backfill leading NaNs
    df = df.sort_index().ffill().bfill()

    # Drop days where everything is NaN (shouldn't happen if at least one series present)
    df = df.dropna(how="all")

    # Convert to list of dicts with ISO timestamps
    records: List[Dict] = []
    for idx, row in df.iterrows():
        entry = {k: (None if pd.isna(v) else float(v)) for k, v in row.items()}
        # timestamp at 00:00:00Z of the day
        ts = datetime.combine(idx.date(), datetime.min.time()).isoformat() + "Z"
        entry["timestamp"] = ts
        records.append(entry)
    # Trim to ensure exactly last N days
    records = trim_history(records)
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backfill", action="store_true", help="Rebuild data.yml with last 5y daily history")
    args = parser.parse_args()

    if args.backfill:
        records = backfill_last_5y()
        if not records:
            # Do not overwrite with empty history
            print("Backfill produced no records; leaving data.yml unchanged.")
            return
        save_history(records)
        plot_history(records)
        return

    # default: append latest snapshot
    records = load_existing()
    last = records[-1] if records else {}
    entry = {}
    for s in FRED_SERIES:
        value = get_fred(s)
        if value is None:
            value = last.get(s)
        entry[s] = value
    for name, symbols in YAHOO_TICKERS.items():
        value = get_yahoo(symbols)
        if name == "TNX" and value is not None:
            value = value / 10.0
        if value is None:
            value = last.get(name)
        entry[name] = value
    entry["timestamp"] = datetime.utcnow().isoformat() + "Z"
    records.append(entry)
    records = trim_history(records)
    save_history(records)
    plot_history(records)

if __name__ == "__main__":
    main()
