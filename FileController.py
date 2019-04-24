import pickle
import json


class FileHandler:

     def create(self):
          pass

     def read(self):
          pass
     def append(self):
          pass

     
d = {"Name":"Rasmus",
     "age":23
     }
json.dump(d,open("Rasmus.txt","w"), indent=2)


file2 = open("Rasmus.txt","r")

#print(file.get("age"))
string = "Rasmus"
d3 = json.load(open(string+".txt","r"))
print(d3.get("Name"))

    #print(line.get("Name"))
#d3 = json.load("text.txt")
#print(d3.get("Name"))

