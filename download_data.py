import yfinance as yf  # 株価データ取得ライブラリ
import matplotlib.pyplot as plt  # グラフ描画ライブラリ

# 日本語フォント問題を回避するため
plt.rcParams['font.family'] = 'sans-serif'

# 分析する企業のティッカーシンボルリスト
companies = ["MSFT", "AAPL", "GOOGL", "NVDA", "XOM", "CVX"]

print("Downloading stock data...")  # データダウンロード開始

# 全企業のデータを保存する辞書
all_data = {}

# 各企業の株価データを取得
for ticker in companies:
    print(f"  Downloading {ticker}...")
    stock = yf.Ticker(ticker)  # ティッカーオブジェクトを作成
    hist = stock.history(period="5y")  # 過去5年間のデータを取得
    all_data[ticker] = hist  # 辞書に保存

# MSFTのデータを表示（確認用）
msft = all_data["MSFT"]
print("\n=== MSFT Stock Price (Last 5 days) ===")
print(msft[["Close"]].tail())  # 終値の最新5日間を表示

# 5年間のリターン（騰落率）を計算
print("\n=== 5-Year Returns ===")
for ticker in companies:
    data = all_data[ticker]
    start_price = data["Close"].iloc[0]  # 5年前の株価
    end_price = data["Close"].iloc[-1]   # 最新の株価
    return_rate = (end_price / start_price) - 1  # リターン計算
    print(f"{ticker}: {return_rate:.2%}")  # パーセント表示

# 折れ線グラフを作成
plt.figure(figsize=(12, 6))  # グラフサイズ指定
for ticker in companies:
    # 各企業の終値を折れ線でプロット
    plt.plot(all_data[ticker].index, all_data[ticker]["Close"], label=ticker)

plt.xlabel("Date")              # X軸ラベル
plt.ylabel("Stock Price (USD)") # Y軸ラベル
plt.title("Stock Price Trends (5 Years)")  # グラフタイトル
plt.legend()                    # 凡例表示
plt.grid(True, alpha=0.3)       # グリッド線（透明度0.3）
plt.savefig("stock_prices.png") # 画像として保存
plt.show()                      # グラフを表示

print("\n✅ Done! Graph saved as stock_prices.png")  # 完了メッセージ