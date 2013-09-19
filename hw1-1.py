# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import itertools

def simulate(dt_start,dt_end,ls_symbols,proportions):


  dt_timeofday = dt.timedelta(hours=16)
  ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

  c_dataobj = da.DataAccess('Yahoo')

  # Keys to be read from the data, it is good to read everything in one go.
  ls_keys = ['close'] #, 'high', 'low', 'close', 'volume', 'actual_close']

  # Reading the data, now d_data is a dictionary with the keys above.
  # Timestamps and symbols are the ones that were specified before.
  ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
  d_data = dict(zip(ls_keys, ldf_data))

  na_price = d_data['close'].values

  na_norm = na_price/na_price[0]

  sym_invest = na_norm*proportions
  fund_invest = sym_invest.sum(axis=1)
  daily_ret=np.append([0],(fund_invest[1:]/fund_invest[:-1])-1)
  #daily_ret=(fund_invest[1:]/fund_invest[:-1])-1

  return (
    daily_ret.std(),
    daily_ret.mean(),
    (math.sqrt(252)*daily_ret.mean())/daily_ret.std(),
    fund_invest[-1]
  )

def main():
  startdate=dt.datetime(2011, 1, 1)
  enddate=dt.datetime(2011, 12, 31)
  #symbols=['C', 'GS', 'IBM', 'HNZ']
  symbols=['BRCM', 'TXN', 'AMD', 'ADI']

  #startdate=dt.datetime(2010, 1, 1)
  #enddate=dt.datetime(2010, 12, 31)
  #symbols=['AXP', 'HPQ', 'IBM', 'HNZ']
  proporps = []
  best_sharpe=0
  possibles=np.arange(11)/10.0

  tests=[possibles[list(x)] for x in list(itertools.ifilter(lambda x: sum(x)==10,itertools.product(range(11),repeat=len(symbols))))]
  
  for y in tests:
    vol, daily_ret, sharpe, cum_ret = simulate(startdate, enddate, symbols,y)
    if best_sharpe<sharpe:
      best_sharpe = sharpe
      proporps = y


  vol, daily_ret, sharpe, cum_ret = simulate(startdate, enddate, symbols,proporps)
  print "Optimal Allocations: ",proporps
  print "Sharpe Ratio: %f" % (sharpe)
  print "Volatility: %f" % (vol)
  print "Average daily return: %f" % (daily_ret)
  print "Cumulative return: %f" % (cum_ret)

if __name__ == '__main__':
  main()

