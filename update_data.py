import os
from datetime import datetime, timedelta

import yaml
import requests
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

FRED_SERIES = ["M2SL", "WALCL", "RRPONTSYD", "PCEPILFE", "BAMLH0A0HYM2"]
YAHOO_TICKERS = {
    "DXY": ["DX-Y.NYB", "DX=F"],
    "TNX": ["^TNX"],  # 10-year yield (percentage)
    "VIX": ["^VIX"],
    "NDX": ["^NDX"],
    "BTCUSD": ["BTC-USD"],
    "GOLD": ["XAUUSD=X", "GC=F"],
}

HISTORY_DAYS = 365 * 3


def load_existing():
    if os.path.exists("data.yml"):
        with open("data.yml", "r") as f:
            data = yaml.safe_load(f) or []
        # migrate old dict format to list
        if isinstance(data, dict):
            data = [data]
        return data
    return []

def get_fred(series_id):
    try:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        df = pd.read_csv(url)
        col = df.columns[-1]
        return float(df.iloc[-1][col])
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

def trim_history(records):
    cutoff = datetime.utcnow() - timedelta(days=HISTORY_DAYS)
    trimmed = [r for r in records if datetime.fromisoformat(r["timestamp"].replace("Z", "")) >= cutoff]
    return trimmed


def save_history(records):
    with open("data.yml", "w") as f:
        yaml.safe_dump(records, f, sort_keys=False)


def plot_history(records):
    df = pd.DataFrame(records)
    if "M2SL" not in df:
        return
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df.set_index("timestamp", inplace=True)
    plt.figure(figsize=(10, 6))
    plt.fill_between(df.index, df["M2SL"], color="skyblue", alpha=0.5)
    plt.plot(df.index, df["M2SL"], color="steelblue")
    plt.title("M2SL (last 3 years)")
    plt.xlabel("Date")
    plt.ylabel("M2SL")
    plt.tight_layout()
    plt.savefig("m2_area.png")
    plt.close()


def main():
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
