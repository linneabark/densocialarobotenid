import json
import os
# -*- coding: utf-8 -*-

class FileHandler:
    #Skapar en ny användare och sparar denna i en jsonfil
     def create(self,name):
          name = name.lower()
          if (os.path.isfile('users/'+name+'.json')):
               return
          d = {'name': name,
               'age':'',
               'sport':'',
               'color':'',
               'wins': '',
               'losses': '',
               'screen':''
          }
          json.dump(d,open('users/'+name+'.json','w'),indent=2)

    #Hittar en person och läser infon som man vill ha

     def read(self,name,info):
          name = name.lower()
          try:
               user = json.load(open('users/'+name+'.json','r'))
               return user.get(info)
          except FileNotFoundError:
               return False
          
     def userExists(self, user):
          if (os.path.isfile('users/'+user+'.json')):
               return True
          else:
               return False
               

     '''
     Detta är copy paste, kanske måste källhänvisa
     https://stackoverflow.com/questions/21035762/python-read-json-file-and-modify
     '''
    # Lägger till info om en person
     def append(self,name,category,info):
          name = name.lower()
          try:
               with open('users/'+name+'.json', 'r+') as f:
                   data = json.load(f)
                   data[category] = info
                   f.seek(0)
                   json.dump(data,f,indent=4)
                   f.truncate()
          except FileNotFoundError:
               return False

     def readScreen(self,name):
         name = name.lower()
         try:
             user = json.load(open('users/' + name + '.json', 'r'))
             return user.get('screen')
         except FileNotFoundError:
             return 'mainscreen'
