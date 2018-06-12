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

def numberTrans(att):
    att = att.replace("1","5")
    att = att.replace("2","6")
    att = att.replace("3","3")
    att = att.replace("4","1")
    att = att.replace("5","2")
    att = att.replace("6","7")
    att = att.replace("7","4")
    att = att.replace("8","9")
    att = att.replace("9","8")
    return att