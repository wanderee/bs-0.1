
import tushare as ts


# 通过tushare包获取国内的股票实时数据
def get_stock_current_data_domestic(code_stock):
    """

    :param code_stock:str,国内的六位股票代码
    :return: DataFrame,
    """
    return ts.get_realtime_quotes(code_stock)


if __name__ == '__main__':
    data = get_stock_current_data_domestic('000001')
    print(data)
    print(data.iloc[0].values)
    print(data.columns.values)