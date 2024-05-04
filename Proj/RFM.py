import pandas_datareader
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
yf.pdr_override()
pandas_datareader.famafrench.get_available_datasets()
start = '2021-12-01'
ff = pandas_datareader.famafrench.FamaFrenchReader('F-F_Research_Data_Factors', freq='M', start=start).read()
##print(ff)
ff_df = ff[0]
ff_df.plot(subplots=True, figsize=(12,4))

 ff_momentum = pandas_datareader.get_data_famafrench('F-F_Momentum_Factor', freq='M', start=start)

