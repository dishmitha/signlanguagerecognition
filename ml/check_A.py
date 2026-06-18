import pandas as pd

df = pd.read_csv("sign_data.csv", header=None)

a_samples = df[df.iloc[:, -1] == "A"]

print("A samples:", len(a_samples))
print(a_samples.head())