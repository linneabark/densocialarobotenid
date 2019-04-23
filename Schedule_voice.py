#from speechController import SpeechController

from main import guiApp, Manager, ScheduleScreen


def start_Schedule(self, manager):
    # Switch from face screen to schedule screen
    manager.current = 'schedule'

    tts = gTTS(text='Här är ditt schema! Säg nästa vecka eller förra veckan för att byta vecka.', lang='sv')
    tts.save('schedule_instruction.mp3')
    self.playSound('schedule_instruction.mp3')

    demand = self.listenSpeech(4)
    words = self.stringSplitter(demand)

    if "nästa" in words:
        x = manager.current

        def f(x):
            list = {
                "schedule": 's2',
                's2': 's3',
                's3': 's4',
                's4': 's5',
                's5': 's6'
            }
            next_screen = list.get(x)
            return next_screen



    elif "förra" in words:
        x = manager.current

        def f(x):
            list = {
                "s2": 'schedule',
                's3': 's2',
                's4': 's3',
                's5': 's4',
                's6': 's5'
            }
            next_screen = list.get(x)
            return next_screen

hej = start_Schedule()
hej.run()