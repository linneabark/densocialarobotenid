#!/usr/bin/env python
#coding: utf-8
import kivy
import random
kivy.require('1.9.0')
 
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.image import Image
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import time


list = ["five", "six", "seven"]

class ScreenOne(Screen):
    pass

class ScreenTwo(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.callbackfun, 0.7)

    def callbackfun(self,dt):
        self.manager.current = 'three'

class ScreenThree(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.callbackfun, 0.7)
    
    def callbackfun(self,dt):
        self.manager.current = 'four'


class ScreenFour(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.callbackfun, 0.7)
    
    def callbackfun(self,dt):
        self.manager.current = random.choice(list)


class ScreenFive(Screen):
    pass
 
class ScreenSix(Screen):
    pass

class ScreenSeven(Screen):
    pass

class Manager(ScreenManager):
    t = time.time()
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.initialize()

    def initialize(self):
        self.add_widget(ScreenOne(name='one'))
        self.add_widget(ScreenTwo(name='two'))
        self.add_widget(ScreenThree(name='three'))
        self.add_widget(ScreenFour(name='four'))
        self.add_widget(ScreenFive(name='five'))
        self.add_widget(ScreenSix(name='six'))
        self.add_widget(ScreenSeven(name='seven'))

class RPSscreenApp(App):
    def build(self):
        return Manager()

if __name__ == "__main__":
    RPSscreenApp().run()