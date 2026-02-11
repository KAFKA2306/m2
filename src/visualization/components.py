"""Reusable visualization components for economic analysis."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import matplotlib.dates as mdates
from ..config import config
from ..utils.logger import logger
class VisualizationComponents:
    """Reusable components for creating economic visualizations."""
    def __init__(self):
        """Initialize visualization components with configuration."""
        self.viz_config = config.visualization_settings
        plt.style.use(self.viz_config['style'])
        plt.rcParams['figure.dpi'] = self.viz_config['figure_dpi']
        plt.rcParams['figure.facecolor'] = self.viz_config['colors']['background']
    def create_stacked_area_chart(
        self, 
        df: pd.DataFrame, 
        variables: List[str],
        title: str,
        ylabel: str,
        ax: Optional[plt.Axes] = None,
        colors: Optional[List[str]] = None
    ) -> plt.Axes:
        """Create stacked area chart for cumulative variables."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 8))
        if colors is None:
            colors = [config.get_indicator_config(var).get('color', '
                     for var in variables]
        bottom = np.zeros(len(df))
        for i, (var, color) in enumerate(zip(variables, colors)):
            if var in df.columns:
                values = df[var].fillna(0).values
                ax.fill_between(df.index, bottom, bottom + values, 
                              alpha=0.7, color=color, 
                              label=config.get_indicator_config(var)['name'])
                bottom += values
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.legend(loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        logger.visualization_start(f"Stacked area chart: {title}")
        return ax
    def create_time_series_plot(
        self,
        df: pd.DataFrame,
        variables: List[str],
        title: str,
        ylabel: str,
        ax: Optional[plt.Axes] = None,
        normalize: bool = False,
        log_scale: bool = False
    ) -> plt.Axes:
        """Create time series plot for flow variables."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 8))
        for var in variables:
            if var in df.columns:
                indicator_config = config.get_indicator_config(var)
                data = df[var].dropna()
                if normalize and not data.empty:
                    data = (data / data.iloc[0]) * 100
                ax.plot(data.index, data.values,
                       label=indicator_config['name'],
                       color=indicator_config.get('color', '
                       linewidth=2, alpha=0.8)
        if log_scale:
            ax.set_yscale('log')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.legend(framealpha=0.9)
        ax.grid(True, alpha=0.3)
        logger.visualization_start(f"Time series plot: {title}")
        return ax
    def add_regime_backgrounds(
        self, 
        ax: plt.Axes, 
        regimes: Optional[Dict] = None
    ) -> plt.Axes:
        """Add economic regime background shading."""
        if regimes is None:
            regimes = config.economic_regimes
        for regime_key, regime_data in regimes.items():
            start = pd.Timestamp(regime_data['start'])
            end = pd.Timestamp(regime_data['end'])
            ax.axvspan(start, end, 
                      alpha=0.15, 
                      color=regime_data['color'],
                      label=regime_data['name'] if regime_key == list(regimes.keys())[0] else "")
        return ax
    def create_correlation_heatmap(
        self,
        df: pd.DataFrame,
        title: str = "Correlation Matrix",
        figsize: Tuple[int, int] = (12, 10),
        mask_upper: bool = True
    ) -> Tuple[plt.Figure, plt.Axes]:
        """Create correlation heatmap with economic groupings."""
        fig, ax = plt.subplots(figsize=figsize)
        correlation_matrix = df.corr()
        mask = None
        if mask_upper:
            mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        colors = ['
        cmap = sns.blend_palette(colors, n_colors=100, as_cmap=True)
        sns.heatmap(correlation_matrix, 
                   mask=mask,
                   annot=True, 
                   cmap=cmap, 
                   center=0,
                   square=True, 
                   fmt='.2f',
                   cbar_kws={'shrink': 0.8, 'label': 'Correlation Coefficient'},
                   ax=ax, 
                   linewidths=0.5)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        logger.visualization_start(f"Correlation heatmap: {title}")
        return fig, ax
    def create_performance_comparison(
        self,
        df: pd.DataFrame,
        assets: List[str],
        title: str = "Asset Performance Comparison",
        normalize_start: float = 100,
        figsize: Tuple[int, int] = (14, 8)
    ) -> Tuple[plt.Figure, plt.Axes]:
        """Create normalized performance comparison chart."""
        fig, ax = plt.subplots(figsize=figsize)
        for asset in assets:
            if asset in df.columns:
                indicator_config = config.get_indicator_config(asset)
                data = df[asset].dropna()
                if not data.empty:
                    normalized = (data / data.iloc[0]) * normalize_start
                    ax.plot(normalized.index, normalized.values,
                           label=indicator_config['name'],
                           color=indicator_config.get('color', '
                           linewidth=2.5, alpha=0.9)
                    ax.fill_between(normalized.index, normalize_start, normalized.values,
                                   alpha=0.15, color=indicator_config.get('color', '
        ax.axhline(y=normalize_start, color='black', linestyle='--', alpha=0.7, linewidth=1)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel(f'Normalized Performance\\n(Start = {normalize_start})', 
                     fontsize=12, fontweight='bold')
        ax.legend(framealpha=0.9)
        ax.set_yscale('log')
        ax.grid(True, alpha=0.3)
        logger.visualization_start(f"Performance comparison: {title}")
        return fig, ax
    def create_volatility_analysis(
        self,
        df: pd.DataFrame,
        asset: str,
        window: int = 30,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 8)
    ) -> Tuple[plt.Figure, plt.Axes]:
        """Create volatility analysis chart."""
        fig, ax = plt.subplots(figsize=figsize)
        if title is None:
            title = f"{config.get_indicator_config(asset)['name']} Volatility Analysis"
        if asset in df.columns:
            returns = df[asset].pct_change().dropna()
            volatility = returns.rolling(window=window).std() * np.sqrt(252) * 100
            indicator_config = config.get_indicator_config(asset)
            color = indicator_config.get('color', '
            ax.plot(volatility.index, volatility.values, 
                   color=color, linewidth=2, alpha=0.8,
                   label=f'{window}-Day Rolling Volatility')
            mean_vol = volatility.mean()
            ax.axhline(y=mean_vol, color=color, linestyle='--', alpha=0.6, 
                      label=f'Mean: {mean_vol:.1f}%')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel('Annualized Volatility (%)', fontsize=12, fontweight='bold')
        ax.legend(framealpha=0.9)
        ax.grid(True, alpha=0.3)
        logger.visualization_start(f"Volatility analysis: {title}")
        return fig, ax
    def create_risk_gauge(
        self,
        df: pd.DataFrame,
        risk_var: str = 'VIX',
        title: str = "Market Risk Gauge",
        thresholds: Dict[str, float] = None,
        figsize: Tuple[int, int] = (12, 6)
    ) -> Tuple[plt.Figure, plt.Axes]:
        """Create risk gauge visualization."""
        fig, ax = plt.subplots(figsize=figsize)
        if thresholds is None:
            thresholds = {'low': 15, 'medium': 25, 'high': 35}
        if risk_var in df.columns:
            data = df[risk_var].dropna()
            low_risk = data <= thresholds['low']
            medium_risk = (data > thresholds['low']) & (data <= thresholds['medium'])
            high_risk = data > thresholds['medium']
            ax.fill_between(data.index, 0, data.values,
                           where=low_risk, color='green', alpha=0.4, 
                           label=f'Low Risk (<{thresholds["low"]})')
            ax.fill_between(data.index, 0, data.values,
                           where=medium_risk, color='orange', alpha=0.4,
                           label=f'Medium Risk ({thresholds["low"]}-{thresholds["medium"]})')
            ax.fill_between(data.index, 0, data.values,
                           where=high_risk, color='red', alpha=0.4,
                           label=f'High Risk (>{thresholds["medium"]})')
            ax.plot(data.index, data.values, color='black', linewidth=2, alpha=0.8)
            for level, value in thresholds.items():
                ax.axhline(y=value, color='gray', linestyle='--', alpha=0.6)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel(config.get_indicator_config(risk_var)['name'], 
                     fontsize=12, fontweight='bold')
        ax.legend(framealpha=0.9)
        ax.grid(True, alpha=0.3)
        logger.visualization_start(f"Risk gauge: {title}")
        return fig, ax
    def save_figure(
        self, 
        fig: plt.Figure, 
        filename: str, 
        title: Optional[str] = None
    ) -> str:
        """Save figure with consistent settings."""
        output_file = f"{filename}.png"
        fig.savefig(output_file, 
                   dpi=self.viz_config['figure_dpi'], 
                   bbox_inches='tight',
                   facecolor=self.viz_config['colors']['background'])
        if title:
            logger.visualization_complete(title, output_file)
        return output_file
viz_components = VisualizationComponents()