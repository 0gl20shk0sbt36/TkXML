from XCP import XCP
# import ttkbootstrap as tk
from tk_ui import UI


class Head:

    def __init__(self, win: UI):
        self.win = win

    def title(self, v):
        self.win.title(v[0])

    def size(self, v):
        self.win.geometry(v[0])


class TkUI:

    win = UI()
    head = Head(win)

    def mainloop(self):
        self.win.mainloop()


def main():
    win = TkUI()
    XCP(win).run('ui.xml')
    win.mainloop()


if __name__ == '__main__':
    main()
