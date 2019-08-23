import numpy as np
import pandas as pd


class ExponentialMovingAverage(object):
    """
    计算指数移动平均EMA
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

    def simple_movingaverage(self, days):

        if days > len(self.data_set):
            raise ValueError('days must be larger than data_set')

        s_mean_list = []
        for d_index in range(len(self.data_set)):
            mean = np.mean(self.data_set.iloc[d_index - days + 1:d_index + 1, self.close_index])
            s_mean_list.append(mean)

        return np.array(s_mean_list)

    def close_price(self):

        close_list = []
        for index in range(len(self.data_set)):
            close_p = self.data_set.iloc[index, self.close_index]

            close_list.append(close_p)

        return np.array(close_list)

    def exponential_movingaverage(self, days):

        simple_mean = self.simple_movingaverage(days)
        multi = 2 / (days + 1)
        print(multi)
        close = self.close_price()

        ema_list = []

        for index in range(len(simple_mean)):
            if index < days - 1:
                ema = np.nan
            elif index == days - 1:
                ema = simple_mean[index]
            else:
                ema = (close[index] - ema_list[-1]) * multi + ema_list[-1]

            ema_list.append(ema)

        return np.array(ema_list)
