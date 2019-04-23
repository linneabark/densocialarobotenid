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

    def playSound(self, fileName):
        mixer.init()
        mixer.music.load(fileName)
        mixer.music.play()
    
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

        self.playSound("internetException.mp3")

        '''mixer.init()
        mixer.music.load("internetException.mp3")
        mixer.music.play()'''
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
            #mixer.init()
            #mixer.music.load("helloName.mp3")
            #mixer.music.play()
            self.playSound("helloName.mp3")
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
        
        #mixer.init()
        #mixer.music.load("helloWhatToDo.mp3")
        #mixer.music.play()

        self.playSound("helloWhatToDo.mp3")


    def playHello(self):
        tts = gTTS(text= 'Hej! Jag heter My, vad heter du?', lang='sv')
        tts.save("helloWhatsYourName.mp3")

        #mixer.init()
        #mixer.music.load("helloWhatsYourName.mp3")
        #mixer.music.play()

        self.playSound("helloWhatsYourName.mp3")

        #delay
        audio = self.listenSpeech(7)
        self.playHelloName(self.recognizedAudio(audio))


    def start_schedule(self, manager):
        pass
    def whatToDo(self):
        tts = gTTS(text='Vill du se schema, räkna matte, spela sten, sax påse eller prata?', lang='sv')
        tts.save("whatToDo.mp3")

        #mixer.init()
        #mixer.music.load("whatToDo.mp3")
        #mixer.music.play()

        self.playSound("whatToDo.mp3")

        #delay
        audio = self.listenSpeech(7)
        self.handleKeyword(self.recognizedAudio(audio))


    def handleKeyword(self, message):
        keywords = self.stringSplitter(message)

        if any("schema" in s for s in keywords):
            x=1 #skicka till schemametod
        elif any(("räkna" in s for s in keywords) or ("matte" in s for s in keywords)):
            x=1 #skicka till mattemetod
        elif any(("sten" in s for s in keywords) or ("sax" in s for s in keywords) or ("påse" in s for s in keywords) or ("spela" in s for s in keywords)):
            self.start_RPSvoice()
        elif any(("prata" in s for s in keywords)):
            x=1 #skicka till pratmetod
        elif any(("klocka" in s for s in keywords) or ("tid" in s for s in keywords)):
            x=1 #skicka till klockmetod
        elif any("info" in s for s in keywords):
            x=1 #Skicka till infometod
        else:
            tts = gTTS(text='Jag förstod inte, kan du säga igen?', lang='sv')
            tts.save("didntUnderstand.mp3")

            #mixer.init()
            #mixer.music.load("didntUnderstand.mp3")
            #mixer.music.play()

            self.playSound("didntUnderstand.mp3")

            audio = self.listenSpeech(7)
            self.handleKeyword(self.recognizedAudio(audio))

    def start_talking(self):
        tts = gTTS(text='Kul att du vill prata! Vill du höra ett skämt eller småprata?', lang='sv')
        tts.save("whatToTalkAbout.mp3")

        #mixer.init()
        #mixer.music.load("whatToTalkAbout.mp3")
        #mixer.music.play()

        self.playSound("didntUnderstand.mp3")

        audio = self.listenSpeech(7)
        self.handleTalkKeyword(self.recognizedAudio(audio))

    def handleTalkKeyword(self, message):
        keywords = self.stringSplitter(message)

        if any("skämt" in s for s in keywords):
            x=1 #Gå till skämtmetod
        elif any("småprata" in s for s in keywords):
            x=1 #Gå till småpratmetod
        else:
            #mixer.init()
            #mixer.music.load("didntUnderstand.mp3")
            #mixer.music.play()

            self.playSound("didntUnderstand.mp3")

            audio = self.listenSpeech(7)
            self.handleTalkKeyword(self.recognizedAudio(audio))

    def smallTalk(self):
        tts = gTTS(text='Hur gammal är du?', lang='sv')
        tts.save("howOld.mp3")

        self.playSound("howOld.mp3")


    def joke(self):
        #Slumpa olika skämt
        tts = gTTS(text='Det var en gång en dansk, en norsk och Bellman som skulle tävla om vem som kunde vara inne i en svinstia i längst tid.'
                        'Först gick dansken in, men efter en minut kom han ut och stönade: Grisen fes!'
                        'Då gick norksen in och efter två minuter kom han ut, grön i ansiktet och stönade: Grisen fes!'
                        'Sedan var det Bellmans tur att gå in i svinstian. Efter tio minuter kom grisen ut och stönade: Bellman fes!', lang='sv')
        tts.save("Bellman.mp3")

        #mixer.init()
        #mixer.music.load("Bellman.mp3")
        #mixer.music.play()

        self.playSound("Bellman.mp3")

        #delay?

        #mixer.init()
        #mixer.music.load("Ljudfiler/drumroll.mp3")
        #mixer.music.play()

        self.playSound("Ljudfiler/drumroll.mp3")

        tts = gTTS(text='Vill du höra ett till skämt, prata eller göra något annat?', lang='sv')
        tts.save("SomethingElse.mp3")

        #mixer.init()
        #mixer.music.load("SomethingElse.mp3")
        #mixer.music.play()

        self.playSound("SomethingElse.mp3")

        audio = self.listenSpeech(7)
        self.PostJoke(self.recognizedAudio(audio))

    def postJoke(self, message):
        keywords = self.stringSplitter(message)

        if any("skämt" in s for s in keywords):
            self.joke()
        elif any("prata" in s for s in keywords):
            self.smallTalk()
        elif any("annat" in s for s in keywords):
            self.whatToDo()
        else:
            tts = gTTS(text='Jag förstod inte, kan du säga igen?', lang='sv')
            tts.save("didntUnderstand.mp3")

            #mixer.init()
            #mixer.music.load("didntUnderstand.mp3")
            #mixer.music.play()

            self.playSound("didntUnderstand.mp3")

            audio = self.listenSpeech(7)
            self.PostJoke(self.recognizedAudio(audio))


    def start_RPSvoice(self):
        while True:
            tts = gTTS(text='Är du redo?', lang='sv')               # Ta bort efter första inspelning
            tts.save("ready.mp3")

            #mixer.init()
            #mixer.music.load("ready.mp3")                           # Skapa fil som säger "Är du redo?"
            #mixer.music.play()

            self.playSound("ready.mp3")

            are_you_ready_answer = self.listenSpeech(3)
            if(self.recognizedAudio(are_you_ready_answer) == "ja"):
                c = random.randint(1, 3)
                print("char:", c)                                   # Skicka c till fysisk design för sten/sax/påse
                # Eventuell delay/klartecken från fysisk design
                tts2 = gTTS(text='Vill du spela igen?', lang='sv')  # Ta bort efter första inspelning
                tts2.save("playAgain.mp3")

                #mixer.init()
                #mixer.music.load("playAgain.mp3")                   # Röstklipp "Vill du spela igen?
                #mixer.music.play()

                self.playSound("playAgain.mp3")

                play_again_answer = self.listenSpeech(3)
                if (self.recognizedAudio(play_again_answer) == "nej"):
                    tts = gTTS(text='Okej, vi kan spela mer en annan gång', lang='sv') # Ta bort efter första inspelning
                    tts.save("playAnotherTime.mp3")

                    #mixer.init()
                    #mixer.music.load("playAnotheTime.mp3")       # Röstklipp "Okej, vi kan spela mer en annan gång"
                    #mixer.music.play()

                    self.playSound("playAnotherTime.mp3")
                    break





