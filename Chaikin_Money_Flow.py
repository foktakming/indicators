import numpy as np
import pandas as pd


class ChaikinMoneyFlow(object):
    """
    计算CMF
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
                # 新添加成交量的列索引
            elif self.data_set.columns[col_num] == "Volume":
                self.volume_index = col_num

    def close_price(self):
        """
        获取收盘价
        :return:
        """
        close_list = []
        for index in range(len(self.data_set)):
            close_p = self.data_set.iloc[index, self.close_index]

            close_list.append(close_p)

        return np.array(close_list)

    def high_price(self):
        """
        获取最高价
        :return:
        """
        high_list = []
        for index in range(len(self.data_set)):
            high = self.data_set.iloc[index, self.high_index]

            high_list.append(high)

        return np.array(high_list)

    def low_price(self):
        """
        获取最低价
        :return:
        """
        low_list = []
        for index in range(len(self.data_set)):
            low = self.data_set.iloc[index, self.low_index]

            low_list.append(low)

        return np.array(low_list)

    def volume_value(self):
        """
        获取成交量
        :return:
        """
        volume_list = []
        for index in range(len(self.data_set)):
            volume = self.data_set.iloc[index, self.volume_index]

            volume_list.append(volume)

        return np.array(volume_list)

    def money_flow_multiplier(self):
        """
        计算资金流乘数
        :return:
        """
        close = self.close_price()
        high = self.high_price()
        low = self.low_price()

        mfm = ((close - low) - (high - close)) / (high - low)

        return mfm

    def money_flow_volume(self):

        volume = self.volume_value()
        multiplier = self.money_flow_multiplier()

        mfv = multiplier * volume

        return mfv

    def sum_of_volume(self, days):
        """
        周期内的volume总和
        :param days: 周期
        :return:
        """
        volume = self.volume_value()
        sum_of_volume_list = []

        for index in range(len(self.data_set)):

            if index < days - 1:
                sum_of_volume = np.nan
            else:
                sum_of_volume = np.sum(volume[index - days + 1: index + 1])

            sum_of_volume_list.append(sum_of_volume)

        return np.array(sum_of_volume_list)

    def sum_of_mfv(self, days):
        """
        周期内的现金流总和
        :param days:
        :return:
        """
        mfv = self.money_flow_volume()
        sum_of_mfv_list = []

        for index in range(len(self.data_set)):

            if index < days - 1:
                sum_of_mfv = np.nan
            else:
                sum_of_mfv = np.sum(mfv[index - days + 1: index + 1])

            sum_of_mfv_list.append(sum_of_mfv)

        return np.array(sum_of_mfv_list)

    def CMF(self, days=20):

        s_mfv = self.sum_of_mfv(days)
        s_volume = self.sum_of_volume(days)

        cmf = s_mfv / s_volume

        return cmf