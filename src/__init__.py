"""Economic analysis system package."""

__version__ = "2.0.0"
__author__ = "Economic Ultrathink System"
__description__ = "Automated economic analysis and visualization system"

# Core modules
from .config import config
from .utils.logger import logger
from .data.fetcher import data_fetcher
from .visualization.components import viz_components
from .analysis.economic_insights import economic_analyzer

__all__ = [
    'config',
    'logger', 
    'data_fetcher',
    'viz_components',
    'economic_analyzer'
]