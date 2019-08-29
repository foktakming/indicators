import numpy as np
import pandas as pd


class CommodityChannelIndex(object):
    """
    计算CCI
    """
    def __init__(self, data_set):
        self.data_set = data_set
        # 确定系数
        self.constant = 0.015

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
            elif self.data_set.columns[col_num] == "Volume":
                self.volume_index = col_num

    def close_price(self):

        close_list = []
        for index in range(len(self.data_set)):
            close_p = self.data_set.iloc[index, self.close_index]

            close_list.append(close_p)

        return np.array(close_list)

    def high_price(self):
        high_list = []
        for index in range(len(self.data_set)):
            high = self.data_set.iloc[index, self.high_index]

            high_list.append(high)

        return np.array(high_list)

    def low_price(self):
        low_list = []
        for index in range(len(self.data_set)):
            low = self.data_set.iloc[index, self.low_index]

            low_list.append(low)

        return np.array(low_list)

    def typical_price(self):

        close = self.close_price()
        high = self.high_price()
        low = self.low_price()

        Typical_price = (high + low + close) / 3

        return Typical_price

    def typical_price_sma(self, days):

        typical_price = self.typical_price()

        if days > len(self.data_set):
            raise ValueError('days must be larger than data_set')

        s_mean_list = []
        for d_index in range(len(self.data_set)):
            mean = np.mean(typical_price[d_index - days + 1:d_index + 1])
            s_mean_list.append(mean)

        return np.array(s_mean_list)

    def mean_deviation(self, days=20):
        """
        计算平均绝对偏离差
        :param days: 偏离差周期
        :return:
        """
        typical_price = self.typical_price()
        # 转换为Dataframe格式
        t_price = pd.DataFrame(typical_price)

        mean_dev_list = []
        for d_index in range(len(self.data_set)):

            if d_index < days - 1:
                mean_dev = np.nan
            else:
                # pandas中有计算偏离差的方法
                mean_dev = np.sum(np.abs(t_price.iloc[d_index - days + 1:d_index + 1, 0].mad()))
            mean_dev_list.append(mean_dev)

        return np.array(mean_dev_list)

    def CCI(self, days=20):

        t_price = self.typical_price()
        t_price_sma = self.typical_price_sma(days)
        mean_dev = self.mean_deviation(days)

        cci = (t_price - t_price_sma) / ((self.constant) * mean_dev)

        return cci
