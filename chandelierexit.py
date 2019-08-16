import numpy as np
import pandas as pd

from ATR import AverageTrueRange


class ChandelierExit(AverageTrueRange):
    """
    类继承ATR
    基于ATR的指标
    """
    def max_high(self, days):

        max_high_list = []
        for index in range(len(self.data_set)):
            max_high = np.max(self.data_set.iloc[index - days:index, self.high_index])

            max_high_list.append(max_high)

        return np.array(max_high_list)

    def min_low(self, days):

        min_low_list = []
        for index in range(len(self.data_set)):
            min_low = np.min(self.data_set.iloc[index - days:index, self.low_index])

            min_low_list.append(min_low)

        return np.array(min_low_list)

    def long_chandelier(self, days=22, multi=3):
        """
        长仓立场位置
        :param days:
        :return:
        """
        max_value = self.max_high(days)
        atr_value = self.AverageTR(days)

        long_chande = max_value - atr_value * multi

        return long_chande

    def short_chandelier(self, days=22, multi=3):
        """
        短仓立场位置
        :param days:
        :return:
        """
        min_value = self.min_low(days)
        atr_value = self.AverageTR(days)

        short_chande = min_value + atr_value * multi

        return short_chande