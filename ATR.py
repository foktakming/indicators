import numpy as np
import pandas as pd


class AverageTrueRange(object):
    """
    计算ATR
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

    def min_price(self):

        min_list = []
        for index in range(len(self.data_set)):

            if index - 1 == -1:
                min_p = self.data_set.iloc[index, self.low_index]
            else:
                min_p = min(self.data_set.iloc[index - 1, self.close_index], self.data_set.iloc[index, self.low_index])

            min_list.append(min_p)

        return np.array(min_list)

    def max_price(self):

        max_list = []
        for index in range(len(self.data_set)):

            if index - 1 == -1:
                max_p = self.data_set.iloc[index, self.high_index]
            else:
                max_p = max(self.data_set.iloc[index - 1, self.close_index], self.data_set.iloc[index, self.high_index])

            max_list.append(max_p)

        return np.array(max_list)

    def close_price(self):

        close_list = []
        for index in range(len(self.data_set)):
            close_p = self.data_set.iloc[index, self.close_index]

            close_list.append(close_p)

        return np.array(close_list)

    def True_Range(self):

        Max = self.max_price()
        Min = self.min_price()

        TR = Max - Min

        return TR

    def AverageTR(self, days=14):

        tr = self.True_Range()

        atr_list = []
        for index in range(len(self.data_set)):

            if index < days:
                atr_value = np.nan
            # 第一天ATR为之前的TR平均值
            elif index == days:
                atr_value = np.average(tr[index - days:index])
            else:
                # 取最新的TR值计算ATR
                atr_value = (tr[index - 1] + atr_list[-1] * 13) / days

            atr_list.append(atr_value)

        return np.array(atr_list)


