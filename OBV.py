import numpy as np
import pandas as pd


class OnBalanceVolume(object):
    """
    计算OBV
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
                # 新添加成交量的列索引
            elif self.data_set.columns[col_num] == "Volume":
                self.volume_index = col_num

    def close_price(self):

        close_list = []
        for index in range(len(self.data_set)):
            close_p = self.data_set.iloc[index, self.close_index]

            close_list.append(close_p)

        return np.array(close_list)

    def obv(self):

        close = self.close_price()

        obv_list = []
        for index in range(len(self.data_set)):
            # 第一个，无比较，为无效值
            if index == 0:
                obv_value = np.nan
            elif index == 1:
                # 第二个开始进行close比较
                if close[index] > close[index - 1]:
                    obv_value = self.data_set.iloc[index, self.volume_index]
                elif close[index] < close[index - 1]:
                    obv_value = 0 - self.data_set.iloc[index, self.volume_index]
                else:
                    obv_value = 0

            else:

                if close[index] > close[index - 1]:

                    obv_value = obv_list[-1] + self.data_set.iloc[index, self.volume_index]

                elif close[index] < close[index - 1]:

                    obv_value = obv_list[-1] - self.data_set.iloc[index, self.volume_index]

                else:
                    obv_value = obv_list[-1]

            obv_list.append(obv_value)

        return np.array(obv_list)
