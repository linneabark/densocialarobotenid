from guizero import App, Picture

screen_height = 480
screen_width = 800

app = App(title="Den Sociala Roboten", height=screen_height, width=screen_width)
#face = Picture(app, image="face.gif")

eyes = Picture(app, image="face images/eyes.png", height=int(0.7*screen_height), width=screen_width)
mouth = Picture(app, image="face images/mouth.png", height=int(0.3*screen_height), width=screen_width)

app.display()
