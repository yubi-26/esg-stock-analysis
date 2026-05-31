import pandas as pd
import matplotlib.pyplot as plt

# 株価リターンデータ（先ほど計算した結果）
returns_data = {
    "MSFT": 0.8963,
    "AAPL": 1.5760,
    "GOOGL": 2.2210,
    "NVDA": 12.0144,
    "XOM": 1.8875,
    "CVX": 1.1004,
}
returns_df = pd.DataFrame(list(returns_data.items()), columns=["Symbol", "5Y_Return"])
print("=== Stock Returns ===")
print(returns_df)

# ESGデータを読み込み
esg_df = pd.read_csv("data/esg_ratings.csv")

# 必要な列だけ抽出
esg_clean = esg_df[["Symbol", "Total ESG Risk score", "Sector"]]
print("\n=== ESG Data (6 companies) ===")
print(esg_clean[esg_clean["Symbol"].isin(returns_df["Symbol"])])

# 株価リターンとESGデータを結合
merged = pd.merge(returns_df, esg_clean, on="Symbol", how="inner")
print("\n=== Merged Data ===")
print(merged)

# 相関分析
if len(merged) > 1:
    correlation = merged["5Y_Return"].corr(merged["Total ESG Risk score"])
    print(f"\n=== Correlation between 5Y Return and ESG Risk Score ===")
    print(f"Correlation: {correlation:.3f}")
    if correlation < 0:
        print("Negative correlation: Better ESG (lower risk) tends to have higher returns")
    else:
        print("Positive correlation: Better ESG does not necessarily mean higher returns")

# 散布図
plt.figure(figsize=(10, 6))
plt.scatter(merged["Total ESG Risk score"], merged["5Y_Return"], alpha=0.7)
for _, row in merged.iterrows():
    plt.annotate(row["Symbol"], (row["Total ESG Risk score"], row["5Y_Return"]))
plt.xlabel("ESG Risk Score (lower is better)")
plt.ylabel("5-Year Return")
plt.title("ESG Risk Score vs 5-Year Stock Return")
plt.grid(True, alpha=0.3)
plt.savefig("esg_vs_return.png")
plt.show()

print("\nDone! Graph saved as esg_vs_return.png")