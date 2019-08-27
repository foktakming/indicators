import numpy as np
import pandas as pd
from OBV import OnBalanceVolume


class MoneyFlowIndex(OnBalanceVolume):
    """
    计算MFI
    """
    def high_price(self):
        """
        获取最高价
        :return:
        """
        high_list = []
        for index in range(len(self.data_set)):

            high =self.data_set.iloc[index, self.high_index]

            high_list.append(high)

        return np.array(high_list)

    def low_price(self):
        """
        获取最低价
        :return:
        """
        low_list = []
        for index in range(len(self.data_set)):
            low = self.data_set.iloc[index, self.low_index]

            low_list.append(low)

        return np.array(low_list)

    def volume_value(self):
        """
        获取成交量
        :return:
        """
        volume_list = []
        for index in range(len(self.data_set)):
            volume = self.data_set.iloc[index, self.volume_index]

            volume_list.append(volume)

        return np.array(volume_list)

    def typical_price(self):

        close = self.close_price()
        high = self.high_price()
        low = self.low_price()

        Typical_price = (high + low + close) / 3

        return Typical_price

    def money_flow(self):

        typical_price = self.typical_price()
        volume = self.volume_value()

        moneyflow = typical_price * volume

        return moneyflow

    def positive_money_flow(self):
        """
        计算正向资金流
        :return:
        """
        moneyflow = self.money_flow()
        typical_price = self.typical_price()

        positive_money_flow_list = []
        for index in range(len(self.data_set)):

            if index == 0:
                positive_flow = np.nan
            else:

                if typical_price[index] > typical_price[index - 1]:
                    positive_flow = moneyflow[index]
                else:
                    positive_flow = 0

            positive_money_flow_list.append(positive_flow)

        return np.array(positive_money_flow_list)

    def negative_money_flow(self):
        """
        计算逆向资金流+
        :return:
        """
        moneyflow = self.money_flow()
        typical_price = self.typical_price()

        negative_money_flow_list = []
        for index in range(len(self.data_set)):

            if index == 0:
                negative_flow = np.nan
            else:

                if typical_price[index] < typical_price[index - 1]:
                    negative_flow = moneyflow[index]
                else:
                    negative_flow = 0

            negative_money_flow_list.append(negative_flow)

        return np.array(negative_money_flow_list)

    def positive_flow_ma(self, days):

        positive_flow = self.positive_money_flow()

        positive_flow_ma_list = []

        for index in range(len(self.data_set)):
            flow_ma = np.mean(positive_flow[index - days + 1:index + 1])

            positive_flow_ma_list.append(flow_ma)

        return np.array(positive_flow_ma_list)

    def negative_flow_ma(self, days):

        negative_flow = self.negative_money_flow()

        negative_flow_ma_list = []

        for index in range(len(self.data_set)):
            flow_ma = np.mean(negative_flow[index - days + 1:index + 1])

            negative_flow_ma_list.append(flow_ma)

        return np.array(negative_flow_ma_list)

    def money_flow_ratio(self, days):

        positive_flow = self.positive_flow_ma(days)
        negative_flow = self.negative_flow_ma(days)

        ratio = positive_flow / negative_flow

        return ratio

    def MFI(self, days=14):

        ratio = self.money_flow_ratio(days)

        mfi = 100 - 100 / (1 + ratio)

        return mfi