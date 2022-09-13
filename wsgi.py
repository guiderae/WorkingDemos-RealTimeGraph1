from flask import Flask, render_template, Response, request
from dataprep.process_realtime_data import ProcessRealtimeData
from utils.data_file_manager import DataFileManager

app = Flask(__name__)


@app.route('/')
def main():
    """
    First create a cache directory if not exist.
    Just show the main.html without any data
    :return:
    """
    csv_filenames = DataFileManager.get_file_names_in_path('static/data')
    return render_template('main.html', filenames=csv_filenames)


@app.route('/runPredict')
def run_predict():
    file_name_only = request.args.get('predictCSVFileName')
    path = 'static/data'
    col_names = ['timestamp', 'sensor_04', 'sensor_18', 'sensor_34']

    rtd = ProcessRealtimeData(path, file_name_only, col_names)
    rtd.process_points()
    return Response(rtd.process_points(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(port=5001, debug=True)


