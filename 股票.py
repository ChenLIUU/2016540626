#先引入后面可能用到的包（package）
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
import seaborn as sns  #画图用的
import tushare as ts

sh = ts.get_k_data(code='sh',ktype='D',autype='qfq', start='1990-12-20')
#code:股票代码，个股主要使用代码，如‘600000’
#ktype:'D':日数据；‘m’：月数据，‘Y’:年数据
#autype:复权选择，默认‘qfq’前复权
#start：起始时间
#end：默认当前时间
#查看下数据前5行
print(sh.head(5))

#将数据列表中的第0列'date'设置为索引
sh.index = pd.to_datetime(sh.date)
#画出上证指数收盘价的走势
sh['close'].plot(figsize=(12,6))
plt.title('上证指数1990-2018年走势图')
plt.xlabel('日期')
plt.show()

#pandas的describe()函数提供了数据的描述性统计
#count:数据样本，mean:均值，std:标准差
print(sh.describe().round(2))

#再查看下每日成交量
#2006年市场容量小，交易量比较小，我们从2007年开始看
sh.loc["2007-01-01":]["volume"].plot(figsize=(12,6))
plt.title('上证指数2007-2018年日成交量图')
plt.xlabel('日期')
plt.show()

#这里的平均线是通过自定义函数，手动设置20,52,252日均线
#移动平均线：
ma_day = [20, 52, 252]

for ma in ma_day:
    column_name = "%s日均线" %(str(ma))
    sh[column_name] =sh["close"].rolling(ma).mean()
sh.tail(3)
#画出2010年以来收盘价和均线图
sh.loc['2010-10-8':][["close", "20日均线", "52日均线", "252日均线"]].plot(figsize=(12, 6))
plt.title('2010-2018上证指数走势图')
plt.xlabel('日期')
plt.show()

#2005年之前的数据噪音太大，主要分析2005年之后的
sh["日收益率"] = sh["close"].pct_change()
sh["日收益率"].loc['2005-01-01':].plot(figsize=(12, 4))
plt.xlabel('日期')
plt.ylabel('收益率')
plt.title('2005-2018年上证指数日收益率')
plt.show()

###这里我们改变一下线条的类型
#(linestyle)以及加一些标记(marker)
sh["日收益率"].loc['2014-01-01':].plot(figsize=(12, 4), linestyle="--", marker="o", color="g")
plt.title('2014-2018年日收益率图')
plt.xlabel('日期')
plt.show()

stocks = {'上证指数': 'sh', '深证指数': 'sz', '沪深300': 'hs300', '上证50': 'sz50', '中小指数': 'zxb', '创业板': 'cyb'}
stock_index = pd.DataFrame()
for stock in stocks.values():
    stock_index[stock] = ts.get_k_data(stock, ktype='D', autype='qfq', start='2005-01-01')['close']
print(stock_index.head())

tech_rets = stock_index.pct_change()[1:]
print(tech_rets.head())

print(enumerate.describe())

print(tech_rets.mean()*100)

sns.jointplot('sh', 'sz', data=tech_rets)
plt.show()

sns.pirplot(tech_rets.iloc[:, 3:].dropna())
plt.show()

returns_fig = sns.PairGrid(tech_rets.iloc[:, 3:].dropna())
returns_fig.map_upper(plot.scatter, color="purple")
returns_fig.map_lower(sns.kdeplot,color="cool_d")
returns_fig.map_diag(plot.hist, bins=30)
plt.show()


def return_risk(stocks,startdate='2006-1-1'):
    close = pd.DataFrame()
    for stock in stocks.value():
        close[stock]=ts.get_k_data(stock,ktype='D',autype='qfq', start=startdate)['close']
    tech_rets=close.pct_change()[1:]
    rets=tech_rets.dropna()
    ret_mean=rets.mean()*100
    ret_std=rets.std()*100
    return ret_mean,ret_std


def plot_return_risk():
    ret, vol = return_risk(stocks)
    color = np.arry([0.18, 0.96, 0.75, 0.3, 0.9, 0.5])
    plt.scatter(ret, vol, marker='o', c=color, s=500, camp=plt.get_cmap('Spectral'))
    plt.xlable("日收益率均值%")
    plt.ylable("标准差%")
    for lable, x, y in zip(stocks.keys(),ret,vol):
        plt.annotate(lable, xy=(x, y), xytext=(20,20),textcoords="offset points",ha="right",va="bottom",bbox=dict
        (boxstyle='round,pad=0.5',fc='yellow',alpha=0.5),arrowprops=dict(arrowstyle="->",connetionstyle="arc3,rad=0"))


stocks={'上证指数':'sh','深证指数':'sz','沪深300':'hs300','上证50':'sz50','中小指数版':'zxb','创业指数版':'cyb'}
plot_return_risk()

stocks = {'中国平安': '601318', '格力电器': '000651', '徐工机械': '000425', '招商银行': '600036', '恒生电子': '600570', '贵州茅台': '600519'}
startdate='2018-1-1'
plot_return_risk()

