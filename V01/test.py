import tkinter as tk
from tkinter import mainloop, messagebox, filedialog
from tkinter.ttk import Treeview
from CurrentData import get_stock_current_data_domestic
from HistoryData import get_stock_history_data_domestic
from DrawPicture import draw_candlestick_charts
import datetime
import os

DEBUG = True
curr_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(curr_path) + os.path.sep + ".")
strategy = father_path + '\\Strategy'


def date_trans(date_str):
    """
    将形式为'xxxx-xx-xx'的日期转化为[xxxx,xx,xx]的形式
    """
    return [int(item) for item in date_str.split('-')]


def isDate(date):
    try:
        datetime.date(date[0], date[1], date[2])
        return True
    except Exception as ex:
        print(ex)
        return False


if __name__ == '__main__':
    # 窗口大小
    Width = 460
    Height = 470
    WH_str = str(Width) + 'x' + str(Height)

    # 股票参数
    code_list = []
    curr_data = {}
    curr_code = None
    start_date = []
    end_date = []
    money = 0

    # 创建主窗口
    window = tk.Tk()
    window.title('股价查询')
    window.geometry(WH_str)
    window.resizable(False, False)

    # 默认的时间参数
    start_str = tk.StringVar()
    start_str.set('2018-06-01')
    end_str = tk.StringVar()
    end_str.set('2019-01-01')
    start_money = tk.StringVar()
    start_money.set('10000')

    # tkinter控件
    e = tk.Entry(window, width=35, show=None, bd=1)
    e.place(x=65, y=25)

    start = tk.Entry(window, width=20, textvariable=start_str, show=None, bd=1)
    start.place(x=160, y=325)

    end = tk.Entry(window, width=20, textvariable=end_str, show=None, bd=1)
    end.place(x=160, y=375)

    m = tk.Entry(window, width=20, textvariable=start_money, show=None, bd=1)
    m.place(x=160, y=425)

    # 股票信息表格
    tree = Treeview(window, columns=("1", "2", "3", "4", "5", "6", "7"))
    col_name = ('code', 'name', 'open', 'pre_close', 'price', 'high', 'low')
    tree.column('#0', width=0)
    for i in range(1, 8):
        tree.column(str(i), width=60)
        tree.heading(str(i), text=col_name[i - 1])


    # 搜索按键的响应函数
    def search_stock():
        stock_code = e.get()
        temp = get_stock_current_data_domestic(stock_code)
        if temp is None:
            return
        this_data = temp.iloc[0].values.tolist()

        if stock_code not in code_list:
            code_list.append(stock_code)

        this_data.insert(0, stock_code)
        curr_data[stock_code] = this_data
        items = tree.get_children()
        [tree.delete(item) for item in items]
        for j in range(0, len(code_list)):
            tree.insert("", j, value=curr_data[code_list[j]][:7])

        # 表格双击事件的响应函数
        def treeviewDoubleClick(event):  # 单击
            global curr_code, start_date, end_date
            # 确认双击事件发生的位置
            for item in tree.selection():
                item_text = tree.item(item, "values")
            # 获取该股票的代码
            curr_code = item_text[0]
            # 查询的日期区间
            start_date = date_trans(start.get())
            end_date = date_trans(end.get())
            # 判断时间是否合法
            if isDate(start_date) is False:
                tk.messagebox.showinfo('时间格式错误', '起始时间格式错误')
                return
            if isDate(end_date) is False:
                tk.messagebox.showinfo('时间格式错误', '结束时间格式错误')
                return

            if DEBUG is True:
                print(curr_code)
                print(start_date)
                print(end_date)

            # 获取历史数据
            history_data = get_stock_history_data_domestic(curr_code,
                                                           start_date, end_date)
            # 绘制K线图
            draw_candlestick_charts(history_data[::-1])

        def treeviewSingleClick(event):
            global curr_code, start_date, end_date
            # 确认双击事件发生的位置
            for item in tree.selection():
                item_text = tree.item(item, "values")
            # 获取该股票的代码
            curr_code = item_text[0]
            # 查询的日期区间
            start_date = date_trans(start.get())
            end_date = date_trans(end.get())

        tree.bind('<Double-1>', treeviewDoubleClick)
        tree.bind('<ButtonRelease-1>', treeviewSingleClick)


    tree.place(x=20, y=80)

    lab1 = tk.Label(window, text='起始日期:')
    lab1.place(x=60, y=325)

    lab2 = tk.Label(window, text='结束日期:')
    lab2.place(x=60, y=375)

    lab3 = tk.Label(window, text='起始资金:')
    lab3.place(x=60, y=425)

    w1 = tk.Button(window, text='搜 索', width=10, command=search_stock)
    w1.place(x=350, y=20)


    def sim_invest():
        # if curr_code is None:
        #     tk.messagebox.showinfo("错误", "没有选择股票")
        #     return
        curr_code = '000001'
        cmd = 'rqalpha run -f {} -s {} -e {} --account stock {} --benchmark 000300.XSHG --plot'
        strategy_path = filedialog.askopenfilename(title='选择一个策略',
                                                   filetypes=[('PY', '*.py'), ('All Files', '*')],
                                                   initialdir=strategy)
        cmd = cmd.format(strategy_path, start.get(), end.get(), m.get())
        if DEBUG:
            print(strategy_path)
            print(cmd)
        os.system(cmd)


    w2 = tk.Button(window, text='模拟投资', width=10, command=sim_invest)
    w2.place(x=350, y=375)

    mainloop()
