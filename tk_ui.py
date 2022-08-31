import ttkbootstrap as tk


class Label(tk.Label):

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


class Text(tk.Text):

    def __init__(self, *args, tab_=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(font='新宋体')
        self.tab_ = None
        self.bind_tab(tab_)

    def bind_tab(self, tab_=None):
        self.unbind('<Tab>')
        if tab_ is not None:
            if isinstance(tab_, int):
                tab_ = ' ' * tab_
            self.tab_ = tab_
            self.bind('<Tab>', self.tab)

    def tab(self, e):
        self.insert(tk.INSERT, self.tab_)
        return 'break'


class Window(tk.Window):

    def __init__(self, title: str = "tk", size=None, iconphoto: str = None, position=None, minsize=None, maxsize=None,
                 themename: str = "litera", resizable=None, hdpi: bool = True, scaling: float = None, transient=None,
                 overrideredirect: bool = False, alpha: float = 1.0):
        """

        :param title: 窗口标题
        :param size: 窗口大小(w, h)
        :param iconphoto: 窗口图标
        :param position: 窗口左上角在屏幕中的位置(x, y)
        :param minsize: 窗口最小大小(w, h)
        :param maxsize: 窗口最大大小(w, h)
        :param themename: 窗口主题
        :param resizable: 设置能否改变大小，需要两个变量(x, y)
        :param hdpi: Windows操作系统支持高dpi。该选项默认启用。
        :param scaling: 设置Tk用于在物理单位(例如点、英寸或毫米)和像素之间转换的当前缩放系数。
        :param transient: 指示窗口管理器这个小部件对于小部件主来说是暂时的。(没搞懂)
        :param overrideredirect: 是否隐藏边框
        :param alpha: 窗口设置透明度(0~1.0)
        """
        super().__init__(title, themename, iconphoto, size, position, minsize, maxsize, resizable, hdpi, scaling,
                         transient, overrideredirect, alpha)


if __name__ == '__main__':
    win = Window()
    win.iconbitmap('test\\logo.ico')
    t = Text(win, undo=True, tab_blans=4)
    t.pack()
    win.mainloop()
