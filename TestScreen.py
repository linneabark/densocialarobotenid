from kivy.uix.screenmanager import Screen


class TestScreen(Screen):
    def send(self,text):
        file = open("familiarNames.txt","a")
        file.write("\n")
        file.write(text)
        file.close()
    pass