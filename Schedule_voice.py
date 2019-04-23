#from speechController import SpeechController

from main import guiApp, Manager, ScheduleScreen

def show_schedule():
    string = input('Enter string: ')
    words = string.split()
    if 'schema' or 'kalender' in words:
        guiApp().run()



    '''def switch_week(self):
        if 1 == 1:
            print('hej')'''


hej = show_schedule()
hej.run()