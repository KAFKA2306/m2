# 経済指標ダッシュボード

[![Open Dashboard](https://img.shields.io/badge/Open%20Dashboard-Visit%20Site-2ea44f?logo=github)](https://kafka2306.github.io/m2/)
[![pages-visualizations](https://github.com/KAFKA2306/m2/actions/workflows/pages.yml/badge.svg)](https://github.com/KAFKA2306/m2/actions/workflows/pages.yml)

経済・市場データを `data.yml` に保存し、Pythonで可視化してGitHub Pagesへ公開するrepositoryです。

- Repository: https://github.com/KAFKA2306/m2
- Dashboard: https://kafka2306.github.io/m2/

## Data flow

```text
refactored_update_data.py
  → data.yml
  → visualize_data.py
  → pages.yml
  → GitHub Pages
```

データ更新は `.github/workflows/update.yml`、公開は `.github/workflows/pages.yml` が担当します。

主なscripts:

- `refactored_update_data.py` — データ更新
- `visualize_data.py` — 保存済みデータから可視化を生成

## Data sources

保存済みデータの取得処理ではFREDとYahoo Financeを使用します。`data.yml` が外部sourceの最新値と一致するとはREADMEだけから判断せず、公開ページに表示される最新保存timestampと取得状態を確認してください。

FRED seriesとしてM2、Federal Reserve assets、reverse repo、core PCE、high-yield spreadなどを扱います。市場系列としてドル、米国債利回り、VIX、NASDAQ 100、Bitcoin、goldを扱います。実際のsymbol/series IDは現在のcode/configを参照してください。

## Local use

```bash
git clone https://github.com/KAFKA2306/m2.git
cd m2
python -m pip install -r requirements.txt
pytest -q
python refactored_update_data.py
python visualize_data.py
```

## Automation

`update.yml` が保存データを更新し、`pages.yml` がtests・visualization build・GitHub Pages publicationを行います。scheduleや実行結果はGitHub Actions上のcurrent workflow stateを確認してください。
