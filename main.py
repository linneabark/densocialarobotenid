#:kivy 1.10.1
import sys
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
# from WebTest import WebManager
from kivy.uix.screenmanager import FadeTransition
import time
import subprocess
import random
import schedule_app
#from pygame import mixer
from kivy.properties import StringProperty

from rpsScreens import RPSScreen, ScreenOne, ScreenTwo, ScreenFour, ScreenThree, ScreenFive, ScreenSix, ScreenSeven
from scheduleScreens import ScheduleScreen, ScheduleScreenTwo, ScheduleScreenThree, ScheduleScreenFour, \
    ScheduleScreenFive, ScheduleScreenSix
from user import User
from TestScreen import TestScreen


#Config.set('kivy','log_level','debug')
#Config.set('graphics', 'fullscreen', 'auto')
# Config.set('kivy','log_level','debug')
# Config.set('graphics', 'fullscreen', 'auto')
from speechController import SpeechController

Config.set('graphics', 'width', '2000')
Config.set('graphics', 'height', '8000')
#Window.size = (586 * 1.3, 325 * 1.3)

class MainScreen(Screen):

    # def play(self):
    #   anim = Animation(x=50, y=50, duration=2.) + Animation(x=-50, y=-50, duration=2.)
    #  anim.repeat = True
    #  anim.start(self.children[0].children[0])
    #  pass
    Window.clearcolor = (1, 1, 1, 1)

    
    if 1==1: # SKRIV ISTÄLLET EN IF SOM I 'OM ROBOTEN PRATAR/AVÄNDER PRATFUNKTIONEN'
        img_src = StringProperty('Images/Face/speaking.gif')
    else:
        img_src = StringProperty('Images/Face/mouthClosed.png')

        img_blinking = StringProperty('Images/Face/eyesOpen.jpg')

    '''def blink(self):
        if 1==1: #Starta klocka och tråd?
            img_blinking = StringProperty('Images/Face/blinking.gif')
            print('Gif started')
        else:
            img_blinking = StringProperty('Images/Face/eyesOpen.jpg')'''

    #threadEyes = threading.Thread(target=blink)
    #threadEyes.start()
    #print('Started eye thread')
    #print('Total number of threads: ', threading.activeCount())
    #print('List of threads: ', threading.enumerate())


    def schema(self):
        ScheduleScreen.showSchema(self)
    pass



class SleepScreen(Screen):
    pass


class MathScreen(Screen):
    pass



class Appview(Screen):
    def launchRPS(self):
        print('Launch RPS')
        # subprocess.Popen('python kv/RPS.py', shell=True)
        # RPSscreenApp().run()
        
    def doSpeech(self):
        print("speech")


    def listen(self):
        thread_listen = Thread(target=self.doSpeech)
        thread_listen.start()

    pass

class Calculator(Screen):

    def calculate(self, calculation):
        if calculation:
            try:
                self.display.text = str(eval(calculation))
            except Exception:
                self.display.text = "Error"
    pass

class ScheduleSScreen(Screen):
    pass


class Manager(ScreenManager):
    t = time.time()
    user = User(None,None,None)
    isVoiceActive = False

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.initialize()
        self.transition = SlideTransition()
        self.transition.duration = 1
        self.transition.direction = 'up'
        #Clock.schedule_interval(self.callback, 2)
        Clock.schedule_interval(self.startTimThread, 8)
        #Clock.schedule_interval(self.startKeywordThread, 8)
        

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
        self.add_widget(ScheduleScreenTwo(name='s2'))
        self.add_widget(ScheduleScreenThree(name='s3'))
        self.add_widget(ScheduleScreenFour(name='s4'))
        self.add_widget(ScheduleScreenFive(name='s5'))
        self.add_widget(ScheduleScreenSix(name='s6'))
        self.add_widget(Calculator(name='calculator'))
        self.add_widget(TestScreen(name='test'))

    def on_touch_down(self,touch):
        self.current_screen.on_touch_down(touch)
        self.t = time.time()

    def startTim(self):
        string = SpeechController().listenForTim(self)
        if string == "familiarUser":
            self.isVoiceActive = True
            SpeechController().playHelloName(self.user.name)
        if string == "hej":
            self.isVoiceActive = True
            SpeechController().playHello()            
            #self.current.moveMouth()

       
        
        #SpeechController.detectKeywords()

                

    def startTimThread(self,sec):
        if not(self.isVoiceActive):
            print("threadstart")
            thread_startTim = Thread(target=self.startTim)
            thread_startTim.start()

    '''def startKeywordThread(self, sec):
        thread_listenKeywords = Thread(taget = self.listenKeywords)
        thread_listenKeywords.start()'''


    def callback(self, sec):
        end = time.time()
        if ((end - self.t) > 1000):
            self.current = 'sleep'
            self.t = time.time()



class guiApp(App):
    def build(self):
        print('GuiApp')
        return Manager()
    def quit(self):
        sys.exit("Shutting down")



if __name__ == '__main__':
    guiApp().run()
