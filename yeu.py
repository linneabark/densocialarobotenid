
'''
Camera Example
==============
This example demonstrates a simple use of the camera. It shows a window with
a buttoned labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.
'''

# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
import time

class MiCamera(App):
    def build(self):
        rl = BoxLayout()
        cam = Camera(resolution=(320,240), size=(1000,600), pos=(0,0),play=True)
        rl.add_widget(cam)
        return rl

if __name__ == "__main__":
    MiCamera().run()
