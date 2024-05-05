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

#print(NVDA_FF_Merge_df.head())

NVDA_FF_Merge_df.drop(columns=['str_date_x', 'str_date_y'], inplace=True)
NVDA_FF_Merge_df.rename(columns={"Adj Close": "NVDA"}, inplace=True)

##print(NVDA_FF_Merge_df.head())

NVDA_FF_Merge_df['NVDA_RF'] = NVDA_FF_Merge_df['NVDA']*100-NVDA_FF_Merge_df['RF']
#print(NVDA_FF_Merge_df.head())

NVDA_FF_Merge_df.dropna(axis=0, inplace=True)
#print(NVDA_FF_Merge_df.head())

#results = OLS(NVDA_FF_Merge_df['NVDA_RF'], NVDA_FF_Merge_df[['Mkt-RF', 'SMB', 'HML', 'Mom']], missing='drop').fit() #mom not in DF
#print(list(NVDA_FF_Merge_df))
NVDA_FF_Merge_df.rename(columns={'Mom   ': 'MOM'}, inplace=True)
#print(list(NVDA_FF_Merge_df))

#results = OLS(NVDA_FF_Merge_df['NVDA_RF'], NVDA_FF_Merge_df[['Mkt-RF', 'SMB', 'HML', 'MOM']], missing='drop').fit()

##print(results.summary())

NVDA_FF_Merge_df_constant = statsmodels.tools.add_constant(NVDA_FF_Merge_df, prepend=True)

#print(NVDA_FF_Merge_df_constant.head())
#print(list(NVDA_FF_Merge_df_constant))


results = OLS(NVDA_FF_Merge_df_constant['NVDA_RF'], NVDA_FF_Merge_df_constant[['const', 'Mkt-RF', 'SMB', 'HML', 'MOM']], missing='drop').fit()
print(results.summary()) #What does this regression show? What do the coefficients mean?
#The regression shows the results of regressing NVDA excess returns on the Fama-French factors and the momentum factor.
# The coefficients represent the estimated effect of each factor on NVDA excess returns.
# The Mkt-RF factor has a positive coefficient, indicating that NVDA excess returns tend to increase when the market return is higher.
# The SMB and HML factors have negative coefficients, indicating that NVDA excess returns tend to decrease when the size and value factors are higher.
# The momentum factor has a positive coefficient, indicating that NVDA excess returns tend to increase when the momentum factor is higher.
# The R-squared value of the regression is 0.648, indicating that the model explains 64.8% of the variation in NVDA excess returns.

##Run a regression of NVDA excess returns on the Fama-French factors and the momentum factor. What do you find?

NVDA_FF_Merge_df_constant['Predicted'] = results.predict(NVDA_FF_Merge_df_constant[['const', 'Mkt-RF', 'SMB', 'HML', 'MOM']])

NVDA_FF_Merge_df_constant[['NVDA_RF', 'Predicted']].plot(figsize=(12,8))
plt.show()
#What does this plot show? What does the model predict? How well does it fit the data?
#The plot shows the actual NVDA excess returns and the predicted excess returns from the regression model.
# The model predicts the NVDA excess returns based on the Fama-French factors and the momentum factor.
# The model fits the data well, as the predicted values closely match the actual values.
