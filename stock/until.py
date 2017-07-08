# *-* coding: utf-8 *-*
import numpy as np
import pandas as pd
from numpy import abs, log, sign
from scipy.stats import rankdata

# 计算alpha时会使用的函数
def ts_sum(df,window=10):
    return df.rolling(window).sum()

def sma(df,window=10):
    return df.rolling(window).mean()

def stddev(df,window=10):
    return df.rolling(window).std()

def correlation(x,y,window=10):
    return x.rolling(window).corr(y)

def covariance(x,y,window=10):
    return x.rolling(window).cov(y)

def rolling_rank(na):
    return rankdata(na)[-1]

def ts_rank(window=10):
    return rolling(window).apply(rolling_rank)

def rolling_prod(na):
    return na.prod(na)
    
def product(df,window=10):
    return df.rolling(window).apply(rolling_prod)

def ts_min(df,window=10):
    return df.rolling(window).min()
    
def ts_max(df,window=10):
    return df.rolling(window).max()

def delta(df,period=1):
    return df.diff(period)
    
def delay(df,period=1):
    return df.shift(period)

def rank(df):
    return df.rank(axis=1,pct=True)

def scale(df,k=1):
    return df.mul(k).div(np.abs(df).sum())

def ts_argmax(df,window=10):
    return df.rolling(window).apply(np.argmax)+1

def ts_argmin(df,window=10):
    return df.rolling(window).apply(np.argmin)+1
    
def decay_linear(df,period=10):
    if df.isnull().values.any():
        df.fillna(method='ffill',inplace=True)
        df.fillna(method='dfill',inplace=True)
        df.fillna(value=0,inplace=True)
    na_lwma=np.zeros_like(df)
    na_lwma[:period,:]=df.ix[:period,:]
    na_series = df.as_matrix()
    divisor = df.as_matrix()
    y =(np.arrange(period)+1)*1.0/divisor
    for row in range(period+1,df.shape[0]):
        x=na_series[row-period+1:row+1,:]
        na_lwma[row,:]-(np.dot(x.T,y))
    return pd.DataFrame(na_lwma,index=df.index,columns=df.columns)

# 定义计算alpha值的类
class Alphas(object):
    def __init__(self, pn_data):
        """
        :传入参数 pn_data: pandas.Panel
        """
        # 获取历史数据
        self.open = pn_data['open']
        self.high = pn_data['high']
        self.low = pn_data['low']
        self.close = pn_data['close']
        self.volume = pn_data['volume']
        self.returns = self.close.pct_change()
    
    #   每个因子的计算公式：
    # alpha020: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open -delay(low, 1))))
    def alpha020(self):
        return -1 * (rank(self.open - delay(self.high, 1)) *
                     rank(self.open - delay(self.close, 1)) *
                     rank(self.open - delay(self.low, 1)))
    
    # alpha045: (-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) *rank(correlation(sum(close, 5), sum(close, 20), 2)))) 
    def alpha045(self):
        df = correlation(self.close, self.volume, 2)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * (rank(sma(delay(self.close, 5), 20)) * df *
                     rank(correlation(ts_sum(self.close, 5), ts_sum(self.close, 20), 2)))
