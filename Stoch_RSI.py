import numpy as np
import pandas as pd
from RSI import RelativeStrengthIndex


class StochRSI(RelativeStrengthIndex):

    def max_rsi(self, rsi_days, period=14):

        rsi = self.RSI(rsi_days)

        max_rsi_list = []
        for index in range(len(rsi)):

            if index < period:
                rsi_value = np.nan
            else:
                rsi_value = np.nanmax(rsi[index - period + 1:index + 1])

            max_rsi_list.append(rsi_value)

        return np.array(max_rsi_list)

    def min_rsi(self, rsi_days, period=14):

        rsi = self.RSI(rsi_days)

        min_rsi_list = []
        for index in range(len(rsi)):

            if index < period:
                rsi_value = np.nan
            else:
                rsi_value = np.nanmin(rsi[index - period + 1:index + 1])

            min_rsi_list.append(rsi_value)

        return np.array(min_rsi_list)

    def stoch_rsi(self, days, period=14):

        rsi = self.RSI(days)
        max_rsi = self.max_rsi(days, period)
        min_rsi = self.min_rsi(days, period)

        stoch_rsi = (rsi - min_rsi) / (max_rsi - min_rsi)

        return stoch_rsi

