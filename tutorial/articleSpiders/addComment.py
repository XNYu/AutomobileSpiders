#coding:utf-8
import os

rootdir = "F:/txt"

comment = "F:/txt2"

list = os.listdir(rootdir)

for l in list:
    if "all" in l:
        print(l.split("-")[0])
        print(type(l))

# for i in range(0,len(list)):
#        path = os.path.join(rootdir,list[i])
#        if "all" in path:
#            continue
#        com = os.path.join(comment,list[i])
#        if os.path.isfile(path):
#             origin = open(path,"a")
#             if os.path.isfile(com):
#                 file = open(com,"r")
#                 line = file.readline()
#                 if not line:
#                     break
#                 origin.write("\n"+line+"\n")
#                 origin.close()
#                 file.close()