import numpy as np
import pandas as pd


class Williams_R_value(object):
    """
    计算威廉指标
    """
    def __init__(self, data_set, days):
        self.data_set = data_set
        self.days = days

        if type(self.data_set) != pd.DataFrame:
            raise ValueError("data_set must be pd.DataFrame ")

        if days > len(self.data_set):
            raise ValueError('days must be larger than data_set')

        # 确定每个价格的列索引
        for col_num in range(len(self.data_set.columns)):

            if self.data_set.columns[col_num] == "Open":
                self.open_index = col_num
            elif self.data_set.columns[col_num] == "High":
                self.high_index = col_num
            elif self.data_set.columns[col_num] == "Low":
                self.low_index = col_num
            elif self.data_set.columns[col_num] == "Close":
                self.close_index = col_num

    def highest(self):
        """
        计算最高价
        :return:
        """
        high_list = []
        for d_index in range(len(self.data_set)):
            high = np.max(self.data_set.iloc[d_index - self.days:d_index, self.high_index])

            high_list.append(high)

        return np.array(high_list)

    def lowest(self):
        """
        计算最低价
        :return:
        """
        low_list = []
        for d_index in range(len(self.data_set)):
            low = np.min(self.data_set.iloc[d_index - self.days:d_index, self.low_index])

            low_list.append(low)

        return np.array(low_list)

    def close_previous(self):
        """
        上一日的收盘价
        :return:
        """
        close_list = []
        for d_index in range(len(self.data_set)):
            if d_index - 1 == -1:
                close = np.nan
            else:
                close = self.data_set.iloc[d_index - 1, self.close_index]

            close_list.append(close)

        return np.array(close_list)

    def will_value(self):

        High = self.highest()
        Low = self.lowest()
        Close = self.close_previous()

        will = (High - Close) / (High - Low) * -100

        return will
