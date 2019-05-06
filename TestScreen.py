from kivy.uix.screenmanager import Screen
from ArduinoHandler import ArduinoHandler

class TestScreen(Screen):
    def send(self,text):
        ArduinoHandler(2).write(text)
    pass