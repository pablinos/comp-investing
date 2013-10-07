import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import csv
import datetime as dt
import pandas as pd

def get_data(dt_start,dt_end,ls_symbols):
    dt_timeofday =dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    c_dataobj = da.DataAccess('Yahoo')

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['close'] #, 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data=dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    return (ldt_timestamps, d_data)

    



with open('orders.csv','rb') as csvfile:
    ordersreader = csv.reader(csvfile, delimiter=',')
    orderdates=[]
    ordersymbols=[]
    for row in ordersreader:
        orderdates.append(dt.datetime(int(row[0]),int(row[1]),int(row[2])))
        ordersymbols.append(row[3]);

orderdates=list(set(orderdates))
ordersymbols=list(set(ordersymbols))
dt_first=min(orderdates)
dt_last=max(orderdates)
dt_end_read=dt_last+dt.timedelta(days=1)

(ldt_dates,df_close)=get_data(dt_first,dt_end_read,ordersymbols)

df_orders = pd.DataFrame(index=ldt_dates, columns=ordersymbols)
df_orders = df_orders.fillna(0.0)

with open('orders.csv','rb') as csvfile:
    ordersreader = csv.reader(csvfile, delimiter=',')
    for row in ordersreader:
        s_type=row[4]
        df_orders[row[3]].ix[dt.datetime(int(row[0]),int(row[1]),int(row[2]),16)]= int(row[5]) * (-1 if s_type=='Sell' else 1)

print df_orders

