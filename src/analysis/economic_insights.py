"""Economic analysis and insights generation."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta
from ..config import config
from ..utils.logger import logger

class EconomicAnalyzer:
    """Advanced economic analysis and insights generation."""
    
    def __init__(self):
        """Initialize economic analyzer with configuration."""
        self.regimes = config.economic_regimes
    
    def analyze_regime_transitions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze economic regime transitions and characteristics."""
        regime_analysis = {}
        
        for regime_key, regime_data in self.regimes.items():
            start_date = pd.Timestamp(regime_data['start'])
            end_date = pd.Timestamp(regime_data['end'])
            
            # Filter data for this regime
            regime_df = df[start_date:end_date]
            
            if regime_df.empty:
                continue
            
            regime_stats = {
                'period': f"{start_date.strftime('%Y-%m')} to {end_date.strftime('%Y-%m')}",
                'duration_days': len(regime_df),
                'name': regime_data['name'],
                'description': regime_data['description'],
                'characteristics': regime_data['characteristics']
            }
            
            # Calculate key metrics for each regime
            for indicator in config.get_all_indicators():
                if indicator in regime_df.columns:
                    series = regime_df[indicator].dropna()
                    
                    if not series.empty and len(series) > 1:
                        start_value = series.iloc[0]
                        end_value = series.iloc[-1]
                        
                        if start_value != 0:
                            total_return = ((end_value - start_value) / start_value) * 100
                            regime_stats[f'{indicator}_return'] = total_return
                        
                        regime_stats[f'{indicator}_mean'] = series.mean()
                        regime_stats[f'{indicator}_volatility'] = series.std()
            
            regime_analysis[regime_key] = regime_stats
            
            logger.economic_summary(
                regime_data['name'],
                {
                    'Duration': f"{regime_stats['duration_days']} days",
                    'Bitcoin Return': f"{regime_stats.get('BTCUSD_return', 0):.1f}%" 
                        if 'BTCUSD_return' in regime_stats else "N/A",
                    'Avg VIX': f"{regime_stats.get('VIX_mean', 0):.1f}" 
                        if 'VIX_mean' in regime_stats else "N/A"
                }
            )
        
        return regime_analysis
    
    def calculate_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate and analyze structural correlations."""
        correlation_matrix = df.corr()
        
        # Extract top correlations
        correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                var1 = correlation_matrix.columns[i]
                var2 = correlation_matrix.columns[j]
                corr_value = correlation_matrix.iloc[i, j]
                
                if not pd.isna(corr_value):
                    correlations.append({
                        'var1': var1,
                        'var2': var2,
                        'correlation': corr_value,
                        'abs_correlation': abs(corr_value)
                    })
        
        # Sort by absolute correlation
        correlations.sort(key=lambda x: x['abs_correlation'], reverse=True)
        
        # Log top correlations
        for corr_data in correlations[:5]:
            logger.correlation_insight(
                corr_data['var1'],
                corr_data['var2'], 
                corr_data['correlation']
            )
        
        return {
            'correlation_matrix': correlation_matrix,
            'top_correlations': correlations[:10],
            'structural_relationships': self._identify_structural_relationships(correlations)
        }
    
    def analyze_performance_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze performance metrics and trends."""
        current_date = df.index[-1]
        
        # Recent performance (30 days vs previous 30 days)
        recent_30d = df.tail(30)
        previous_30d = df.iloc[-60:-30] if len(df) >= 60 else df.iloc[:30]
        
        performance_metrics = {}
        
        for indicator in config.get_all_indicators():
            if indicator in df.columns:
                indicator_config = config.get_indicator_config(indicator)
                
                # Current value
                current_value = df[indicator].iloc[-1]
                
                # Total return since start
                start_value = df[indicator].dropna().iloc[0]
                if start_value != 0:
                    total_return = ((current_value - start_value) / start_value) * 100
                else:
                    total_return = 0
                
                # Recent performance
                recent_avg = recent_30d[indicator].mean()
                previous_avg = previous_30d[indicator].mean()
                
                recent_change = 0
                if not pd.isna(recent_avg) and not pd.isna(previous_avg) and previous_avg != 0:
                    recent_change = ((recent_avg - previous_avg) / previous_avg) * 100
                
                # Volatility metrics
                returns = df[indicator].pct_change().dropna()
                if not returns.empty:
                    volatility = returns.std() * np.sqrt(252) * 100  # Annualized
                    max_drawdown = self._calculate_max_drawdown(df[indicator])
                else:
                    volatility = 0
                    max_drawdown = 0
                
                performance_metrics[indicator] = {
                    'current_value': current_value,
                    'total_return': total_return,
                    'recent_30d_change': recent_change,
                    'volatility': volatility,
                    'max_drawdown': max_drawdown,
                    'category': indicator_config.get('category', 'unknown'),
                    'name': indicator_config.get('name', indicator)
                }
                
                logger.performance_metric(
                    f"{indicator} Total Return", 
                    total_return, 
                    "%"
                )
        
        return performance_metrics
    
    def detect_market_regime(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect current market regime based on key indicators."""
        recent_data = df.tail(30)  # Last 30 days
        
        regime_indicators = {}
        
        # VIX levels (fear/complacency)
        if 'VIX' in recent_data.columns:
            avg_vix = recent_data['VIX'].mean()
            if avg_vix > 30:
                vix_regime = "High Stress"
            elif avg_vix > 20:
                vix_regime = "Elevated Risk"  
            else:
                vix_regime = "Complacent"
            
            regime_indicators['volatility'] = {
                'level': avg_vix,
                'regime': vix_regime
            }
        
        # Interest rate environment
        if 'TNX' in recent_data.columns:
            avg_yield = recent_data['TNX'].mean() * 100  # Convert to percentage
            if avg_yield > 5:
                rate_regime = "Restrictive"
            elif avg_yield > 3:
                rate_regime = "Neutral"
            else:
                rate_regime = "Accommodative"
            
            regime_indicators['interest_rates'] = {
                'level': avg_yield,
                'regime': rate_regime
            }
        
        # Credit conditions  
        if 'BAMLH0A0HYM2' in recent_data.columns:
            avg_spread = recent_data['BAMLH0A0HYM2'].mean()
            if avg_spread > 6:
                credit_regime = "Stress"
            elif avg_spread > 4:
                credit_regime = "Caution"
            else:
                credit_regime = "Benign"
            
            regime_indicators['credit'] = {
                'level': avg_spread,
                'regime': credit_regime
            }
        
        # Asset momentum (risk-on/risk-off)
        risk_assets = ['NDX', 'BTCUSD']
        momentum_scores = []
        
        for asset in risk_assets:
            if asset in df.columns:
                # 30-day return
                asset_30d_return = (recent_data[asset].iloc[-1] / recent_data[asset].iloc[0] - 1) * 100
                momentum_scores.append(asset_30d_return)
        
        if momentum_scores:
            avg_momentum = np.mean(momentum_scores)
            if avg_momentum > 5:
                momentum_regime = "Risk-On"
            elif avg_momentum < -5:
                momentum_regime = "Risk-Off"
            else:
                momentum_regime = "Neutral"
            
            regime_indicators['momentum'] = {
                'level': avg_momentum,
                'regime': momentum_regime
            }
        
        return regime_indicators
    
    def generate_economic_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive economic insights."""
        logger.info("🧠 Generating economic insights...")
        
        insights = {
            'data_overview': {
                'period': f"{df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}",
                'total_days': len(df),
                'indicators': len(df.columns)
            },
            'regime_analysis': self.analyze_regime_transitions(df),
            'correlations': self.calculate_correlations(df),
            'performance': self.analyze_performance_metrics(df),
            'current_regime': self.detect_market_regime(df),
            'key_insights': self._generate_key_insights(df)
        }
        
        logger.analysis_insight(f"Analysis complete for {len(df)} data points")
        return insights
    
    def _calculate_max_drawdown(self, series: pd.Series) -> float:
        """Calculate maximum drawdown for a time series."""
        if series.empty:
            return 0
        
        peak = series.expanding().max()
        drawdown = (series - peak) / peak
        max_drawdown = drawdown.min() * 100  # Convert to percentage
        
        return max_drawdown
    
    def _identify_structural_relationships(self, correlations: List[Dict]) -> Dict[str, str]:
        """Identify key structural economic relationships."""
        relationships = {}
        
        # Look for key economic relationships
        for corr_data in correlations:
            var1, var2 = corr_data['var1'], corr_data['var2']
            corr_value = corr_data['correlation']
            
            # Fisher Effect (inflation-interest rates)
            if set([var1, var2]) == set(['PCEPILFE', 'TNX']) and corr_value > 0.8:
                relationships['fisher_effect'] = f"Strong positive correlation ({corr_value:.3f}) confirms Fisher Effect"
            
            # Risk-on correlation (stocks-crypto)
            if set([var1, var2]) == set(['NDX', 'BTCUSD']) and corr_value > 0.8:
                relationships['risk_on'] = f"High correlation ({corr_value:.3f}) indicates risk-on behavior convergence"
            
            # Monetary policy coordination
            if set([var1, var2]) == set(['WALCL', 'RRPONTSYD']) and corr_value > 0.7:
                relationships['monetary_policy'] = f"Fed balance sheet and repo ops coordination ({corr_value:.3f})"
            
            # Safe haven competition
            if set([var1, var2]) == set(['DXY', 'GOLD']):
                if corr_value < -0.3:
                    relationships['safe_haven'] = f"Negative correlation ({corr_value:.3f}) shows dollar-gold competition"
                elif corr_value > 0.3:
                    relationships['safe_haven'] = f"Positive correlation ({corr_value:.3f}) shows safe haven convergence"
        
        return relationships
    
    def _generate_key_insights(self, df: pd.DataFrame) -> List[str]:
        """Generate key narrative insights."""
        insights = []
        
        # Bitcoin performance insight
        if 'BTCUSD' in df.columns:
            btc_start = df['BTCUSD'].dropna().iloc[0]
            btc_current = df['BTCUSD'].iloc[-1]
            btc_return = ((btc_current - btc_start) / btc_start) * 100
            
            if btc_return > 500:
                insights.append(f"Bitcoin demonstrates exceptional wealth creation with {btc_return:.0f}% total return")
        
        # Monetary policy insight
        if 'M2SL' in df.columns and 'WALCL' in df.columns:
            m2_change = (df['M2SL'].iloc[-1] - df['M2SL'].iloc[0]) / df['M2SL'].iloc[0] * 100
            fed_change = (df['WALCL'].iloc[-1] - df['WALCL'].iloc[0]) / df['WALCL'].iloc[0] * 100
            
            if m2_change > 10 and fed_change < 0:
                insights.append("Money supply growth continues while Fed balance sheet normalizes")
        
        # Volatility insight
        if 'VIX' in df.columns:
            recent_vix = df['VIX'].tail(30).mean()
            if recent_vix < 20:
                insights.append(f"Low volatility environment (VIX: {recent_vix:.1f}) suggests market complacency")
        
        # Correlation insight
        if 'NDX' in df.columns and 'BTCUSD' in df.columns:
            correlation = df[['NDX', 'BTCUSD']].corr().iloc[0, 1]
            if correlation > 0.8:
                insights.append(f"Strong NASDAQ-Bitcoin correlation ({correlation:.2f}) indicates institutional adoption")
        
        return insights

# Global economic analyzer instance
economic_analyzer = EconomicAnalyzer()