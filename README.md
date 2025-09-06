# m2

GitHub Actionsを用いて指標データを自動取得・保存するように再設計しました。`update_data.py`がFREDとYahooから値を取得し、結果は`data.yml`に保存されます。取得に失敗した場合は既存の`data.yml`を参照して補完します。履歴を再構築したい場合は`--backfill`で5年分を一括取得できます。

`data.yml`には5年分の履歴が保持され、キャッシュ兼フォールバックとして機能します。また、M2SLの面グラフを`m2_area.png`に生成しますが、バイナリのためリポジトリには含まれません。

使い方（CLI）

- 依存関係の導入（ローカル実行する場合）：

  `pip install pandas yfinance pyyaml matplotlib requests`

- 最新スナップショットを1行追記：

  `python3 update_data.py`

- 直近5年の履歴を再構築（バックフィル）：

  `python3 update_data.py --backfill`

- 出力：`data.yml`（日次の配列）と`m2_area.png`（M2SLの面グラフ）。

自動実行（GitHub Actions）

- `.github/workflows/update.yml` が毎日 00:00 UTC（cron: `0 0 * * *`）で実行し、依存を導入→`python update_data.py`→`data.yml`に差分があればコミットします。

注意点

- `^TNX`（10年利回り）はYahooが「利回り×10」で返すため、スクリプト側で`/10`補正しています。
- GOLDは`XAUUSD=X`と`GC=F`を試行し、利用可能な方を採用します。

（参考）以下は旧版のWindows向けExcel自動更新の説明で、現在のリポジトリ構成とは異なります。必要であれば別リポジトリ/ブランチで提供可能です。
自動取得＆自動更新、まで一式そろえました ✅
以下のファイルを同じフォルダに置いて使ってください（Windows 10 / VSCode想定）。

auto_update_liquidity_alloc.py — FRED＋Yahooから指標を取得してExcelを更新

.env — FREDのAPIキーを入れる場所（FRED_API_KEY=...）

run_auto_update.bat — クリック実行＆タスクスケジューラ用

liquidity_allocation_dashboard.xlsx — 既存の配分ダッシュボード

README_liquidity_auto_update.txt — 手順書


使い方（3分）

1. Python 3.11+ をインストール（PATHに追加）。


2. .env を開き、FREDのAPIキーを設定（無料：FREDサイトで取得）。


3. run_auto_update.bat をダブルクリック → 依存パッケージを自動導入し、Excelを更新します。

更新結果は auto_update_log.txt に記録されます。




自動更新（毎日）にする

タスク スケジューラ → 「基本タスクの作成」

トリガー：毎日 08:05（JST 推奨）

操作：プログラム開始 → C:\Windows\System32\cmd.exe

引数：/c "cd /d C:\Path\To\Folder && run_auto_update.bat"

完了！



取得する指標とロジック

FRED：M2SL（M2, 兆換算） / WALCL（FRB総資産, 兆） / RRPONTSYD（RRP, 十億） /
PCEPILFE（コアPCE指数→YoY化） / BAMLH0A0HYM2（HY OAS, %）

Yahoo：DX-Y.NYB or DX=F（DXY） / ^TNX（10年利回り＝値/10） / ^VIX / ^NDX / BTC-USD / XAUUSD=X or GC=F（金）

Excel 側で L/I/G/R スコア → 合計S → 配分（株・BTC・金・米債・EM+コモ）を自動計算。

Growthのみ手動（Inputsの「-1/0/+1」）にしてあり、NFPやISMの肌感を反映できます。


何かカスタム（例：DXYの別ティッカー、Slack通知、Googleスプレッドシート版）もすぐ作れます。欲しい拡張、教えてください！
