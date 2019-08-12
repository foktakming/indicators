class Mean_Indicator(object):
    """
    有关平均值的指标
    1.sma
    2.boll
    """

    def __init__(self, data_set, price="Close"):
        """
        确定数据 和 计算用的价格
        """
        self.data_set = data_set

        for col_num in range(len(self.data_set.columns)):
            if self.data_set.columns[col_num] == price:
                self.price = col_num
                break

        if type(self.data_set) != pd.DataFrame:
            raise ValueError("data_set must be pd.DataFrame ")

    def data_mean(self, days=2):

        if days > len(self.data_set):
            raise ValueError('days must be larger than data_set')

        mean_list = []
        for d_index in range(len(self.data_set)):
            mean = np.mean(self.data_set.iloc[d_index - days:d_index, self.price])
            mean_list.append(mean)

        #         数组形式返回
        return np.array(mean_list)

    def data_std(self, days=2):

        if days > len(self.data_set):
            raise ValueError('days must be larger than data_set')

        std_list = []
        for d_index in range(len(self.data_set)):
            std = np.std(self.data_set.iloc[d_index - days:d_index, self.price])
            std_list.append(std)

        return np.array(std_list)

    def Boll(self, days):

        boll_mean = self.data_mean(days)
        boll_std = self.data_std(days)

        if days >= 50:
            multi_dev = 2.1
        elif days <= 10:
            multi_dev = 1.9
        else:
            multi_dev = 2

        boll_upper = boll_mean + boll_std * multi_dev
        boll_lower = boll_mean - boll_std * multi_dev

        boll = [boll_mean, boll_upper, boll_lower]

        return boll

