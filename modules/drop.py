'''
import json

dict = {'Python' : '.py', 'C++' : '.cpp', 'Java' : '.java'}

json = json.dumps(dict)
f = open("dict.json","w")
f.write(json)
f.close()
'''
from util.utils import Utils
import requests as r
from dotenv import load_dotenv
load_dotenv()
import os
import json

class DropManager(object):

    pool = [5, 6, 11, 14, 15, 16, 17, 19, 43, 44, 52, 53, 72, 75, 76, 86, 87, 91, 101, 102, 167, 224, 225, 236, 238, 239, 240]
    drops = []

    @staticmethod
    def find_droped():
        for p in DropManager.pool:
            if Utils.find("ships/"+str(p)):
                DropManager.drops.append(p)
                print(DropManager.drops)
                DropManager.send_drop(p)
                return p

        return -1

    @staticmethod
    def send_drop(p):
        password = os.getenv("SEND_PASS")
        data = {
            'map' : '34',
            'ship' : str(p),
            'PASS' : password
        }
        response = r.post('https://azurlanekurutsukaren.herokuapp.com/savedrop', json=data)
        '''response = r.post('http://localhost:3000/savedrop', json=data)'''
        print(response)