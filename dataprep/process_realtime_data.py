import json
from dataprep.data_source_manager import DataSourceManager
import pandas as pd


class ProcessRealtimeData:
    """Class used to process, predict and yield plotting data for one point

    """
    def __init__(self, csv_path, csv_filename, col_names):
        """Class initializer (Constructor)

        Just so that the model does not have to be retrained each time we want to make a prediction,
        the values of scaler, pca, column means, and model that are all calculated at train time are saved.
        So this constructor retrieves all those values necessary to prepare each point for prediction.
        :param csv_filename: File name ( including path ) of the optional csv file used as a data source
        :type: string
        :param csv_path: path to csv data
        :type: string
        :param col_names
        :type: list of string
        """
        self.csv_filename = csv_filename
        self.csv_path = csv_path
        self.col_names = col_names

        self.row_counter = 0




    def process_points(self):
        """Process one point from the prediction data
        This function is a generator that yields messages back to client.  The messages can be one of two types:
        (1) event: update
        (2) event: jobfinished
        The message 'event: update' contains a json object associated with the 'data:' key.  The json object
        contains the prediction data as well as plotting data for two PC's (see self.__create_dict())
        An external data source generator (DataSourceManager.csv_line_reader()) is used to retrieve prediction data one
        point at a time.
        :return: none  NOTE:  This class method is a generator, so there is no return. However it does yield
        a JSON serialized dictionary that contains the data for plotting the prediction graph
        """

        # gen is a generator that is an iterable of dictionaries. Each dictionary contains one row of prediction data
        # including timestamp and sensor data

        gen = DataSourceManager.csv_line_reader(self.csv_path, self.csv_filename)

        while True:
            row = next(gen, None)  # Get next row where row is a dictionary
            if row is None:
                # The value of this yield, when received by the client javascript, will shut down the socket that is
                # used for pushing the prediction data.
                yield "event: jobfinished\ndata: " + "none" + "\n\n"
                break  # Terminate this event loop
            else:
                plot_dict = self.__create_plot_dict(row)
                dict_as_json = json.dumps(plot_dict)
                yield "event: update\ndata: " + dict_as_json + "\n\n"

    def __create_plot_dict(self, one_row_dict):
        """Private method to create a dictionary
        :param one_row_dict: One row as a DataFrame
        :type: dictionary
        :return: A dictionary of data that will be used for plotting the real time prediction
        """
        # Get values of specified keys:
        sensor_values = [one_row_dict[x] for x in self.col_names]
        # Build new dict with specified col_names:
        plot_dict = dict(zip(self.col_names, sensor_values))

        return plot_dict

