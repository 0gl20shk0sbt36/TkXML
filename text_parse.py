from heapq import heappop, heappush


def index(string: str, index_str_list, only_allow=None, not_allow=None,
          index_str_index_list=None, index_str_map=None) -> dict:
    if only_allow is not None and not_allow is not None:
        raise TypeError()
    if isinstance(index_str_list, list):
        index_str_list = index_str_list.copy()
    if index_str_index_list is None:
        index_str_index_list = []
        index_str_map = {}
        if isinstance(index_str_list, list):
            index_str_list_ = index_str_list.copy()
        else:
            index_str_list_ = index_str_list
        for i in index_str_list_:
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


def light(string):
    ln_col = LnCol(string)
    n = index(string, ['"""', "'''"], None, '\\')
    split_ = [0]
    for i in n:
        if len(i) % 2 == 1:
            n[i].append((-1, -1))
        start = None
        for j in n[i]:
            if start is None:
                start = j[0]
                split_.append(start)
            else:
                split_.append(j[1])
                start = None
        # if n[i][-1] == (-1, -1):
        #     n[i].pop()
    if split_[-1] != -1:
        split_.append(-1)
    print(split_)
    print(len(split_))
    n_ = []
    string_ = []
    n_s = True
    # print(len(split_))
    for i in range(len(split_) - 1):
        # print('1:', split_[i * 4], split_[i * 4 + 1] + 1, ln_col.get_ln_col(split_[i * 4], split_[i * 4 + 1] + 1))
        # string_.append(string[split_[i * 4]: split_[i * 4 + 1] + 1])
        # print('2:', split_[i * 4 + 1], split_[i * 4 + 2] + 1, ln_col.get_ln_col(split_[i * 4 + 1], split_[i * 4 + 2] + 1))
        # # if i * 4 + 2 != len(split_):
        # n_.append(string[split_[i * 4 + 1]: split_[i * 4 + 2] + 1])
        if n_s:
            # print(split_[i], split_[i+1])
            string_.append(string[split_[i]: split_[i+1]])
            n_s = False
        else:
            # print(split_[i], split_[i+1])
            n_.append(string[split_[i]: split_[i+1]])
            n_s = True
    print(len(n_))
    print(n_)
    print(len(string_))
    print(string_)
    # for i in
    # for i in n_:
    #     for j in n_[i]:
    #         print(repr(string[j[0]: j[1]]))
    # return n_


def main():
    with open(r'D:\Project\python\text_editor2\python_interpreter\L'
              r'ib\site-packages\line_profiler\line_profiler.py') as f:
    # with open('1.py') as f:
        string = f.read()
    light(string)
    # for i in n:
    #     for j in n[i]:
    #         print(repr(string[j[0]: j[1]]))


if __name__ == '__main__':
    main()
