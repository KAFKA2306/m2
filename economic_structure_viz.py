import yaml
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
def load_data():
    """Load and preprocess the data from data.yml"""
    with open('data.yml', 'r') as f:
        data = yaml.safe_load(f)
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    df = df.dropna(how='all')
    return df
def create_monetary_policy_stack(df):
    """Create comprehensive monetary policy visualization with stacked areas"""
    fig, axes = plt.subplots(2, 1, figsize=(16, 12))
    fig.suptitle('Monetary Policy Architecture: Stock vs Flow Variables', fontsize=18, fontweight='bold')
    ax1 = axes[0]
    m2_norm = df['M2SL'] / 1000 if 'M2SL' in df.columns else pd.Series(index=df.index)
    walcl_norm = df['WALCL'] / 1000000 if 'WALCL' in df.columns else pd.Series(index=df.index)
    rrr_norm = df['RRPONTSYD'] / 1000 if 'RRPONTSYD' in df.columns else pd.Series(index=df.index)
    if not m2_norm.empty:
        ax1.fill_between(m2_norm.index, 0, m2_norm.values, 
                        alpha=0.7, color='steelblue', label='M2 Money Supply (Trillions $)')
    if not walcl_norm.empty:
        ax1.fill_between(walcl_norm.index, 0, walcl_norm.values,
                        alpha=0.6, color='darkgreen', label='Fed Assets (Trillions $)')
    if not rrr_norm.empty and rrr_norm.max() > 0:
        rrr_scaled = rrr_norm * 100
        ax1.fill_between(rrr_scaled.index, 0, rrr_scaled.values,
                        alpha=0.5, color='crimson', label='Reverse Repo Ops (×100B $)')
    ax1.set_title('Monetary Policy Stock Variables\n(Cumulative Positions & Balance Sheet)', 
                  fontsize=14, fontweight='bold')
    ax1.set_ylabel('Trillions of Dollars', fontsize=12)
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2021-12-31'), 
                alpha=0.1, color='red', label='COVID QE Era')
    ax1.axvspan(pd.Timestamp('2022-01-01'), pd.Timestamp('2023-12-31'), 
                alpha=0.1, color='orange', label='Tightening Cycle')
    ax2 = axes[1]
    if 'TNX' in df.columns:
        ax2.plot(df.index, df['TNX'] * 100, linewidth=3, color='navy', 
                label='10Y Treasury Yield (%)', alpha=0.8)
    if 'BAMLH0A0HYM2' in df.columns:
        ax2.plot(df.index, df['BAMLH0A0HYM2'], linewidth=2, color='red', 
                label='High Yield Spread (%)', alpha=0.8)
    if 'VIX' in df.columns:
        ax2_twin = ax2.twinx()
        ax2_twin.plot(df.index, df['VIX'], linewidth=2, color='gray', alpha=0.6,
                     label='VIX (Volatility)', linestyle='--')
        ax2_twin.set_ylabel('VIX Level', color='gray', fontsize=11)
        ax2_twin.tick_params(axis='y', labelcolor='gray')
    ax2.set_title('Financial Flow Variables\n(Rates, Spreads & Risk Pricing)', 
                  fontsize=14, fontweight='bold')
    ax2.set_xlabel('Time Period', fontsize=12)
    ax2.set_ylabel('Rate/Spread (%)', fontsize=12)
    ax2.legend(loc='upper left', framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('monetary_policy_architecture.png', dpi=300, bbox_inches='tight')
    plt.show()
def create_asset_cumulative_context(df):
    """Create asset level visualizations showing cumulative wealth context"""
    fig, axes = plt.subplots(2, 2, figsize=(20, 12))
    fig.suptitle('Asset Level Analysis: Cumulative Wealth & Store of Value', fontsize=18, fontweight='bold')
    ax1 = axes[0, 0]
    if 'BTCUSD' in df.columns:
        btc_data = df['BTCUSD'].dropna()
        ax1.fill_between(btc_data.index, 0, btc_data.values, 
                        alpha=0.6, color='orange', label='Bitcoin Price')
        ax1.plot(btc_data.index, btc_data.values, color='darkorange', linewidth=2)
        milestones = [
            (pd.Timestamp('2021-04-14'), 'ATH $65k'),
            (pd.Timestamp('2021-11-10'), 'ATH $69k'),
            (pd.Timestamp('2022-11-09'), 'FTX Collapse'),
            (pd.Timestamp('2024-03-14'), 'ETF Launch Impact')
        ]
        for date, label in milestones:
            if date in btc_data.index:
                ax1.annotate(label, (date, btc_data[date]), 
                           xytext=(10, 20), textcoords='offset points',
                           fontsize=8, alpha=0.8)
    ax1.set_title('Bitcoin: Digital Store of Value\n(Logarithmic Growth Pattern)', fontweight='bold')
    ax1.set_ylabel('Price (USD)', fontsize=11)
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.3)
    ax2 = axes[0, 1]
    if 'GOLD' in df.columns:
        gold_data = df['GOLD'].dropna()
        ax2.fill_between(gold_data.index, 0, gold_data.values,
                        alpha=0.6, color='gold', label='Gold Price')
        ax2.plot(gold_data.index, gold_data.values, color='darkgoldenrod', linewidth=2)
        gold_ma = gold_data.rolling(window=90).mean()
        ax2.plot(gold_ma.index, gold_ma.values, color='red', linewidth=2, 
                linestyle='--', alpha=0.8, label='90-Day Trend')
    ax2.set_title('Gold: Traditional Safe Haven\n(Inflation Hedge & Crisis Asset)', fontweight='bold')  
    ax2.set_ylabel('Price (USD/oz)', fontsize=11)
    ax2.legend(framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax3 = axes[1, 0]
    if 'NDX' in df.columns:
        ndx_data = df['NDX'].dropna()
        ax3.fill_between(ndx_data.index, 0, ndx_data.values,
                        alpha=0.5, color='cyan', label='NASDAQ 100')
        ax3.plot(ndx_data.index, ndx_data.values, color='blue', linewidth=2)
        peak = ndx_data.expanding().max()
        drawdown = (ndx_data - peak) / peak * 100
        ax3_twin = ax3.twinx()
        ax3_twin.fill_between(drawdown.index, 0, drawdown.values, 
                             alpha=0.3, color='red', label='Drawdown %')
        ax3_twin.set_ylabel('Drawdown (%)', color='red', fontsize=10)
        ax3_twin.tick_params(axis='y', labelcolor='red')
    ax3.set_title('NASDAQ 100: Innovation Economy\n(Growth Asset with Tech Focus)', fontweight='bold')
    ax3.set_ylabel('Index Level', fontsize=11)
    ax3.grid(True, alpha=0.3)
    ax4 = axes[1, 1]  
    if 'DXY' in df.columns:
        dxy_data = df['DXY'].dropna()
        baseline = 100
        above = dxy_data.where(dxy_data >= baseline, baseline)
        below = dxy_data.where(dxy_data < baseline, baseline)
        ax4.fill_between(dxy_data.index, baseline, above.values,
                        alpha=0.6, color='green', label='USD Strength')
        ax4.fill_between(dxy_data.index, below.values, baseline,  
                        alpha=0.6, color='red', label='USD Weakness')
        ax4.axhline(y=baseline, color='black', linestyle='-', alpha=0.8, linewidth=1)
        ax4.plot(dxy_data.index, dxy_data.values, color='darkblue', linewidth=2)
    ax4.set_title('US Dollar Index: Global Reserve Currency\n(Relative Strength vs Trading Partners)', fontweight='bold')
    ax4.set_ylabel('DXY Index', fontsize=11)  
    ax4.legend(framealpha=0.9)
    ax4.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('asset_cumulative_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
def create_economic_regime_analysis(df):
    """Analyze and visualize economic regime transitions"""
    fig, axes = plt.subplots(3, 1, figsize=(18, 15))
    fig.suptitle('Economic Regime Analysis: 2020-2025 Structural Shifts', fontsize=18, fontweight='bold')
    regimes = [
        ('2020-03-01', '2021-06-30', 'COVID Crisis & QE', 'red'),
        ('2021-07-01', '2022-03-01', 'Reopening Boom', 'green'), 
        ('2022-03-01', '2023-12-31', 'Inflation Fight', 'orange'),
        ('2024-01-01', '2025-09-06', 'New Equilibrium', 'blue')
    ]
    ax1 = axes[0]
    if 'M2SL' in df.columns:
        m2_growth = df['M2SL'].pct_change(periods=252).dropna() * 100
        ax1.plot(m2_growth.index, m2_growth.values, linewidth=3, color='steelblue',
                label='M2 Growth Rate (Annualized %)')
    if 'TNX' in df.columns:
        ax1_twin = ax1.twinx()
        ax1_twin.plot(df.index, df['TNX'] * 100, linewidth=3, color='red', alpha=0.8,
                     label='10Y Treasury Yield (%)')
        ax1_twin.set_ylabel('Interest Rate (%)', color='red', fontsize=11)
        ax1_twin.tick_params(axis='y', labelcolor='red')
    for start, end, name, color in regimes:
        ax1.axvspan(pd.Timestamp(start), pd.Timestamp(end), 
                   alpha=0.15, color=color, label=name)
    ax1.set_title('Monetary Policy Regime Shifts', fontsize=14, fontweight='bold')
    ax1.set_ylabel('M2 Growth Rate (%)', fontsize=11)
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax2 = axes[1]
    assets = ['NDX', 'BTCUSD', 'GOLD']
    colors = ['blue', 'orange', 'gold']
    for asset, color in zip(assets, colors):
        if asset in df.columns:
            normalized = (df[asset] / df[asset].iloc[0] * 100).dropna()
            ax2.fill_between(normalized.index, 100, normalized.values, 
                           alpha=0.3, color=color)
            ax2.plot(normalized.index, normalized.values, linewidth=2, 
                    color=color, label=f'{asset} (Normalized)')
    ax2.axhline(y=100, color='black', linestyle='-', alpha=0.5)
    ax2.set_title('Risk Asset Relative Performance\n(Normalized to Starting Point = 100)', 
                  fontsize=14, fontweight='bold')
    ax2.set_ylabel('Relative Performance', fontsize=11)
    ax2.legend(framealpha=0.9)
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3)
    ax3 = axes[2]
    if 'VIX' in df.columns and 'BAMLH0A0HYM2' in df.columns:
        ax3.fill_between(df.index, 0, df['VIX'], alpha=0.6, color='gray', 
                        label='VIX (Market Fear)')
        ax3.plot(df.index, df['VIX'], color='black', linewidth=2)
        ax3_twin = ax3.twinx()
        ax3_twin.plot(df.index, df['BAMLH0A0HYM2'], color='purple', linewidth=3,
                     label='High Yield Spread (%)', alpha=0.8)
        ax3_twin.set_ylabel('Credit Spread (%)', color='purple', fontsize=11)
        ax3_twin.tick_params(axis='y', labelcolor='purple')
        ax3.axhline(y=30, color='red', linestyle='--', alpha=0.8, label='High Stress (VIX>30)')
        ax3.axhline(y=20, color='orange', linestyle='--', alpha=0.8, label='Elevated Risk')
    ax3.set_title('Market Stress Indicators\n(Volatility & Credit Risk)', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Time Period', fontsize=12)
    ax3.set_ylabel('VIX Level', fontsize=11)
    ax3.legend(loc='upper left', framealpha=0.9)
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('economic_regime_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
def create_flow_stock_framework(df):
    """Demonstrate the conceptual difference between flow and stock variables"""
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Economic Variable Classification: Stock vs Flow Analysis', fontsize=18, fontweight='bold')
    stock_vars = [
        ('M2SL', 'Money Supply M2\n(Stock of Money)', 'steelblue'),
        ('WALCL', 'Fed Balance Sheet\n(Stock of Assets)', 'darkgreen'),
        ('PCEPILFE', 'Price Level Index\n(Cumulative Inflation)', 'purple')
    ]
    for i, (var, title, color) in enumerate(stock_vars):
        ax = axes[0, i]
        if var in df.columns:
            data = df[var].dropna()
            ax.fill_between(data.index, 0, data.values, alpha=0.6, color=color)
            ax.plot(data.index, data.values, color=color, linewidth=2, alpha=0.9)
            ax.text(0.05, 0.95, 'STOCK VARIABLE\n(Cumulative Level)', 
                   transform=ax.transAxes, fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8),
                   verticalalignment='top')
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
    flow_vars = [
        ('TNX', '10Y Treasury Yield\n(Flow of Returns)', 'red'),
        ('BAMLH0A0HYM2', 'Credit Risk Premium\n(Flow of Risk)', 'orange'),
        ('VIX', 'Implied Volatility\n(Flow of Fear)', 'gray')
    ]
    for i, (var, title, color) in enumerate(flow_vars):
        ax = axes[1, i]
        if var in df.columns:
            data = df[var].dropna()
            ax.plot(data.index, data.values, color=color, linewidth=3, alpha=0.8)
            mean_val = data.mean()
            ax.axhline(y=mean_val, color=color, linestyle='--', alpha=0.5, linewidth=2,
                      label=f'Mean: {mean_val:.2f}')
            ax.text(0.05, 0.95, 'FLOW VARIABLE\n(Rate/Intensity)', 
                   transform=ax.transAxes, fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8),
                   verticalalignment='top')
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.legend(framealpha=0.9)
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('stock_flow_framework.png', dpi=300, bbox_inches='tight')
    plt.show()
def generate_structural_insights(df):
    """Generate insights about economic structure and relationships"""
    print("\\n" + "="*90)
    print("ECONOMIC STRUCTURE ANALYSIS: STOCK VS FLOW PARADIGM")
    print("="*90)
    print("\\n🏛️  STOCK VARIABLES (Cumulative Levels - Area Charts Appropriate):")
    stock_vars = ['M2SL', 'WALCL', 'RRPONTSYD', 'PCEPILFE', 'DXY', 'NDX', 'BTCUSD', 'GOLD']
    for var in stock_vars:
        if var in df.columns:
            current = df[var].iloc[-1]
            start = df[var].iloc[0] 
            total_change = ((current - start) / start * 100) if start != 0 else 0
            print(f"   📊 {var}: {total_change:+.1f}% total change (${current:,.0f} current)")
    print("\\n⚡ FLOW VARIABLES (Rates/Intensities - Line Charts Appropriate):")
    flow_vars = ['TNX', 'BAMLH0A0HYM2', 'VIX']
    for var in flow_vars:
        if var in df.columns:
            current = df[var].iloc[-1]
            mean_val = df[var].mean()
            volatility = df[var].std()
            print(f"   📈 {var}: {current:.2f} current, {mean_val:.2f} avg, {volatility:.2f} std")
    print("\\n🎭 REGIME TRANSITION ANALYSIS:")
    covid_period = df['2020-03':'2021-06']  
    tightening_period = df['2022-03':'2023-12']
    current_period = df['2024-01':]
    periods = [
        ("COVID/QE Era", covid_period),
        ("Tightening Cycle", tightening_period), 
        ("New Equilibrium", current_period)
    ]
    for name, period_df in periods:
        if not period_df.empty:
            print(f"\\n   {name} ({period_df.index[0].strftime('%Y-%m')} - {period_df.index[-1].strftime('%Y-%m')}):")
            if 'VIX' in period_df.columns:
                avg_vix = period_df['VIX'].mean()
                print(f"   • Average VIX: {avg_vix:.1f} ({'High Stress' if avg_vix > 25 else 'Moderate' if avg_vix > 15 else 'Low Stress'})")
            if 'BTCUSD' in period_df.columns:
                btc_return = (period_df['BTCUSD'].iloc[-1] / period_df['BTCUSD'].iloc[0] - 1) * 100
                print(f"   • Bitcoin Performance: {btc_return:+.0f}%")
            if 'TNX' in period_df.columns:
                avg_yield = period_df['TNX'].mean() * 100
                print(f"   • Average 10Y Yield: {avg_yield:.2f}%")
    print("\\n🔗 STRUCTURAL RELATIONSHIPS:")
    if all(col in df.columns for col in ['M2SL', 'WALCL']):
        m2_fed_corr = df['M2SL'].corr(df['WALCL'])
        print(f"   • M2 ↔ Fed Assets: {m2_fed_corr:.3f} (Monetary Policy Coordination)")
    if all(col in df.columns for col in ['PCEPILFE', 'TNX']):
        inflation_yield_corr = df['PCEPILFE'].corr(df['TNX']) 
        print(f"   • Inflation ↔ Bond Yields: {inflation_yield_corr:.3f} (Fisher Effect)")
    if all(col in df.columns for col in ['NDX', 'BTCUSD']):
        stocks_crypto_corr = df['NDX'].corr(df['BTCUSD'])
        print(f"   • Stocks ↔ Bitcoin: {stocks_crypto_corr:.3f} (Risk-On Correlation)")
    if all(col in df.columns for col in ['DXY', 'GOLD']):
        dollar_gold_corr = df['DXY'].corr(df['GOLD'])
        print(f"   • Dollar ↔ Gold: {dollar_gold_corr:.3f} (Safe Haven Competition)")
    print("\\n" + "="*90)
def main():
    """Main execution function"""
    print("🚀 Loading economic data for structural analysis...")
    df = load_data()
    print("\\n📊 Creating economic structure visualizations...")
    create_monetary_policy_stack(df)
    print("✅ Monetary policy architecture complete")
    create_asset_cumulative_context(df) 
    print("✅ Asset cumulative analysis complete")
    create_economic_regime_analysis(df)
    print("✅ Economic regime analysis complete")
    create_flow_stock_framework(df)
    print("✅ Stock vs flow framework complete")
    generate_structural_insights(df)
    print("\\n🎉 Economic structure analysis complete!")
    print("Generated files:")
    print("• monetary_policy_architecture.png")
    print("• asset_cumulative_analysis.png") 
    print("• economic_regime_analysis.png")
    print("• stock_flow_framework.png")
if __name__ == "__main__":
    main()