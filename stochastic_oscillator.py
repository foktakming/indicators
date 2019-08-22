import numpy as np
import pandas as pd


class StochasticOscillator(object):
    """
    计算随机指标KD值
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

    def max_high(self, period):
        """
        周期内最大
        :param period:
        :return:
        """
        max_high_list = []
        for index in range(len(self.data_set)):
            max_high = np.max(self.data_set.iloc[index - period + 1:index + 1, self.high_index])

            max_high_list.append(max_high)

        return np.array(max_high_list)

    def min_low(self, period):
        """
        周期内最低
        :param period:
        :return:
        """
        min_low_list = []
        for index in range(len(self.data_set)):
            min_low = np.min(self.data_set.iloc[index - period + 1:index + 1, self.low_index])

            min_low_list.append(min_low)

        return np.array(min_low_list)

    def d_value(self, k_value):
        """
        计算 %D的通用公式
        :param k_value: 计算%D 的 %K
        :return:
        """
        d_value_list = []
        for index in range(len(self.data_set)):
            d = np.mean(k_value[index - 3 + 1: index + 1])

            d_value_list.append(d)

        return np.array(d_value_list)

    def fast_k_value(self, period=14):
        """
        计算fast %K
        :param period:
        :return:
        """
        close = self.close_price()
        low = self.min_low(period)
        high = self.max_high(period)

        k_value = (close - low) / (high - low) * 100

        return k_value



    def fast_d_value(self, period=14):
        """
        计算fast %D
        :param period:
        :return:
        """
        return self.d_value(self.fast_k_value(period))

    def slow_k_value(self, period=14):
        """
        计算 slow %K
        :param period:
        :return:
        """
        slow = self.fast_d_value(period)

        return slow

    def slow_d_value(self, period=14):
        """
        计算 slow %D
        :param period:
        :return:
        """
        return self.d_value(self.slow_k_value(period))

    def full_k_value(self, period=14, days=10):
        """
        计算 full %K
        :param period: 计算fast %K 的周期
        :param days: 计算full %k 的周期
        :return:
        """
        fast_k_value = self.fast_k_value(period)

        full_k_value_list = []
        for index in range(len(self.data_set)):
            full_k = np.mean(fast_k_value[index - days + 1:index + 1])

            full_k_value_list.append(full_k)

        return np.array(full_k_value_list)

    def full_d_value(self, period=14, days=10):
        """
        计算 full %D
        :param period:
        :param days: 
        :return:
        """
        return self.d_value(self.full_k_value(period, days))