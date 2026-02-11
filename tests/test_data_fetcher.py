"""Tests for data fetching module."""
import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from datetime import date, datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from data.fetcher import DataFetcher
from config import config
class TestDataFetcher:
    """Test suite for DataFetcher class."""
    def setup_method(self):
        """Set up test fixtures."""
        self.fetcher = DataFetcher()
    def test_init(self):
        """Test DataFetcher initialization."""
        assert self.fetcher.fred_config == config.api_settings['fred']
        assert self.fetcher.yahoo_config == config.api_settings['yahoo']
    @patch('data.fetcher.pd.read_csv')
    def test_fetch_fred_current_success(self, mock_read_csv):
        """Test successful FRED data fetch."""
        mock_df = pd.DataFrame({
            'DATE': ['2023-01-01', '2023-01-02'],
            'M2SL': [20000.0, 20100.0]
        })
        mock_read_csv.return_value = mock_df
        result = self.fetcher.fetch_fred_current('M2SL')
        assert result == 20100.0
        mock_read_csv.assert_called_once()
    @patch('data.fetcher.pd.read_csv')
    def test_fetch_fred_current_failure(self, mock_read_csv):
        """Test FRED data fetch failure."""
        mock_read_csv.side_effect = Exception("Connection error")
        result = self.fetcher.fetch_fred_current('M2SL')
        assert result is None
    @patch('data.fetcher.pd.read_csv')
    def test_fetch_fred_current_empty_data(self, mock_read_csv):
        """Test FRED fetch with empty data."""
        mock_df = pd.DataFrame()
        mock_read_csv.return_value = mock_df
        result = self.fetcher.fetch_fred_current('M2SL')
        assert result is None
    @patch('data.fetcher.requests.get')
    def test_fetch_fred_history_success(self, mock_get):
        """Test successful FRED history fetch."""
        mock_response = Mock()
        mock_response.text = "DATE,M2SL\\n2023-01-01,20000.0\\n2023-01-02,20100.0"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        start_date = date(2023, 1, 1)
        result = self.fetcher.fetch_fred_history('M2SL', start_date)
        assert isinstance(result, pd.Series)
        assert len(result) > 0
        mock_get.assert_called_once()
    @patch('data.fetcher.yf.Ticker')
    def test_fetch_yahoo_current_success(self, mock_ticker_class):
        """Test successful Yahoo Finance data fetch."""
        mock_ticker = Mock()
        mock_history = pd.DataFrame({
            'Close': [100.0, 105.0]
        })
        mock_ticker.history.return_value = mock_history
        mock_ticker_class.return_value = mock_ticker
        result = self.fetcher.fetch_yahoo_current(['AAPL'])
        assert result == 105.0
    @patch('data.fetcher.yf.Ticker')
    @patch('data.fetcher.requests.get')
    def test_fetch_yahoo_current_fallback(self, mock_requests, mock_ticker_class):
        """Test Yahoo Finance fallback API."""
        mock_ticker = Mock()
        mock_ticker.history.side_effect = Exception("yfinance error")
        mock_ticker_class.return_value = mock_ticker
        mock_response = Mock()
        mock_response.json.return_value = {
            "quoteResponse": {
                "result": [{"regularMarketPrice": 110.0}]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        result = self.fetcher.fetch_yahoo_current(['AAPL'])
        assert result == 110.0
    @patch('data.fetcher.yf.Ticker')
    def test_fetch_yahoo_history_success(self, mock_ticker_class):
        """Test successful Yahoo Finance history fetch."""
        mock_ticker = Mock()
        mock_history = pd.DataFrame({
            'Close': [100.0, 105.0, 110.0]
        }, index=pd.date_range('2023-01-01', periods=3, freq='D'))
        mock_ticker.history.return_value = mock_history
        mock_ticker_class.return_value = mock_ticker
        result = self.fetcher.fetch_yahoo_history(['AAPL'])
        assert isinstance(result, pd.Series)
        assert len(result) == 3
    @patch.object(DataFetcher, 'fetch_fred_current')
    @patch.object(DataFetcher, 'fetch_yahoo_current')
    def test_fetch_all_current(self, mock_yahoo, mock_fred):
        """Test fetching all current indicators."""
        mock_fred.return_value = 20000.0
        mock_yahoo.return_value = 100.0
        result = self.fetcher.fetch_all_current()
        assert isinstance(result, dict)
        assert len(result) > 0
        for series_id in config.fred_series.keys():
            assert series_id in result
        for ticker_id in config.yahoo_tickers.keys():
            assert ticker_id in result
    def test_fetch_all_current_with_fallback(self):
        """Test fetch with fallback data."""
        fallback_data = {
            'M2SL': 19500.0,
            'BTCUSD': 45000.0
        }
        with patch.object(self.fetcher, 'fetch_fred_current', return_value=None), \
             patch.object(self.fetcher, 'fetch_yahoo_current', return_value=None):
            result = self.fetcher.fetch_all_current(fallback_data)
            assert result['M2SL'] == 19500.0
            assert result['BTCUSD'] == 45000.0
    def test_to_date_index(self):
        """Test date index conversion."""
        df = pd.DataFrame({
            'DATE': ['2023-01-01', '2023-01-02'],
            'VALUE': [100, 110]
        })
        result = self.fetcher._to_date_index(df, 'DATE')
        assert isinstance(result.index, pd.DatetimeIndex)
        assert len(result) == 2
        assert result.index[0].time() == datetime.min.time()
class TestDataIntegration:
    """Integration tests for data fetching."""
    def test_config_indicators_exist(self):
        """Test that all configured indicators are accessible."""
        for series_id in config.fred_series.keys():
            indicator_config = config.get_indicator_config(series_id)
            assert 'name' in indicator_config
            assert 'category' in indicator_config
        for ticker_id in config.yahoo_tickers.keys():
            indicator_config = config.get_indicator_config(ticker_id)
            assert 'name' in indicator_config
            assert 'symbols' in indicator_config
    def test_all_indicators_list(self):
        """Test getting all indicators."""
        all_indicators = config.get_all_indicators()
        assert len(all_indicators) > 0
        assert 'M2SL' in all_indicators
        assert 'BTCUSD' in all_indicators
    def test_indicators_by_category(self):
        """Test getting indicators by category."""
        monetary_policy = config.get_indicators_by_category('monetary_policy')
        assert len(monetary_policy) > 0
        assert 'M2SL' in monetary_policy
        assert all('source' in config for config in monetary_policy.values())
if __name__ == '__main__':
    pytest.main([__file__])