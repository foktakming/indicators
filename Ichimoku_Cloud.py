import numpy as np
import pandas as pd


class IchimokuCloud(object):
    """
    计算 一目均衡云
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
        获取收盘价,用于信号判断
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

    def high_move(self, days):
        """
        周期内最高价
        :param days: 周期
        :return:
        """
        high = self.high_price()

        high_move_list = []
        for index in range(len(self.data_set)):

            if index < days - 1:
                high_move = np.nan
            else:
                high_move = np.max(high[index - days + 1:index + 1])

            high_move_list.append(high_move)

        return np.array(high_move_list)

    def low_move(self, days):
        """
        周期内最低价
        :param days: 周期
        :return:
        """
        low = self.low_price()

        low_move_list = []
        for index in range(len(self.data_set)):

            if index < days - 1:
                low_move = np.nan
            else:
                low_move = np.min(low[index - days + 1:index + 1])

            low_move_list.append(low_move)

        return np.array(low_move_list)

    def convesion_line(self, days=9):

        high = self.high_move(days)
        low = self.low_move(days)

        conversion = (high + low) / 2

        return conversion

    def base_line(self, days=26):

        high = self.high_move(days)
        low = self.low_move(days)

        base = (high + low) / 2

        return base

    def leading_a(self, c_days=9, b_days=26):
        """
        A领先线
        :param c_days:
        :param b_days:
        :return:
        """
        conversion = self.convesion_line(c_days)
        base = self.base_line(b_days)

        leading = (conversion + base) / 2

        return leading

    def leading_b(self, days=52):
        """
        B领先线
        :param days:
        :return:
        """
        high = self.high_move(days)
        low = self.low_move(days)

        leading = (high + low) / 2

        return leading

    def long_position(self):
        """
        突破压力位
        :return:
        """
        a_leading = self.leading_a()
        b_leading = self.leading_b()

        long_position_list = []
        for index in range(len(self.data_set)):

            if a_leading[index] > b_leading[index]:
                long_value = a_leading[index]
            elif a_leading[index] < b_leading[index]:
                long_value = b_leading[index]
            else:
                long_value = np.nan

            long_position_list.append(long_value)

        return np.array(long_position_list)

    def short_position(self):
        """
        下行支撑位
        :return:
        """
        a_leading = self.leading_a()
        b_leading = self.leading_b()

        short_position_list = []
        for index in range(len(self.data_set)):

            if a_leading[index] > b_leading[index]:
                short_value = b_leading[index]
            elif a_leading[index] < b_leading[index]:
                short_value = a_leading[index]
            else:
                short_value = np.nan

            short_position_list.append(short_value)

        return np.array(short_position_list)