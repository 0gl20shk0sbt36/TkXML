from urwid.str_util import get_width


def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        print(inside_code)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring


def strB2Q(ustring):
    """半角转全角"""
    rst_ring = []
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif 32 <= inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248
        rst_ring.append(chr(inside_code))
    return ''.join(rst_ring)


def get_spacing(string):
    num = 0
    for i in string:
        num += get_width(ord(i))
    return num
