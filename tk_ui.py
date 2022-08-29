import ttkbootstrap as tk


class UI:

    def __init__(self,
                 title: str = "tk",
                 size=None,
                 iconphoto: str = None,
                 position=None,
                 minsize=None,
                 maxsize=None,
                 themename: str = "litera",
                 resizable=None,
                 hdpi: bool = True,
                 scaling: float = None,
                 transient=None,
                 overrideredirect: bool = False,
                 alpha: float = 1.0):
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
        self.win = tk.Window(title, themename, iconphoto, size, position, minsize, maxsize, resizable,
                             hdpi, scaling, transient, overrideredirect, alpha)
        self.values = {}

    def add_values(self, *value, **values):
        if len(value) == 1 and isinstance(value[0], dict):
            self.values.update(value[0])
        elif len(value) == 2 and isinstance(value[0], str):
            self.values[value[0]] = value[1]
        elif values:
            self.values.update(values)
        else:
            raise ValueError()

    def iconphoto(self, path):
        self.win.iconphoto(True, tk.PhotoImage(file=path))

    def iconbitmap(self, path):
        self.win.iconbitmap(path)

    def title(self, string: str):
        """设置窗口标题

        :param string: 标题
        :return:
        """
        self.win.title(string)

    def geometry(self, new_geometry: str):
        self.win.geometry(new_geometry)

    def mainloop(self):
        self.win.mainloop()


if __name__ == '__main__':
    ui = UI(iconphoto='logo.ico')
    ui.mainloop()
