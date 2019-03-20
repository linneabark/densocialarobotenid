from guizero import App, Picture, PushButton

def talk():
    if mouth.image == "faceimages/mouth2.png":
        mouth.image = "faceimages/mouth.png"
    else:
        mouth.image ="faceimages/mouth2.png"

screen_height = 480
screen_width = 800

app = App(title="Den Sociala Roboten", height=screen_height, width=screen_width)

move_mouth_button = PushButton(app, command=talk, text="Talk")
eyes = Picture(app, image="faceimages/eyes.png", height=int(0.7*screen_height), width=screen_width)
mouth = Picture(app, image="faceimages/mouth.png", height=int(0.3*screen_height), width=screen_width)



app.display()

