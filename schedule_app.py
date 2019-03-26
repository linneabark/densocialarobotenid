# Schedule app
# Allows the user to swipe between weeks to see different schedules

from kivy.app import App

from kivy.uix.label import Label

class ScheduleApp(App):
    def build(self):
        return Label(text='hej')

if __name__ == '__main__':
    ScheduleApp().run()