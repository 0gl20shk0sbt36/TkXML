from time import sleep
from tkinter import filedialog, messagebox, TclError, SEL
import tkinter as tk
from heapq import heappop, heappush
from keyword import kwlist


def tab(text):
    text.insert('insert', '    ')
    return 'break'


def bind_tab(text):
    text.bind('<Tab>', lambda e: tab(text))


def get_builtins():
    builtins = __builtins__.copy()
    for i in ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__build_class__', '__import__']:
        builtins.pop(i)
    return list(builtins.keys())
    # print(globals()['__builtins__'])
    # for i in globals():
    #     if i in builtins:
    #         print(i)
    #         builtins.remove(i)
    # return builtins


class LnCol:

    def __init__(self, text):
        self.text = []
        self.text_num = []
        self.get_ln(text)

    def get_ln(self, text: str):
        self.text_num = [0]
        self.text = text.split('\n')
        for i, ii in enumerate(self.text, 1):
            self.text_num.append(len(ii) + self.text_num[i - 1] + (i != len(text)))

    def get_one_ln_col(self, num: int) -> str:
        if num == 0:
            return '1.0'
        for i in range(len(self.text_num)):
            if self.text_num[i] >= num:
                return f'{i}.{num - self.text_num[i - 1]}'

    def get_ln_col(self, *nums):
        return tuple([self.get_one_ln_col(i) for i in nums])


def index(string: str, index_str_list: list[str], only_allow=None, not_allow=None,
          index_str_index_list=None, index_str_map=None) -> dict:
    if only_allow is not None and not_allow is not None:
        raise TypeError()
    index_str_list = index_str_list.copy()
    if index_str_index_list is None:
        index_str_index_list = []
        index_str_map = {}
        for i in index_str_list.copy():
            n = string.find(i)
            if n < 0:
                index_str_list.remove(i)
                continue
            heappush(index_str_index_list, n)
            index_str_map[n] = i
    if not index_str_index_list:
        return {}
    index_list = {}
    n = heappop(index_str_index_list)
    index_str = index_str_map.pop(n)
    index_int = string.find(index_str, n + len(index_str))
    if index_int >= 0:
        heappush(index_str_index_list, index_int)
        index_str_map[index_int] = index_str
    index_str_len = len(index_str)
    if only_allow is not None:
        add_l = n == 0
        add_r = (n + len(index_str)) == len(string)
        for i in only_allow:
            if not add_l and n - len(i) >= 0 and string[n - len(i): n] == i:
                add_l = True
            if not add_r and n + len(i) <= len(string) and string[n + index_str_len: n + index_str_len + len(i)] == i:
                add_r = True
        if add_l and add_r:
            index_list[index_str] = index_list.get(index_str, []) + [(n, n + index_str_len)]
    elif not_allow is not None:
        add_l = True
        add_r = True
        for i in not_allow:
            if n - len(i) >= 0 and string[n - len(i): n] == i:
                add_l = False
            if n + len(i) <= len(string) and string[n: n + len(i)] == i:
                add_r = False
        if add_l and add_r:
            index_list[index_str] = index_list.get(index_str, []) + [(n, n + index_str_len)]
    else:
        index_list[index_str] = index_list.get(index_str, []) + [(n, n + index_str_len)]
    index_list_ = index(string, index_str_list, only_allow, not_allow, index_str_index_list, index_str_map)
    for i in index_list_:
        index_list[i] = index_list.get(i, []) + index_list_[i]
    return index_list


def light_text(text, builtins):
    string = text.get('1.0', 'end')[:-1]
    ln_col = LnCol(string)
    n = index(string, builtins, '''~!@#$%^&*()`{}|[]\\:;<>?,./\n\'\" ''')
    for i in n.keys():
        num_list = []
        for j in n[i]:
            num_list.append(ln_col.get_ln_col(*j))
        n[i] = num_list
    text.tag_remove('builtins', '1.0', 'end')
    for i in n.keys():
        for j in n[i]:
            text.tag_add('builtins', j[0], j[1])
    n = index(string, kwlist, '''~!@#$%^&*()`{}|[]\\:;<>?,./\n\'\" ''')
    for i in n.keys():
        num_list = []
        for j in n[i]:
            num_list.append(ln_col.get_ln_col(*j))
        n[i] = num_list
    text.tag_remove('kwlist', '1.0', 'end')
    for i in n.keys():
        for j in n[i]:
            text.tag_add('kwlist', j[0], j[1])


def get_win_text_change(win_text, get_values, set_values, win_ln_col):
    text = win_text.get('1.0', 'end')
    builtins = get_builtins()
    # print(builtins)
    win_text.tag_configure('builtins', foreground='#8888c6')
    win_text.tag_configure('kwlist', foreground="#cc7832")
    ln_col = win_text.index(tk.INSERT).split('.')
    win_ln_col['text'] = f'行:{ln_col[0]} 列:{ln_col[1]}'
    while get_values('run'):
        text_ = win_text.get('1.0', 'end')
        # print(repr(text_))
        if text != text_:
            set_values('change', True)
            light_text(win_text, builtins)
            text = text_
        ln_col_ = win_text.index(tk.INSERT).split('.')
        if ln_col_ != ln_col:
            win_ln_col['text'] = f'行:{ln_col_[0]} 列:{ln_col_[1]}'
            ln_col = ln_col_
        sleep(0.1)


def new(win, win_text, path, change, default_title, set_values):
    if change:
        choice = messagebox.askyesnocancel('是否保存', '您的文本内容有修改，是否保存')
        if choice is None:
            return
        elif choice:
            if not save(win, win_text, path, set_values):
                return
    set_values('path', None)
    win.title(default_title)
    win_text.delete('1.0', 'end')


def save(win, win_text, path, set_values):
    if path is None:
        path = filedialog.asksaveasfilename()
    if not path:
        return False
    with open(path, 'w') as f:
        f.write(win_text.get('1.0', 'end')[:-1])
    win.title(path)
    set_values('path', path)
    return True


def save_as(win, win_text, set_values):
    path = filedialog.asksaveasfilename()
    if not path:
        return False
    with open(path, 'w') as f:
        f.write(win_text.get('1.0', 'end')[:-1])
    win.title(path)
    set_values('path', path)
    return True


def quit_(win, set_values):
    win.destroy()
    set_values('run', False)


def undo(win_text):
    try:
        win_text.edit_undo()
    except TclError:
        pass


def redo(win_text):
    try:
        win_text.edit_redo()
    except TclError:
        pass


def select_all(text):
    text.event_generate('<<SelectAll>>')


def cut(text):
    if not text.tag_ranges(SEL):
        ln = int(text.index('insert').split('.')[0])
        text.tag_add(SEL, f'{ln}.0', f'{ln + 1}.0')
    text.event_generate("<<Cut>>")
    return 'break'


def copy(text):
    if not text.tag_ranges(SEL):
        ln = int(text.index('insert').split('.')[0])
        text.tag_add(SEL, f'{ln}.0', f'{ln + 1}.0')
    text.event_generate("<<Copy>>")
    return 'break'


def paste(text):
    text.event_generate("<<Paste>>")


def comment(text):
    ln = 0
    if not text.tag_ranges(SEL):
        ln = int(text.index('insert').split('.')[0])
        if text.get(f'{ln}.0', f'{ln}.1') != '#':
            text.insert(f'{ln}.0', '#')
        else:
            text.delete(f'{ln}.0', f'{ln}.1')
        text.mark_set('insert', f'{ln + 1}.0')
    else:
        start, end = text.tag_ranges(SEL)
        start, end = int(start.string.split('.')[0]), int(end.string.split('.')[0])
        no_comment = False
        for ln in range(start, end):
            if text.get(f'{ln}.0', f'{ln}.1') != '#':
                no_comment = True
        if no_comment:
            for ln in range(start, end):
                text.insert(f'{ln}.0', '#')
        else:
            for ln in range(start, end):
                text.delete(f'{ln}.0', f'{ln}.1')
        # text.tag_remove(SEL, *text.tag_ranges(SEL))
    return 'break'


__all__ = {'change': False, 'path': None, 'new': new, 'save': save, 'get_win_text_change': get_win_text_change,
           'save_as': save_as, 'quit': quit_, 'undo': undo, 'redo': redo, 'paste': paste, 'copy': copy, 'cut': cut,
           'select_all': select_all, 'comment': comment, 'light_text': light_text}
