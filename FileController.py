import json


class FileHandler:
    #Skapar en ny användare och sparar denna i en jsonfil
     def create(self,name):
          d = {"name": name,
               "age":"",
               "interests":"",
               "color":""
          }
          json.dump(d,open("users/"+name+".json","w"),indent=2)

    #Hittar en person och läser infon som man vill ha
     def read(self,name,info):
          user = json.load(open(name+".json","r"))
          return user.get(info)
          

     '''
     Detta är copy paste, kanske måste källhänvisa
     https://stackoverflow.com/questions/21035762/python-read-json-file-and-modify
     '''
    # Lägger till info on en person
     def append(self,name,category,info):
          with open(name+".json", "r+") as f:
              data = json.load(f)
              data[category] = info
              f.seek(0)
              json.dump(data,f,indent=4)
              f.truncate()