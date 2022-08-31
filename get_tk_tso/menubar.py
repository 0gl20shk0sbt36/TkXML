from ttkbootstrap import Menu
from get_tk_tso.str_dispose import get_spacing

keys_Keys = {'ctrl': 'Control', 'break': 'Cancel', 'esc': 'Escape', 'pageup': 'Prior',
             'pagedown': 'Next', 'caps lock': 'Caps_Lock'}


class CallPointer:

    def __init__(self, _o, v, v_names):
        self._o = _o
        self.v = v
        self.v_names = v_names

    def __call__(self, *args, **kwargs):
        return self._o(*[self.v[i] for i in self.v_names])


def no_action(*args, **kwargs):
    pass


def preprocessing_start_call(v: tuple[dict, dict]):
    v[1]['path'] = ['.']
    v[0]['label_len_max'] = {}
    v[1]['key'] = ''


def preprocessing_greater_than_sign(v: tuple[dict, dict], n: str):
    """符号:>

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    v[1]['path'].append(n)
    v[0]['label_len_max']['\\'.join(v[1]['path'])] = 0


def preprocessing_less_than_sign(v: tuple[dict, dict], n: str):
    """符号:<

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    v[1]['path'].pop()


def preprocessing_a(v: tuple[dict, dict], n: str):
    """符号:@

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    v[0]['label_len_max']['\\'.join(v[1]['path'])] = max(v[0]['label_len_max']['\\'.join(v[1]['path'])],
                                                         get_spacing(n + v[1]['key']))
    v[1]['key'] = ''


def preprocessing_key(v: tuple[dict, dict], n: str):
    """符号:% $

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    v[1]['key'] = n


def preprocessing_end_call(v: tuple[dict, dict]):
    print(v)


__preprocessing_operators__ = {'>': preprocessing_greater_than_sign, '<': preprocessing_less_than_sign,
                               '@': preprocessing_a, '$': preprocessing_key, '%': preprocessing_key}


def start_call(v: tuple[dict, dict]):
    v[1]['path'] = ['.']
    v[1]['path_menubar'] = [Menu(v[0]['win'], tearoff=0)]
    v[1]['function'] = no_action
    v[1]['key'] = ''
    v[1]['bind'] = True
    v[1]['context'] = v[0]['win']
    v[0]['win'].config(menu=v[1]['path_menubar'][0])


def greater_than_sign(v: tuple[dict, dict], n: str):
    """符号:>

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    v[1]['path'].append(n)
    v[1]['path_menubar'].append(Menu(v[1]['path_menubar'][-1], tearoff=0))


def less_than_sign(v: tuple[dict, dict], n: str):
    """符号:<

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    v[1]['path_menubar'][-2].add_cascade(label=v[1]['path'].pop(), font='微软雅黑', menu=v[1]['path_menubar'].pop())


def number_sign(v: tuple[dict, dict], n: str):
    """符号:#

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    pass


def per_cent(v: tuple[dict, dict], n: str):
    """符号:%

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    v[1]['key'] = n
    v[1]['bind'] = True


def dollar_sign(v: tuple[dict, dict], n: str):
    """符号:$

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    v[1]['key'] = n
    v[1]['bind'] = False


def vertical_bar(v: tuple[dict, dict], n: str):
    """符号:|

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    v[1]['context'] = v[0][n]


def and_sign(v: tuple[dict, dict], n: str):
    """符号:&

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    n = n.split(' ')
    function = v[0][n[0]]
    name = []
    if len(n) != 1:
        name = n[1:]
    v[1]['function'] = CallPointer(function, v[0], name)


def a(v: tuple[dict, dict], n: str):
    """符号:@

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    if v[1]['key']:
        if get_spacing(n) % 2:
            n += ' '
        n += '\u3000' * ((v[1]['label_len_max']['\\'.join(v[1]['path'])] +
                          6 - get_spacing(n + v[1]['key'])) // 2) + v[1]['key']
        if v[1]['bind']:
            key = v[1]['key'].split('+')
            for i, ii in enumerate(key):
                if ii.lower() in keys_Keys:
                    key[i] = keys_Keys[ii.lower()]
                elif len(ii) == 1 and 'A' < ii < 'Z' and 'Shift' not in key:
                    key[i] = ii.lower()
            key = '-'.join(key)
            v[1]['context'].bind(f'<{key}>', v[1]['function'])
    v[1]['path_menubar'][-1].add_command(label=n, command=v[1]['function'], font='微软雅黑')
    v[1]['function'] = no_action
    v[1]['key'] = ''
    v[1]['context'] = v[0]['win']


def backslash(v: tuple[dict, dict], n: str):
    """符号:/

    :param v: 变量字典元组(self.values, locals_)
    :param n: 参数
    """
    v[1]['path_menubar'][-1].add_separator()


__operators__ = {'>': greater_than_sign, '<': less_than_sign, '#': number_sign, '%': per_cent, '$': dollar_sign,
                 '|': vertical_bar, '&': and_sign, '@': a, '/': backslash}
