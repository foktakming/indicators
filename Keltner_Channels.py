import numpy as np
import pandas as pd

from EMA import ExponentialMovingAverage
from ATR import AverageTrueRange


class KeltnerChannels(ExponentialMovingAverage, AverageTrueRange):
    """
    计算肯特钠通道
    """
    def middle_line(self, days=20):
        """
        中线=ema20
        :param days:
        :return:
        """
        middle = self.exponential_movingaverage(days)

        return middle

    def atr_10(self, days=10):

        atr = self.AverageTR(days)

        return atr

    def upper_line(self):
        """
        上轨道
        :return:
        """
        middle = self.middle_line()
        atr = self.atr_10()

        upper = middle + atr * 2

        return upper

    def low_line(self):
        """
        下轨道
        :return:
        """
        middle = self.middle_line()
        atr = self.atr_10()

        lower = middle - atr * 2

        return lower
