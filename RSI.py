import numpy as np
import pandas as pd


class RelativeStrengthIndex(object):
    """
    计算RSI
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

    def current_close(self):

        current_close_list = []
        for index in range(len(self.data_set)):
            c_price = self.data_set.iloc[index, self.close_index]

            current_close_list.append(c_price)

        return np.array(current_close_list)

    def previous_close(self):

        previous_close_list = []
        for index in range(len(self.data_set)):

            if index - 1 == -1:
                p_close = np.nan
            else:
                p_close = self.data_set.iloc[index - 1, self.close_index]

            previous_close_list.append(p_close)

        return np.array(previous_close_list)

    def price_change(self):
        """
        收盘价变动
        :return:
        """
        current_close_price = self.current_close()
        previous_close_price = self.previous_close()

        change = current_close_price - previous_close_price

        return change

    def gain(self):

        change = self.price_change()

        gain_list = []
        for gl in change:

            if gl > 0:
                gain_value = gl
            # 有可能会无变化，等于0
            elif gl <= 0:
                gain_value = 0
            else:
                gain_value = np.nan

            gain_list.append(gain_value)

        return np.array(gain_list)

    def loss(self):
        change = self.price_change()

        loss_list = []
        for gl in change:

            if gl >= 0:
                loss_value = 0
            elif gl < 0:
                loss_value = gl
            else:
                loss_value = np.nan
            loss_list.append(loss_value)

        return np.array(loss_list)

    def average_gain(self, days):

        gain = self.gain()

        ave_gain_list = []
        for index in range(len(self.data_set)):

            if index < days:
                ave_gain = np.nan
            elif index == days:
                # 第一天为nan，所以退后一格
                ave_gain = np.mean(gain[index - days + 1:index + 1])
            else:
                ave_gain = (ave_gain_list[-1] * (days - 1) + gain[index]) / days

            ave_gain_list.append(ave_gain)

        return np.array(ave_gain_list)

    def average_loss(self, days):

        loss = self.loss()

        ave_loss_list = []
        for index in range(len(self.data_set)):

            if index < days:
                ave_loss = np.nan
            elif index == days:
                ave_loss = np.mean(loss[index - days + 1:index + 1])
            else:
                ave_loss = (ave_loss_list[-1] * (days - 1) + loss[index]) / days

            ave_loss_list.append(ave_loss)

        return np.array(ave_loss_list)

    def RS(self, days):
        ave_gain = self.average_gain(days)
        ave_loss = np.abs(self.average_loss(days))

        rs = ave_gain / ave_loss

        return rs

    def RSI(self, days):

        rs = self.RS(days)

        rsi = 100 - 100 / (1 + rs)

        return rsi