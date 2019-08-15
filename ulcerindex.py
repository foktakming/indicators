import numpy as np
import pandas as pd


class UlcerIndex(object):
    """
    计算的当前Ulcer index
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

    def close_price(self):

        close_list = []
        for index in range(len(self.data_set)):

            close_p = self.data_set.iloc[index, self.close_index]

            close_list.append(close_p)

        return np.array(close_list)

    def max_close(self, days):

        max_close_list = []

        for index in range(len(self.data_set)):
            max_close = np.max(self.data_set.iloc[index - days + 1:index + 1, self.close_index])

            max_close_list.append(max_close)

        return np.array(max_close_list)

    def precent_drawdown(self, days):
        """
        回撤百分比
        :param days:
        :return:
        """
        close = self.close_price()
        max_close = self.max_close(days)

        drawdown = (close - max_close) / max_close * 100

        return drawdown

    def squared_average(self, days):

        precent_drawdown = self.precent_drawdown(days)

        squared_list = []
        for index in range(len(precent_drawdown)):
            if index - days < 0:
                squared = np.nan
            else:
                # 选取至今日最新的数据
                squared = np.sum(np.square(precent_drawdown)[index - days + 1:index + 1])

            squared_list.append(squared)

        squared_ave = np.array(squared_list) / days

        return squared_ave

    def UI_value(self, days):

        squared_average = self.squared_average(days)

        ulcer_index = np.sqrt(squared_average)

        return ulcer_index