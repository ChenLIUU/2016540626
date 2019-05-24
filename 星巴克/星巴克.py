import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts

s_1 = '000157'
s_2 = '600031'

sdate = '2010-01-01'
edate = '2018-12-31'

df_s1 = ts.get_k_data(s_1, start=sdate, end=edate).sort_index(axis=0, ascending=True)
df_s2 = ts.get_k_data(s_2, start=sdate, end=edate).sort_index(axis=0, ascending=True)

df = pd.concat([df_s1.open, df_s2.open], axis=1, keys=['s1_open', 's2_open'])
df.ffill(axis=0, inplace=True)
df.to_csv('./星巴克/s12.csv')

corr = df.corr(method='pearson', min_periods=1)
print(corr)

df.s1_open.plot(figsize=(20, 12))
df.s2_open.plot(figsize=(20, 12))
plt.show()

data = pd.read_csv('./星巴克/directory.csv')
print(data.head())
print(data.describe())
print(data.info())
print(data.isnull().sum())
print(data[data['City'].isnull()])


def fill_na(x):
    return x


data['City'] = data['City'].fillna(fill_na(data['State/Province']))
data['Country'][data['Country'] == 'TW'] = 'CN'