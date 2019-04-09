# Schedule app
# Allows the user to swipe between weeks to see different schedules
import kivy
kivy.require('1.9.0')
from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, SwapTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.lang import Builder


kv = Builder.load_file("Schedule.kv")

class ScreenOne(Screen):
    pass

class ScreenTwo(Screen):
    pass

screen_manager = ScreenManager()

screen_manager.add_widget(ScreenOne(name="screen_one"))
screen_manager.add_widget(ScreenTwo(name="screen_two"))

class ScheduleApp(App):
    def build(self):
        return screen_manager

if __name__ == '__main__':
    ScheduleApp().run()