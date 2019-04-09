# Schedule app
# Allows the user to swipe between weeks to see different schedules
import kivy
kivy.require('1.9.0')
from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.lang import Builder


kv = Builder.load_file("Schedule.kv")

class ScreenOne(Screen):
    pass
class ScreenTwo(Screen):
    pass
class ScreenThree(Screen):
    pass
class ScreenFour(Screen):
    pass
class ScreenFive(Screen):
    pass
class ScreenSix(Screen):
    pass

screen_manager = ScreenManager()

screen_manager.add_widget(ScreenOne(name="screen_one"))
screen_manager.add_widget(ScreenTwo(name="screen_two"))
screen_manager.add_widget(ScreenThree(name="screen_three"))
screen_manager.add_widget(ScreenFour(name="screen_four"))
screen_manager.add_widget(ScreenFive(name="screen_five"))
screen_manager.add_widget(ScreenSix(name="screen_six"))

class ScheduleApp(App):
    def build(self):
        return screen_manager

if __name__ == '__main__':
    ScheduleApp().run()