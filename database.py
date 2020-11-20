import numpy as np
import pickle
import os

class Database:
    
    def write(self,name,cnic,*args):
        if os.path.isfile('./db.pkl'):
            with open('./db.pkl', 'rb') as book:
                data = pickle.load(book)
            print(data)
            irises = []
            for i in args:
                irises.append(i.ravel())
            username = name.replace(" ","")
            if username not in data.keys():
                data[username] = {
                    'name':name,
                    'cnic':cnic,
                    'iris':irises,
                    'customers':{}
                }
            print(data)
            with open('./db.pkl','wb') as book:
                pickle.dump(data, book)
            
        else:
            data = {}
            irises = []
            for i in args:
                irises.append(i.ravel())
            username = name.replace(" ","")
            data[username] = {
                'name':name,
                'cnic':cnic,
                'iris':irises,
                'customers':{}
            }
            with open('./db.pkl','wb') as book:
                pickle.dump(data,book)


    def read(self):
        with open('./db.pkl','rb') as book:
            data = pickle.load(book)
        return data
 
