
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec  # 分割子图
import mpl_finance as mpf

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def draw_candlestick_charts(stock_data):
    fig = plt.figure(figsize=(8, 6), dpi=100, facecolor="white")  
    gs = gridspec.GridSpec(2, 1, left=0.06, bottom=0.15, right=0.96, top=0.96, wspace=None, hspace=0,
                           height_ratios=[3.5, 1])
    KAV = fig.add_subplot(gs[0, :])
    VOL = fig.add_subplot(gs[1, :])

    # 绘制K线图
    mpf.candlestick2_ochl(KAV, stock_data['open'], stock_data['close'],
                          stock_data['high'], stock_data['low'], width=0.5,
                          colorup='r', colordown='g')  # 绘制K线走势

    KAV.plot(np.arange(0, len(stock_data.index)), stock_data['ma5'], 'black', label='M5', lw=1.0)
    KAV.plot(np.arange(0, len(stock_data.index)), stock_data['ma10'], 'green', label='M10', lw=1.0)
    KAV.plot(np.arange(0, len(stock_data.index)), stock_data['ma20'], 'blue', label='M20', lw=1.0)

    KAV.legend(loc='best')

    KAV.set_title(u"日K线")
    KAV.set_ylabel(u"价格")
    KAV.set_xlim(0, len(stock_data.index))  # 设置一下x轴的范围
    KAV.set_xticks(range(0, len(stock_data.index), 15))  # X轴刻度设定 每15天标一个日期

    # 绘制成交量图
    VOL.bar(np.arange(0, len(stock_data.index)), stock_data['volume'],
                  color=['g' if stock_data['open'][x] > stock_data['close'][x] else 'r' for x in
                         range(0, len(stock_data.index))])
    VOL.set_ylabel(u"成交量")
    VOL.set_xlabel("日期")
    VOL.set_xlim(0, len(stock_data.index))  # 设置一下x轴的范围
    VOL.set_xticks(range(0, len(stock_data.index), 15))  # X轴刻度设定 每15天标一个日期
    VOL.set_xticklabels(
        [stock_data.index[index] for index in VOL.get_xticks()])  # 标签设置为日期

    # X-轴每个ticker标签都向右倾斜45度
    for label in KAV.xaxis.get_ticklabels():
        label.set_visible(False)  # 隐藏标注 避免重叠

    for label in VOL.xaxis.get_ticklabels():
        label.set_rotation(45)
        label.set_fontsize(10)  # 设置标签字体

    plt.show()


if __name__ == '__main__':
    from HistoryData import get_stock_history_data_domestic
    data = get_stock_history_data_domestic('600797', [2018, 6, 1], [2019, 1, 1])
    draw_candlestick_charts(data.iloc[::-1])