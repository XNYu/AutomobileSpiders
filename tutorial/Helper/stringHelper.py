#coding:utf-8


def format(att):
    if att is None:
        return "--"
    # att = att.decode("string-escape")
    att = att.strip()
    att = att.replace("\t", "")
    att = att.replace("\r", "")
    att = att.replace("\n", "")
    att = att.replace(" ", "")
    return att