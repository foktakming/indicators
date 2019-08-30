import numpy as np
import pandas as pd
from True_Strength_Index import TrueStrengthIndex


class MassIndex(TrueStrengthIndex):
    """
    计算MI
    """
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

    def max_price_variation(self):
        """
        当日最大价差
        :return:
        """
        high = self.high_price()
        low = self.low_price()

        price_variation = high - low

        return price_variation

    def ema_ratio(self, days):

        price_var = self.max_price_variation()

        s_ema = self.exponential_movingaverage(days, price_data=price_var)
        d_ema = self.second_smooth(days, days, price_data=s_ema)

        ratio = s_ema / d_ema

        return ratio

    def MI(self, days=9, period=25):
        """
        对ratio求和
        :param days: 计算ema的周期
        :param period: 求和的周期
        :return:
        """
        ratio = self.ema_ratio(days)

        mass_index_list = []
        for index in range(len(self.data_set)):

            if index < period - 1:
                mass_index = np.nan
            else:
                mass_index = np.sum(ratio[index - period + 1: index + 1])

            mass_index_list.append(mass_index)

        return np.array(mass_index_list)
