"""Data fetching module for economic indicators."""

import requests
import pandas as pd
import yfinance as yf
import io
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Any
from ..config import config
from ..utils.logger import logger

class DataFetcher:
    """Centralized data fetching system for economic indicators."""
    
    def __init__(self):
        """Initialize data fetcher with configuration."""
        self.fred_config = config.api_settings['fred']
        self.yahoo_config = config.api_settings['yahoo']
    
    def fetch_fred_current(self, series_id: str) -> Optional[float]:
        """Fetch current value from FRED API."""
        try:
            url = f"{self.fred_config['base_url']}?id={series_id}"
            df = pd.read_csv(url)
            
            if df.empty:
                return None
                
            col = df.columns[-1]
            value = df.iloc[-1][col]
            
            # Handle non-numeric values
            if pd.isna(value) or value == '.':
                return None
            
            result = float(value)
            logger.data_fetch_success('FRED', series_id, result)
            return result
            
        except Exception as e:
            logger.data_fetch_error('FRED', series_id, str(e))
            return None
    
    def fetch_fred_history(self, series_id: str, start_date: date) -> Optional[pd.Series]:
        """Fetch historical data from FRED API."""
        try:
            url = f"{self.fred_config['base_url']}?id={series_id}"
            response = requests.get(url, timeout=self.fred_config['timeout'])
            response.raise_for_status()
            
            df = pd.read_csv(io.StringIO(response.text))
            col = df.columns[-1]
            
            # FRED returns either 'DATE' or 'observation_date'
            date_col = "DATE" if "DATE" in df.columns else (
                "observation_date" if "observation_date" in df.columns else None
            )
            
            if date_col is None:
                logger.data_fetch_error('FRED', series_id, "No date column found")
                return None
            
            df = self._to_date_index(df, date_col)
            
            # Convert to numeric and drop missing values
            series = pd.to_numeric(df[col], errors="coerce").dropna()
            
            # Filter by start date
            series = series[series.index.date >= start_date]
            
            logger.data_fetch_success('FRED', f"{series_id}_history", len(series))
            return series
            
        except Exception as e:
            logger.data_fetch_error('FRED', f"{series_id}_history", str(e))
            return None
    
    def fetch_yahoo_current(self, symbols: List[str]) -> Optional[float]:
        """Fetch current value from Yahoo Finance."""
        for symbol in symbols:
            try:
                # Try yfinance first
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1d")
                
                if not hist.empty and "Close" in hist:
                    result = float(hist["Close"].iloc[-1])
                    logger.data_fetch_success('Yahoo', symbol, result)
                    return result
                    
            except Exception:
                # Try direct API fallback
                try:
                    url = f"{self.yahoo_config['fallback_url']}?symbols={symbol}"
                    response = requests.get(url, timeout=self.yahoo_config['timeout'])
                    response.raise_for_status()
                    
                    data = response.json()
                    if data.get("quoteResponse", {}).get("result"):
                        result = float(data["quoteResponse"]["result"][0]["regularMarketPrice"])
                        logger.data_fetch_success('Yahoo', symbol, result)
                        return result
                        
                except Exception as e:
                    logger.data_fetch_error('Yahoo', symbol, str(e))
                    continue
        
        logger.data_fetch_error('Yahoo', str(symbols), "All symbols failed")
        return None
    
    def fetch_yahoo_history(self, symbols: List[str], period: str = "5y") -> Optional[pd.Series]:
        """Fetch historical data from Yahoo Finance."""
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period, interval="1d")
                
                if not hist.empty and "Close" in hist:
                    series = hist["Close"].copy()
                    series = self._to_date_index(series.to_frame()).iloc[:, 0]
                    
                    logger.data_fetch_success('Yahoo', f"{symbol}_history", len(series))
                    return series
                    
            except Exception as e:
                logger.data_fetch_error('Yahoo', f"{symbol}_history", str(e))
                continue
        
        logger.data_fetch_error('Yahoo', f"{symbols}_history", "All symbols failed")
        return None
    
    def fetch_all_current(self, fallback_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Fetch current values for all configured indicators."""
        results = {}
        fallback = fallback_data or {}
        
        # Fetch FRED series
        logger.data_fetch_start('FRED', list(config.fred_series.keys()))
        for series_id, indicator_config in config.fred_series.items():
            value = self.fetch_fred_current(series_id)
            
            # Apply scaling if configured
            if value is not None and indicator_config.get('display_scale', 1) != 1:
                value = value * indicator_config['display_scale']
            
            # Use fallback if fetch failed
            if value is None and fallback:
                value = fallback.get(series_id)
                if value is not None:
                    logger.info(f"🔄 Using fallback for {series_id}: {value}")
            
            results[series_id] = value
        
        # Fetch Yahoo tickers
        logger.data_fetch_start('Yahoo', list(config.yahoo_tickers.keys()))
        for ticker_id, ticker_config in config.yahoo_tickers.items():
            value = self.fetch_yahoo_current(ticker_config['symbols'])
            
            # Apply scaling if configured
            if value is not None and ticker_config.get('display_scale', 1) != 1:
                value = value * ticker_config['display_scale']
            
            # Use fallback if fetch failed
            if value is None and fallback:
                value = fallback.get(ticker_id)
                if value is not None:
                    logger.info(f"🔄 Using fallback for {ticker_id}: {value}")
            
            results[ticker_id] = value
        
        return results
    
    def fetch_all_history(self, start_date: date) -> pd.DataFrame:
        """Fetch historical data for all configured indicators."""
        # Create date index
        date_index = pd.date_range(start=start_date, end=datetime.now().date(), freq="D")
        df = pd.DataFrame(index=date_index)
        
        # Fetch FRED series
        logger.data_fetch_start('FRED', list(config.fred_series.keys()))
        for series_id, indicator_config in config.fred_series.items():
            series = self.fetch_fred_history(series_id, start_date)
            
            if series is not None and not series.empty:
                # Apply scaling
                if indicator_config.get('display_scale', 1) != 1:
                    series = series * indicator_config['display_scale']
                df[series_id] = series
        
        # Fetch Yahoo tickers
        logger.data_fetch_start('Yahoo', list(config.yahoo_tickers.keys()))
        for ticker_id, ticker_config in config.yahoo_tickers.items():
            series = self.fetch_yahoo_history(ticker_config['symbols'])
            
            if series is not None and not series.empty:
                # Apply scaling
                if ticker_config.get('display_scale', 1) != 1:
                    series = series * ticker_config['display_scale']
                df[ticker_id] = series
        
        # Ensure all expected columns exist
        for indicator in config.get_all_indicators():
            if indicator not in df.columns:
                df[indicator] = pd.Series(index=df.index, dtype=float)
        
        # Forward-fill and backfill
        df = df.sort_index().ffill().bfill()
        
        # Drop rows where everything is NaN
        df = df.dropna(how='all')
        
        logger.info(f"📊 Historical data fetched: {len(df)} days, {len(df.columns)} indicators")
        return df
    
    def _to_date_index(self, df: pd.DataFrame, date_col: str = None) -> pd.DataFrame:
        """Convert DataFrame to date index."""
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col]).dt.tz_localize(None)
            df = df.set_index(date_col)
        
        df.index = pd.to_datetime(df.index).tz_localize(None)
        df.index = df.index.normalize()  # Remove time component
        
        return df

# Global data fetcher instance
data_fetcher = DataFetcher()