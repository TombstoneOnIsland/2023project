import tkinter as tk
import bilian
from time import *

class Climbgui():
    def __init__(self,windows):
        self.tk_window = windows

    def init_windows(self):
        self.tk_window.title('爬取招标信息界面')
        self.tk_window.geometry('300x350+760+280')
        self.climb_excute_key_label = tk.Label(master=self.tk_window,text='请输入要爬取的招标关键词')
        self.climb_excute_key_entry = tk.Entry(master=self.tk_window,width=20)

        self.climb_excute_page_label = tk.Label(master=self.tk_window,text='请输入要爬取的页数')
        self.climb_excute_page_entry = tk.Entry(master=self.tk_window,width=20)

        self.climb_excute_key_label.grid(row=1,column=0)
        self.climb_excute_key_entry.grid(row=2,column=0)

        self.climb_excute_page_label.grid(row=1,column=1)
        self.climb_excute_page_entry.grid(row=2,column=1)

        self.climb_excute_button = tk.Button(master=self.tk_window,text='爬取',width=10,height=1,command=self.climb)
        self.climb_excute_button.grid(row=3,column=0,columnspan=4,pady=5)

        self.climb_result_label = tk.Label(master=self.tk_window,text='执行结果')
        self.climb_result_label.grid(row=4,column=0,columnspan=4)
        self.climb_result_entry = tk.Text(master=self.tk_window,width=40,height=18)
        self.climb_result_entry.grid(row=5,column=0,columnspan=4)


    def climb(self):
        bilian.climbnum = 0
        key = self.climb_excute_key_entry.get().strip()
        page = int(self.climb_excute_page_entry.get().strip())
        begin_time = time()
        bilian.start_climb(key=key,pages=page)
        end_time = time()
        total_time = str(end_time-begin_time)
        self.climb_result_entry.delete(1.0, 'end')
        self.climb_result_entry.insert(1.0, '本次共爬取招标信息:'+str(bilian.climbnum)+'条。')
        self.climb_result_entry.delete(2.0, 'end')
        self.climb_result_entry.insert(2.0, '\n本次爬取关键词为:'+key+',爬取总页数为:'+str(page)+'。')
        self.climb_result_entry.delete(3.0, 'end')
        self.climb_result_entry.insert(3.0, '\n本次爬取结果已保存到文件:result.csv。')
        self.climb_result_entry.delete(4.0, 'end')
        self.climb_result_entry.insert(4.0, '\n本次爬取总运行时间:'+total_time+'s。')

if __name__ == '__main__':
    windows = tk.Tk()
    gui = Climbgui(windows)
    gui.init_windows()
    windows.mainloop()
