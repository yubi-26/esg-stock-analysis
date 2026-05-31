import pandas as pd
import yfinance as yf

# ESGデータを読み込み
esg_df = pd.read_csv("data/esg_ratings.csv")

# 最初の50社のSymbolを取得（ESGスコアがある企業）
symbols = esg_df["Symbol"].dropna().tolist()[:50]

print(f"対象企業: {len(symbols)}社")
print(symbols)

# リターンを保存するリスト
returns_list = []

print("\n株価データをダウンロード中...")

for symbol in symbols:
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="5y")
        
        if len(hist) > 0:
            start_price = hist["Close"].iloc[0]
            end_price = hist["Close"].iloc[-1]
            return_rate = (end_price / start_price) - 1
            
            returns_list.append({
                "Symbol": symbol,
                "5Y_Return": return_rate
            })
            print(f"  ✓ {symbol}: {return_rate:.2%}")
        else:
            print(f"  ✗ {symbol}: データなし")
            
    except Exception as e:
        print(f"  ✗ {symbol}: エラー")

# 結果をDataFrameに変換
returns_df = pd.DataFrame(returns_list)

print(f"\n=== 結果 ===")
print(f"成功: {len(returns_df)}社 / {len(symbols)}社")

# 保存
returns_df.to_csv("data/stock_returns_50.csv", index=False)
print("\n保存完了: data/stock_returns_50.csv")

# 上位5社と下位5社を表示
print("\n=== リターン上位5社 ===")
print(returns_df.nlargest(5, "5Y_Return"))

print("\n=== リターン下位5社 ===")
print(returns_df.nsmallest(5, "5Y_Return"))