import pandas as pd

df = pd.read_csv("word_data.csv", header=None)

print(df.shape)

print(df[63].value_counts())