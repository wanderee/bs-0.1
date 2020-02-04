import pandas_datareader.data as web
import datetime
import tushare as ts


# 从雅虎财经得到股票历史数据
def get_stock_history_data(stock_code, start, end):
    """

    :param stock_code: str,对应的股票的代码，符合pandas_datareader包的形式
    :param start: list,查询的起始时间，形式应如[2018,6,1]
    :param end: list,查询的终止时间，形式应如[2019,1,1]
    :return: 返回一个6列的DateFrame，形式为[Date,High,Low,Open,Close,Volume,Adj Close]
    """
    return web.DataReader(stock_code, "yahoo",
                          datetime.datetime(start[0], start[1], start[2]),
                          datetime.datetime(end[0], end[1], end[2]))


# 利用tushare包获取股票历史数据（仅限国内）
def get_stock_history_data_domestic(stock_code, start, end):
    """

    :param stock_code: str,对应的股票的代码,仅需要6位数字代码即可
    :param start: list,查询的起始时间，形式应如[2018,6,1]
    :param end: list,查询的终止时间，形式应如[2019,1,1]
    :return:DataFrame 具体参考tushare.get_hist_date()函数
    """
    return ts.get_hist_data(stock_code,
                            str(datetime.datetime(start[0], start[1], start[2]).date()),
                            str(datetime.datetime(end[0], end[1], end[2]).date()))


if __name__ == '__main__':
    data = get_stock_history_data_domestic("600797", [2018, 6, 1], [2018, 7, 1])
    print(data.columns)
    print(data.index)
    print(data)
