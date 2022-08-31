from os import chdir
from os.path import split
from get_tk_tso import Menubar
import ttkbootstrap as tk
from logic import __all__


def main():
    v = {'win': tk.Window()}
    v.update(__all__)
    Menubar('menubar.tk_ui.tso', v)


if __name__ == '__main__':
    chdir(split(__file__)[0])
    main()
