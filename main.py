#:kivy 1.10.1

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, \
    ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, SwapTransition, SlideTransition
#from WebTest import WebManager
from kivy.uix.screenmanager import FadeTransition
import time

class MainScreen(Screen):
    def play(self):
        anim = Animation(x=50, y=50, duration=2.) + Animation(x=-50, y=-50, duration=2.)
        anim.repeat = True
        anim.start(self.children[0].children[0])
    pass


class ScheduleScreen(Screen):
    def showSchema(self,*args):
        #wb = WebManager()
        #wb.findSchema()
        self.children[0].children[1].background_normal = 'test.png'


    pass

class SleepScreen(Screen):
    pass


class Manager(ScreenManager):
    t = time.time()
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.initialize()
        self.transition = SlideTransition()
        self.transition.duration = 1
        self.transition.direction = 'up'
        Clock.schedule_interval(self.callback, 2)

    def initialize(self):
        self.add_widget(MainScreen(name="main"))
        self.add_widget(ScheduleScreen(name="schedule"))
        self.add_widget(SleepScreen(name='sleep'))

    def on_touch_down(self,touch):
        self.current_screen.on_touch_down(touch)
        self.t = time.time()

    def callback(self,sec):
        end = time.time()
        if ((end - self.t) > 20):
            self.current = 'sleep'
            self.t = time.time()


class guiApp(App):
    def build(self):
        return Manager()


if __name__ == '__main__':
    guiApp().run()