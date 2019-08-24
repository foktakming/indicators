import numpy as np
import pandas as pd


class RateOfChange(object):
    """
    计算ROC
    """
    def __init__(self, data_set):
        self.data_set = data_set

        if type(self.data_set) != pd.DataFrame:
            raise ValueError("data_set must be pd.DataFrame ")

        for col_num in range(len(self.data_set.columns)):

            if self.data_set.columns[col_num] == "Open":
                self.open_index = col_num
            elif self.data_set.columns[col_num] == "High":
                self.high_index = col_num
            elif self.data_set.columns[col_num] == "Low":
                self.low_index = col_num
            elif self.data_set.columns[col_num] == "Close":
                self.close_index = col_num

    def close_current(self):
        """
        今收
        :return:
        """
        close_list = []
        for index in range(len(self.data_set)):
            close_p = self.data_set.iloc[index, self.close_index]

            close_list.append(close_p)

        return np.array(close_list)

    def close_previous(self, days):
        """
        n日前的收盘
        :param days:
        :return:
        """
        close_list = []
        for index in range(len(self.data_set)):

            if index < days - 1:
                close_p = np.nan
            else:
                close_p = self.data_set.iloc[index - days + 1, self.close_index]

            close_list.append(close_p)

        return np.array(close_list)

    def ROC(self, days):

        current_close = self.close_current()
        previous_close = self.close_previous(days)

        roc = (current_close - previous_close) / previous_close * 100

        return roc