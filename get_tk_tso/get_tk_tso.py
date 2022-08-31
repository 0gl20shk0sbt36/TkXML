from get_tso.get_tso import TSO
from importlib import import_module


def no_action(*args, **kwargs):
    pass


class Menubar:

    def __init__(self, values: dict = None):
        if values is None:
            values = {}
        self.menubar = import_module('get_tk_tso.menubar')
        self.TSO = TSO(self.menubar.__operators__, [('>', '<')], values, self.menubar.start_call)

    def parse(self, path):
        self.TSO.preprocessing(self.menubar.__preprocessing_operators__, path, None,
                               self.menubar.preprocessing_start_call)
        self.TSO.parse_from_file(path)
        # print(values)
