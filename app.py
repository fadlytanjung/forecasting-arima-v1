from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from Arima import Arima
import time,json,re,os

UPLOAD_FOLDER = 'input/tempData/'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def main():
    return render_template('index.html')

@app.route("/model", methods=["GET"])
def model_page():
    return render_template('model_page.html')

@app.route("/process_model",  methods=["GET","POST"])
def process_model():

    error = ""
    if 'file' in request.files:
            filetxt = request.files["file"]
            if filetxt and allowed_file(filetxt.filename):
                filename = secure_filename(filetxt.filename)
                # filetxt.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filetxt.save(os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv'))
                # print(result2.read(),"hehe")
                # with open(os.path.join(app.config['UPLOAD_FOLDER'], filetxt.filename), 'r', encoding="utf-8") as f:
                    # f.read()
                    # text = f.read()
                    # f.close()
            else:
                error = "Format file salah"

    # obj = Arima('input/tempData/'+filetxt.filename)
    obj = Arima('input/tempData/data.csv')

    columns = obj.get_columns()
    len_columns = obj.len_columns()

    dic_column = {}
    dic_model = []
    dic_forecast = []
    arr = [i for i in range(len_columns)]

    for i in range(1, len_columns):
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
        model = obj.model(set_index, index_name_model_column)
        plot_model = obj.show_plot_model(
        set_index, model, index_name_model_column)

        # insert data model
        model_json = json.loads(plot_model)
        dic_model.append({"data": model_json, "table": index_name_model_column,
        "title":columns[index_name_model_column]})


    with open('static/result/data_model.json', 'w+') as f:
        json.dump(dic_model, f)
        f.close()

    return render_template('process_model.html',model=dic_model)

@app.route("/predict", methods=["GET"])
def predict():
    return render_template('predict_page.html')

@app.route("/predict_result",  methods=["GET","POST"])
def predict_result():

    tahun = request.form['year']
    obj = Arima('input/tempData/data.csv')

    columns = obj.get_columns()
    len_columns = obj.len_columns()

    dic_column = {}
    dic_forecast = []
    arr = [i for i in range(len_columns)]

    for i in range(1, len_columns):
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
        forecast_future = obj.forecast_future(
            set_index, index_name_model_column, int(tahun))

        #insert data forecast
        forecast_json = json.loads(forecast_future)
        dic_forecast.append({"data": forecast_json, "table": index_name_model_column,
                            "title": columns[index_name_model_column]})

    with open('static/result/data_forecast.json', 'w+') as f:
        json.dump(dic_forecast, f)
        f.close()

    return render_template('predict_result.html',predict=dic_forecast)

if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

