# 🧠 経済超分析ダッシュボード

[![Open Dashboard](https://img.shields.io/badge/Open%20Dashboard-Visit%20Site-2ea44f?logo=github)](https://kafka2306.github.io/m2/)
[![update-data](https://github.com/KAFKA2306/m2/actions/workflows/update.yml/badge.svg)](https://github.com/KAFKA2306/m2/actions/workflows/update.yml)
[![pages-visualizations](https://github.com/KAFKA2306/m2/actions/workflows/pages.yml/badge.svg)](https://github.com/KAFKA2306/m2/actions/workflows/pages.yml)
[![dashboard-deploy](https://github.com/KAFKA2306/m2/actions/workflows/dashboard-deploy.yml/badge.svg)](https://github.com/KAFKA2306/m2/actions/workflows/dashboard-deploy.yml)

**2020年から2025年までの金融政策、資産市場、および経済体制の移行を追跡する自動経済分析ダッシュボード**

## 🎯 ダッシュボードの機能

### 📊 **ライブダッシュボード**: [kafka2306.github.io/m2](https://kafka2306.github.io/m2)
（上の「Open Dashboard」ボタンからもアクセスできます）

- GitHub Actionsによる**リアルタイムデータ更新**（UTC時間で毎日9時）
- FREDとYahoo Financeから取得した**11の主要経済指標**
- **過去5年間（2020-2025年）**にわたる1,825件以上のデータポイント
- **ストック（蓄積）とフロー（変動）の分析**に対応した適切な可視化手法
- **経済体制の検出**と移行分析機能
- **レスポンシブデザイン**を採用し、デスクトップ・モバイル両端末に最適化

### 🏛️ 主要分析対象領域

1. **金融政策体系**
   - M2マネーサプライ（積み上げエリアチャート表示）
   - 連邦準備制度のバランスシート（WALCL）
   - リバースレポオペレーション（RRPONTSYD）
   - 金利環境（10年物米国債利回り）

2. **資産ユニバースのパフォーマンス**
   - ビットコイン（₿） - デジタル価値保存手段
   - 金（🥇） - 伝統的安全資産
   - NASDAQ 100指数（💻） - イノベーション経済
   - USドル指数（💵） - 世界基軸通貨

3. **リスク要因とフロー変数**
   - VIXボラティリティ指数（恐怖指数）
   - ハイイールドクレジットスプレッド（信用リスク指標）
   - コアPCE物価指数（インフレ指標）

## 🚀 自動化パイプライン

### GitHub Actionsワークフロー
- **トリガー**: UTC時間で毎日9時、および手動実行可能
- **データソース**: FRED APIおよびYahoo Finance API
- **処理工程**: Pythonによる分析パイプライン
- **デプロイ**: GitHub Pagesでの公開（メンテナンス不要）
- **モニタリング**: 更新データ/可視化結果の自動コミット機能

### データフロー
```
FRED API + Yahoo Finance → Pythonスクリプト → データ処理 → 
可視化データ生成 → HTMLダッシュボード → GitHub Pages公開
```

## 📈 生成された経済インサイト

### 🎭 経済体制分析（2020-2025年）
1. **COVID/QE時代**（2020-2021年）：大規模な景気刺激策実施、ビットコイン+246%上昇
2. **経済再開ブーム**（2021-2022年）：成長加速局面
3. **インフレ抑制戦**（2022-2023年）：積極的な金融引き締め政策
4. **新たな均衡状態**（2024-2025年）：政策の正常化過程

### 🔗 発見された構造的相関関係
- **インフレ ↔ 債券利回り**：0.946（フィッシャー効果）
- **NASDAQ ↔ ビットコイン**：0.919（リスクオン局面における連動性）
- **FRB資産 ↔ レポ金利**：0.896（政策協調関係）
- **ドル ↔ 金**：0.171（安全資産としての競合関係）

### ⚡ ストック対フローの分析枠組み
- **ストック変数**（エリアチャート表示）：M2、FRB資産、物価水準 - 累積的な性質
- **フロー変数**（ラインチャート表示）：金利、ボラティリティ、スプレッド - 強度指標

## 🛠️ 技術的実装

### 主要スクリプト
- `update_data.py` - データ取得と過去データの補完処理
- `visualize_data.py` - 包括的な時系列データ分析
- `economic_structure_viz.py` - ストック/フロー分析枠組みの可視化
- `economic_ultrathink_dashboard.py` - マスターダッシュボード生成
- `generate_dashboard_site.py` - HTMLウェブサイト作成

### 依存ライブラリ
```python
pandas, numpy, matplotlib, seaborn, requests, yfinance, pyyaml, scipy
```

### データソース
- **FRED**: M2SL, WALCL, RRPONTSYD, PCEPILFE, BAMLH0A0HYM2
- **Yahoo Finance**: DXY, TNX, VIX, NDX, BTC-USD, Gold

## 📊 生成された可視化データ

1. `economic_ultrathink_dashboard.png` - 総合経済分析
2. `monetary_policy_architecture.png` - FRB政策ツールの可視化（積み上げエリアチャート）
3. `asset_cumulative_analysis.png` - 資産蓄積パターン分析
4. `economic_regime_analysis.png` - 経済体制の移行分析
5. `stock_flow_framework.png` - 変数分類フレームワーク
6. `economic_correlation_matrix.png` - 構造的相関関係マトリックス
7. `economic_indicators_overview.png` - 全時系列データの概要
8. `volatility_analysis.png` - リスクパターン分析

## 🚀 導入手順

### ローカル開発環境
```bash
# リポジトリのクローン
git clone https://github.com/KAFKA2306/m2.git
cd m2

# 依存ライブラリのインストール
pip install pandas numpy matplotlib seaborn requests yfinance pyyaml scipy

# データ更新と可視化データ生成
python update_data.py
python economic_ultrathink_dashboard.py

# ダッシュボードウェブサイトの生成
python generate_dashboard_site.py
```
