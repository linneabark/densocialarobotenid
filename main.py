#:kivy 1.10.1

import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from threading import Thread
import threading
from kivy.core.window import Window
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
import subprocess
import random
import schedule_app

#Config.set('kivy','log_level','debug')
#Config.set('graphics', 'fullscreen', 'auto')
#from speechController import SpeechController

Config.set('graphics', 'width', '2000')
Config.set('graphics', 'height', '8000')
Window.size=(586*1.3,325*1.3)

class MainScreen(Screen):
    #def play(self):
     #   anim = Animation(x=50, y=50, duration=2.) + Animation(x=-50, y=-50, duration=2.)
      #  anim.repeat = True
      #  anim.start(self.children[0].children[0])
  #  pass
    Window.clearcolor = (1, 1, 1, 1)

    def schema(self):
        ScheduleScreen.showSchema(self)
        
   # def doSpeech(self):
    #    sc = SpeechController()
     #   sc.listenSpeech()

    #def listenToSpeech(self):
     #   thread1 = Thread(target=self.doSpeech)
      #  thread1.start()
       # print(threading.enumerate())
        
    pass


class ScheduleScreen(Screen):
    def showSchema(self,*args):
        #wb = WebManager()
        #wb.findSchema()
        self.children[0].children[1].background_normal = 'test.png'
    pass

class SleepScreen(Screen):
    pass

class MathScreen(Screen):
    pass

class RPSScreen(Screen):
    print('RPSScreen')

class ScreenOne(Screen):
    pass

class ScreenTwo(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.callbackfun, 0.7)

    def callbackfun(self, dt):
        self.manager.current = 'three'

class ScreenThree(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.callbackfun, 0.7)

    def callbackfun(self, dt):
        self.manager.current = 'four'

class ScreenFour(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.callbackfun, 0.7)

    def callbackfun(self, dt):
        list = ["five", "six", "seven"]
        self.manager.current = random.choice(list)

class ScreenFive(Screen):
    pass

class ScreenSix(Screen):
    pass

class ScreenSeven(Screen):
    pass

class Appview(Screen):
    def launchRPS(self):
        print('Launch RPS')
        #subprocess.Popen('python kv/RPS.py', shell=True)
        #RPSscreenApp().run()
    pass

class ScreenThree(Screen):
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
        self.add_widget(Appview(name='appview'))
        self.add_widget(MathScreen(name='math'))
        self.add_widget(RPSScreen(name='rps'))
        self.add_widget(ScreenOne(name='one'))
        self.add_widget(ScreenTwo(name='two'))
        self.add_widget(ScreenThree(name='three'))
        self.add_widget(ScreenFour(name='four'))
        self.add_widget(ScreenFive(name='five'))
        self.add_widget(ScreenSix(name='six'))
        self.add_widget(ScreenSeven(name='seven'))
        self.add_widget(ScreenThree(name='s2'))


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
        print('GuiApp')
        return Manager()


if __name__ == '__main__':
    guiApp().run()
