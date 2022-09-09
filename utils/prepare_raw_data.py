from os.path import join
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np


class PrepareRawData:
    """
    This class is a utility that is not part of the web application.  This class is used to prepare the data
    for plotting by replacing all blank values with the columnwise mean and then scaling all sensor columns.
    An assumption is made that the first column in the csv is a timestamp and the last column is the target.
    See the method get_scaler()
    """
    def __init__(self, source_file_names_path, dest_data_path, file_names):
        self.source_path = source_file_names_path
        self.dest_path = dest_data_path
        self.file_names = file_names

    @staticmethod
    def replace_nan_with_mean(df):
        """
        First replace all empty cells with NaN
        Then replace NaN columnwise with mean of each column inplace
        :param df: DataFrame
        :type: Pandas DataFrame
        :return: none
        """
        cols = df.columns
        # Replace blanks with np.nan
        df_no_blank = df.replace(r'^\s*$', np.nan, regex=True)
        # Columnwise replace all nan with mean of column
        df.fillna(value=df_no_blank[cols].mean(numeric_only=True), inplace=True)

    @staticmethod
    def get_scaler(training_df):
        """Get a scaler for training data
        Apply MinManScaler to the training data using the range (0, 1)
        :param training_df:
        :type: Pandas DataFrame
        :return: scaler for the training data
        :type: MinMaxScaler
        """
        # Get sensor names.  Assume first column is 'timestamp' and last column is target, so remove them
        sensor_names = training_df.columns[1:-1]
        min_max_scaler = MinMaxScaler(feature_range=(0, 1))
        scaler = min_max_scaler.fit(training_df[sensor_names])

        return scaler

    @staticmethod
    def scale_dataframe(scaler, data_df):
        """Transform given dataframe using given scaler as applied to the given columns

        :param scaler: The scaler that has been fit to the dataframe
        :type: MinMaxScaler
        :param data_df: Dataframe to be scaled
        :type: Pandas DataFrame
        :return: dataframe of scaled data
        :type: DataFrame
        """
        sensor_names = data_df.columns[1:-1]
        scaled_data = scaler.transform(data_df[sensor_names])
        scaled_df = pd.DataFrame(data=scaled_data,
                         index=data_df['timestamp'],
                         columns=sensor_names)

        return scaled_df

    def do_data_prep(self):
        """
        Prepare and scale all csv files found in self.surce_path.  Write prepared data to csv files and store in
        self.dest_path
        :return:
        """
        counter = 0
        for file_name in self.file_names:
            df = pd.read_csv(join(self.source_path, file_name))
            PrepareRawData.replace_nan_with_mean(df)
            scaler = PrepareRawData.get_scaler(df)
            scaled_dataframe = PrepareRawData.scale_dataframe(scaler, df)
            scaled_dataframe.to_csv(join(self.dest_path, "scaled_data" + str(counter) + ".csv"))
            counter += 1


source_data_path = "../static/rawdata"
dest_data_path = "../static/data"
file_names = ["prediction_slice0.csv", "prediction_slice1.csv", "prediction_slice2.csv"]

data_prep = PrepareRawData(source_data_path, dest_data_path, file_names)
data_prep.do_data_prep()
