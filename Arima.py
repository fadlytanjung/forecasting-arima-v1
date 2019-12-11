import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARIMAResults

# monkey patch around bug in ARIMA class
def __getnewargs__(self):
	return ((self.endog), (self.k_lags, self.k_diff, self.k_ma))
ARIMA.__getnewargs__ = __getnewargs__

class Arima:
    def __init__(self, data,order=(1, 1, 0),
                 sensasional_order=(1, 1, 1, 365)):
        self.order = order
        self.sensasional_order = sensasional_order
        self.data = self.read_data(data)

    def read_data(self,path):
        df = pd.read_csv(path, delimiter=';')
        return df

    def get_columns(self):
        return list(self.data.columns)

    def len_columns(self):
        return len(self.get_columns())

    def drop_column(self,column):
        return self.data.drop(self.data.columns[column],axis=1)

    def convert_date_to_time(self,data):
        data[str(self.get_columns()[0])] = pd.to_datetime(
            data[str(self.get_columns()[0])]
        , format='%Y')
        
        return data

    def set_index(self,data):
        data = data.set_index(self.get_columns()[0])

        return data

    def model(self,data,name_model):
        model = sm.tsa.SARIMAX(
            data[list(data.columns)[0]], order=self.order,
            sensasional_order=self.sensasional_order)
        results = model.fit()
        
        # save model
        results.save('static/arima_model/'+str(name_model)+'.pkl')
        print(results.summary())
        return results

    def show_plot_model(self,data,model,name_file):
        # model[1]['forecast'] = model[0].predict(start=1, end=6, dynamic=True)
        data['forecast'] = model.predict(dynamic=False)
        data[[list(data.columns)[0], 'forecast']].plot(figsize=(12, 8))
        # return plt.show()
        data_model = data.to_json(orient='table')
        plt.savefig('static/image_plot_model/'+str(name_file)+'.png')
        return data_model

    def forecast_future(self, data, name_model,number_of_year):
        
        results_model = ARIMAResults.load(
            'static/arima_model/'+str(name_model)+'.pkl')
        df_perdict = data.reset_index()

        mon = df_perdict[self.get_columns()[0]]
        mon = mon + pd.DateOffset(years=number_of_year)
        
        future_dates = mon[-number_of_year - 1:]
        df_perdict = df_perdict.set_index(self.get_columns()[0])
        
        future = pd.DataFrame(index=future_dates, columns=df_perdict.columns)
        df_perdict = pd.concat([df_perdict, future])

        df_perdict['forecast'] = results_model.predict(
            start=len(data)-1, end=len(data)+number_of_year, dynamic=True)
        df_perdict[[str(data.columns[0]), 'forecast']
                ].iloc[-number_of_year - 12:].plot(figsize=(12, 8))
        
        plt.savefig('static/image_plot_forecast/'+str(name_model)+'.png')
        model = df_perdict[-number_of_year:].to_json(orient='table')
        
        return model

if __name__ == "__main__":
    
    obj = Arima('data/RealArima.csv')
    
    columns = obj.get_columns()
    len_columns = obj.len_columns()
    
    dic_column = {}
    dic_model = []
    dic_forecast = []
    arr = [i for i in range(len_columns)]

    for i in range(1,len_columns):
        arr_ = []
        for j in range(1, len(arr)):
            if i != j:
                arr_.append(arr[j])
        # print(arr_)
        dic_column[i] = columns[i]
        drop_columns = obj.drop_column(arr_)
        
        #set index name column
        index_name_model_column = i
        convert_to_time = obj.convert_date_to_time(drop_columns)
        set_index = obj.set_index(convert_to_time)
        model = obj.model(set_index,index_name_model_column)
        plot_model = obj.show_plot_model(set_index,model,index_name_model_column)    
        forecast_future = obj.forecast_future(set_index,index_name_model_column,1)
        
        # insert data model
        model_json = json.loads(plot_model)
        dic_model.append(model_json)

        #insert data forecast
        forecast_json = json.loads(forecast_future)
        dic_forecast.append(forecast_json)

    with open('static/result/data_model.json', 'w+') as f:
        json.dump(dic_model, f)
        f.close()

    with open('static/result/data_forecast.json','w+') as f:
        json.dump(dic_forecast,f)
        f.close()



