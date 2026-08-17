# 経済指標ダッシュボード

[![Open Dashboard](https://img.shields.io/badge/Open%20Dashboard-Visit%20Site-2ea44f?logo=github)](https://kafka2306.github.io/m2/)
[![pages-visualizations](https://github.com/KAFKA2306/m2/actions/workflows/pages.yml/badge.svg)](https://github.com/KAFKA2306/m2/actions/workflows/pages.yml)

経済・市場データを `data.yml` に保存し、Pythonで可視化してGitHub Pagesへ公開するrepositoryです。

- Repository: https://github.com/KAFKA2306/m2
- Dashboard: https://kafka2306.github.io/m2/

## Data flow

```text
データ取得
  → data.yml
  → 可視化
  → 静的HTML/PNG
  → GitHub Pages
```

現在のデータ更新entry pointは `refactored_update_data.py` です。`update_data.py` の互換wrapperは使用しません。

主なscripts:

- `refactored_update_data.py` — データ更新
- `visualize_data.py` — 基本可視化
- `economic_structure_viz.py` — 追加可視化
- `economic_ultrathink_dashboard.py` — ダッシュボード用可視化
- `generate_dashboard_site.py` — `dashboard/` の静的サイト生成

## Data sources

保存済みデータの取得処理ではFREDとYahoo Financeを使用します。`data.yml` が外部sourceの最新値と一致するとはREADMEだけから判断せず、分析時には対象期間と取得状態を確認してください。

FRED seriesとして、M2、Federal Reserve assets、reverse repo、core PCE、high-yield spreadなどを扱います。市場系列としてドル、米国債利回り、VIX、NASDAQ 100、Bitcoin、goldを扱います。実際のsymbol/series IDは現在のcode/configを参照してください。

## Local use

```bash
git clone https://github.com/KAFKA2306/m2.git
cd m2
pip install pandas numpy matplotlib seaborn requests yfinance pyyaml scipy
python refactored_update_data.py
python visualize_data.py
python economic_ultrathink_dashboard.py
python generate_dashboard_site.py
```

Tests:

```bash
pytest -q
```

## Automation

`.github/workflows/` がdata update、visualization、GitHub Pages publicationの実行定義です。scheduleや有効状態はGitHub Actions上のcurrent workflow stateを確認してください。
