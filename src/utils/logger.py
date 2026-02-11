"""Logging utilities for economic analysis system."""
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
class EconomicAnalysisLogger:
    """Centralized logging system for economic analysis pipeline."""
    def __init__(self, name: str = "economic_analysis", log_level: str = "INFO"):
        """Initialize logger with specified name and level."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        if not self.logger.handlers:
            self._setup_handlers()
    def _setup_handlers(self):
        """Set up console and file handlers."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        log_file = Path("logs") / f"economic_analysis_{datetime.now().strftime('%Y%m%d')}.log"
        log_file.parent.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        file_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(message, **kwargs)
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(message, **kwargs)
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(message, **kwargs)
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(message, **kwargs)
    def data_fetch_start(self, source: str, indicators: list):
        """Log start of data fetching."""
        self.info(f"🚀 Starting data fetch from {source}: {', '.join(indicators)}")
    def data_fetch_success(self, source: str, indicator: str, value: Optional[float]):
        """Log successful data fetch."""
        if value is not None:
            self.info(f"✅ {source} | {indicator}: {value}")
        else:
            self.warning(f"⚠️ {source} | {indicator}: No data returned")
    def data_fetch_error(self, source: str, indicator: str, error: str):
        """Log data fetch error."""
        self.error(f"❌ {source} | {indicator}: {error}")
    def visualization_start(self, viz_name: str):
        """Log start of visualization generation."""
        self.info(f"📊 Generating visualization: {viz_name}")
    def visualization_complete(self, viz_name: str, output_file: str):
        """Log completion of visualization."""
        self.info(f"✅ Visualization complete: {viz_name} → {output_file}")
    def analysis_insight(self, insight: str, value: Optional[float] = None):
        """Log analysis insight."""
        if value is not None:
            self.info(f"💡 {insight}: {value}")
        else:
            self.info(f"💡 {insight}")
    def performance_metric(self, metric: str, value: float, unit: str = ""):
        """Log performance metric."""
        self.info(f"📈 {metric}: {value:.2f} {unit}")
    def regime_transition(self, from_regime: str, to_regime: str, date: str):
        """Log regime transition."""
        self.info(f"🎭 Regime transition: {from_regime} → {to_regime} on {date}")
    def correlation_insight(self, var1: str, var2: str, correlation: float):
        """Log correlation insight."""
        strength = "Strong" if abs(correlation) > 0.7 else "Moderate" if abs(correlation) > 0.4 else "Weak"
        direction = "positive" if correlation > 0 else "negative"
        self.info(f"🔗 {var1} ↔ {var2}: {correlation:.3f} ({strength} {direction})")
    def economic_summary(self, period: str, key_metrics: dict):
        """Log economic period summary."""
        self.info(f"📊 Economic Summary - {period}:")
        for metric, value in key_metrics.items():
            self.info(f"   • {metric}: {value}")
logger = EconomicAnalysisLogger()