#!/usr/bin/env python3

import yaml
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def load_data():
    """Load and preprocess the data from data.yml"""
    with open('data.yml', 'r') as f:
        data = yaml.safe_load(f)
    
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    
    # Clean data - remove any rows with all NaN
    df = df.dropna(how='all')
    
    return df

def create_time_series_overview(df):
    """Create comprehensive time series overview"""
    fig, axes = plt.subplots(4, 3, figsize=(20, 16))
    fig.suptitle('Economic & Financial Indicators Overview (2020-2025)', fontsize=20, fontweight='bold')
    
    # Define plot configurations
    plots = [
        ('M2SL', 'Money Supply M2', 'Money Supply (Billions)', 'blue'),
        ('WALCL', 'Fed Assets', 'Assets (Millions)', 'green'),  
        ('RRPONTSYD', 'Reverse Repo Rate', 'Rate (%)', 'red'),
        ('PCEPILFE', 'Core PCE Price Index', 'Index', 'purple'),
        ('BAMLH0A0HYM2', 'High Yield Spread', 'Spread (%)', 'orange'),
        ('DXY', 'US Dollar Index', 'Index', 'brown'),
        ('TNX', '10-Year Treasury', 'Yield (%)', 'pink'),
        ('VIX', 'Volatility Index', 'VIX', 'gray'),
        ('NDX', 'NASDAQ 100', 'Index', 'cyan'),
        ('BTCUSD', 'Bitcoin Price', 'Price (USD)', 'gold'),
        ('GOLD', 'Gold Price', 'Price (USD)', 'darkgoldenrod')
    ]
    
    for i, (col, title, ylabel, color) in enumerate(plots):
        row, col_idx = i // 3, i % 3
        ax = axes[row, col_idx]
        
        if col in df.columns:
            series = df[col].dropna()
            ax.plot(series.index, series.values, color=color, linewidth=2, alpha=0.8)
            ax.fill_between(series.index, series.values, alpha=0.3, color=color)
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.set_ylabel(ylabel, fontsize=10)
            ax.tick_params(axis='x', rotation=45, labelsize=8)
            ax.tick_params(axis='y', labelsize=8)
            ax.grid(True, alpha=0.3)
    
    # Remove empty subplot
    if len(plots) < 12:
        axes[3, 2].remove()
    
    plt.tight_layout()
    plt.savefig('economic_indicators_overview.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_correlation_analysis(df):
    """Create correlation heatmap and analysis"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Correlation heatmap
    correlation_matrix = df.corr()
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    
    sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='RdYlBu_r', center=0,
                square=True, ax=ax1, fmt='.2f', cbar_kws={'shrink': 0.5})
    ax1.set_title('Correlation Matrix of Economic Indicators', fontsize=14, fontweight='bold')
    
    # Top correlations analysis
    corr_pairs = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr_pairs.append((
                correlation_matrix.columns[i],
                correlation_matrix.columns[j], 
                correlation_matrix.iloc[i, j]
            ))
    
    corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    
    # Plot top 10 correlations
    top_10 = corr_pairs[:10]
    labels = [f"{pair[0]}-{pair[1]}" for pair in top_10]
    values = [pair[2] for pair in top_10]
    colors = ['red' if v < 0 else 'green' for v in values]
    
    bars = ax2.barh(range(len(values)), values, color=colors, alpha=0.7)
    ax2.set_yticks(range(len(labels)))
    ax2.set_yticklabels(labels, fontsize=10)
    ax2.set_xlabel('Correlation Coefficient', fontsize=12)
    ax2.set_title('Top 10 Correlations Between Indicators', fontsize=14, fontweight='bold')
    ax2.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax2.text(val + (0.01 if val > 0 else -0.01), i, f'{val:.3f}', 
                va='center', ha='left' if val > 0 else 'right', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('correlation_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_economic_relationships(df):
    """Analyze key economic relationships"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Key Economic Relationships', fontsize=16, fontweight='bold')
    
    # 1. Money Supply vs Inflation (PCE)
    ax1 = axes[0, 0]
    if 'M2SL' in df.columns and 'PCEPILFE' in df.columns:
        ax1.scatter(df['M2SL'], df['PCEPILFE'], alpha=0.6, color='blue', s=20)
        z = np.polyfit(df['M2SL'].dropna(), df['PCEPILFE'].dropna(), 1)
        p = np.poly1d(z)
        ax1.plot(df['M2SL'].dropna(), p(df['M2SL'].dropna()), "r--", alpha=0.8)
        ax1.set_xlabel('Money Supply M2')
        ax1.set_ylabel('Core PCE Price Index')
        ax1.set_title('Money Supply vs Inflation')
    
    # 2. Bond Yield vs High Yield Spread
    ax2 = axes[0, 1]
    if 'TNX' in df.columns and 'BAMLH0A0HYM2' in df.columns:
        ax2.scatter(df['TNX'], df['BAMLH0A0HYM2'], alpha=0.6, color='green', s=20)
        z = np.polyfit(df['TNX'].dropna(), df['BAMLH0A0HYM2'].dropna(), 1)
        p = np.poly1d(z)
        ax2.plot(df['TNX'].dropna(), p(df['TNX'].dropna()), "r--", alpha=0.8)
        ax2.set_xlabel('10-Year Treasury Yield')
        ax2.set_ylabel('High Yield Spread')
        ax2.set_title('Risk-Free Rate vs Credit Spread')
    
    # 3. VIX vs Stock Market (NDX)
    ax3 = axes[1, 0]
    if 'VIX' in df.columns and 'NDX' in df.columns:
        ax3.scatter(df['VIX'], df['NDX'], alpha=0.6, color='red', s=20)
        z = np.polyfit(df['VIX'].dropna(), df['NDX'].dropna(), 1)
        p = np.poly1d(z)
        ax3.plot(df['VIX'].dropna(), p(df['VIX'].dropna()), "r--", alpha=0.8)
        ax3.set_xlabel('VIX (Volatility)')
        ax3.set_ylabel('NASDAQ 100 Index')
        ax3.set_title('Market Volatility vs Stock Prices')
    
    # 4. Dollar Index vs Gold
    ax4 = axes[1, 1]
    if 'DXY' in df.columns and 'GOLD' in df.columns:
        ax4.scatter(df['DXY'], df['GOLD'], alpha=0.6, color='gold', s=20)
        z = np.polyfit(df['DXY'].dropna(), df['GOLD'].dropna(), 1)
        p = np.poly1d(z)
        ax4.plot(df['DXY'].dropna(), p(df['DXY'].dropna()), "r--", alpha=0.8)
        ax4.set_xlabel('US Dollar Index')
        ax4.set_ylabel('Gold Price')
        ax4.set_title('Dollar Strength vs Gold Price')
    
    plt.tight_layout()
    plt.savefig('economic_relationships.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_performance_dashboard(df):
    """Create performance dashboard with key metrics"""
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
    
    # Calculate recent performance (last 30 days vs previous 30 days)
    recent_30d = df.tail(30)
    previous_30d = df.iloc[-60:-30]
    
    # Key metrics summary
    ax_summary = fig.add_subplot(gs[0, :])
    ax_summary.axis('off')
    
    # Calculate percentage changes
    metrics = {}
    for col in df.columns:
        if col in recent_30d.columns and col in previous_30d.columns:
            recent_avg = recent_30d[col].mean()
            previous_avg = previous_30d[col].mean() 
            if not pd.isna(recent_avg) and not pd.isna(previous_avg) and previous_avg != 0:
                pct_change = ((recent_avg - previous_avg) / previous_avg) * 100
                metrics[col] = pct_change
    
    # Display metrics
    summary_text = "Performance Summary (Last 30 Days vs Previous 30 Days):\\n\\n"
    for i, (indicator, change) in enumerate(metrics.items()):
        color = "🔴" if change < 0 else "🟢"
        summary_text += f"{color} {indicator}: {change:+.2f}%    "
        if i % 4 == 3:
            summary_text += "\\n"
    
    ax_summary.text(0.05, 0.5, summary_text, transform=ax_summary.transAxes, 
                   fontsize=12, verticalalignment='center', fontfamily='monospace')
    
    # Recent trends plots
    indicators = ['M2SL', 'BTCUSD', 'GOLD', 'VIX', 'TNX', 'NDX']
    
    for i, indicator in enumerate(indicators):
        if indicator in df.columns:
            row = 1 + i // 3
            col = i % 3
            ax = fig.add_subplot(gs[row, col])
            
            # Last 90 days
            recent_data = df[indicator].tail(90)
            ax.plot(recent_data.index, recent_data.values, linewidth=2, alpha=0.8)
            ax.fill_between(recent_data.index, recent_data.values, alpha=0.3)
            ax.set_title(f'{indicator} - Last 90 Days', fontweight='bold')
            ax.tick_params(axis='x', rotation=45, labelsize=8)
            ax.grid(True, alpha=0.3)
    
    plt.suptitle('Economic Indicators Performance Dashboard', fontsize=18, fontweight='bold')
    plt.savefig('performance_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_volatility_analysis(df):
    """Analyze volatility patterns"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Volatility Analysis', fontsize=16, fontweight='bold')
    
    # Calculate rolling volatility (30-day)
    rolling_window = 30
    
    # 1. VIX vs Market Volatility
    ax1 = axes[0, 0]
    if 'VIX' in df.columns and 'NDX' in df.columns:
        ndx_returns = df['NDX'].pct_change().dropna()
        ndx_volatility = ndx_returns.rolling(window=rolling_window).std() * np.sqrt(252) * 100
        vix_aligned = df['VIX'].reindex(ndx_volatility.index)
        
        ax1.scatter(vix_aligned, ndx_volatility, alpha=0.6, s=20)
        ax1.set_xlabel('VIX')
        ax1.set_ylabel('NDX 30-Day Volatility (%)')
        ax1.set_title('VIX vs Realized NASDAQ Volatility')
        ax1.grid(True, alpha=0.3)
    
    # 2. Bitcoin Volatility
    ax2 = axes[0, 1]
    if 'BTCUSD' in df.columns:
        btc_returns = df['BTCUSD'].pct_change().dropna()
        btc_volatility = btc_returns.rolling(window=rolling_window).std() * np.sqrt(252) * 100
        ax2.plot(btc_volatility.index, btc_volatility.values, color='orange', linewidth=2)
        ax2.set_ylabel('Annualized Volatility (%)')
        ax2.set_title('Bitcoin 30-Day Rolling Volatility')
        ax2.grid(True, alpha=0.3)
    
    # 3. Interest Rate Volatility  
    ax3 = axes[1, 0]
    if 'TNX' in df.columns:
        tnx_changes = df['TNX'].diff().dropna()
        tnx_volatility = tnx_changes.rolling(window=rolling_window).std()
        ax3.plot(tnx_volatility.index, tnx_volatility.values, color='red', linewidth=2)
        ax3.set_ylabel('Yield Change Volatility')
        ax3.set_title('10-Year Treasury Volatility')
        ax3.grid(True, alpha=0.3)
    
    # 4. Cross-Asset Volatility Comparison
    ax4 = axes[1, 1]
    vol_data = {}
    for asset in ['NDX', 'BTCUSD', 'GOLD', 'DXY']:
        if asset in df.columns:
            returns = df[asset].pct_change().dropna()
            volatility = returns.rolling(window=rolling_window).std() * np.sqrt(252) * 100
            vol_data[asset] = volatility
    
    for asset, vol in vol_data.items():
        ax4.plot(vol.index, vol.values, label=asset, linewidth=2, alpha=0.8)
    
    ax4.set_ylabel('Annualized Volatility (%)')
    ax4.set_title('Cross-Asset Volatility Comparison')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('volatility_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_insights(df):
    """Generate key insights from the data"""
    print("\\n" + "="*80)
    print("KEY INSIGHTS FROM ECONOMIC DATA ANALYSIS")
    print("="*80)
    
    # Data overview
    print(f"\\n📊 DATA OVERVIEW:")
    print(f"   • Time Period: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
    print(f"   • Total Days: {len(df)} trading days")
    print(f"   • Indicators: {len(df.columns)} economic/financial variables")
    
    # Recent performance
    print(f"\\n📈 RECENT PERFORMANCE (Last 30 Days):")
    recent_30d = df.tail(30)
    previous_30d = df.iloc[-60:-30] if len(df) >= 60 else df.iloc[:30]
    
    for col in ['M2SL', 'BTCUSD', 'GOLD', 'VIX', 'TNX', 'NDX']:
        if col in df.columns:
            recent_avg = recent_30d[col].mean()
            previous_avg = previous_30d[col].mean()
            if not pd.isna(recent_avg) and not pd.isna(previous_avg) and previous_avg != 0:
                pct_change = ((recent_avg - previous_avg) / previous_avg) * 100
                emoji = "🔴" if pct_change < 0 else "🟢"
                print(f"   {emoji} {col}: {pct_change:+.2f}%")
    
    # Extreme values
    print(f"\\n⚡ NOTABLE EXTREMES:")
    for col in ['VIX', 'BTCUSD', 'TNX']:
        if col in df.columns:
            max_val = df[col].max()
            min_val = df[col].min()
            max_date = df[col].idxmax().strftime('%Y-%m-%d')
            min_date = df[col].idxmin().strftime('%Y-%m-%d')
            print(f"   • {col}: Max {max_val:.2f} on {max_date}, Min {min_val:.2f} on {min_date}")
    
    # Correlations
    print(f"\\n🔗 STRONGEST CORRELATIONS:")
    corr_matrix = df.corr()
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_pairs.append((
                corr_matrix.columns[i],
                corr_matrix.columns[j],
                corr_matrix.iloc[i, j]
            ))
    
    corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    for i, (var1, var2, corr) in enumerate(corr_pairs[:5]):
        relationship = "Strong Positive" if corr > 0.7 else "Strong Negative" if corr < -0.7 else "Moderate"
        print(f"   • {var1} ↔ {var2}: {corr:.3f} ({relationship})")
    
    print("\\n" + "="*80)

def main():
    """Main function to run all visualizations"""
    print("🚀 Loading economic data...")
    df = load_data()
    
    print(f"📊 Loaded {len(df)} data points from {df.index.min()} to {df.index.max()}")
    
    print("\\n📈 Creating visualizations...")
    
    # Generate all visualizations
    create_time_series_overview(df)
    print("✅ Time series overview complete")
    
    create_correlation_analysis(df)
    print("✅ Correlation analysis complete")
    
    create_economic_relationships(df)
    print("✅ Economic relationships complete")
    
    create_performance_dashboard(df)
    print("✅ Performance dashboard complete")
    
    create_volatility_analysis(df)
    print("✅ Volatility analysis complete")
    
    # Generate insights
    generate_insights(df)
    
    print("\\n🎉 All visualizations completed! Check the generated PNG files.")

if __name__ == "__main__":
    main()