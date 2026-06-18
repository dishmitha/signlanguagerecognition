import pandas as pd

df = pd.read_csv("sign_data.csv", header=None)

print(sorted(df.iloc[:, -1].unique()))

import pandas as pd

df = pd.read_csv("sign_data.csv", header=None)

counts = df.iloc[:, -1].value_counts().sort_index()

print(counts)
print("\nMin:", counts.min())
print("Max:", counts.max())

import joblib

model = joblib.load("sign_model.pkl")

print(model.n_features_in_)