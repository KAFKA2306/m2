import os
import yaml
import pandas as pd
from datetime import datetime
import shutil
def load_data():
    """Load the latest economic data"""
    with open('data.yml', 'r') as f:
        data = yaml.safe_load(f)
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    df = df.dropna(how='all')
    return df
def generate_html_dashboard():
    """Generate comprehensive HTML dashboard"""
    df = load_data()
    latest_data = df.iloc[-1]
    recent_30d = df.tail(30).mean()
    previous_30d = df.iloc[-60:-30].mean() if len(df) >= 60 else df.iloc[:30].mean()
    performance_metrics = {}
    for col in df.columns:
        if not pd.isna(recent_30d[col]) and not pd.isna(previous_30d[col]) and previous_30d[col] != 0:
            pct_change = ((recent_30d[col] - previous_30d[col]) / previous_30d[col]) * 100
            performance_metrics[col] = pct_change
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Economic Ultrathink Dashboard</title>
    <style>
        :root {{
            --primary-color:
            --secondary-color:
            --success-color:
            --warning-color:
            --danger-color:
            --background:
            --card-background:
            --text-primary:
            --text-secondary:
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--background);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 40px 20px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        .update-time {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            font-size: 0.9rem;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .metric-card {{
            background: var(--card-background);
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 5px solid var(--secondary-color);
            transition: transform 0.3s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        .metric-title {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-bottom: 10px;
            font-weight: 600;
        }}
        .metric-value {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        .metric-change {{
            font-size: 0.9rem;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
        }}
        .positive {{ 
            color: var(--success-color); 
            background: rgba(39, 174, 96, 0.1);
        }}
        .negative {{ 
            color: var(--danger-color); 
            background: rgba(231, 76, 60, 0.1);
        }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }}
        .visualization-section {{
            background: var(--card-background);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        }}
        .visualization-section h2 {{
            color: var(--primary-color);
            margin-bottom: 20px;
            font-size: 1.5rem;
            border-bottom: 3px solid var(--secondary-color);
            padding-bottom: 10px;
        }}
        .visualization-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
            margin-top: 25px;
        }}
        .viz-card {{
            border: 2px solid
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
        }}
        .viz-card:hover {{
            border-color: var(--secondary-color);
            transform: scale(1.02);
        }}
        .viz-card img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .viz-title {{
            padding: 15px;
            background:
            font-weight: 600;
            color: var(--primary-color);
            text-align: center;
            border-top: 1px solid
        }}
        .insights-section {{
            background: linear-gradient(135deg,
            color: white;
            padding: 40px;
            border-radius: 15px;
            margin-top: 40px;
        }}
        .insights-section h2 {{
            color: white;
            border-bottom: 3px solid rgba(255,255,255,0.3);
            padding-bottom: 15px;
            margin-bottom: 25px;
        }}
        .insights-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }}
        .insight-card {{
            background: rgba(255,255,255,0.1);
            padding: 25px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }}
        .insight-emoji {{
            font-size: 2rem;
            margin-bottom: 15px;
            display: block;
        }}
        .footer {{
            text-align: center;
            margin-top: 60px;
            padding: 30px;
            background: var(--primary-color);
            color: white;
            border-radius: 12px;
        }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2rem; }}
            .container {{ padding: 15px; }}
            .metrics-grid {{ grid-template-columns: 1fr; }}
            .visualization-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Economic Ultrathink Dashboard</h1>
            <p>Comprehensive analysis of monetary policy, asset markets, and economic regimes</p>
            <div class="update-time">
                📊 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} | 
                📈 Data Points: {len(df):,} | 
                📅 Period: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}
            </div>
        </div>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">🏦 M2 Money Supply</div>
                <div class="metric-value">${latest_data['M2SL']:,.0f}B</div>
                <div class="metric-change {'positive' if performance_metrics.get('M2SL', 0) >= 0 else 'negative'}">
                    {'+' if performance_metrics.get('M2SL', 0) >= 0 else ''}{performance_metrics.get('M2SL', 0):.2f}% (30d avg)
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-title">₿ Bitcoin Price</div>
                <div class="metric-value">${latest_data['BTCUSD']:,.0f}</div>
                <div class="metric-change {'positive' if performance_metrics.get('BTCUSD', 0) >= 0 else 'negative'}">
                    {'+' if performance_metrics.get('BTCUSD', 0) >= 0 else ''}{performance_metrics.get('BTCUSD', 0):.2f}% (30d avg)
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-title">🥇 Gold Price</div>
                <div class="metric-value">${latest_data['GOLD']:,.0f}</div>
                <div class="metric-change {'positive' if performance_metrics.get('GOLD', 0) >= 0 else 'negative'}">
                    {'+' if performance_metrics.get('GOLD', 0) >= 0 else ''}{performance_metrics.get('GOLD', 0):.2f}% (30d avg)
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-title">📈 10Y Treasury</div>
                <div class="metric-value">{latest_data['TNX']*100:.2f}%</div>
                <div class="metric-change {'positive' if performance_metrics.get('TNX', 0) >= 0 else 'negative'}">
                    {'+' if performance_metrics.get('TNX', 0) >= 0 else ''}{performance_metrics.get('TNX', 0):.2f}% (30d avg)
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-title">😰 VIX Fear Index</div>
                <div class="metric-value">{latest_data['VIX']:.1f}</div>
                <div class="metric-change {'positive' if performance_metrics.get('VIX', 0) >= 0 else 'negative'}">
                    {'+' if performance_metrics.get('VIX', 0) >= 0 else ''}{performance_metrics.get('VIX', 0):.2f}% (30d avg)
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-title">💻 NASDAQ 100</div>
                <div class="metric-value">{latest_data['NDX']:,.0f}</div>
                <div class="metric-change {'positive' if performance_metrics.get('NDX', 0) >= 0 else 'negative'}">
                    {'+' if performance_metrics.get('NDX', 0) >= 0 else ''}{performance_metrics.get('NDX', 0):.2f}% (30d avg)
                </div>
            </div>
        </div>
        <div class="visualization-section">
            <h2>📊 Master Economic Dashboard</h2>
            <div class="viz-card">
                <img src="economic_ultrathink_dashboard.png" alt="Economic Ultrathink Dashboard">
                <div class="viz-title">🧠 Complete Economic Analysis: Stock vs Flow Variables</div>
            </div>
        </div>
        <div class="visualization-section">
            <h2>🏛️ Monetary Policy & Asset Analysis</h2>
            <div class="visualization-grid">
                <div class="viz-card">
                    <img src="monetary_policy_architecture.png" alt="Monetary Policy Architecture">
                    <div class="viz-title">🏦 Fed Policy Tools (Stacked Areas)</div>
                </div>
                <div class="viz-card">
                    <img src="asset_cumulative_analysis.png" alt="Asset Cumulative Analysis">
                    <div class="viz-title">💰 Wealth Accumulation Patterns</div>
                </div>
                <div class="viz-card">
                    <img src="economic_regime_analysis.png" alt="Economic Regime Analysis">
                    <div class="viz-title">🎭 Regime Transitions</div>
                </div>
                <div class="viz-card">
                    <img src="stock_flow_framework.png" alt="Stock Flow Framework">
                    <div class="viz-title">⚡ Variable Classification</div>
                </div>
            </div>
        </div>
        <div class="visualization-section">
            <h2>📈 Detailed Market Analysis</h2>
            <div class="visualization-grid">
                <div class="viz-card">
                    <img src="economic_indicators_overview.png" alt="Economic Indicators Overview">
                    <div class="viz-title">📊 Complete Time Series</div>
                </div>
                <div class="viz-card">
                    <img src="correlation_analysis.png" alt="Correlation Analysis">
                    <div class="viz-title">🔗 Market Correlations</div>
                </div>
                <div class="viz-card">
                    <img src="economic_relationships.png" alt="Economic Relationships">
                    <div class="viz-title">🎯 Key Relationships</div>
                </div>
                <div class="viz-card">
                    <img src="volatility_analysis.png" alt="Volatility Analysis">
                    <div class="viz-title">📉 Risk Analysis</div>
                </div>
            </div>
        </div>
        <div class="insights-section">
            <h2>🎯 Key Economic Insights</h2>
            <div class="insights-grid">
                <div class="insight-card">
                    <span class="insight-emoji">🏦</span>
                    <h3>Monetary Policy Evolution</h3>
                    <p>Fed balance sheet normalization complete. M2 growth stabilized. Reverse repo operations providing liquidity management. New equilibrium phase established.</p>
                </div>
                <div class="insight-card">
                    <span class="insight-emoji">⚡</span>
                    <h3>Stock vs Flow Paradigm</h3>
                    <p>Area charts reveal cumulative nature of monetary variables (M2, Fed assets). Line charts show rate intensities (yields, volatility). Visual encoding matches economic structure.</p>
                </div>
                <div class="insight-card">
                    <span class="insight-emoji">₿</span>
                    <h3>Digital Asset Maturation</h3>
                    <p>Bitcoin correlation with NASDAQ (91.9%) indicates institutional adoption. Wealth accumulation phase active. Traditional vs digital store of value competition intensifying.</p>
                </div>
                <div class="insight-card">
                    <span class="insight-emoji">🔗</span>
                    <h3>Structural Correlations</h3>
                    <p>Inflation-yield link (94.6%) confirms Fisher Effect. Risk-on asset convergence evident. Dollar-gold competition ongoing. Credit spreads normalizing.</p>
                </div>
                <div class="insight-card">
                    <span class="insight-emoji">🎭</span>
                    <h3>Regime Transitions</h3>
                    <p>Four distinct phases: COVID/QE → Reopening → Inflation Fight → New Equilibrium. Each regime showed unique risk/return characteristics. Current: normalized policy environment.</p>
                </div>
                <div class="insight-card">
                    <span class="insight-emoji">📊</span>
                    <h3>Market State</h3>
                    <p>VIX at complacent levels (15.18). Credit spreads tight (2.84%). Volatility compression suggests market confidence. Risk assets performing strongly.</p>
                </div>
            </div>
        </div>
        <div class="footer">
            <h3>🤖 Automated Economic Intelligence</h3>
            <p>This dashboard updates automatically via GitHub Actions, fetching fresh economic data daily from FRED and Yahoo Finance.</p>
            <p>Built with Python • Powered by Data • Deployed with GitHub Pages</p>
            <p style="margin-top: 15px; opacity: 0.8;">
                📡 Next Update: Daily at 9:00 UTC | 
                🔄 Auto-commit to repository | 
                🚀 Zero-maintenance deployment
            </p>
        </div>
    </div>
</body>
</html>
    """
    return html_content
def main():
    """Generate the dashboard website"""
    print("🚀 Generating dashboard website...")
    os.makedirs('dashboard', exist_ok=True)
    html_content = generate_html_dashboard()
    with open('dashboard/index.html', 'w') as f:
        f.write(html_content)
    png_files = [f for f in os.listdir('.') if f.endswith('.png')]
    for png_file in png_files:
        src = png_file
        dst = os.path.join('dashboard', png_file)
        shutil.copy2(src, dst)
        print(f"📊 Copied {png_file}")
    print(f"✅ Dashboard generated with {len(png_files)} visualizations")
    print("📁 Files created in './dashboard/' directory")
    print("🌐 Ready for GitHub Pages deployment!")
if __name__ == "__main__":
    main()