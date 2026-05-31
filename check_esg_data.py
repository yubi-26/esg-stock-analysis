import pandas as pd

# ESGデータを読み込み
esg_df = pd.read_csv("data/esg_ratings.csv")

print("=== データの先頭5行 ===")
print(esg_df.head())

print("\n=== 列名一覧 ===")
print(esg_df.columns.tolist())

print(f"\n=== データサイズ ===")
print(f"{len(esg_df)} rows, {len(esg_df.columns)} columns")