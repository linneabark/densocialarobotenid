import kivy
import random

kivy.require('1.9.0')

from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.image import Image
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

i = random.randint(1, 3)

if i == 1:
    pic = "Sten.png"
elif i == 2:
    pic = "Sax.png"
else:
    pic = "Pase.png"

Builder.load_string("""
    #: import choice random.choice

<ScreenOne>:
    FloatLayout:
        Image:
            source: "sten_sax.png"
        Button:
            text: "Spela sten, sax, påse!"
            size: 150,75
            size_hint: None, None
            pos: 315,220
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 0.5
                root.manager.current = 'screen_two'

<ScreenTwo>:
    FloatLayout:
        Image:
            source: "Sten.PNG"
        Button:
            text: "Sten"
            size: 150,75
            size_hint: None, None
            pos: 315,220
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 0.5
                root.manager.current = 'screen_three'

<ScreenThree>:
    FloatLayout:
        Image:
            source: "Sax.PNG"
        Button:
            text: "Sax"
            size: 150,75
            size_hint: None, None
            pos: 315,220
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 0.5
                root.manager.current = 'screen_four'

<ScreenFour>:
    FloatLayout:
        Image:
            source: "Pase.PNG"
        Button:
            text: "Påse"
            size: 150,75
            size_hint: None, None
            pos: 315,220
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 0.5
                root.manager.current = choice(root.manager.screen_names[4:]) 

<ScreenFive>:
    FloatLayout:
        Image:
            source: "Pase.PNG"
        Button:
            text: "Spela igen"
            size: 150,75
            size_hint: None, None
            pos: 315,220
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 0.5
                root.manager.current = 'screen_one'

<ScreenSix>:
    FloatLayout:
        Image:
            source: "Sten.PNG"
        Button:
            text: "Spela igen"
            size: 150,75
            size_hint: None, None
            pos: 315,220
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 0.5
                root.manager.current = 'screen_one'

<ScreenSeven>:
    FloatLayout:
        Image:
            source: "Sax.PNG"
        Button:
            text: "Spela igen"
            size: 150,75
            size_hint: None, None
            pos: 315,220
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 0.5
                root.manager.current = 'screen_one'
""")


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


class ScreenSeven(Screen):
    pass


screen_manager = ScreenManager()

screen_manager.add_widget(ScreenOne(name="screen_one"))
screen_manager.add_widget(ScreenTwo(name="screen_two"))
screen_manager.add_widget(ScreenThree(name="screen_three"))
screen_manager.add_widget(ScreenFour(name="screen_four"))
screen_manager.add_widget(ScreenFive(name="screen_five"))
screen_manager.add_widget(ScreenSix(name="screen_six"))
screen_manager.add_widget(ScreenSeven(name="screen_seven"))


class KivyTut2App(App):

    def build(self):
        return screen_manager


sample_app = KivyTut2App()
sample_app.run()