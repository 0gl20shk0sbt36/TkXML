class TSOFileError(BaseException):

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error


class CallPointer:

    def __init__(self, _o, v, v_names):
        self._o = _o
        self.v = v
        self.v_names = v_names

    def __call__(self, *args, **kwargs):
        return self._o(*[self.v[i] for i in self.v_names])


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
        if [i for i in operators.values() if callable(i)]:
            raise TypeError(f"The value in parameter operators is not callable")
        self.__operators = operators
        self.__pairing = pairing
        if [i for i in pairing if i[0] == i[1]]:
            raise ValueError()
        self.__pairing_num = {i[0]: 0 for i in pairing} | {i[1]: 0 for i in pairing}
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
        # string = [i.lstrip(' ') for i in string.split('\n')]
        string = [i.lstrip(' ') for i in string.split('\n') if i.lstrip(' ')]
        for i in string:
            if i[0] not in self.__operators:
                raise TSOFileError(f'操作符 {i[0]} 不存在')
            if i[0] in self.__pairing_num.keys():
                self.__pairing_num[i[0]] += 1
        for i in self.__pairing:
            if self.__pairing_num[i[0]] != self.__pairing_num[i[1]]:
                raise TSOFileError(f'操作符 "{i[0]}" 与 "{i[1]}" 不匹配')
        return string

    def parse_from_file(self, path):
        n = read_file(path)
        self.start_call((self.values, self.locale_))
        n = self.format_checker(n)
        for i in n:
            self.__operators[i[0]]((self.values, self.locale_), i[1:])
        self.end_call((self.values, self.locale_))
        self.locale_ = {}
