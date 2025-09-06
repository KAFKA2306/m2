"""Configuration management for economic analysis system."""

import yaml
import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuration manager for economic indicators and analysis settings."""
    
    def __init__(self, config_path: str = None):
        """Initialize configuration from YAML file."""
        if config_path is None:
            config_path = Path(__file__).parent / "indicators.yml"
        
        with open(config_path, 'r') as f:
            self._config = yaml.safe_load(f)
    
    @property
    def fred_series(self) -> Dict[str, Any]:
        """Get FRED series configuration."""
        return self._config['fred_series']
    
    @property
    def yahoo_tickers(self) -> Dict[str, Any]:
        """Get Yahoo Finance ticker configuration."""
        return self._config['yahoo_tickers']
    
    @property
    def stock_variables(self) -> list:
        """Get list of stock (cumulative) variables."""
        return self._config['variable_types']['stock_variables']['variables']
    
    @property
    def flow_variables(self) -> list:
        """Get list of flow (rate/intensity) variables."""
        return self._config['variable_types']['flow_variables']['variables']
    
    @property
    def economic_regimes(self) -> Dict[str, Any]:
        """Get economic regime definitions."""
        return self._config['economic_regimes']
    
    @property
    def visualization_settings(self) -> Dict[str, Any]:
        """Get visualization configuration."""
        return self._config['visualization']
    
    @property
    def data_settings(self) -> Dict[str, Any]:
        """Get data configuration."""
        return self._config['data']
    
    @property
    def api_settings(self) -> Dict[str, Any]:
        """Get API configuration."""
        return self._config['apis']
    
    def get_indicator_config(self, indicator: str) -> Dict[str, Any]:
        """Get configuration for a specific indicator."""
        # Check FRED series first
        if indicator in self.fred_series:
            return {**self.fred_series[indicator], 'source': 'fred'}
        
        # Check Yahoo tickers
        if indicator in self.yahoo_tickers:
            return {**self.yahoo_tickers[indicator], 'source': 'yahoo'}
        
        raise KeyError(f"Indicator '{indicator}' not found in configuration")
    
    def get_indicators_by_category(self, category: str) -> Dict[str, Any]:
        """Get all indicators in a specific category."""
        indicators = {}
        
        # Check FRED series
        for indicator, config in self.fred_series.items():
            if config.get('category') == category:
                indicators[indicator] = {**config, 'source': 'fred'}
        
        # Check Yahoo tickers
        for indicator, config in self.yahoo_tickers.items():
            if config.get('category') == category:
                indicators[indicator] = {**config, 'source': 'yahoo'}
        
        return indicators
    
    def get_all_indicators(self) -> list:
        """Get list of all configured indicators."""
        return list(self.fred_series.keys()) + list(self.yahoo_tickers.keys())

# Global configuration instance
config = Config()