from kivy.uix.screenmanager import Screen
from ArduinoHandler2 import ArduinoHandler

class TestScreen(Screen):
    def send(self,text):
        ArduinoHandler().write(text)
    pass