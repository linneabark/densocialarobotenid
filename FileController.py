import pickle
import json


class FileHandler:

     def create(self,name):
          d = {"name": name,
               "age":"",
               "interests":"",
               "color":""
          }
          json.dump(d,open(name+".json","w"),indent=2)


     def read(self,name,string):
          user = json.load(open(name+".json","r"))
          return user.get(string)
          

     '''
     Detta är copy paste, kanske måste källhänvisa
     https://stackoverflow.com/questions/21035762/python-read-json-file-and-modify
     '''
     def append(self,name,category,info):
          with open(name+".json", "r+") as f:
              data = json.load(f)
              data[category] = info
              f.seek(0)
              json.dump(data,f,indent=4)
              f.truncate()


