import numpy as np
import pandas as pd


class VortexIndicator(object):
    """
    计算漩涡指标：+VI，-VI
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

    def current_high(self):
        """
        今高
        :return:
        """
        high_list = []

        for index in range(len(self.data_set)):
            current_high = self.data_set.iloc[index, self.high_index]

            high_list.append(current_high)

        return np.array(high_list)

    def current_low(self):
        """
        今低
        :return:
        """
        low_list = []

        for index in range(len(self.data_set)):
            current_low = self.data_set.iloc[index, self.low_index]

            low_list.append(current_low)

        return np.array(low_list)

    def previous_high(self):
        """
        昨高
        :return:
        """
        previous_high_list = []

        for index in range(len(self.data_set)):

            if index - 1 == -1:
                previous_high = np.nan
            else:
                previous_high = self.data_set.iloc[index - 1, self.high_index]

            previous_high_list.append(previous_high)

        return np.array(previous_high_list)

    def previous_low(self):
        """
        昨低
        :return:
        """
        previous_low_list = []

        for index in range(len(self.data_set)):

            if index - 1 == -1:
                previous_low = np.nan
            else:
                previous_low = self.data_set.iloc[index - 1, self.low_index]

            previous_low_list.append(previous_low)

        return np.array(previous_low_list)

    def min_price(self):

        min_list = []
        for index in range(len(self.data_set)):

            if index - 1 == -1:
                min_p = self.data_set.iloc[index, self.low_index]
            else:
                min_p = min(self.data_set.iloc[index - 1, self.close_index], self.data_set.iloc[index, self.low_index])

            min_list.append(min_p)

        return np.array(min_list)

    def max_price(self):

        max_list = []
        for index in range(len(self.data_set)):

            if index - 1 == -1:
                max_p = self.data_set.iloc[index, self.high_index]
            else:
                max_p = max(self.data_set.iloc[index - 1, self.close_index], self.data_set.iloc[index, self.high_index])

            max_list.append(max_p)

        return np.array(max_list)

    def close_price(self):

        close_list = []
        for index in range(len(self.data_set)):
            close_p = self.data_set.iloc[index, self.close_index]

            close_list.append(close_p)

        return np.array(close_list)

    def True_Range(self):

        Max = self.max_price()
        Min = self.min_price()

        TR = Max - Min

        return TR

    def VM_positive(self):

        c_high = self.current_high()
        p_low = self.previous_low()

        vm_positive = np.abs(c_high - p_low)

        return vm_positive

    def VM_negative(self):

        c_low = self.current_low()
        p_high = self.previous_high()

        vm_negative = np.abs(c_low - p_high)

        return vm_negative

    def VI_positive(self, days=14):
        """
        计算 +VI
        :param days:
        :return:
        """
        TR = self.True_Range()

        TR_days = []
        for index in range(len(TR)):
            tr = np.sum(TR[index - days:index])

            TR_days.append(tr)

        VM_p = self.VM_positive()

        VM_p_days = []
        for index in range(len(VM_p)):
            vm_p = np.sum(VM_p[index - days:index])

            VM_p_days.append(vm_p)

        TR_days = np.array(TR_days)
        VM_p_days = np.array(VM_p_days)

        vi_positive = VM_p_days / TR_days

        return vi_positive

    def VI_negative(self, days=14):
        """
        计算 -VI
        :param days:
        :return:
        """
        TR = self.True_Range()

        TR_days = []
        for index in range(len(TR)):
            tr = np.sum(TR[index - days:index])

            TR_days.append(tr)

        VM_n = self.VM_negative()

        VM_n_days = []
        for index in range(len(VM_n)):
            vm_n = np.sum(VM_n[index - days:index])

            VM_n_days.append(vm_n)

        TR_days = np.array(TR_days)
        VM_n_days = np.array(VM_n_days)

        vi_negative = VM_n_days / TR_days

        return vi_negative