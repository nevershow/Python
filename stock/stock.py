# *-* coding: utf-8 *-*
import os
import numpy as np
import pandas as pd
from until import Alphas
from pandas import ExcelWriter

def get_pn_data():
  flag = os.path.exists('NewData')
  open, high, low, close, volume, d = {}, {}, {}, {}, {}, {}
  folder = 'NewData/' if flag else 'Data/'
  xls = [f for f in os.listdir(folder) if f.endswith('.xls') or f.endswith('.xlsx')]
  ''.
  xls.sort()
  for f in xls:
    print 'Reading %s...' % f
    df = pd.read_excel(folder + f)
    if flag:
      d[f[:-5]] = df
    else:
      open[f[:-4]] = df['open']
      high[f[:-4]] = df['high']
      low[f[:-4]] = df['low']
      close[f[:-4]] = df['close']
      volume[f[:-4]] = df['volume']

  if not flag:
    d['open'] = pd.DataFrame(open)
    d['high'] = pd.DataFrame(high)
    d['low'] = pd.DataFrame(low)
    d['close'] = pd.DataFrame(close)
    d['volume'] = pd.DataFrame(volume)

    os.mkdir('NewData')
    for x in d:
      print 'Writing %s.xlsx...' % x
      writer = ExcelWriter('NewData/%s.xlsx' % x)
      d[x].to_excel(writer)
      writer.save()

  return pd.Panel.from_dict(d)


pn_data = get_pn_data()
alpha = Alphas(pn_data)

alpha020 = alpha.alpha020()
writer = ExcelWriter('alpha020.xlsx')
alpha020.to_excel(writer)
writer.save()

alpha045 = alpha.alpha045()
writer = ExcelWriter('alpha045.xlsx')
alpha045.to_excel(writer)
writer.save()
