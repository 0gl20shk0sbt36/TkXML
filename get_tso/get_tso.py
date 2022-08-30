class TSOFileError(BaseException):

    def __init__(self, file_path, error_name, error_text=None, ln=None):
        self.error = f"""
TSOFileError: 
    error name: {error_name}
    error file path: {file_path}
    error file text: {error_text}
    error file text ln: {ln}
"""

    def __str__(self):
        return self.error


def pass_call(*args, **kwargs):
    pass


def read_file(path):
    with open(path, errors='ignore') as f:
        n = f.readline()
    if n[:9] == '#coding="':
        encoding = n[9:-1]
        with open(path, encoding=encoding) as f:
            n = f.read()[len(n):]
    else:
        with open(path) as f:
            n = f.read()
    return n


class TSO:

    def __init__(self, operators: dict, pairing=None, values=None, start_call=pass_call, end_call=pass_call):
        if values is None:
            values = {}
        if pairing is None:
            pairing = []
        self.values = values
        i = {i: operators[i] for i in operators if callable(operators[i])}
        if i:
            raise TypeError(f"""The value in parameter operators is not callable
key: values    {i}""")
        self.__operators = operators
        self.__pairing = pairing
        if [i for i in pairing if i[0] == i[1]]:
            raise ValueError()
        self.__pairing_num = {i[0]: 0 for i in pairing} | {i[1]: 0 for i in pairing}
        self.__path = None
        if callable(start_call):
            self.start_call = start_call
        if callable(end_call):
            self.end_call = end_call
        self.locale_ = {}

    def preprocessing(self, operators, path, values=None, start_call=pass_call, end_call=pass_call):
        if values is None:
            values = {}
        n = read_file(path)
        start_call((self.locale_, values))
        for i in [i.lstrip(' ') for i in n.split('\n') if i.lstrip(' ')]:
            operators[i[0]]((self.locale_, values), i[1:])
        end_call((self.locale_, values))

    def format_checker(self, string: str):
        string = string.split('\n')
        string_ = [i.lstrip(' ') for i in string if i.lstrip(' ')]
        for i, ii in enumerate(string_):
            if ii[0] not in self.__operators:
                raise TSOFileError(self.__path, '操作符不存在', string[i], i)
            if ii[0] in self.__pairing_num.keys():
                self.__pairing_num[ii[0]] += 1
        for i in self.__pairing:
            if self.__pairing_num[i[0]] != self.__pairing_num[i[1]]:
                raise TSOFileError(self.__path, '操作符不匹配', f'"{i[0]}" 和 "{i[1]}"')
        return string, string_

    def parse_from_file(self, path):
        self.__path = path
        n = read_file(path)
        self.start_call((self.values, self.locale_))
        n, n_ = self.format_checker(n)
        for i in n_:
            self.__operators[i[0]]((self.values, self.locale_), i[1:])
        self.end_call((self.values, self.locale_))
        self.locale_ = {}
