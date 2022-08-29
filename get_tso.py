def get_format(file: str):
    menubar_format = []
    for i in file.split('\n'):
        if not i:
            continue
        i = i.lstrip(' ')
        if len(i) == 1:
            menubar_format.append((i[0], ''))
        else:
            menubar_format.append((i[0], i[1:]))
    return menubar_format


class TSOFileError(BaseException):

    def __init__(self, file_path, error_name, error_text, ln):
        self.error = f"""TSOFileError: 
    error name: {error_name}
    error file path: {file_path}
    error file text: {error_text}
    error file text ln: {ln}
"""

    def __str__(self):
        return self.error


class TSO:

    def __init__(self, operators: dict):
        self.operators = operators
        self.path = None

    def format_checker(self, string: str):
        string_ = []
        string = string.split('\n')
        for i in string:
            string_.append(i.lstrip(' '))
        for i, ii in enumerate(string_):
            if ii[0] not in self.operators:
                raise TSOFileError(self.path, '操作符不存在', string[i], i)


# TSO({'&'})
