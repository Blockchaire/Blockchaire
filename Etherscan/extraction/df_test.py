import pandas as pd

filename = 'maker1'
df = pd.read_feather(filename + '.feather')
print(filename)
print(df.head())
print(df.tail())
print(df.columns)
print(df.shape)