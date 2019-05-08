#:kivy 1.10.1
import random

from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation


class RPSScreen(Screen):
    pass

# Lägg till en skärm som räknar ner tills spelet startar

class ScreenOne(Screen):
    pass


class ScreenTwo(Screen):
   # def animate(self):
      #  print('Animation')
      #  if(self.children[0].children[0].pos == (80,10)):
     #       self.children[0].children[0].pos = (0, 0)
      #  anim = Animation(pos=(80, 10))
       # anim.repeat = True
        #anim.start(self.children[0].children[0])

    def on_enter(self, *args):
        #self.animate()
        Clock.schedule_once(self.callbackfun, 5)


    def callbackfun(self, dt):
        self.manager.current = 'four'

class ScreenThree(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.callbackfun, 1)

    def callbackfun(self, dt):
        self.manager.current = 'four'


class ScreenFour(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.callbackfun, 1)

    def callbackfun(self, dt):
        list = ["five", "six", "seven"]
        self.manager.current = random.choice(list)


class ScreenFive(Screen):
    pass


class ScreenSix(Screen):
    pass


class ScreenSeven(Screen):
    pass
