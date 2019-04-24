from kivy.uix.screenmanager import ScreenManager, Screen



class ScheduleScreen(Screen):
    def showSchema(self, *args):
        # wb = WebManager()
        # wb.findSchema()
        self.children[0].children[1].background_normal = 'test.png'

    pass



class ScheduleScreenTwo(Screen):
    pass

class ScheduleScreenThree(Screen):
    pass

class ScheduleScreenFour(Screen):
    pass

class ScheduleScreenFive(Screen):
    pass

class ScheduleScreenSix(Screen):
    pass
