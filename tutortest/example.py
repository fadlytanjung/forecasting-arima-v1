import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
# import seaborn as sns

import os

df = pd.read_csv('data.csv')
df.columns = ["month", "average_monthly_ridership"]

df['average_monthly_ridership'].unique() #cleaning data
df = df.drop(df.index[df['average_monthly_ridership'] == ' n=114']) # delete data
df['average_monthly_ridership'].unique()

df['average_monthly_ridership'] = df['average_monthly_ridership'].astype(np.int32)
df['month'] = pd.to_datetime(df['month'], format = '%Y-%m')
# print(df)
# exit()
# df.dtypes
# df.plot.line(x = 'month', y = 'average_monthly_ridership')
# plt.show()

df = df.set_index('month')
print(df)
exit()
mod = sm.tsa.SARIMAX(df['average_monthly_ridership'], trend='n', order=(0,1,0), seasonal_order=(1,1,1,12))
results = mod.fit()
# print(results.summary())

df['forecast'] = results.predict(start = 102, end= 120, dynamic= True)  
df[['average_monthly_ridership', 'forecast']].plot(figsize=(12, 8))
# plt.show()

def forcasting_future_months(df, no_of_months):
    df_perdict = df.reset_index()
    mon = df_perdict['month']
    mon = mon + pd.DateOffset(months = no_of_months)
    future_dates = mon[-no_of_months -1:]

    df_perdict = df_perdict.set_index('month')
    future = pd.DataFrame(index=future_dates, columns= df_perdict.columns)
    df_perdict = pd.concat([df_perdict, future])
    print(df_perdict)
    # exit()
    df_perdict['forecast'] = results.predict(start = 114, end = 125, dynamic= True)  
    df_perdict[['average_monthly_ridership', 'forecast']].iloc[-no_of_months - 12:].plot(figsize=(12, 8))
    plt.show()
    return df_perdict[-no_of_months:]

predicted = forcasting_future_months(df,12)
print(predicted)