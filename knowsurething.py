import numpy as np
import pandas as pd
from rate_of_change import RateOfChange


class KnowSureThing(RateOfChange):
    """
    计算KST
    """
    def RCMA(self, roc_period, sma_period):
        """

        :param roc_period: 计算roc的周期
        :param sma_period: 计算roc的sma的周期
        :return:
        """
        roc = self.ROC(roc_period)

        rcma_list = []
        for index in range(len(self.data_set)):
            rcma = np.mean(roc[index - sma_period + 1: index + 1])

            rcma_list.append(rcma)

        return np.array(rcma_list)

    def KST(self, period_1=10, period_2=15, period_3=20, period_4=30, sma_1=10, sma_2=15):
        """

        :param period_1: 计算RCMA1的roc周期
        :param period_2: 计算RCMA2的roc周期
        :param period_3: 计算RCMA3的roc周期
        :param period_4: 计算RCMA4的roc周期
        :param sma_1:
        :param sma_2:
        :return:
        """
        rcma1 = self.RCMA(roc_period=period_1, sma_period=sma_1)
        rcma2 = self.RCMA(roc_period=period_2, sma_period=sma_1)
        rcma3 = self.RCMA(roc_period=period_3, sma_period=sma_1)
        rcma4 = self.RCMA(roc_period=period_4, sma_period=sma_2)

        kst = rcma1 * 1 + rcma2 * 2 + rcma3 * 3 + rcma4 * 4

        return kst

    def kst_signal(self, period_1=10, period_2=15, period_3=20, period_4=30, sma_1=10, sma_2=15):

        kst = self.KST(period_1, period_2, period_3, period_4, sma_1, sma_2)

        signal_list = []
        kst_sma = 9
        for index in range(len(self.data_set)):
            signal = np.mean(kst[index - kst_sma + 1: index + 1])

            signal_list.append(signal)

        return np.array(signal_list)