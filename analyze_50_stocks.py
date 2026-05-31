import pandas as pd
import matplotlib.pyplot as plt

# リターンデータを読み込み
returns_df = pd.read_csv("data/stock_returns_50.csv")
print(f"リターンデータ: {len(returns_df)}社")

# ESGデータを読み込み
esg_df = pd.read_csv("data/esg_ratings.csv")
print(f"ESGデータ: {len(esg_df)}社")

# 結合
merged = pd.merge(returns_df, esg_df, on="Symbol", how="inner")
print(f"結合後: {len(merged)}社")

# 相関分析
correlation = merged["5Y_Return"].corr(merged["Total ESG Risk score"])
print(f"\n=== 相関係数 ===")
print(f"5年リターン vs ESGリスクスコア: {correlation:.3f}")

# セクターごとの分析
print("\n=== セクター別平均リターン ===")
sector_returns = merged.groupby("Sector")["5Y_Return"].mean().sort_values(ascending=False)
print(sector_returns)

# セクター別ESGスコア
print("\n=== セクター別平均ESGスコア ===")
sector_esg = merged.groupby("Sector")["Total ESG Risk score"].mean().sort_values()
print(sector_esg)

# 散布図
plt.figure(figsize=(10, 6))
plt.scatter(merged["Total ESG Risk score"], merged["5Y_Return"], alpha=0.6)
plt.xlabel("ESG Risk Score (lower is better)")
plt.ylabel("5-Year Return")
plt.title(f"ESG Risk Score vs 5-Year Return (n={len(merged)} companies)")
plt.grid(True, alpha=0.3)
plt.savefig("esg_vs_return_50.png")
plt.show()

print("\nDone! Graph saved as esg_vs_return_50.png")