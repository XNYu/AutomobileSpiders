import os

def mkdir(id):
    path = "F:/pcauto/images/"+id
    if not os.path.exists(path):
        os.makedirs(path)
        print("success")