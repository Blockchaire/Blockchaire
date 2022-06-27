import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('../transactions.xlsx')
print('Data loaded')
df.token_symbol = df.token_symbol.astype(str)

df.time = pd.to_datetime(df.time, format="%Y-%m-%d %H:%M:%S")
df_time = df.copy()
df_time.set_index(df_time.time, inplace=True)
df_time['count'] = 1

dai = df_time[df_time.token_symbol=='DAI']
mkr = df_time[df_time.token_symbol=='MKR']
print('Preparing the graph')
sns.catplot(data=dai, x='sender', y='value')