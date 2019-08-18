import numpy as np
import pandas as pd
from EMA import ExponentialMovingAverage


class TrueStrengthIndex(ExponentialMovingAverage):
    """
    计算TSI
    """

    def previous_close_price(self):
        """
        上一日close
        :return:
        """
        previous_close_list = []
        for index in range(len(self.data_set)):

            if index - 1 == -1:
                previous_close = np.nan
            else:
                previous_close = self.data_set.iloc[index - 1, self.close_index]

            previous_close_list.append(previous_close)

        return np.array(previous_close_list)

    def pc(self):
        """
        价格涨跌值
        :return:
        """
        current_close = self.close_price()
        previous_close = self.previous_close_price()

        pc_value = current_close - previous_close

        return pc_value

    def absolute_pc(self):

        pc = self.pc()

        abs_pc = np.abs(pc)

        return abs_pc

    def simple_movingaverage(self, days, price_data=None):
        """
        重写计算sma
        增加选择计算的数组
        :param days:
        :param price_data:
        :return:
        """
        if days > len(self.data_set):
            raise ValueError('days must be larger than data_set')

        if type(price_data) != np.ndarray:
            raise ValueError("type of data must be ndarray")

        s_mean_list = []
        for d_index in range(len(self.data_set)):
            mean = np.mean(price_data[d_index - days + 1:d_index + 1])
            s_mean_list.append(mean)

        return np.array(s_mean_list)

    def exponential_movingaverage(self, days, price_data=None):
        """
        重写计算ema
        增加选择计算的数组
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
            if index < days - 1:
                ema = np.nan
            elif index == days - 1:
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
            if index < first_days - 1 + second_days - 1:
                ema = np.nan
            elif index == first_days - 1 + second_days - 1:
                ema = sma[index]
            else:
                ema = (price_data[index - 1] - ema_list[-1]) * multi + ema_list[-1]

            ema_list.append(ema)

        return np.array(ema_list)

    def TSI(self, first_days=25, second_days=13):

        pc = self.pc()
        abs_pc = self.absolute_pc()

        first_smooth_pc = self.exponential_movingaverage(days=first_days, price_data=pc)
        second_smooth_pc = self.second_smooth(first_days=first_days, second_days=second_days,
                                              price_data=first_smooth_pc)

        first_smooth_abs_pc = self.exponential_movingaverage(days=first_days, price_data=abs_pc)
        second_smooth_abs_pc = self.second_smooth(first_days=first_days, second_days=second_days,
                                                  price_data=first_smooth_abs_pc)

        tsi = 100 * (second_smooth_pc / second_smooth_abs_pc)

        return tsi
