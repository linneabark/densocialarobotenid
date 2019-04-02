# Schedule app
# Allows the user to swipe between weeks to see different schedules

from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, SwapTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout



class ScheduleApp(App):
    def build(self):
        return PageLayout()

if __name__ == '__main__':
    ScheduleApp().run()