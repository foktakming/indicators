import numpy as np
import pandas as pd
from True_Strength_Index import TrueStrengthIndex


class TripleEMA(TrueStrengthIndex):

    def exponential_movingaverage(self, days, price_data=None):
        """
        重写计算ema
        :param days:
        :param price_data:
        :return:
        """
        if price_data is None:
            raise ValueError("no data to calculate")

        if type(price_data) != np.ndarray:
            raise ValueError("type of data must be ndarray")

        sma = self.simple_movingaverage(days=days, price_data=price_data)
        multi = 2 / (days + 1)

        ema_list = []
        for index in range(len(sma)):
            # 实际为nan的数量为 days-1，索引为days -2
            if index < days - 2:
                ema = np.nan
            elif index == days - 2:
                ema = sma[index + 1]
            else:
                ema = (price_data[index] - ema_list[-1]) * multi + ema_list[-1]

            ema_list.append(ema)

        return np.array(ema_list)

    def second_smooth(self, first_days, second_days, price_data=None):
        """
        计算第二次平滑时的ema
        :param first_days: 第一次计算ema的周期
        :param second_days: 第二次计算ema的周期，ema中的ema
        :param price_data:
        :return:
        """
        sma = self.simple_movingaverage(days=second_days, price_data=price_data)
        multi = 2 / (second_days + 1)

        ema_list = []
        #         调用了两次ema，对数据切片时，计算当前的数值需要提前1格
        for index in range(len(sma)):
            if index < first_days - 2 + second_days - 2:
                ema = np.nan
            elif index == first_days - 2 + second_days - 2:
                ema = sma[index + 1]
            else:
                ema = (price_data[index] - ema_list[-1]) * multi + ema_list[-1]

            ema_list.append(ema)

        return np.array(ema_list)

    def third_smooth(self, first_days, second_days, third_days, price_data=None):
        """
        计算第三次ema
        ema of ema of ema
        :param first_days:
        :param second_days:
        :param third_days:
        :param price_data:
        :return:
        """
        sma = self.simple_movingaverage(days=second_days, price_data=price_data)
        multi = 2 / (third_days + 1)

        ema_list = []
        for index in range(len(sma)):
            if index < first_days - 2 + second_days - 2 + third_days - 2:
                ema = np.nan
            elif index == first_days - 2 + second_days - 2 + third_days - 2:
                ema = sma[index + 1]
            else:
                ema = (price_data[index] - ema_list[-1]) * multi + ema_list[-1]

            ema_list.append(ema)

        return np.array(ema_list)

    def TRIX(self, first_days, second_days, third_days, price_data, period=1):
        """
        计算trix
        :param first_days:
        :param second_days:
        :param third_days:
        :param price_data:
        :param period: 计算trix的周期
        :return: 返回值为百分比
        """
        first_smooth_close = self.exponential_movingaverage(days=first_days, price_data=price_data)

        second_smooth_close = self.second_smooth(first_days=first_days, second_days=second_days,
                                                 price_data=first_smooth_close)

        triple_smooth_value = self.third_smooth(first_days=first_days, second_days=second_days,
                                                third_days=third_days, price_data=second_smooth_close)

        trix_list = []
        for index in range(len(self.data_set)):

            if index - period < 0:
                diviors = np.nan
            else:
                diviors = triple_smooth_value[index] - triple_smooth_value[index - period]

            trix = diviors / triple_smooth_value[index - period] * 100

            trix_list.append(trix)

        return np.array(trix_list)