#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
import random
import time
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
        funcName = ""


    def stringSplitter(self, string):
        stringArray = string.split()
        i = 0
        for x in stringArray:
            stringArray[i] = stringArray[i].lower()
            i = i+1
        return stringArray

    def playSound(self, fileName):
        mixer.init()
        mixer.music.load(fileName)
        mixer.music.play()
    
    def mp3Exception(self):
        tts = gTTS(text= 'Jag kunde inte förstå vad du sa, kan du prata tydligare?', lang='sv')
        tts.save("Ljudfiler/speakClear.mp3")
        self.playSound("Ljudfiler/speakClear.mp3")
        print("Function name: ", funcName)
        if(funcName == "listenForTim"):
            self.listenForTim()
        elif(funcName == "playHello"):
            self.playHello()
        elif(funcName == "handleKeywords"):
            self.handleKeywords()
        elif(funcName == "startTalking"):
            self.startTalking()
        elif(funcName == "startRPSVoice"):
            self.startRPSVoice()

    def internetException(self):
        tts = gTTS(text= 'Inget internet', lang='sv')
        tts.save("Ljudfiler/internetException.mp3")

        self.playSound("Ljudfiler/internetException.mp3")

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
            print("mp3Exception")
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
            tts.save("Ljudfiler/helloName.mp3")
            self.playSound("Ljudfiler/helloName.mp3")
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
            return audio
            #self.tryListen(audio)
        

    def containsHiMyAndName(self, stringArray):
        if any(("hej" in s for s in stringArray) and ("kim" in s for s in stringArray) and ("heter" in s for s in stringArray)):
               return True
        return False

    def detectName(self, stringArray):
        namePos = stringArray.index("heter") + 1
        name = stringArray[namePos]
        return name

   
    def listenForTim(self, manager):
        funcName = "listenForTim"
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
        tts.save("Ljudfiler/helloWhatToDo.mp3")
        self.playSound("Ljudfiler/helloWhatToDo.mp3")
        self.whatToDo()


    def playHello(self):
        funcName = "playHello"
        tts = gTTS(text= 'Hej! Jag heter Kim, vad heter du?', lang='sv')
        tts.save("Ljudfiler/helloWhatsYourName.mp3")
        self.playSound("Ljudfiler/helloWhatsYourName.mp3")

        time.sleep(4)
        audio = self.listenSpeech(7)
        self.playHelloName(self.recognizedAudio(audio))

    def whatToDo(self):
        funcName = "whatToDo"
        time.sleep(1)
        tts = gTTS(text='Vill du se schema, räkna matte, spela sten, sax, påse eller prata?', lang='sv')
        tts.save("Ljudfiler/whatToDo.mp3")
        self.playSound("Ljudfiler/whatToDo.mp3")

        time.sleep(6)
        audio = self.listenSpeech(7)
        self.handleKeyword(self.recognizedAudio(audio))


    def handleKeyword(self, message):
        funcName = "handleKeyword"
        keywords = self.stringSplitter(message)
        print("keywords: ", keywords)

        if any("schema" in s for s in keywords):
            x=1 #skicka till schemametod
        elif any(("räkna" in s for s in keywords) or ("matte" in s for s in keywords)):
            x=1 #skicka till mattemetod
        elif any(("sten" in s for s in keywords) or ("sax" in s for s in keywords) or ("påse" in s for s in keywords) or ("spela" in s for s in keywords)):
            self.startRPSVoice()
        elif any(("prata" in s for s in keywords)):
            self.startTalking()      #skicka till pratmetod
        elif any(("klocka" in s for s in keywords) or ("tid" in s for s in keywords)):
            x=1 #skicka till klockmetod
        elif any("info" in s for s in keywords):
            x=1 #Skicka till infometod
        else:
            tts = gTTS(text='Kan du upprepa?', lang='sv')
            tts.save("Ljudfiler/didntUnderstand.mp3")
            self.playSound("Ljudfiler/didntUnderstand.mp3")

            audio = self.listenSpeech(7)
            self.handleKeyword(self.recognizedAudio(audio))

    def startTalking(self):
        funcName = "startTalking"
        tts = gTTS(text='Kul att du vill prata! Vill du höra ett skämt eller småprata?', lang='sv')
        tts.save("Ljudfiler/whatToTalkAbout.mp3")
        self.playSound("Ljudfiler/whatToTalkAbout.mp3")

        time.sleep(5)
        audio = self.listenSpeech(7)
        self.handleTalkKeyword(self.recognizedAudio(audio))

    def handleTalkKeyword(self, message):
        keywords = self.stringSplitter(message)

        if any("skämt" in s for s in keywords):
            self.joke()        #Gå till skämtmetod
        elif any(("småprata" in s for s in keywords) or ("prata" in s for s in keywords)):
            self.smallTalk() #Gå till småpratmetod
        else:
            self.playSound("Ljudfiler/didntUnderstand.mp3")

            audio = self.listenSpeech(7)
            self.handleTalkKeyword(self.recognizedAudio(audio))

    def smallTalk(self):
        tts = gTTS(text='Hur gammal är du?', lang='sv')
        tts.save("Ljudfiler/howOld.mp3")

        self.playSound("Ljudfiler/howOld.mp3")
        

    def joke(self):
        funcName = "joke"
        #Slumpa olika skämt
        tts = gTTS(text='Det var en gång en dansk, en norsk och Bellman som skulle tävla om vem som kunde vara inne i en svinstia i längst tid.'
                        'Först gick dansken in, men efter en minut kom han ut och stönade: Grisen fes!'
                        'Då gick norsken in och efter två minuter kom han ut, grön i ansiktet och stönade: Grisen fes!'
                        'Sedan var det Bellmans tur att gå in i svinstian. Efter tio minuter kom grisen ut och stönade: Bellman fes!', lang='sv')
        tts.save("Ljudfiler/Bellman.mp3")
        self.playSound("Ljudfiler/Bellman.mp3")

        time.sleep(38)
        self.playSound("Ljudfiler/drumroll.mp3")   #Dab?

        tts = gTTS(text='Vill du höra ett till skämt, prata eller göra något annat?', lang='sv')
        tts.save("Ljudfiler/SomethingElse.mp3")
        self.playSound("Ljudfiler/SomethingElse.mp3")

        time.sleep(5)
        audio = self.listenSpeech(7)
        self.postJoke(self.recognizedAudio(audio))

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
            tts.save("Ljudfiler/didntUnderstand.mp3")
            self.playSound("Ljudfiler/didntUnderstand.mp3")

            audio = self.listenSpeech(7)
            self.PostJoke(self.recognizedAudio(audio))


    def startRPSVoice(self):
        funcName = "startRPSVoice"
        while True:
            tts = gTTS(text='Nu spelar vi! Är du redo?', lang='sv')               # Ta bort efter första inspelning
            tts.save("ready.mp3")
            self.playSound("ready.mp3")
            time.sleep(2)
            are_you_ready_answer = self.listenSpeech(5)
            if(self.recognizedAudio(are_you_ready_answer) == "ja"):
                tts = gTTS(text='Sten, sax, påse!', lang='sv')               # Ta bort efter första inspelning
                tts.save("Ljudfiler/stenSaxPase.mp3")
                self.playSound("Ljudfiler/stenSaxPase.mp3")
                time.sleep(3)
                sign = random.randint(1, 3)
                if(sign == 1):
                    tts = gTTS(text='Jag valde sten!', lang='sv')               # Ta bort efter första inspelning
                    tts.save("Ljudfiler/iChoseStone.mp3")
                    self.playSound("Ljudfiler/iChoseStone.mp3")
                elif(sign == 2):
                    tts = gTTS(text='Jag valde sax!', lang='sv')               # Ta bort efter första inspelning
                    tts.save("Ljudfiler/iChoseScissors.mp3")
                    self.playSound("Ljudfiler/iChoseScissors.mp3")
                elif(sign == 3):
                    tts = gTTS(text='Jag valde påse!', lang='sv')               # Ta bort efter första inspelning
                    tts.save("Ljudfiler/iChosePaper.mp3")
                    self.playSound("Ljudfiler/iChosePaper.mp3")
                print("char:", sign)                                   # Skicka c till fysisk design för sten/sax/påse
                # Eventuell delay/klartecken från fysisk design
                tts2 = gTTS(text='Vill du spela igen?', lang='sv')  # Ta bort efter första inspelning
                tts2.save("Ljudfiler/playAgain.mp3")
                self.playSound("Ljudfiler/playAgain.mp3")

                play_again_answer = self.listenSpeech(3)
                if (self.recognizedAudio(play_again_answer) == "nej"):
                    tts = gTTS(text='Okej, vi kan spela mer en annan gång', lang='sv') # Ta bort efter första inspelning
                    tts.save("Ljudfiler/playAnotherTime.mp3")
                    self.playSound("Ljudfiler/playAnotherTime.mp3")
                    self.whatToDo()
                    break
            elif(self.recognizedAudio(are_you_ready_answer) == "nej"):
                time.sleep(2)
                startRPSVoice()
            else:
                tts2 = gTTS(text='Fattar ej, vi testar igen!', lang='sv')  # Ta bort efter första inspelning
                tts2.save("Ljudfiler/tryAgain.mp3")
                self.playSound("Ljudfiler/tryAgain.mp3")





