import numpy as np
import pandas as pd
from EMA import ExponentialMovingAverage


class PPO_MACD(ExponentialMovingAverage):
    """
    计算ppo 和 macd
    因为较相似，所以一起计算
    """
    def ppo(self, days_1=12, days_2=26):

        ema12 = self.exponential_movingaverage(days_1)
        ema26 = self.exponential_movingaverage(days_2)

        ppo = (ema12 - ema26) / ema26 * 100

        return ppo

    def ppo_signal(self, days_1=12, days_2=26, days_3=9):
        """
        ppo的信号线
        :param days_1:
        :param days_2:
        :param days_3: 信号线的周期
        :return:
        """
        ppo = self.ppo(days_1, days_2)

        signal_days = max(days_1, days_2) + days_3

        simple_mean_list = []
        for s_index in range(len(self.data_set)):
            simple_mean_value = np.mean(ppo[s_index - days_3 + 1:s_index + 1])

            simple_mean_list.append(simple_mean_value)

        simple_mean = np.array(simple_mean_list)

        multi = 2 / (days_3 + 1)

        signal_list = []

        for index in range(len(simple_mean)):
            if index < signal_days - 2:
                signal = np.nan
            elif index == signal_days - 2:
                signal = simple_mean[index]
            else:
                signal = (ppo[index] - signal_list[-1]) * multi + signal_list[-1]

            signal_list.append(signal)

        return np.array(signal_list)

    def macd(self, days_1=12, days_2=26):

        ema12 = self.exponential_movingaverage(days_1)
        ema26 = self.exponential_movingaverage(days_2)

        macd = ema12 - ema26

        return macd

    def macd_signal(self, days_1=12, days_2=26, days_3=9):
        """
        macd 信号线
        :param days_1:
        :param days_2:
        :param days_3: 信号线的周期
        :return:
        """
        macd = self.macd(days_1, days_2)

        signal_days = max(days_1, days_2) + days_3

        simple_mean_list = []
        for s_index in range(len(self.data_set)):
            simple_mean_value = np.mean(macd[s_index - days_3 + 1:s_index + 1])

            simple_mean_list.append(simple_mean_value)

        simple_mean = np.array(simple_mean_list)

        multi = 2 / (days_3 + 1)

        signal_list = []

        for index in range(len(simple_mean)):
            if index < signal_days - 2:
                signal = np.nan
            elif index == signal_days - 2:
                signal = simple_mean[index]
            else:
                signal = (macd[index] - signal_list[-1]) * multi + signal_list[-1]

            signal_list.append(signal)

        return np.array(signal_list)

    def histogram_ppo(self, days_1=12, days_2=26, days_3=9):

        ppo = self.ppo(days_1, days_2)

        ppo_signal = self.ppo_signal(days_1, days_2, days_3)

        histogram = ppo - ppo_signal

        return histogram

    def histogram_macd(self, days_1=12, days_2=26, days_3=9):

        macd = self.macd(days_1, days_2)

        macd_signal = self.macd_signal(days_1, days_2, days_3)

        histogram = macd - macd_signal

        return histogram
