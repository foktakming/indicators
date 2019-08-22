import numpy as np
import pandas as pd


class Volatility(object):
    """
    计算波动率
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

    def mean(self, period):
        """
        计算均值
        :param period: 计算周期
        :return:
        """
        if period > len(self.data_set):
            raise ValueError('days must be larger than data_set')

        mean_list = []
        for index in range(len(self.data_set)):
            mean = np.mean(self.data_set.iloc[index - period + 1:index + 1, self.close_index])

            mean_list.append(mean)

        return np.array(mean_list)

    def deviation(self, mean_period):
        """
        均值偏差
        :param mean_period:
        :return:
        """
        close = self.close_price()
        mean = self.mean(mean_period)

        dev = close - mean

        return dev

    def deviation_squared(self, mean_period):

        dev_squared = np.square(self.deviation(mean_period))

        return dev_squared

    def average_deviation_squared(self, mean_period, dev_period):
        """
        偏差平方的均值
        :param mean_period:close价格均值周期
        :param dev_period: dev平方的均值周期
        :return:
        """
        dev_squared = self.deviation_squared(mean_period)

        average_dev_squ_list = []
        for index in range(len(self.data_set)):
            average_dev_squ = np.mean(dev_squared[index - dev_period + 1:index + 1])

            average_dev_squ_list.append(average_dev_squ)

        return np.array(average_dev_squ_list)

    def vol_value(self, mean_period, dev_period):

        ave_dev_squ = self.average_deviation_squared(mean_period, dev_period)

        vol = np.sqrt(ave_dev_squ)

        return vol
