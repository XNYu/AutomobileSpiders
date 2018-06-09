#coding=utf-8
import json
import chardet

def getDict():
    file = open('inputs/types.txt', 'r')
    types = []
    for line in file.readlines():
        # line = line.replace("\r","")
        line = line.replace("\n","")
        types.append(line)
    f2 = open('inputs/names.txt','r')
    dict={}
    names=[]
    curType=''
    for line in f2.readlines():
        line = line.replace('\n','')
        line = line.strip()
        if(line in types):
            dict[curType] = names
            names=[]
            curType = line
            continue
        names.append(line)
    dict[curType] = names
    dict.pop("")
    # for d in dict:
    #     print(d)
        # print(dict[d])
    return dict
