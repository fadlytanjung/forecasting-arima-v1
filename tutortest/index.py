import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA
# import seaborn as sns

import os

df = pd.read_csv('dummyArima.csv',delimiter=';')
df = df.drop(df.columns[[1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]],axis=1)


# df['Pendapatan Pajak Daerah'] = df['Pendapatan Pajak Daerah'].astype(np.int32)
df['Tahun'] = pd.to_datetime(df['Tahun'], format = '%Y')
print(df)
# exit()
# df.dtypes
# df.plot.line(x = 'Tahun', y ='Pendapatan Pajak Daerah')
# plt.show()
df = df.set_index('Tahun')
# print(df)
# exit()
mod = sm.tsa.SARIMAX(df['Hasil Retribusi Daerah'], order=(1,1,0),
sensasional_order=(1,1,1,365))
results = mod.fit()
print(results.summary())

df['forecast'] = results.predict(start=2, end=6, dynamic= True)  
df[['Hasil Retribusi Daerah', 'forecast']].plot(figsize=(12, 8))
# plt.show()

def forcasting_future_year(df, no_of_year):
    df_perdict = df.reset_index()
    mon = df_perdict['Tahun']
    mon = mon + pd.DateOffset(years = no_of_year)
    future_dates = mon[-no_of_year -1:]
    df_perdict = df_perdict.set_index('Tahun')
    future = pd.DataFrame(index=future_dates, columns= df_perdict.columns)
    df_perdict = pd.concat([df_perdict, future])
   
    df_perdict['forecast'] = results.predict(start =6 , end = 7+no_of_year, dynamic= True)  
    df_perdict[['Hasil Retribusi Daerah', 'forecast']].iloc[-no_of_year - 12:].plot(figsize=(12, 8))
    plt.show()
    return df_perdict[-no_of_year:]

predicted = forcasting_future_year(df,1)
print(predicted)