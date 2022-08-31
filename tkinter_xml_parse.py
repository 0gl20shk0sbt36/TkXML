import string

from XCP import XCP
# import ttkbootstrap as tk
import tk_ui as tk
# from get_tso import TSO
from importlib import import_module
from get_tk_tso import Menubar


class XCPBindTemplate:

    def __init__(self, parent_self, name):
        self.parent_self = parent_self
        self.name = name
        self.__yield__ = []

    def yield_bind_class(self, obj, name: str = None):
        if name is None:
            obj = obj(self, self.__name__)
            setattr(self, obj.__name__, obj)
        else:
            obj = obj(self, name)
            setattr(self, name, obj)
        self.__yield__.extend([[self.name] + i for i in getattr(obj, '__yield__', [])])

    def yield_bind_function(self, name):
        if isinstance(name, str):
            self.__yield__.append([self.name, name])
        else:
            self.__yield__.append([self.name, name.__name__])


class Head(XCPBindTemplate):

    def __init__(self, parent_self, name):
        super().__init__(parent_self, name)

    def title(self, v):
        self.parent_self.win.title(v[0])

    def size(self, v):
        self.parent_self.win.geometry(v[0])

    def ico(self, v):
        self.parent_self.win.iconbitmap(v[0])

    def logic(self, v):
        self.parent_self.values.update(import_module(v[0]).__all__)

    def end_run(self, v):
        self.parent_self.end_run_path = v[0]


class Body(XCPBindTemplate):

    def __init__(self, parent_self, name):
        super().__init__(parent_self, name)
        self.yield_bind_function(self.menubar)
        self.yield_bind_function(self.text)

    def menubar(self, v, y):
        num = 0
        for i in y:
            if i[0] == ['menubar_info']:
                if num:
                    raise
                self.parent_self.values[v['name']] = Menubar(self.parent_self.values).parse(i[1]['path'])

    def text(self, v, y):
        text = tk.Text(self.parent_self.values['win'])
        self.parent_self.values[v['name']] = text
        for i in y:
            if len(i[0]) >= 2:
                if i[0][0] == 'args':
                    args = i[0][1]
                    text_ = i[2]
                    if args == 'tab_':
                        if text_.isdigit():
                            text.bind_tab(int(text_))
                        elif text_[0] == text_[-1] and text_[0] == '"':
                            text.bind_tab(text_[1: -1])
                    elif args == 'font':
                        text.config(font=text_)
        text.pack()
        # self.parent_self.values[v['name']]

    def label(self, v, y):
        pass


class TkUI:

    def __init__(self):
        self.win = tk.Window()
        self.values = {'win': self.win}
        self.__yield__ = []
        self.bind(Head, 'head')
        self.bind(Body, 'body')

    def bind(self, obj, name: str = None):
        if name is None:
            obj = obj(self, obj.__name__)
            setattr(self, obj.__name__, obj)
        else:
            obj = obj(self, name)
            setattr(self, name, obj)
        self.__yield__.extend(getattr(obj, '__yield__', []))

    def mainloop(self):
        self.win.mainloop()

# def main():
#     win = TkUI()
#     XCP(win).run('test\\ui.xml')
#     win.mainloop()
#
#
# if __name__ == '__main__':
#     main()
