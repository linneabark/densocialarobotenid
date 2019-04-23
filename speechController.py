#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
import random

from gtts import gTTS
from pygame import mixer
import pygame.mixer
from pygame.mixer import Sound
import speech_recognition as sr
#from kivy.core.audio import SoundLoader


class SpeechController():
    def __init__(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        

    def stringSplitter(self, string):
        stringArray = string.split()
        i = 0
        for x in stringArray:
            stringArray[i] = stringArray[i].lower()
            i += 1
        return stringArray

        
    
    def mp3Exception(self):
        tts = gTTS(text= 'Jag kunde inte forsta vad du sa, kan du saga en gang till?', lang='sv')
        tts.save("repeatName.mp3")
        mixer.init()
        mixer.music.load("internetException.mp3")
        mixer.music.play()
        #sound = SoundLoader.load("repeatName.mp3")
        #if sound:
         #   sound.play()
        #sound.play()

    def internetException(self):
        tts = gTTS(text= 'Inget internet', lang='sv')
        tts.save("internetException.mp3")
        mixer.init()
        mixer.music.load("internetException.mp3")
        mixer.music.play()
        print("hej")

    
    def recognizedAudio(self,audio):
        try:
            string = self.r.recognize_google(audio, language="sv-SV")
            #string = self.recognize_azure(audio, key = "9528141d0163486b986c549ddc3f6a4e", language = "sv-SV")
            return string
        except sr.UnknownValueError:
            print("Please try again")
            self.mp3Exception()
        except sr.RequestError as e:
            print("no internet")
            self.internetException()
        except OSError as e:
            print("oserror")

    def tryListen(self,audio):
        try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
            print("You said: " + self.r.recognize_google(audio, language = "sv-SV"))
            string = self.r.recognize_google(audio, language = "sv-SV")
            tts = gTTS(text='Hej ' +string + ' hur mar du?', lang='sv')
            tts.save("helloName.mp3")
            #sound = SoundLoader.load("helloName.mp3")
            #if sound:
            #    sound.play()
            #sound.play()
            mixer.init()
            mixer.music.load("helloName.mp3")
            mixer.music.play()
        except sr.UnknownValueError:
            print("Please try again")
            self.mp3Exception()
        except sr.RequestError as e:
            print("no internet")
            self.internetException()
        except OSError as e:
            print("oserror")
        #audiolisten()
        #print("Google Speech Recognition could not understand audio")
            
    def listenSpeech(self, time):
        with self.m as source:
            #audio = r.record(source, duration = 5)
            mixer.init()
            while(mixer.get_busy()):
                print("hej")
            if(mixer.Channel(1).get_busy()):
                print("Channel 1 busy")
            audio = self.r.listen(source, phrase_time_limit=time)
            #self.r.snowboy_wait_for_hot_word()
            return audio
            #self.tryListen(audio)
        

    def containsHiMyAndName(self, stringArray):
        if any(("hej" in s for s in stringArray) and ("karin" in s for s in stringArray) and ("heter" in s for s in stringArray)):
               return True
        return False

    def detectName(self, stringArray):
        namePos = stringArray.index("heter") + 1
        name = stringArray[namePos]
        return name

   
    def listenForTim(self, manager):
        audio = self.listenSpeech(5)
        string = self.recognizedAudio(audio)
        if(string == None):
            return
        stringArray = self.stringSplitter(string)
        print(stringArray)
        if(self.containsHiMyAndName(stringArray)):
                manager.user.name = self.detectName(stringArray)
                print('Familiar user')
                return "familiarUser"
        for x in stringArray:
            if(x == "hej"):
                print('Hej')
                return x
                break

   

                   
    def playHelloName(self, name):
        if(name == None):
            name = ""
        tts = gTTS(text= 'Hej' + name + 'vad vill du göra?', lang='sv')
        tts.save("helloWhatToDo.mp3")
        
        mixer.init()
        mixer.music.load("helloWhatToDo.mp3")
        mixer.music.play()


    def playHello(self):
        tts = gTTS(text= 'Hej! Jag heter My, vad heter du?', lang='sv')
        tts.save("helloWhatsYourName.mp3")

        mixer.init()
        mixer.music.load("helloWhatsYourName.mp3")
        mixer.music.play()

        audio = self.listenSpeech(7)
        self.playHelloName(self.recognizedAudio(audio))

    def start_schedule(self, manager):
        
        manager.current = "schedule"

    def start_RPSvoice(self):
        while True:
            tts = gTTS(text='Är du redo?', lang='sv')               # Ta bort efter första inspelning
            tts.save("ready.mp3")
            mixer.init()
            mixer.music.load("ready.mp3")                           # Skapa fil som säger "Är du redo?"
            mixer.music.play()
            are_you_ready_answer = self.listenSpeech(3)
            if(self.recognizedAudio(are_you_ready_answer) == "ja"):
                c = random.randint(1, 3)
                print("char:", c)                                   # Skicka c till fysisk design för sten/sax/påse
                # Eventuell delay/klartecken från fysisk design
                tts2 = gTTS(text='Vill du spela igen?', lang='sv')  # Ta bort efter första inspelning
                tts2.save("playAgain.mp3")
                mixer.init()
                mixer.music.load("playAgain.mp3")                   # Röstklipp "Vill du spela igen?
                mixer.music.play()
                play_again_answer = self.listenSpeech(3)
                if (self.recognizedAudio(play_again_answer) == "nej"):
                    tts = gTTS(text='Okej, vi kan spela mer en annan gång', lang='sv') # Ta bort efter första inspelning
                    tts.save("playAnotherTime.mp3")
                    mixer.init()
                    mixer.music.load("playAnotheTime.mp3")       # Röstklipp "Okej, vi kan spela mer en annan gång"
                    mixer.music.play()
                    break





