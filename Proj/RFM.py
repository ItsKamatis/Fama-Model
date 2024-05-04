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
NVDA_data = web.DataReader('NVDA', 'yahoo', 'start', 'end')['Adj Close']
NVDA_data.head()