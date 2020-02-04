
import tkinter as tk
from tkinter import YES, BOTH, Frame, filedialog, NW, mainloop, messagebox
from tkinter.ttk import Treeview

from PIL import ImageTk
class VSM_Window:
    def __init__(self):
        self.search_text = []  # 保存搜索结构的list
        self.npages = 0  # 当前已经加载的页数
        self.curr_page = 0  # 当前页数
        self.oneSearch = 10  # 一页有多少信息
        self.allpage = 0  # 一共有多少页

        self.search_VSM = VSM()
        self.search_enable = False  # 但前是否能够进行搜索

        self.Width = 500
        self.Height = 270
        self.WH_str = str(self.Width) + 'x' + str(self.Height)
        self.window = tk.Tk()

        self.datas = []

    def create_index(self):
        self.datas = F.open_csv(self.search_VSM.input_path_csv)
        self.search_VSM.create_index()
        #         self.search_VSM.print_all()
        self.search_VSM.cal_tf_and_idf()
        self.list_head = self.search_VSM.list_head
        #         print(self.datas)
        self.search_enable = True

    def load_index(self):
        try:
            self.search_VSM.input_path = self.search_VSM.input_path_csv[:-4]
            self.datas = F.open_csv(self.search_VSM.input_path_csv)
            self.search_enable = True

            return self.search_VSM.load_index()

        except:
            return False

    def save_index(self):
        if self.search_enable:
            if messagebox.askokcancel("Quit", "是否要保存索引"):
                self.search_VSM.save()
        self.window.destroy()

    def main_window(self):
        self.window.title('CSV搜索')
        self.window.geometry(self.WH_str)
        self.window.resizable(False, False)

        canvas = tk.Canvas(self.window, width=500, height=270, bg='green')
        canvas.pack(expand=YES, fill=BOTH)

        # image = ImageTk.PhotoImage(file = r"logo.jpg")
        # canvas.create_image(1, 1, image = image, anchor = NW)

        self.e = tk.Entry(self.window, width=35, show=None, bd=1)
        self.e.place(x=125, y=205)
        self.w1 = tk.Button(self.window, text='搜 索', width=10, command=self.get_text_and_search)
        self.w1.place(x=400, y=200)

        self.file_get = tk.Button(self.window, text='打开文件', command=self.get_filepath)
        self.file_get.place(x=30, y=200)

        self.window.protocol("WM_DELETE_WINDOW", self.save_index)  # 当窗口关闭是询问是否需要保存索引

        mainloop()

    def main_loop(self):
        pass

    def get_filepath(self):
        try:
            self.search_VSM.input_path_csv = filedialog.askopenfilename(title='打开文件', filetypes=[('csv', '*.csv'),
                                                                                                 ('All Files', '*')])
        except:
            messagebox.showinfo("提示", "打开文件错误")
        if self.load_index() == False:
            print("----- create the index successfully  -----")
            self.search_VSM.new()
            self.create_index()
        else:
            print("----- load the index successfully -----")

    def get_text_and_search(self, enable_page=True):
        if self.search_enable == False:
            messagebox.showinfo('提示', '没有选择csv文件')
            return

        search_text = self.e.get()
        if search_text == '':
            return
        if enable_page:
            self.new_search()
            pages_search = self.search_VSM.search(search_text)
            self.allpage = pages_search // self.oneSearch
            if pages_search % self.oneSearch != 0:
                self.allpage += 1
        #         self.search_VSM.print_all()
        X = self.search_VSM.get_result(self.oneSearch, True)
        if len(X) != 0:
            self.npages += 1
        #         self.test_head()
        #         print(self.datas)
        for i in X:
            self.search_text.append(self.datas[i])
        if enable_page:
            self.curr_page = self.npages
            self.show_info_window(self.search_text, self.datas[0])

    def show_info_window(self, show_data, show_tag):

        self.test_head()
        self.root = tk.Tk()
        # 设置窗口大小和位置
        '''
            窗口宽度的计算
        '''
        self.root.geometry('500x330+400+300')
        # 不允许改变窗口大小
        self.root.resizable(False, False)
        # 设置窗口标题
        self.root.title('搜索结果')
        # 使用Treeview组件实现表格功能
        frame = Frame(self.root)
        frame.place(x=0, y=10, width=480, height=280)
        # 滚动条
        scrollBar = tk.Scrollbar(frame)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        #         self.test_head()
        button_page_up = tk.Button(self.root, text='上一页', width=10, command=self.page_up)
        button_page_up.place(x=70, y=295)
        button_page_down = tk.Button(self.root, text='下一页', width=10, command=self.page_down)
        button_page_down.place(x=335, y=295)

        self.label_page = tk.Label(self.root, text=str(self.curr_page) + "/" + str(self.allpage) + "页")
        self.label_page.place(x=225, y=300)

        colunms_result = []
        for i in range(1, len(show_tag) + 1):
            colunms_result.append('c' + str(i))
        self.tree = Treeview(frame, columns=colunms_result, show="headings", yscrollcommand=scrollBar.set)
        # 设置每列宽度和对齐方式
        for i in range(0, len(show_tag)):
            width_col = int(480 / (len(show_tag)) - 5)
            if width_col < 60:
                width_col = 60
            self.tree.column(colunms_result[i], width=width_col, anchor='center')
            self.tree.heading(colunms_result[i], text=show_tag[i])
            if i == 7:
                self.tree.column(colunms_result[i], width=width_col, anchor='center')
                self.tree.heading(colunms_result[i], text='……')
                break

        self.tree.pack(side=tk.LEFT, fill=tk.Y)
        # Treeview组件与垂直滚动条结合
        scrollBar.config(command=self.tree.yview)

        # 定义并绑定Treeview组件的鼠标单击事件
        def treeviewClick(event):
            for item in self.tree.selection():
                item_text = self.tree.item(item, "values")
                self.show_more_info(show_data[show_data.index(list(item_text))], show_tag)

        # 插入演示数据
        show_copy = show_data[:]
        self.insert_table_info(show_copy)

        self.tree.bind('<Double-1>', treeviewClick)
        self.root.mainloop()

    def insert_table_info(self, insert_datas):
        for i in range(0, len(insert_datas)):
            show_str = insert_datas[i]
            #             for j in range(0,len(self.search_VSM.list_head)):
            #                 if len(insert_datas[0][j]) >10:
            #                     show_str[j] = show_str[j][0:4]+'…'
            self.tree.insert('', i, values=show_str)

    def show_more_info(self, show_data, show_tag):

        #         print(show_data)
        w = tk.Tk()
        w.geometry('400x400+600+400')
        w.title(show_data[0])
        txt = tk.Text(w, width='380', height='380')
        for i in range(0, len(show_tag)):
            data_str = show_tag[i] + ':' + show_data[i] + '\n'
            txt.insert('end', data_str)
        txt.pack()

    def page_up(self):
        if self.curr_page > 1:
            self.curr_page -= 1
            for x in self.tree.get_children():
                self.tree.delete(x)

            insert_info = self.search_text[(self.curr_page - 1) * self.oneSearch:(self.curr_page) * self.oneSearch]
            self.label_page["text"] = str(self.curr_page) + "/" + str(self.allpage) + "页"
            self.insert_table_info(insert_info)
        else:
            messagebox.showinfo('提示', '没有上一页了')

    def page_down(self):
        self.test_head()
        if self.curr_page < self.allpage:
            self.curr_page += 1
            for x in self.tree.get_children():
                self.tree.delete(x)
            if self.curr_page > self.npages:
                self.get_text_and_search(False)
            insert_info = self.search_text[(self.curr_page - 1) * self.oneSearch:(self.curr_page) * self.oneSearch]
            self.label_page["text"] = str(self.curr_page) + "/" + str(self.allpage) + "页"
            self.insert_table_info(insert_info)
        else:
            messagebox.showinfo('提示', '没有下一页了')
            return
        if self.curr_page > self.npages:
            self.get_text_and_search(False)

    def new_search(self):
        self.search_text = []
        self.npages = 0
        self.curr_page = 0
        self.oneSearch = 10
        self.allpage = 0

    def test_head(self):
        return

    #         print(len(self.search_VSM.search_heap))

    def print_page_info(self):
        return
        print("allpage:", self.allpage)
        print("napges:", self.npages)
        print("currpage:", self.curr_page)
        print("oneSearch:", self.oneSearch)


if __name__ == '__main__':
    VM = VSM_Window()
    VM.main_window()
    VM.main_loop()
    # VM.get_text_and_search()