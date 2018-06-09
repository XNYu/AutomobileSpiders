import os

def mkdir(id):
    path = "F:/images/"+id
    if not os.path.exists(path):
        os.makedirs(path)