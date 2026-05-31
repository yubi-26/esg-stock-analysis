import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import ttest_ind

# データ読み込み
returns_df = pd.read_csv("data/stock_returns_50.csv")
esg_df = pd.read_csv("data/esg_ratings.csv")
merged = pd.merge(returns_df, esg_df, on="Symbol", how="inner")
print(f"分析対象企業: {len(merged)}社")

# 1. 相関分析
correlation = merged["5Y_Return"].corr(merged["Total ESG Risk score"])
print(f"\n=== 相関係数: {correlation:.3f} ===")

# 2. t検定
high_esg = merged[merged["Total ESG Risk score"] <= 18]["5Y_Return"]
low_esg = merged[merged["Total ESG Risk score"] >= 25]["5Y_Return"]
t_stat, p_value = ttest_ind(high_esg, low_esg)
print(f"\n=== t検定 ===")
print(f"高ESG群: {len(high_esg)}社, 平均リターン {high_esg.mean():.2%}")
print(f"低ESG群: {len(low_esg)}社, 平均リターン {low_esg.mean():.2%}")
print(f"p-value: {p_value:.4f}")

# 3. 散布図 + 回帰直線
plt.figure(figsize=(10, 6))
slope, intercept, r_value, p_val, std_err = stats.linregress(merged["Total ESG Risk score"], merged["5Y_Return"])
regression_line = slope * merged["Total ESG Risk score"] + intercept
plt.scatter(merged["Total ESG Risk score"], merged["5Y_Return"], alpha=0.6)
plt.plot(merged["Total ESG Risk score"], regression_line, 'r--', label=f'回帰直線 (傾き={slope:.3f})')
plt.xlabel("ESG Risk Score (lower is better)")
plt.ylabel("5-Year Return")
plt.title(f"ESG Risk Score vs 5-Year Return\n相関係数: {correlation:.3f} | n={len(merged)}社")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("esg_vs_return_regression.png", dpi=150)
plt.close()

# 4. セクター別散布図
sectors = merged["Sector"].unique()
colors = plt.cm.tab20(range(len(sectors)))
plt.figure(figsize=(12, 8))
for sector, color in zip(sectors, colors):
    subset = merged[merged["Sector"] == sector]
    plt.scatter(subset["Total ESG Risk score"], subset["5Y_Return"], label=sector, alpha=0.7, color=color)
plt.xlabel("ESG Risk Score (lower is better)")
plt.ylabel("5-Year Return")
plt.title("ESG Risk Score vs 5-Year Return by Sector")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("esg_vs_return_by_sector.png", dpi=150)
plt.close()

# 5. セクター別箱ひげ図
plt.figure(figsize=(12, 6))
sector_order = merged.groupby("Sector")["5Y_Return"].median().sort_values(ascending=False).index
sector_data = [merged[merged["Sector"] == s]["5Y_Return"] for s in sector_order]
plt.boxplot(sector_data, labels=sector_order, patch_artist=True)
plt.xticks(rotation=45, ha='right')
plt.ylabel("5-Year Return")
plt.title("5-Year Return Distribution by Sector")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("sector_boxplot.png", dpi=150)
plt.close()

# 6. トップ10とボトム10
print("\n=== リターン上位10社 ===")
top10 = merged.nlargest(10, "5Y_Return")[["Symbol", "Sector", "5Y_Return", "Total ESG Risk score"]]
print(top10.to_string(index=False))

print("\n=== リターン下位10社 ===")
bottom10 = merged.nsmallest(10, "5Y_Return")[["Symbol", "Sector", "5Y_Return", "Total ESG Risk score"]]
print(bottom10.to_string(index=False))

# 7. セクター別集計
print("\n=== セクター別集計 ===")
sector_summary = merged.groupby("Sector").agg({
    "5Y_Return": ["mean", "median", "count"],
    "Total ESG Risk score": "mean"
}).round(4)
print(sector_summary)

print("\n✅ 分析完了！生成された画像:")
print("  - esg_vs_return_regression.png (散布図+回帰直線)")
print("  - esg_vs_return_by_sector.png (セクター別散布図)")
print("  - sector_boxplot.png (セクター別箱ひげ図)")