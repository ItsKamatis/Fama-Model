import pandas_datareader as pdr
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
yf.pdr_override()
pdr.famafrench.get_available_datasets()
start = dt.datetime(2020, 1, 1)
end = dt.datetime.today()
ff = pdr.famafrench.FamaFrenchReader('F-F_Research_Data_Factors', freq='M', start=start).read()
##print(ff)
ff_df = ff[0]
ff_df.plot(subplots=True, figsize=(12,4))

ff_momentum = pdr.famafrench.FamaFrenchReader('F-F_Momentum_Factor', freq='M', start=start).read()
ff_mom_df = ff_momentum[0]
##print(ff_momentum)

ff_merged_df = pd.merge(ff_df, ff_mom_df, on='Date', how='inner', sort=True, copy=True, indicator=False, validate='one_to_one')

### Not working IDK why ###
NVDA_data = yf.download('NVDA', start, end)['Adj Close'].resample('ME').ffill().pct_change() ###fixed
###print(NVDA_data.head())
NVDA_df = NVDA_data.to_frame()
##NVDA_df.dropna(inplace=True) dropna creates shape mismatch
##print(NVDA_df.head())



#Converting date formatting in both dataframes
#print(NVDA_df.index.dtype)
#print(ff_merged_df.index.dtype)

NVDA_df['str_date'] =NVDA_data.index.astype(str)
NVDA_df['dt_date'] = pd.to_datetime(NVDA_df.str_date).dt.strftime('%Y-%m')
#print(NVDA_df.dt_date.dtype)

ff_merged_df['str_date'] = ff_merged_df.index.astype(str)
ff_merged_df['dt_date'] = pd.to_datetime(ff_merged_df.str_date).dt.strftime('%Y-%m')
#print(ff_merged_df.dt_date.dtype)

#Performing Merge

NVDA_FF_Merge_df = pd.merge(NVDA_df, ff_merged_df, how = 'inner', on = 'dt_date', sort=True, copy=True, indicator=False, validate='one_to_one')
