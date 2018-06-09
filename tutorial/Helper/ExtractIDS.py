import json

file = open("../inputs/title.txt","r")
dict = {}
index =0
for line in file.readlines():
    dict[str(index)] = line
    index+=1
file.close()
length = len(dict)

values = set()
for key in dict.keys():
    val = dict[key]
    if val in values:
        del dict[key]
    else:
        values.add(val)
print(len(dict))
file = open("../inputs/extracted_titles.txt","w")
for index in range(0,length):
    id = str(index)
    if id in dict.keys():
        file.write(dict[id])
file.close()
