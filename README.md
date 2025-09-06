# 🧠 Economic Ultrathink Dashboard

[![Dashboard Deploy](https://github.com/KAFKA2306/m2/actions/workflows/dashboard-deploy.yml/badge.svg)](https://github.com/KAFKA2306/m2/actions/workflows/dashboard-deploy.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Dashboard-blue?logo=github)](https://kafka2306.github.io/m2/)
[![update-data](https://github.com/KAFKA2306/m2/actions/workflows/update.yml/badge.svg)](https://github.com/KAFKA2306/m2/actions/workflows/update.yml)
[![pages-visualizations](https://github.com/KAFKA2306/m2/actions/workflows/pages.yml/badge.svg)](https://github.com/KAFKA2306/m2/actions/workflows/pages.yml)

**Automated economic analysis dashboard tracking monetary policy, asset markets, and regime transitions from 2020-2025.**

## 🎯 Dashboard Features

### 📊 **Live Dashboard**: [kafka2306.github.io/m2](https://kafka2306.github.io/m2)

- **Real-time data updates** via GitHub Actions (daily at 9 AM UTC)
- **11 key economic indicators** from FRED and Yahoo Finance
- **5 years of historical data** (2020-2025) with 1,825+ data points
- **Stock vs Flow analysis** with appropriate visualization paradigms
- **Economic regime detection** and transition analysis
- **Responsive design** optimized for desktop and mobile

### 🏛️ Key Analysis Areas

1. **Monetary Policy Architecture**
   - M2 Money Supply (stacked area visualization)
   - Federal Reserve Balance Sheet (WALCL)
   - Reverse Repo Operations (RRPONTSYD)
   - Interest rate environment (10Y Treasury)

2. **Asset Universe Performance**
   - Bitcoin (₿) - Digital store of value
   - Gold (🥇) - Traditional safe haven  
   - NASDAQ 100 (💻) - Innovation economy
   - US Dollar Index (💵) - Global reserve currency

3. **Risk & Flow Variables**
   - VIX Volatility Index (Fear gauge)
   - High Yield Credit Spreads (Credit risk)
   - Core PCE Price Index (Inflation)

## 🚀 Automation Pipeline

### GitHub Actions Workflow
- **Trigger**: Daily at 9 AM UTC + manual dispatch
- **Data Sources**: FRED API, Yahoo Finance API
- **Processing**: Python analytics pipeline
- **Deployment**: GitHub Pages (zero-maintenance)
- **Monitoring**: Automatic commit of updated data/visualizations

### Data Flow
```
FRED API + Yahoo Finance → Python Scripts → Data Processing → 
Visualization Generation → HTML Dashboard → GitHub Pages Deployment
```

## 📈 Economic Insights Generated

### 🎭 Regime Analysis (2020-2025)
1. **COVID/QE Era** (2020-2021): Massive stimulus, Bitcoin +246%
2. **Reopening Boom** (2021-2022): Growth acceleration
3. **Inflation Fight** (2022-2023): Aggressive tightening  
4. **New Equilibrium** (2024-2025): Policy normalization

### 🔗 Structural Correlations Discovered
- **Inflation ↔ Bond Yields**: 0.946 (Fisher Effect)
- **NASDAQ ↔ Bitcoin**: 0.919 (Risk-on convergence)
- **Fed Assets ↔ Repo Rate**: 0.896 (Policy coordination)
- **Dollar ↔ Gold**: 0.171 (Safe haven competition)

### ⚡ Stock vs Flow Paradigm
- **Stock Variables** (Area charts): M2, Fed assets, price levels - cumulative nature
- **Flow Variables** (Line charts): Interest rates, volatility, spreads - intensity measures

## 🛠️ Technical Implementation

### Core Scripts
- `update_data.py` - Data fetching and historical backfill
- `visualize_data.py` - Comprehensive time series analysis  
- `economic_structure_viz.py` - Stock/flow paradigm visualization
- `economic_ultrathink_dashboard.py` - Master dashboard generation
- `generate_dashboard_site.py` - HTML website creation

### Dependencies
```python
pandas, numpy, matplotlib, seaborn, requests, yfinance, pyyaml, scipy
```

### Data Sources
- **FRED**: M2SL, WALCL, RRPONTSYD, PCEPILFE, BAMLH0A0HYM2
- **Yahoo Finance**: DXY, TNX, VIX, NDX, BTC-USD, Gold

## 📊 Generated Visualizations

1. `economic_ultrathink_dashboard.png` - Master economic analysis
2. `monetary_policy_architecture.png` - Fed policy tools (stacked areas)
3. `asset_cumulative_analysis.png` - Wealth accumulation patterns
4. `economic_regime_analysis.png` - Regime transitions
5. `stock_flow_framework.png` - Variable classification
6. `economic_correlation_matrix.png` - Structural relationships
7. `economic_indicators_overview.png` - Complete time series
8. `volatility_analysis.png` - Risk pattern analysis

## 🚀 Getting Started

### Local Development
```bash
# Clone repository
git clone https://github.com/KAFKA2306/m2.git
cd m2

# Install dependencies
pip install pandas numpy matplotlib seaborn requests yfinance pyyaml scipy

# Update data and generate visualizations
python update_data.py
python economic_ultrathink_dashboard.py

# Generate dashboard website
python generate_dashboard_site.py
```

### GitHub Pages Setup
1. Enable GitHub Pages in repository settings
2. Set source to "GitHub Actions"
3. Workflow will auto-deploy to `https://yourusername.github.io/m2`

## 🎯 Economic Philosophy

This dashboard embodies the **"ultrathink"** approach to economic analysis:

- **Visual encoding matches economic structure** (areas for stocks, lines for flows)
- **Regime-aware analysis** recognizing structural breaks
- **Multi-asset perspective** across traditional and digital store of value
- **Correlation-based insights** revealing economic relationships
- **Automated intelligence** removing manual update burden

## 🤖 Automation Benefits

- **Zero maintenance** after initial setup
- **Always current** with latest economic data
- **Consistent methodology** across time periods
- **Version controlled** analysis and visualizations
- **Publicly accessible** economic intelligence

---

## 📜 Previous Version (Japanese)

GitHub Actionsを用いて指標データを自動取得・保存するように再設計しました。`update_data.py`がFREDとYahooから値を取得し、結果は`data.yml`に保存されます。取得に失敗した場合は既存の`data.yml`を参照して補完します。履歴を再構築したい場合は`--backfill`で5年分を一括取得できます。

`data.yml`には5年分の履歴が保持され、キャッシュ兼フォールバックとして機能します。また、M2SLの面グラフを`m2_area.png`に生成しますが、バイナリのためリポジトリには含まれません。

### 使い方（CLI）

- 依存関係の導入（ローカル実行する場合）：
  `pip install pandas yfinance pyyaml matplotlib requests`

- 最新スナップショットを1行追記：
  `python3 update_data.py`

- 直近5年の履歴を再構築（バックフィル）：
  `python3 update_data.py --backfill`

- 出力：`data.yml`（日次の配列）と`m2_area.png`（M2SLの面グラフ）。

### 自動実行（GitHub Actions）

- `.github/workflows/update.yml` が毎日 00:00 UTC（cron: `0 0 * * *`）で実行し、依存を導入→`python update_data.py`→`data.yml`に差分があればコミットします。

---

**Built with Python • Powered by Economic Data • Deployed with GitHub Actions**

*"Making economic analysis as automated as software deployment"* 🚀
