import pandas_datareader as pdr
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
from statsmodels.api import OLS
import statsmodels.tools
yf.pdr_override()


pdr.famafrench.get_available_datasets()
start = dt.datetime(2020, 1, 1)
end = dt.datetime.today()
stock = 'FDGRX'

ff = pdr.famafrench.FamaFrenchReader('F-F_Research_Data_Factors', freq='M', start=start).read()
ff_df = ff[0]
ff_df.plot(subplots=True, figsize=(12,4))
ff_momentum = pdr.famafrench.FamaFrenchReader('F-F_Momentum_Factor', freq='M', start=start).read()
ff_mom_df = ff_momentum[0]
ff_merged_df = pd.merge(ff_df, ff_mom_df, on='Date', how='inner', sort=True, copy=True, indicator=False, validate='one_to_one')

stock_data = yf.download(stock, start, end)['Adj Close'].resample('ME').ffill().pct_change()
stock_df = stock_data.to_frame()
stock_df['str_date'] =stock_data.index.astype(str)
stock_df['dt_date'] = pd.to_datetime(stock_df.str_date).dt.strftime('%Y-%m')

ff_merged_df['str_date'] = ff_merged_df.index.astype(str)
ff_merged_df['dt_date'] = pd.to_datetime(ff_merged_df.str_date).dt.strftime('%Y-%m')

stock_FF_Merge_df = pd.merge(stock_df, ff_merged_df, how = 'inner', on = 'dt_date', sort=True, copy=True, indicator=False,
                             validate='one_to_one')

stock_FF_Merge_df.drop(columns=['str_date_x', 'str_date_y'], inplace=True)
stock_FF_Merge_df.rename(columns={"Adj Close": "Stock"}, inplace=True)
stock_FF_Merge_df['Stock_RF'] = stock_FF_Merge_df['Stock']*100-stock_FF_Merge_df['RF']
stock_FF_Merge_df.dropna(axis=0, inplace=True)
stock_FF_Merge_df.rename(columns={'Mom   ': 'MOM'}, inplace=True)

stock_FF_Merge_df_constant = statsmodels.tools.add_constant(stock_FF_Merge_df, prepend=True)
results = OLS(stock_FF_Merge_df_constant['Stock_RF'],
              stock_FF_Merge_df_constant[['const', 'Mkt-RF', 'SMB', 'HML', 'MOM']], missing='drop').fit()
print(results.summary())
stock_FF_Merge_df_constant['Predicted'] = results.predict(stock_FF_Merge_df_constant[['const', 'Mkt-RF', 'SMB', 'HML', 'MOM']])

stock_FF_Merge_df_constant[['Stock_RF', 'Predicted']].plot(figsize=(12,8))
plt.show()

