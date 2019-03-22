#:kivy 1.10.1

import kivy
from kivy.app import App
import time
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


class MainScreen(Screen):
    def play(self):
        anim = Animation(x=50, y=50, duration=2.) + Animation(x=-50, y=-50, duration=2.)
        anim.repeat = True
        anim.start(self.children[0].children[0])
    pass


class SchemaScreen(Screen):
    def showSchema(self,*args):
       # wb = WebManager()
        #wb.findSchema()
        self.children[0].children[1].background_normal = 'test.png'


    pass


class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.initialize()
        self.transition = SlideTransition()
        self.transition.duration = 1
        self.transition.direction = 'up'

    def initialize(self):
        self.add_widget(MainScreen(name="main"))
        self.add_widget(SchemaScreen(name="schema"))


class guiApp(App):
    def build(self):
        return Manager()


if __name__ == '__main__':
    guiApp().run()
