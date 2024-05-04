import pandas_datareader
import pandas as pd
import matplotlib.pyplot as plt

pandas_datareader.famafrench.get_available_datasets()
start = '2021-12-01'
ff = pandas_datareader.famafrench.FamaFrenchReader(
    'F-F_Momentum_Factor', freq='W', start=start).read()
print('F-F_Momentum_Factor')
ff_df = ff[0]
ff_df.plot(subplots=True, figsize=(12, 4))

# ff2 = pandas_datareader.famafrench.FamaFrenchReader('F-F_Momentum_Factors_daily', freq='W', start=start).read()
# ff_mom_df = pandas_datareader.famafrench.FamaFrenchReader('F_F_Momentum_Factor', freq='W', start=start).read()[0]
# ff_mom_df.plot(subplots=True, figsize=(12,4))

# NVDA_df = pandas_datareader.get_data_yahoo('NVDA', start=start)[
# 'Adj Close'].resample('M').ffill().pct_change()
