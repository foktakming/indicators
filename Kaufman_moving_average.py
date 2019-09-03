import numpy as np
import pandas as pd


class KaufmanMovingAverage(object):
    """
    计算考夫曼自适应移动平均线
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
        """
        获取收盘价
        :return:
        """
        close_list = []
        for index in range(len(self.data_set)):
            close_p = self.data_set.iloc[index, self.close_index]

            close_list.append(close_p)

        return np.array(close_list)

    def close_previous(self, days):
        """
        n日前的收盘
        :param days:
        :return:
        """
        close_list = []
        for index in range(len(self.data_set)):

            if index < days - 1:
                close_p = np.nan
            else:
                close_p = self.data_set.iloc[index - days + 1, self.close_index]

            close_list.append(close_p)

        return np.array(close_list)

    def change(self, days):

        close_cur = self.close_price()
        close_pre = self.close_previous(days)

        change = np.abs(close_cur - close_pre)

        return change

    def kaufman_volatility(self, days):

        change = self.change(days)

        volatility_list = []
        for index in range(len(self.data_set)):

            if index < days - 1:
                vol = np.nan
            else:
                vol = np.sum(change[index - days + 1:index + 1])

            volatility_list.append(vol)

        return np.array(volatility_list)

    def ER(self, days):

        change = self.change(days)
        volatility = self.kaufman_volatility(days)

        er = change / volatility

        return er

    def SC(self, days, short=2, long=30):

        er = self.ER(days)

        short_constant = 2 / (short + 1)
        long_constant = 2 / (long + 1)

        sc = np.square(er * (short_constant - long_constant) + long_constant)

        return sc

    def KAMA(self, days=10):

        close = self.close_price()
        sc = self.SC(days)

        kama_list = []

        for index in range(len(self.data_set)):

            if index < days * 2 - 2:
                kama = np.nan
            elif index == days * 2 - 2:
                kama = sc[index] * close[index]
            else:
                kama = kama_list[-1] + (sc[index] * close[index] - kama_list[-1])

            kama_list.append(kama)

        return np.array(kama_list)
