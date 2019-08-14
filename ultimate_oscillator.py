import numpy as np
import pandas as pd


class UltimateOscillator(object):
    """
    计算终极摇摆指标
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
        """
        求今低与昨收的最小值
        :return:
        """
        min_list = []
        for index in range(len(self.data_set)):

            if index - 1 == -1:
                min_p = self.data_set.iloc[index, self.low_index]
            else:
                min_p = min(self.data_set.iloc[index - 1, self.close_index], self.data_set.iloc[index, self.low_index])

            min_list.append(min_p)

        return np.array(min_list)

    def max_price(self):
        """
        求今高与昨收的最大值
        :return:
        """
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

    def Buying_Pressure(self):

        Close = self.close_price()
        Min = self.min_price()

        BP = Close - Min

        return BP

    def True_Range(self):

        Max = self.max_price()
        Min = self.min_price()

        TR = Max - Min

        return TR

    def Average_P(self, days):
        """
        计算 BP 与 TR 的比值
        :param days:
        :return:
        """
        BP = self.Buying_Pressure()
        TR = self.True_Range()

        Ave = []
        for period in range(len(BP)):

            average_value = (np.sum(BP[period - days:period])) / (np.sum(TR[period - days:period]))

            Ave.append(average_value)

        return np.array(Ave)

    def UO_value(self, days_1=7, days_2=14, days_3=28):

        Average_1 = self.Average_P(days_1)
        Average_2 = self.Average_P(days_2)
        Average_3 = self.Average_P(days_3)

        ratio_ave_1 = days_3 / days_1
        ratio_ave_2 = days_3 / days_2
        ratio_ave_3 = days_3 / days_3

        UO = 100 * (Average_1 * ratio_ave_1 + Average_2 * ratio_ave_2 + Average_3) / (
                    ratio_ave_1 + ratio_ave_2 + ratio_ave_3)

        return UO