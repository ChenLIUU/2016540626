import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#正常显示画图时出现的中文
from pylab import mpl#matplotlib中，frontend就是我们写的python代码，而backend就是负责显示我们代码所写图形的底层代码。
#这里使用微软雅黑字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
#画图时显示负号
mpl.rcParams['axes.unicode_minus'] = False
'''You can use the proper typesetting Unicode minus (see https://en.wikipedia.org/wiki/Plus_sign#Plus_sign) or the ASCII hyphen for minus, which some people prefer. The matplotlibrc param axes.unicode_minus controls the default behavior.
The default is to use the Unicode minus.'''
import seaborn as sns
import tushare as ts


df = ts.get_k_data('sh', ktype='D', autype='qfq', start='2006-1-1')
df.index = pd.to_datetime(df.date)
tech_rets = df.close.pct_change()[1:]
rets = tech_rets.dropna()
print(rets.head(100))
print(rets.quantile(0.05))


def monte_carlo(start_price, days, mu, sigma):
    dt = 1/days
    price = np.zeros(days)
    price[0] = start_price
    shock = np.zeros(days)
    drift = np.zeros(days)

    for x in range(1, days):
        shock[x] = np.random.normal(loc=mu*dt, scale=sigma*np.sqrt(dt))
        drift[x] = mu*dt
        price[x] = price[x-1] + (price[x-1]*(drift[x]+shock[x]))
    return price


runs = 10000
start_price = 2641.34
days = 365
mu = rets.mean
sigma = rets.std()
simulations = np.zeros(runs)

for run in range(runs):
    simulations[run] = monte_carlo(start_price, days, mu, sigma)[days-1]
q = np.percentile(simulations, 1)

plt.figure(figsize=(10, 6))
plt.hist(simulations, bins=100, color='grey')
plt.figtext(0.6, 0.8, s='初始价格:%.2f' % start_price)
plt.figtext(0.6, 0.7, '预期价格均值：%.2f' % simulations.mean())
plt.figtext(0.15, 0.6, 'q(0.99:%.2f)' % q)
plt.axvline(x=q, linewidth=6, color='r')
plt.title('经过%s天上证指数的模特卡罗模拟后价格分布图' % days, weight='bold')
plt.show()

from time import time
np.random.seed(2018)
t0 = time()
s0 = 2641.34
T = 1.0;
r = 0.05;
sigma = rets.std()
M = 50;
dt = T/M;
I = 250000
s = np.zeros(M = 1, I)
s[0] = s0
for t in range(1, M+1):
    z = np.random.standard_normal(I)
    s[t] = s[t-1]*np.exp((r-0.5*sigma**2)*dt+sigma*np.sqrt(dt)*z)
s_m = np.sum(s[-1]/I)
tnpl = time()-t0
print('经过250000次模拟，得出1年后上证指数的预期平均收盘价为：%.2f' % s_m)