import pandas as pd

df = pd.read_csv("sign_data.csv", header=None)

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nSamples per letter:")
print(df.iloc[:, -1].value_counts().sort_index())