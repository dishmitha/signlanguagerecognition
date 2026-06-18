# check_dataset_features.py

import pandas as pd

df = pd.read_csv("sign_data.csv", header=None)

print(df.iloc[0, :10])