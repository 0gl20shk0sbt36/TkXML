from os import chdir
from os.path import split

from XCP import XCP
from tkinter_xml_parse import TkUI


def main():
    win = TkUI()
    XCP(win).run('ui.xml')
    win.mainloop()


if __name__ == '__main__':
    chdir(split(__file__)[0])
    main()
