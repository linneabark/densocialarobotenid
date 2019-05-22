#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
import os
import random
import time
from gtts import gTTS
from pygame import mixer
import pygame.mixer
from pygame.mixer import Sound
import speech_recognition as sr
import datetime
#from kivy.core.audio import SoundLoader
from mutagen.mp3 import MP3
from FileController import FileHandler
from fractions import Fraction
import sys

from ArduinoHandler2 import ArduinoHandler



from FileController import FileHandler

class SpeechController():
    def __init__(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.funcName = ""
        self.speaking = False
        self.name = ""
        self.manager = ""
        self.differentJoke = []
        self.differentSmallTalk =[]
        self.playedRPSBefore = False
        self.counterRPS = 0


    def keywordRecognition(self, string, keyword):
        if string == None or keyword == None:
            return

        stringArray = string.split()
        for i, x in enumerate(stringArray):
            stringArray[i] = x.lower()
        keyword = keyword.lower()

        if any(keyword in s for s in stringArray):
            return True

    def speakingFalse(self):
        self.speaking = False

    def booleanSchedule(self, screen):
        if screen == 'schedule' or screen == 's2' or screen == 's3' or screen == 's4' or screen == 's5' or screen == 's6':
            return True
        else:
            return False
        
        
    def playSound(self, fileName):
        screen = FileHandler().readScreen(self.name)
        if self.booleanSchedule(screen):
            screen = screen
        else:
            FileHandler().append(self.name,'screen','talking' + screen)
        self.speaking = True
        audio = MP3(fileName)
        length = audio.info.length
        mixer.init()
        mixer.music.load(fileName)
        mixer.music.play()
        time.sleep(length)
        self.speaking = False
        FileHandler().append(self.name, 'screen', screen)
    
    
    
    def mp3Exception(self):
        FileHandler().append(self.name,'screen','confusedscreen')
        self.didntUnderstand()
        self.fromWhatFunc()
        

    def fromWhatFunc(self):
        print("Function name: ", self.funcName)
        if(self.funcName == "listenForKim"):
            self.listenForKim()
        if(self.funcName == "playHello"):
            self.playHello()
        elif(self.funcName == 'playHelloName'):
            self.playHelloName()
        elif(self.funcName == "startTalking"):
            self.startTalking()
        elif(self.funcName == "startRPSVoice"): #klar
            self.startRPSVoice()
        elif (self.funcName == "goodbye"): #klar
            self.goodbye()
        elif (self.funcName == "haveYouPlayed"): #klar
            self.haveYouPlayed()
        elif (self.funcName == "handleKeyword"): #klar
            self.whatToDo()
        elif (self.funcName == "askQuestion"): #klar
            self.smallTalk()
        elif (self.funcName == "wantToHearAJoke"): #klar
            self.wantToHearAJoke()
        elif (self.funcName == "wantToContinueTalking"): #klar
            self.wantToContinueTalking()
        elif (self.funcName == "postJoke"): #klar
            self.postJoke()
        elif (self.funcName == "postTalk"):
            self.postTalk()
        elif (self.funcName == "playerChoice"):
            self.playerChoice()
        elif (self.funcName == "playRPSPhrases"):
            self.playRPSPhrases()
        elif (self.funcName == "startSchedule"):
            self.startSchedule()
        elif (self.funcName == "startMath"):
            self.startMath()
        elif (self.funcName == "help"):
            self.help()
        elif (self.funcName == "whatToDo"):
            self.whatToDo()
        elif (self.funcName == "playAgain"):
            self.playAgain()

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
            self.overallKeyword(string)
            string = string.lower()
            return string
        except sr.UnknownValueError:
            print("mp3Exception")
            self.mp3Exception()
        except sr.RequestError as e:
            print("no internet")
            self.internetException()
        except OSError as e:
            print("oserror")

    '''def tryListen(self,audio):
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
        #print("Google Speech Recognition could not understand audio")'''
            
    def listenSpeech(self, time):
        self.playSound("Ljudfiler/startBeep.mp3")
        with self.m as source:
            #audio = r.record(source, duration = 5)
            mixer.init()
            audio = self.r.listen(source, phrase_time_limit=time)
            self.playSound("Ljudfiler/stopBeep.mp3")
            return audio
            #self.tryListen(audio)

    def goodbye(self):  # Lägg till personliga fraser
        self.funcName = "goodbye"
        tts = gTTS(text='Vill du verkligen säga hejdå?', lang='sv')
        tts.save("Ljudfiler/goodbye.mp3")
        self.playSound("Ljudfiler/goodbye.mp3")

        audio = self.listenSpeech(5)
        answer = self.recognizedAudio(audio)

        if self.keywordRecognition(answer, 'ja'):
            tts = gTTS(text='Okej! ' + self.name + 'det var kul att leka med dig. Ses snart igen!', lang='sv')
            tts.save("Ljudfiler/goodbyeSleep.mp3")
            self.playSound("Ljudfiler/goodbyeSleep.mp3")
            ArduinoHandler().write(b'k')
            FileHandler().append(self.name,"screen","sleep")
            sys.exit()
        elif self.keywordRecognition(answer, 'nej'):
            tts = gTTS(text='Okej! ' + self.name + 'då fortsätter vi leka!', lang='sv')
            tts.save("Ljudfiler/okKeepPlaying.mp3")
            self.playSound("Ljudfiler/okKeepPlaying.mp3")
            self.fromWhatFunc()
        elif self.keywordRecognition(answer, 'avsluta'):
            FileHandler().append(self.name,'screen','goodbye')
        else:
            self.didntUnderstand()
            self.goodbye()


    '''def containsHiKimAndName(self, stringArray):
        if any(("hej" in s for s in stringArray) and ("kim" in s for s in stringArray) and ("heter" in s for s in stringArray)):
               return True
        return False'''

    def detectName(self, string):
        stringArray = string.split()
        if len(stringArray) == 1:
            self.name = stringArray[0]
        else:
            namePos = stringArray.index("heter") + 1
            self.name = stringArray[namePos]
        return self.name

   
    def listenForKim(self):
        self.funcName = "listenForKim"
        print('Listen for Kim')
        audio = self.listenSpeech(5)
        string = self.recognizedAudio(audio)
        if(string == None):
            return
        #stringArray = self.stringSplitter(string)
        #print(stringArray)
        #if(self.containsHiMyAndName(stringArray)):
        #    self.name = self.detectName(stringArray)
            #print('Familiar user')
            #return "familiarUser"
        if self.keywordRecognition(string,'hej'):
            self.playHelloName()
        elif self.keywordRecognition(string,'spela'):
            self.startRPSVoice()
        elif self.keywordRecognition(string,'prata'):
            self.smallTalk()
        else:
            self.didntUnderstand()
            self.listenForKim()
                   
    def playHelloName(self):
        self.funcName = 'playHelloName'

        print('In playHelloName()')
        
        self.startPhrases()
        
        print('Before recording')
        string = 'oklart'
        audio = self.listenSpeech(4)
        string = self.recognizedAudio(audio)
        self.name = string

        print('After recording, name: ' + string)
        
        if (FileHandler().userExists(self.name)):
            #tts = gTTS(text='Hej' + name + ', kul att se dig igen! Vad vill du göra idag?', lang='sv')
            #tts.save("Ljudfiler/existingUser.mp3")
            FileHandler().append(self.name, 'screen', 'redheartscreen')
            #self.playSound("Ljudfiler/existingUser.mp3")
            #self.whatToDo()
            self.helloPhrasesFamiliarUser(self.name) # Skicka in bara "name"?
        else:
            FileHandler().create(self.name)
            #FileHandler().append(self.name, 'screen', 'mainscreen')
            self.helloPhrasesUnknownUser(self.name)

    def startPhrases(self):
        nr = random.randint(1,4)
        if (nr == 1):
            tts = gTTS(text='Hej! Jag heter Kim, vad heter du?', lang='sv')
        elif (nr == 2):
            tts = gTTS(text='Tjenare! Mitt namn är Kim, vad är ditt?', lang='sv')
        elif (nr == 3):
            tts = gTTS(text='Äntligen någon som vill leka! Det är jag som är Kim, vad heter du?', lang='sv')
        elif (nr == 4):
            tts = gTTS(text= self.timeOfDay() + ' Mitt namn är Kim, vad heter du?', lang='sv')

        tts.save("Ljudfiler/helloWhatsYourName.mp3")
        self.playSound("Ljudfiler/helloWhatsYourName.mp3")


    def timeOfDay(self):
        hour = datetime.datetime.now().hour
        string = 'Nej men tjena!' 
        if hour < 10:
            string = 'God morgon!'
        elif hour > 10 and hour < 14:
            string = 'Goddag!'
        elif hour > 14 and hour < 18:
            string = 'God eftermiddag!'
        elif hour > 18:
            string = 'Gokväll!'
        return string


    def helloPhrasesFamiliarUser(self, name):
        nr = random.randint(1, 4)

        if (nr == 10): # Om aktuell user har en sport i sin json-fil
            nr = 5
            sport = "fotboll" # Välj sporten från json-filen
        if (nr == 1):
            tts = gTTS(text='Hej ' + name + ', jag har saknat dig! Vad vill du göra?', lang='sv')
        elif (nr == 2):
            tts = gTTS(text = 'Tjena ' + name + 'vad kul att du vill leka igen. Det var så kul sist!', lang ='sv')
        elif (nr == 3):
            tts = gTTS(text='Vad kul att träffa dig igen ' + name + ', nu ska vi leka!', lang='sv')
        elif (nr == 4):
            tts = gTTS(text='Tjena polare! Vad vill du hitta på idag ' + name + '?', lang='sv')
        elif (nr == 5):
            self.haveYouPlayed(name, sport)
        tts.save("Ljudfiler/helloWhatToDo.mp3")
        self.playSound("Ljudfiler/helloWhatToDo.mp3")
        self.whatToDo()

    def haveYouPlayed(self, name, sport):
        self.funcName = "haveYouPlayed"
        tts = gTTS(text='Hej ' + name + ', har du spelat någon ' + sport + 'sedan sist?')
        tts.save("Ljudfiler/helloHaveYouPlayed.mp3")
        self.playSound("Ljudfiler/helloHaveYouPlayed.mp3")

        audio = self.listenSpeech(4)
        answer = self.recognizedAudio(audio)

        if self.keywordRecognition(answer, 'ja'):
            tts = gTTS(text='Vad kul! Jag älskar ' + sport)
            tts.save("Ljudfiler/iLoveX.mp3")
            self.playSound("Ljudfiler/iLoveX.mp3")
        elif self.keywordRecognition(answer, 'nej'):
            tts = gTTS(text='Okej, hoppas du får spela det snart!')
            tts.save("Ljudfiler/hopeToPlaySoon.mp3")
            self.playSound("Ljudfiler/hopeToPlaySoon.mp3")
        else:
            self.didntUnderstand()

    '''def playHello(self):
        self.funcName = "playHello"
        #self.helloPhrasesUnknownUser()
        audio = self.listenSpeech(4)
        answer = self.recognizedAudio(audio)
        self.name = answer
        self.playHelloName(answer)'''

    def helloPhrasesUnknownUser(self, name):
        nr = random.randint(1,5)
        if (nr == 1):
            tts = gTTS(text='Hej! Trevligt att träffa dig,' + name + '! Vad vill du göra nu?', lang='sv')
        elif (nr == 2):
            tts = gTTS(text='Hej ' + name + ', vad kul att få lära känna dig! Vad vill du hitta på?', lang='sv')
        elif (nr == 3):
            tts = gTTS(text='Äntligen någon som vill leka! Vad ska vi göra ' + name + '?', lang='sv')
        elif (nr == 4):
            tts = gTTS(text='Hallå!' + self.name + 'Äntligen en till kompis!', lang='sv')
        elif (nr == 5):
            tts = gTTS(text= self.name + ', det var ett fint namn! Vad vill du göra?', lang='sv')

        tts.save("Ljudfiler/helloWhatsYourName.mp3")
        self.playSound("Ljudfiler/helloWhatsYourName.mp3")
        self.whatToDo()


    def whatToDo(self):
        FileHandler().append(self.name, 'screen','mainscreen')
        self.funcName = "whatToDo"
        #tts = gTTS(text='Vill du se schema, räkna matte, spela sten sax påse eller prata?', lang='sv')
        tts = gTTS(text='säg ett nyckelord', lang='sv')
        tts.save("Ljudfiler/whatToDo.mp3")
        self.playSound("Ljudfiler/whatToDo.mp3")
        audio = self.listenSpeech(4)
        answer = self.recognizedAudio(audio)
        print(answer)
        if self.keywordRecognition(answer,'upprepa'):
            self.whatToDo()
        else:
            self.handleKeyword(answer)


    def handleKeyword(self, message):
        self.funcName = "handleKeyword"

        if self.keywordRecognition(message,'schema') or self.keywordRecognition(message,'kalender'):
            self.startSchedule()
        elif self.keywordRecognition(message,'räkna') or self.keywordRecognition(message,'matte'):
            self.startMath()
        elif self.keywordRecognition(message,'sten') or self.keywordRecognition(message,'sax') or self.keywordRecognition(message,'påse') or self.keywordRecognition(message,'spela'):
            print('Startar RPS')
            self.startRPSVoice()
        elif self.keywordRecognition(message,'prata'):
            self.startTalking()      #skicka till pratmetod
        else:
            self.didntUnderstand()
            audio = self.listenSpeech(4)
            self.handleKeyword(self.recognizedAudio(audio))

    def overallKeyword(self, string):
        print('Overall keyword: ' + string)
        if self.keywordRecognition(string,'hejdå') or (self.keywordRecognition(string,'hej') and self.keywordRecognition(string,'då')):
            self.goodbye()
        elif self.keywordRecognition(string, 'kim'):
            self.whatToDo()
        elif self.keywordRecognition(string, 'hjälp'):
            self.help()
        elif self.keywordRecognition(string, 'klocka'):
            self.whatTime()
        elif self.keywordRecognition(string, 'app'):
            FileHandler().append(self.name,'screen','appview')
            sys.exit()
        elif self.keywordRecognition(string, 'avsluta'):
            sys.exit()
        elif self.keywordRecognition(string,'schema') or self.keywordRecognition(string,'kalender'):
            self.startSchedule()
        elif self.keywordRecognition(string,'räkna') or self.keywordRecognition(string,'matte'):
            self.startMath()
        elif self.keywordRecognition(string,'spela'):
            print('Startar RPS')
            self.startRPSVoice()
        elif self.keywordRecognition(string,'prata'):
            self.startTalking()
        elif self.keywordRecognition(string, 'vakna'):
            ArduinoHandler().write(b'l')
        elif self.keywordRecognition(string, 'sov'):
            ArduinoHandler().write(b'k')
        elif self.keywordRecognition(string, 'skaka'):
            ArduinoHandler().write(b'i')
        elif self.keywordRecognition(string, 'dab'):
            ArduinoHandler().write(b'e')
        elif self.keywordRecognition(string, 'apa'):
            ArduinoHandler().write(b'h')
        elif self.keywordRecognition(string, 'somna'):
            ArduinoHandler().write(b'k')
        elif self.keywordRecognition(string, 'vakna'):
            ArduinoHandler().write(b'l')
        elif self.keywordRecognition(string, 'höger'):
            ArduinoHandler().write(b'v')
        elif self.keywordRecognition(string, 'återställ'):
            ArduinoHandler().write(b'R')
        elif self.keywordRecognition(string, 'krossa'):
            ArduinoHandler().write(b'c')
            ArduinoHandler().write(b'R')
        elif self.keywordRecognition(string, 'klippa'):
            ArduinoHandler().write(b'b')
            ArduinoHandler().write(b'R')
        elif self.keywordRecognition(string, 'prassla'):
            ArduinoHandler().write(b'a')
            ArduinoHandler().write(b'R')
        elif self.keywordRecognition(string, 'okej'):
            ArduinoHandler().write(b'd')
            ArduinoHandler().write(b'R')
        elif self.keywordRecognition(string, 'skämt'):
            self.joke()
        

                                    


    '''
    def isWhatToDoKeyword(self, string):
        if self.keywordRecognition(string, 'schema') or self.keywordRecognition(string,'kalender') or self.keywordRecognition(string,'räkna') or
        self.keywordRecognition(string,'matte') or self.keywordRecognition(string,'sten') or self.keywordRecognition(string,'sax') or
        self.keywordRecognition(string,'påse') or self.keywordRecognition(string,'spela') or self.keywordRecognition(string,'prata'):
                return True
        else:
            return False'''
    

    def demo(self):
        tts = gTTS(text='Hej! Jag heter Kim, vad heter du?', lang='sv')  # Behöver testas!!
        tts.save("Ljudfiler/demo.mp3")
        self.playSound("Ljudfiler/demo.mp3")

        audio1 = self.listenSpeech(4)
        answer1 = self.recognizedAudio(audio1)

        tts = gTTS(text='Vad kul att träffa dig ' + answer1, lang='sv')  # Behöver testas!!
        tts.save("Ljudfiler/demo.mp3")
        self.playSound("Ljudfiler/demo.mp3")

        audio2 = self.listenSpeech(4)
        answer2 = self.recognizedAudio(audio2)

        tts = gTTS(text='Jag mår bra tack! Det är jätteroligt att vara här på Johannebergskolan idag!', lang='sv')  # Behöver testas!!
        tts.save("Ljudfiler/demo.mp3")
        self.playSound("Ljudfiler/demo.mp3")

        audio3 = self.listenSpeech(4)
        answer3 = self.recognizedAudio(audio2)


    def help(self):
        self.funcName = "help"
        tts = gTTS(text='Jag ska hjälpa dig. Säg ALTERNATIV för att få alternativ om vad du kan göra, '
                        'säg HEJDÅ för att avsluta, säg APP för att öppna appen, '
                        ', säg KLOCKA för att veta tiden, säg PAUS för att pausa, '
                        'säg UPPREPA för att höra alternativen igen.', lang='sv')
        tts.save("Ljudfiler/helpOptions.mp3")
        self.playSound("Ljudfiler/helpOptions.mp3")

        audio = self.listenSpeech(4)
        answer = self.recognizedAudio(audio)

        if self.keywordRecognition(answer, 'upprepa'):
            self.help()

    def whatTime(self):
        hour = str(datetime.datetime.now().hour)
        minute = str(datetime.datetime.now().minute)

        if(int(minute) < 10):        
            tts = gTTS(text='Klockan är ' + hour + ' noll ' + minute, lang='sv') # Behöver testas!!
        else:
            tts = gTTS(text='Klockan är ' + hour + ' ' + minute, lang='sv')
        tts.save("Ljudfiler/clock.mp3")
        self.playSound("Ljudfiler/clock.mp3")
        time.sleep(1)
        self.whatToDo()


    def didntUnderstand(self):
        nr = random.randint(1, 6)
        if(nr == 1):
            tts = gTTS(text='Jag förstod inte, kan du säga igen!', lang='sv')
        if(nr == 2):
            tts = gTTS(text='Kan du upprepa det där?', lang='sv')
        if(nr == 3):
            tts = gTTS(text='Jag har sockervadd i öronen, du får säga igen.', lang='sv')
        if(nr == 4):
            tts = gTTS(text='Kan du prata tydligare?', lang='sv')
        if(nr == 5):
            tts = gTTS(text='Kan du upprepa?', lang='sv')
        if (nr == 6):
            tts = gTTS(text='Jag har persilja i öronen, du får säga igen.', lang='sv')

        tts.save("Ljudfiler/didntUnderstand1.mp3")
        self.playSound("Ljudfiler/didntUnderstand1.mp3")


    def startTalking(self):
        self.funcName = "startTalking"
        tts = gTTS(text='Kul att du vill prata!', lang='sv')
        tts.save("Ljudfiler/whatToTalkAbout.mp3")
        self.playSound("Ljudfiler/whatToTalkAbout.mp3")
        self.smallTalk()

    def whatColor(self,string):
        #eventuellt kolla efter rött, blått etc.
        print(string)
        if self.keywordRecognition(string, 'röd'):
            tts = gTTS(text='Ja, röd som tomater och kärleken!', lang='sv')
        elif self.keywordRecognition(string, 'blå'):
            tts = gTTS(text='Det är också min favoritfärg!', lang='sv')
        elif self.keywordRecognition(string, 'gul'):
            tts = gTTS(text='Gult rimmar med fult!', lang='sv')
        elif self.keywordRecognition(string, 'grön'):
            tts = gTTS(text='åh vad härligt, som en sommaräng!', lang='sv')
        elif self.keywordRecognition(string, 'rosa'):
            tts = gTTS(text='åh, nu blev jag sugen på sockervadd!', lang='sv')
        elif self.keywordRecognition(string, 'brun'):
            tts = gTTS(text='Är du helt säker på det, då ser det ju ut som ... Chokladmousse!', lang='sv')
        elif self.keywordRecognition(string, 'lila'):
            tts = gTTS(text='Ja det är fint!', lang='sv')
        else:
            tts = gTTS(text='Det är en fin färg!', lang='sv')

        tts.save("Ljudfiler/favoriteColors.mp3")
        self.playSound("Ljudfiler/favoriteColors.mp3")

    def whatSport(self,string):
        print(string)
        if self.keywordRecognition(string, 'fotboll'):
            tts = gTTS(text='Min med! Zlatan är min idol.', lang='sv')
        elif self.keywordRecognition(string, 'löpning'):
            tts = gTTS(text='Jag slår vad om att jag slår dig på 100 meter.', lang='sv')
        elif self.keywordRecognition(string, 'hockey'):
            tts = gTTS(text='Såg du hockey VM? Sverige var ju grymma!', lang='sv') # Uppdatera innan redovisning
        elif self.keywordRecognition(string, 'ishockey'):
            tts = gTTS(text='Såg du hockey VM? Sverige var ju grymma!', lang='sv')  # Uppdatera innan redovisning
        elif self.keywordRecognition(string, 'innebandy'):
            tts = gTTS(text='Åh då kan du lära mig hur man håller klubban!', lang='sv')
        elif self.keywordRecognition(string, 'handboll'):
            tts = gTTS(text='Är det för svårt att hantera bollen med fötterna eller?', lang='sv')
        elif self.keywordRecognition(string, 'esport'):
            tts = gTTS(text='Va? Det är ju ingen riktig sport.', lang='sv')
        elif self.keywordRecognition(string, 'skidor'):
            tts = gTTS(text='Se upp i backen! Annars får du tusen hål i nacken.', lang='sv')
        else:
            tts = gTTS(text='Oj det låter farligt!', lang='sv')

        tts.save("Ljudfiler/favoriteSport.mp3")
        self.playSound("Ljudfiler/favoriteSport.mp3")
            

    def askQuestion(self, tts):
        self.funcName = "askQuestion"
        tts.save("Ljudfiler/askQuestion.mp3")
        self.playSound("Ljudfiler/askQuestion.mp3")
        audio = self.listenSpeech(4)
        string = self.recognizedAudio(audio)
        return string
    
    def smallTalk(self):
        question = random.randint(1,5)

        if (len(self.differentSmallTalk) == 4):
            tts = gTTS(text='Nu har jag slut på samtalsämnen, men wow vilken intellektuell resa vi har gjort ' + self.name, lang='sv')
            tts.save("Ljudfiler/endOfConversation.mp3")
            self.playSound("Ljudfiler/endOfConversation.mp3")
            self.differentSmallTalk = []
            self.whatToDo()
        if question == 1 and 1 not in self.differentSmallTalk:
            self.differentSmallTalk.append(1)
            tts = gTTS(text='Hur gammal är du? ' + self.name, lang='sv')
            string = self.askQuestion(tts)
            FileHandler().append(self.name,"age",string)
            tts = gTTS(text= 'Då är du äldre än mig, jag är bara 2 månader!', lang='sv')
            tts.save("Ljudfiler/wowage.mp3")
            self.playSound("Ljudfiler/wowage.mp3")
            
        elif question == 2 and 2 not in self.differentSmallTalk:
            self.differentSmallTalk.append(2)
            tts = gTTS(text='Vilken är din favoritfärg?', lang='sv')
            string = self.askQuestion(tts)
            self.whatColor(string)
            FileHandler().append(self.name, "color", string)

        elif question == 3 and 3 not in self.differentSmallTalk:
            self.differentSmallTalk.append(3)
            tts = gTTS(text='Vilken är din favoritsport?', lang='sv')
            string = self.askQuestion(tts)
            self.whatSport(string)
            FileHandler().append(self.name, "sport", string)

        elif question == 4 and 4 not in self.differentSmallTalk:
            self.differentSmallTalk.append(4)
            self.wantToHearAJoke()

        elif question == 5 and 5 not in self.differentSmallTalk:
            self.differentSmallTalk.append(5)
            tts = gTTS(text='Vad vill du bli när du blir stor?', lang='sv')


        self.smallTalk()

    def wantToHearAJoke(self):
        self.funcName = "wantToHearAJoke"
        tts = gTTS(text='Vill du höra ett skämt?', lang='sv')
        tts.save("Ljudfiler/wantToHearAJoke.mp3")
        self.playSound("Ljudfiler/wantToHearAJoke.mp3")

        audio = self.listenSpeech(3)
        answer = self.recognizedAudio(audio)

        if self.keywordRecognition(answer, 'ja'):
            self.joke()
        elif self.keywordRecognition(answer,'nej'):
            tts = gTTS(text='Okej, då slipper du.', lang='sv')
            tts.save("Ljudfiler/ok.mp3")
            self.playSound("Ljudfiler/ok.mp3")
            self.smallTalk()
        else:
            self.didntUnderstand()
            self.wantToHearAJoke()

    def wantToContinueTalking(self):
        self.funcName = "wantToContinueTalking"
        tts = gTTS(text='Vill du fortsätta prata?', lang='sv')
        tts.save("Ljudfiler/wantToContinueTalking.mp3")
        self.playSound("Ljudfiler/wantToContinueTalking.mp3")

        audio = self.listenSpeech(3)
        answer = self.recognizedAudio(audio)

        if self.keywordRecognition(answer, 'ja'):
            self.smallTalk()
        elif self.keywordRecognition(answer, 'nej'):
            tts = gTTS(text='Okej, då gör vi något annat', lang='sv')
            tts.save("Ljudfiler/okLetsDoSomethingElse.mp3")
            self.playSound("Ljudfiler/okLetsDoSomethingElse.mp3")
            self.whatToDo()
        else:
            self.didntUnderstand()
            self.wantToContinueTalking()


    def joke(self):
        self.funcName = "joke"
        nr = random.randint(1, 4)
        if (len(self.differentJoke) == 4):
            tts = gTTS(text = 'Nu har jag slut på skämt, du och jag ' + self.name + ' vilken skrattfest vi har haft. Låt oss fortsätta prata.', lang='sv')
            tts.save("Ljudfiler/joke.mp3")
            self.playSound("Ljudfiler/joke.mp3")
            self.differentJoke = []
            self.smallTalk()
        elif (nr == 1 and 1 not in self.differentJoke):
            self.differentJoke.append(1)
            tts1 = gTTS(text='Vad sa den ena kannibalen till den andra?', lang='sv')
            tts1.save("Ljudfiler/firstPartofJoke.mp3")
            self.playSound("Ljudfiler/firstPartofJoke.mp3")
            time.sleep(1)
            tts = gTTS(text = 'Är du go eller!', lang='sv')
        elif (nr == 2 and 2 not in self.differentJoke):
            self.differentJoke.append(2)
            tts1 = gTTS(text = 'Vet du vad man får om man korsar en giraff och en igelkott? ', lang='sv')
            tts1.save("Ljudfiler/firstPartofJoke.mp3")
            self.playSound("Ljudfiler/firstPartofJoke.mp3")
            time.sleep(1)
            tts = gTTS(text = 'En tre meter lång tandborste!', lang='sv')
        elif (nr == 3):
            self.differentJoke.append(3)
            tts1 = gTTS(text='Vad sa marsgubbarna när de landade på jorden?', lang='sv')
            tts1.save("Ljudfiler/firstPartofJoke.mp3")
            self.playSound("Ljudfiler/firstPartofJoke.mp3")
            time.sleep(1)
            tts = gTTS(text = 'Hej jordgubbar!', lang='sv')
        elif (nr == 4):
            self.differentJoke.append(4)
            tts1 = gTTS(text='Vad är en groda utan ben?', lang='sv')
            tts1.save("Ljudfiler/firstPartofJoke.mp3")
            self.playSound("Ljudfiler/firstPartofJoke.mp3")
            time.sleep(1)
            tts = gTTS(text='Hopplös!', lang='sv')
        else:
            self.joke()


        time.sleep(0.5)
        tts.save("Ljudfiler/joke.mp3")
        self.playSound("Ljudfiler/joke.mp3")
        self.playSound("Ljudfiler/drumroll.mp3")   #Dab?        
        if(nr == 3):
            #ArduinoHandler().write(b'i')
            tts1 = gTTS(text='Det var ett dåligt skämt', lang='sv')
            tts1.save("Ljudfiler/badJoke.mp3")
            self.playSound("Ljudfiler/badJoke.mp3")

        self.postJoke()


    def postJoke(self):
        self.funcName = "postJoke"
        tts = gTTS(text='Vill du höra ett till skämt?', lang='sv')
        tts.save("Ljudfiler/oneMoreJoke.mp3")
        self.playSound("Ljudfiler/oneMoreJoke.mp3")

        audio = self.listenSpeech(4)
        answer = self.recognizedAudio(audio)

        if self.keywordRecognition(answer, 'ja'):
            self.joke()
        elif self.keywordRecognition(answer, 'nej'):
            self.smallTalk()
        else:
            self.didntUnderstand()
            self.postJoke()

    def postTalk(self, message):
        self.funcName = 'postTalk'

        if self.keywordRecognition(message,'skämt'):
            self.joke()
        elif self.keywordRecognition(message,'prata'):
            self.smallTalk()
        elif self.keywordRecognition(message,'annat'):
            self.whatToDo()
        else:
            self.didntUnderstand()
            audio = self.listenSpeech(4)
            self.postTalk(self.recognizedAudio(audio))

    def signalToHand(self, sign):
        if (sign == 1):
            ArduinoHandler().write(b'c')
        elif (sign == 2):
            ArduinoHandler().write(b'b')
        else:
            ArduinoHandler().write(b'a')
            

    def startRPSVoice(self):
        print('In startRPSVoice')
        self.funcName = "startRPSVoice"
        sign = random.randint(1, 3)
        self.playRPSPhrases()
        self.signalToHand(sign)
        tts2 = gTTS(text='Gör dig redo! Sten, ' + '  ' + ' sax, ' + '  ' + ' påse', lang='sv')
        tts2.save("Ljudfiler/stenSaxPase.mp3")
        self.playSound("Ljudfiler/stenSaxPase.mp3")
        print("sign:", sign)
        user = self.playerChoice()
        self.rockPaperScissors(sign,user)
        ArduinoHandler().write(b'R')
        print('Before playAgain')
        self.playAgain()
        print('After playAgain')
        #elif(answer == "nej"):
            #self.startRPSVoice()
        #elif(answer == "tillbaka"):
            #tts3 = gTTS(text='Okej, vi går tillbaka', lang='sv')  # Ta bort efter första inspelning
            #tts3.save("Ljudfiler/goBack.mp3")
            #self.playSound("Ljudfiler/goBack.mp3")
            #self.whatToDo()
        #elif(answer == "upprepa"):
            #self.startRPSVoice()
        #else:
            #tts2 = gTTS(text='Jag förstod inte, vi testar igen!', lang='sv')  # Ta bort efter första inspelning
            #tts2.save("Ljudfiler/tryAgain.mp3")
            #self.playSound("Ljudfiler/tryAgain.mp3")
            #self.startRPSVoice()

    def playerChoice(self):
        self.funcName = "playerChoice"
        tts1 = gTTS(text='Vad valde du?', lang='sv')
        tts1.save("Ljudfiler/playerChoice.mp3")
        self.playSound("Ljudfiler/playerChoice.mp3")
        audio = self.listenSpeech(3)
        answer = self.recognizedAudio(audio)
        if self.keywordRecognition(answer, 'sten'):
            return 1
        elif self.keywordRecognition(answer, 'sax'):
            return 2
        elif self.keywordRecognition(answer, 'påse'):
            return 3
        else:
            tts1 = gTTS(text='Jag förstod inte vad du sa, ' + self.name + ', vi tar det igen.', lang='sv')
            tts1.save("Ljudfiler/playerChoiceUnclear.mp3")
            self.playSound("Ljudfiler/playerChoiceUnclear.mp3")
            self.playerChoice()
        
    def rockPaperScissors(self, sign, user):
        currentWins = FileHandler().read(self.name, 'wins')
        if (currentWins == ""):
            currentWins = 0
        else:
            currentWins = int(currentWins)

        currentLosses = FileHandler().read(self.name, 'losses')
        if (currentLosses == ""):
            currentLosses = 0
        else:
            currentLosses = int(currentLosses)
        
        if(sign == 1 and user == 1):
            tts = gTTS(text='Jag valde också sten, så det blev lika!', lang='sv')
            tts.save("Ljudfiler/iChoseX.mp3")
            self.playSound("Ljudfiler/iChoseX.mp3")
        elif(sign == 1 and user == 2):
            tts = gTTS(text='Jag valde sten, så då vann jag!', lang='sv')
            currentLosses += 1
            FileHandler().append(self.name, 'losses', str(currentLosses))
            tts.save("Ljudfiler/iChoseX.mp3")
            self.playSound("Ljudfiler/iChoseX.mp3")
            ArduinoHandler().write(b'e')
            time.sleep(4)
            ArduinoHandler().write(b'R')
        elif(sign == 1 and user == 3):
            tts = gTTS(text='Jag valde sten, så du vann, grattis!', lang='sv')
            currentWins += 1
            FileHandler().append(self.name, 'wins', str(currentWins))
            tts.save("Ljudfiler/iChoseX.mp3")
            self.playSound("Ljudfiler/iChoseX.mp3")
        elif(sign == 2 and user == 1):
            tts = gTTS(text='Jag valde sax, så du vann, grattis!', lang='sv')
            currentWins += 1
            FileHandler().append(self.name, 'wins', str(currentWins))
            tts.save("Ljudfiler/iChoseX.mp3")
            self.playSound("Ljudfiler/iChoseX.mp3")
        elif (sign == 2 and user == 2):
            tts = gTTS(text='Jag valde också sax, så det blev lika!', lang='sv')
            tts.save("Ljudfiler/iChoseX.mp3")
            self.playSound("Ljudfiler/iChoseX.mp3")
        elif (sign == 2 and user == 3):
            tts = gTTS(text='Jag valde sax, så då vann jag!', lang='sv')
            currentLosses += 1
            FileHandler().append(self.name, 'losses', str(currentLosses))
            tts.save("Ljudfiler/iChoseX.mp3")
            self.playSound("Ljudfiler/iChoseX.mp3")
            ArduinoHandler().write(b'e')
            time.sleep(4)
            ArduinoHandler().write(b'R')
        elif (sign == 3 and user == 1):
            tts = gTTS(text='Jag valde påse, så då vann jag!', lang='sv')
            currentLosses += 1
            FileHandler().append(self.name, 'losses', str(currentLosses))
            tts.save("Ljudfiler/iChoseX.mp3")
            self.playSound("Ljudfiler/iChoseX.mp3")
            ArduinoHandler().write(b'e')
            time.sleep(4)
            ArduinoHandler().write(b'R')
        elif(sign == 3 and user == 2):
            tts = gTTS(text='Jag valde påse, så du vann, grattis!', lang='sv')
            currentWins += 1
            FileHandler().append(self.name, 'wins', str(currentWins))
            tts.save("Ljudfiler/iChoseX.mp3")
            self.playSound("Ljudfiler/iChoseX.mp3")
        elif (sign == 3 and user == 3):
            tts = gTTS(text='Jag valde också påse, så det blev lika!', lang='sv')
            tts.save("Ljudfiler/iChoseX.mp3")
            self.playSound("Ljudfiler/iChoseX.mp3")

    def playAgain(self):
        self.funcName = "playAgain"
        tts = gTTS(text='Vill du spela igen?', lang='sv')  # Ta bort efter första inspelning
        tts.save("Ljudfiler/playAgain.mp3")
        self.playSound("Ljudfiler/playAgain.mp3")

        play_again_answer = self.listenSpeech(3)
        answer = self.recognizedAudio(play_again_answer)
        if self.keywordRecognition(answer, 'ja'):
            tts = gTTS(text='Vad kul, ' + self.name, lang='sv')               # Ta bort efter första inspelning
            tts.save("Ljudfiler/fun.mp3")
            self.playSound("Ljudfiler/fun.mp3")
            self.startRPSVoice()
        elif self.keywordRecognition(answer, 'nej'):
            tts = gTTS(text='Okej, vi kan spela mer en annan gång', lang='sv') # Ta bort efter första inspelning
            tts.save("Ljudfiler/playAnotherTime.mp3")
            self.playSound("Ljudfiler/playAnotherTime.mp3")
            self.whatToDo()
        elif self.keywordRecognition(answer, 'upprepa'):
            tts = gTTS(text='Okej, vi tar det igen', lang='sv') # Ta bort efter första inspelning
            tts.save("Ljudfiler/takeItAgain.mp3")
            self.playSound("Ljudfiler/takeItAgain.mp3")
            self.playAgain()
        else:
            self.didntUnderstand()
            self.playAgain()

    def playRPSPhrases(self):
        self.funcName = "playRPSPhrases"
        self.counterRPS += 1
        currentWins = FileHandler().read(self.name, 'wins')
        if (currentWins == ""):
            currentWins = 0
        else:
            currentWins = int(currentWins)

        currentLosses = FileHandler().read(self.name, 'losses')
        if (currentLosses == ""):
            currentLosses = 0
        else:
            currentLosses = int(currentLosses)
        print('In playRPSPhrases')
        #if (("users/" + self.name + ".json")):
        #tts1 = gTTS(text='Kul att du vill spela med mig igen! Du har vunnit ' + str(currentWins) + ' , och jag har vunnit ' + str(currentLosses), lang='sv')

        if (self.counterRPS % 2 == 1):
            self.currentScoreRPS(currentWins, currentLosses)

        if(currentWins == 0 and currentLosses == 0 and not self.playedRPSBefore):
                self.playedRPSBefore = True
                tts = gTTS(text='Det här är vår första match, spännande!', lang='sv')
                tts.save("Ljudfiler/firstGame.mp3")
                self.playSound("Ljudfiler/firstGame.mp3")


        nr = random.randint(1, 10)
        if(nr == 1):
            tts = gTTS(text='Passa dig, ' + self.name + ', jag känner mig vass idag!', lang='sv')
        elif(nr == 2):
            tts = gTTS(text='Jag märker om du fuskar ' + self.name + '!', lang='sv')
        elif(nr == 3):
            tts = gTTS(text='Jag är olympisk mästare på sten sax påse', lang='sv')
        elif(nr == 4):
            tts = gTTS(text='Hoppas du har dina tur-strumpor på dig idag!', lang='sv')
        elif(nr == 5):
            tts = gTTS(text='Tvinga mig inte att krossa dig', lang='sv')
        else:
            tts = gTTS(text='Nu spelar vi!', lang='sv')
        tts.save("Ljudfiler/RPSPhrase.mp3")
        self.playSound("Ljudfiler/RPSPhrase.mp3")

    def currentScoreRPS(self, currentWins, currentLosses):
        nr = random.randint(1,2)
        if nr == 1:
            tts = gTTS(text='Du har vunnit ' + str(currentWins) + ' , och jag har vunnit ' + str(currentLosses), lang='sv')
            if (currentWins > currentLosses):
                tts = gTTS(text='Du leder!', lang='sv')
                tts.save("Ljudfiler/youAreWinning.mp3")
                self.playSound("Ljudfiler/youAreWinning.mp3")
            elif (currentWins < currentLosses):
                tts = gTTS(text='Jag leder!', lang='sv')
                tts.save("Ljudfiler/youAreLoosing.mp3")
                self.playSound("Ljudfiler/youAreLoosing.mp3")
                # else:
                #    tts = gTTS(text='wow, det står lika, detta blir spännande!', lang='sv')
                #    tts.save("Ljudfiler/weAreEven.mp3")
                #    self.playSound("Ljudfiler/weAreEven.mp3")
        elif nr == 2:
            if currentWins > currentLosses:
                tts = gTTS(text='Ställningen är ' + str(currentWins) + ' ' + str(currentLosses) + ' till dig',
                           lang='sv')
            elif currentLosses > currentWins:
                tts = gTTS(text='Ställningen är ' + str(currentLosses) + ' ' + str(currentWins) + ' till mig',
                           lang='sv')
            elif currentLosses == currentWins:
                tts = gTTS(text='Ställningen är ' + str(currentWins) + ' ' + str(currentLosses),
                           lang='sv')


        tts.save("Ljudfiler/existingUserRPS.mp3")
        self.playSound("Ljudfiler/existingUserRPS.mp3")


    def startSchedule(self):
        # Switch from face screen to schedule screen
        self.funcName = "startSchedule"
        FileHandler().append(self.name, 'screen', 'schedule')
        
        tts = gTTS(text='Du kan välja att klicka på pilarna eller säga nästa eller förra för att byta mellan olika veckor.', lang='sv')
        tts.save('Ljudfiler/schedule_instruction.mp3')
        self.playSound('Ljudfiler/schedule_instruction.mp3')
        self.switchSchedule()

    def switchSchedule(self):
        audio = self.listenSpeech(4)
        answer = self.recognizedAudio(audio)

        self.overallKeyword(answer)

        if self.keywordRecognition(answer, 'nästa'):
            self.nextWeek()
        elif self.keywordRecognition(answer, 'förra'):
            self.lastWeek()
        elif self.keywordRecognition(answer, 'upprepa'):
            self.startSchedule()

    def nextWeek(self):
        current_screen = FileHandler().readScreen(self.name)
        print('Skärmen i filehandler:' + current_screen)
        if current_screen == 'schedule':
            FileHandler().append(self.name, 'screen', 's2')
        elif current_screen == 's2':
            FileHandler().append(self.name, 'screen', 's3')
        elif current_screen == 's3':
            FileHandler().append(self.name, 'screen', 's4')
        elif current_screen == 's4':
            FileHandler().append(self.name, 'screen', 's5')
        elif current_screen == 's5':
            FileHandler().append(self.name, 'screen', 's6')
        elif current_screen == 's6':
            tts = gTTS(text= 'Du är på sista veckan.')
        time.sleep(3)
        self.switchSchedule()

    def lastWeek(self):
        current_screen = FileHandler().readScreen(self.name)
        if current_screen == 'schedule':
            tts = gTTS(text= 'Du är på första veckan.')
        elif current_screen == 's2':
            FileHandler().append(self.name, 'screen', 'schedule')
        elif current_screen == 's3':
            FileHandler().append(self.name, 'screen', 's2')
        elif current_screen == 's4':
            FileHandler().append(self.name, 'screen', 's3')
        elif current_screen == 's5':
            FileHandler().append(self.name, 'screen', 's4')
        elif current_screen == 's6':
            FileHandler().append(self.name, 'screen', 's5')
        time.sleep(3)
        self.switchSchedule()

    
    def subtraction(self, first_term, second_term):
        return first_term - second_term


    def addition(self, first_term, second_term):
        return first_term + second_term


    def multiplication(self, first_term, second_term):
        return first_term * second_term

    def division(self, first_term, second_term):
        
        if((first_term % second_term) != 0):

            heltal = int(first_term / second_term)
            rest = Fraction(first_term % second_term)
            
            ttsMathDivFrac = gTTS(text=str(heltal) + "och" + str(rest) + "över" + str(second_term), lang='sv')
            ttsMathDivFrac.save("Ljudfiler/MathDivFrac.mp3")
            self.playSound("Ljudfiler/MathDivFrac.mp3")
            return
        else:
            ttsMathDiv = gTTS(text=str(int(first_term / second_term)), lang='sv')
            ttsMathDiv.save("Ljudfiler/answerDivisionInteger.mp3")
            self.playSound("Ljudfiler/answerDivisionInteger.mp3")
            return 
        


    def findNumbers(self, str_input):
        temporary = list()
        i = 0
        temporary2 = []

        while i < len(str_input):
            if str_input[i].isdigit():
              temporary2.append(str_input[i])
            elif temporary2:
              temporary.append("".join(temporary2))
              temporary2 = []
            i = i + 1
            if i == len(str_input) and temporary2:
                temporary.append("".join(temporary2))
        print(temporary)
        return temporary


    def startMath(self):
        FileHandler().append(self.name, 'screen','mathvoicescreen')
        self.funcName = "startMath"
        print("mathtest start")
        ttsMath1 = gTTS(text='Vad vill du räkna?', lang='sv')
        ttsMath1.save("Ljudfiler/newCount.mp3")
        self.playSound("Ljudfiler/newCount.mp3")
        audio = self.listenSpeech(8)
        str_input = self.recognizedAudio(audio)
        print(str_input)

        temp = list()
        temp.extend(self.findNumbers(str_input))

        if len(temp) < 2:
            ttsMath2 = gTTS(text='Fler siffror tack.', lang='sv')
            ttsMath2.save("Ljudfiler/tooFewNumbers.mp3")
            self.playSound("Ljudfiler/tooFewNumbers.mp3")
            self.startMath()

        if len(temp) > 2:
            ttsMath3 = gTTS(text='Bara två siffror tack.', lang='sv')
            ttsMath3.save("Ljudfiler/fewerNumbersPlease.mp3")
            self.playSound("Ljudfiler/fewerNumbersPlease.mp3")
            self.startMath()

        first_term = int(temp[0])
        second_term = int(temp[1])

        operator_count = 0
        operator_input = str_input.lower()
        print(operator_input)
        operators = {
            'PLUS' : ["addera", "+"],
            'MINUS': ["minus", "-"],
            'MULTIPLIKATION' : ["gånger", "multiplicerat", "*"],
            'DIVISION' : ["delat", "dividerat", "/"]
        }

        actual_operator = None
        for operator, synonyms in operators.items():
            count = 0
            for synonym in synonyms:
                count += operator_input.count(synonym)
            if count > 0:
                actual_operator = operator
            operator_count += count
        #FileHandler().append(self.name, 'screen', 'smartscreen')

        if operator_count > 1:
            ttsMath4 = gTTS(text='Bara ett räknesätt tack.', lang='sv')
            ttsMath4.save("Ljudfiler/tooManyOperators.mp3")
            self.playSound("Ljudfiler/tooManyOperators.mp3")
        elif operator_count < 1:
            ttsMath5 = gTTS(text='Bestäm ett räknesätt.', lang='sv')
            ttsMath5.save("Ljudfiler/tooFewOperators.mp3")
            self.playSound("Ljudfiler/tooFewOperators.mp3")

        if actual_operator == 'MINUS':
            ttsMath6 = gTTS(text=str(self.subtraction(first_term, second_term)), lang='sv')
            ttsMath6.save("Ljudfiler/answerSubtraction.mp3")
            self.playSound("Ljudfiler/answerSubtraction.mp3")
            
        elif actual_operator == 'PLUS':
            ttsMath7 = gTTS(text=str(self.addition(first_term, second_term)), lang='sv')
            ttsMath7.save("Ljudfiler/answerAddition.mp3")
            self.playSound("Ljudfiler/answerAddition.mp3")
        elif actual_operator == 'MULTIPLIKATION':
            ttsMath8 = gTTS(text=str(self.multiplication(first_term, second_term)), lang='sv')
            ttsMath8.save("Ljudfiler/answerMultiplication.mp3")
            self.playSound("Ljudfiler/answerMultiplication.mp3")
            print(self.multiplication(first_term, second_term))
        elif actual_operator == 'DIVISION':
            self.division(first_term, second_term)
        else:
            ttsMath10 = gTTS(text='Försök igen med två siffror och en operator.', lang='sv')
            ttsMath10.save("Ljudfiler/tryAgainMath.mp3")
            self.playSound("Ljudfiler/tryAgainMath.mp3")
            self.startMath()
            
        tts = gTTS(text='Vill du räkna ett tal till?', lang='sv')
        tts.save("Ljudfiler/countAgain.mp3")
        self.playSound("Ljudfiler/countAgain.mp3")

        audio2 = self.listenSpeech(3)
        answer = self.recognizedAudio(audio2)

        if self.keywordRecognition(answer, 'ja'):
            self.startMath()
        elif self.keywordRecognition(answer, 'nej'):
            self.whatToDo()
        else:
            self.didntUnderstand()
            self.startMath()
   
