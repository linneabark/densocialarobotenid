import random

def start_RPSvoice():
    while True:
        str_input = input("Är du redo, ja/nej: ")
        if(str_input == "ja"):
            c = random.randint(1, 3)
            print("char:", c)                                   #Skicka c till fysisk design
            play_again = input("Vill du spela igen, ja/nej: ")  #Röstklipp "Vill du spela igen?"
            if(play_again == "nej"):
                print("Okej, vi kan spela mer en annan gång")   #Röstklipp "Okej, vi kan spela mer en annan gång"
                break



if __name__ == '__main__':
    start_RPSvoice().run()