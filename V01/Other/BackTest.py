import HistoryData


class DailyLog:
    def __init__(self, start):
        self.start = start
        self.log = []
        '''
        log中应该有包括盈利，买卖记录，资金信息等内容
        '''


class Count:
    def __init__(self, money, start):
        self.vest_value = money
        self.curr_money = money
        self.stock_worth = 0
        # self.all_worth = 0
        self.daily_log = DailyLog(start)
        self.stock_info = {}

    def buy_stock(self):
        pass

    def sell_stock(self):
        pass

    def cal_stock_worth(self):
        pass

    def print_count_info(self):
        self.cal_stock_worth()
        return self.money, self.stock_worth


stock_code = '000000'
start_date = [2018, 1, 1]
end_data = [2020, 1, 1]
