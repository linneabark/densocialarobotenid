#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
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

from FileController import FileHandler

class SpeechController():
    def __init__(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.funcName = ""
        self.speaking = False
        self.name = ""
        self.manager = ""


    def stringSplitter(self, string):
        if(string == None):
            return [""]
        stringArray = string.split()
        i = 0
        for x in stringArray:
            stringArray[i] = stringArray[i].lower()
            i += 1
        return stringArray

    def speakingFalse(self):
        self.speaking = False
        
    def playSound(self, fileName):
        FileHandler().append(self.name,"screen","talkingscreen")
        self.speaking = True
        audio = MP3(fileName)
        length = audio.info.length
        mixer.init()
        mixer.music.load(fileName)
        mixer.music.play()
        time.sleep(length-0.05)
        self.speaking = False
        FileHandler().append(self.name, "screen", "main")
        
    
    def mp3Exception(self):
        tts = gTTS(text= 'MP3, kan du prata tydligare?', lang='sv')
        tts.save("Ljudfiler/speakClear.mp3")
        self.playSound("Ljudfiler/speakClear.mp3")
        self.fromWhatFunc()
        

    def fromWhatFunc(self):
        print("Function name: ", self.funcName)
        if(self.funcName == "listenForTim"):
            self.listenForTim()
        if(self.funcName == "playHello"):
            self.playHello()
        elif(self.funcName == "handleKeywords"):
            self.handleKeywords()
        elif(self.funcName == "startTalking"):
            self.startTalking()
        elif(self.funcName == "startRPSVoice"):
            self.startRPSVoice()
        elif (self.funcName == "goodbye"):
            self.goodbye()
        elif (self.funcName == "haveYouPlayed"):
            self.haveYouPlayed()
        elif (self.funcName == "handleKeyword"):
            self.handleKeyword()
        elif (self.funcName == "handleTalkKeyword"):
            self.handleTalkKeyword()
        elif (self.funcName == "askQuestion"):
            self.askQuestion()
        elif (self.funcName == "wantToHearAJoke"):
            self.wantToHearAJoke()
        elif (self.funcName == "wantToContinueTalking"):
            self.wantToContinueTalking()
        elif (self.funcName == "postJoke"):
            self.postJoke()
        elif (self.funcName == "postTalk"):
            self.postTalk()
        elif (self.funcName == "playerChoice"):
            self.playerChoice()
        elif (self.funcName == "playRPSPhrases"):
            self.playRPSPhrases()
        elif (self.funcName == "start_Schedule"):
            self.start_Schedule()
        elif (self.funcName == "startMath"):
            self.startMath()
        elif (self.funcName == "help"):
            self.help()

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
            self.overallKeyword(string)
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
        self.playSound("Ljudfiler/startRecording.mp3")
        with self.m as source:
            #audio = r.record(source, duration = 5)
            mixer.init()
            audio = self.r.listen(source, phrase_time_limit=time)
            self.playSound("Ljudfiler/stopRecording.mp3")
            return audio
            #self.tryListen(audio)

    def goodbye(self):  # Lägg till personliga fraser
        self.funcName = "goodbye"
        tts = gTTS(text='Vill du verkligen säga hejdå?', lang='sv')
        tts.save("Ljudfiler/goodbye.mp3")
        self.playSound("Ljudfiler/goodbye.mp3")

        audio = self.listenSpeech(5)
        answer = self.recognizedAudio(audio)

        if(answer == "ja"):
            tts = gTTS(text='Okej, det var kul att leka med dig. Ses snart igen!', lang='sv')
            tts.save("Ljudfiler/goodbyeSleep.mp3")
            self.playSound("Ljudfiler/goodbyeSleep.mp3")
            FileHandler().append(self.name,"screen","sleep")
        elif(answer == "nej"):
            tts = gTTS(text='Okej, då fortsätter vi leka!', lang='sv')
            tts.save("Ljudfiler/okKeepPlaying.mp3")
            self.playSound("Ljudfiler/okKeepPlaying.mp3")
            self.fromWhatFunc()
        elif(answer == "avsluta"):
            sys.exit()
        else:
            self.didntUnderstand()
            self.goodbye()


    def containsHiMyAndName(self, stringArray):
        if any(("hej" in s for s in stringArray) and ("kim" in s for s in stringArray) and ("heter" in s for s in stringArray)):
               return True
        return False

    def detectName(self, stringArray):
        namePos = stringArray.index("heter") + 1
        self.name = stringArray[namePos]
        return self.name

   
    def listenForTim(self):
        self.funcName = "listenForTim"
        print('Listen for Tim')
        audio = self.listenSpeech(5)
        string = self.recognizedAudio(audio)
        if(string == None):
            return
        stringArray = self.stringSplitter(string)
        print(stringArray)
        if(self.containsHiMyAndName(stringArray)):
            self.name = self.detectName(stringArray)
            FileHandler().create(self.name)
            print('Familiar user')
            return "familiarUser"
        elif any("hej" in s for s in stringArray):
            return "hej"
        elif any("spela" in s for s in stringArray):
            self.startRPSVoice()
        elif any("prata" in s for s in stringArray):
            self.smallTalk()
                   
    def playHelloName(self, name):
        if(name == None):
            name = ""
        FileHandler().create(name)
        self.name = name
        self.helloPhrasesFamiliarUser(self.name) # Skicka in bara "name"?
        self.whatToDo()

    def helloPhrasesFamiliarUser(self, name):
        nr = random.randint(1, 4)

        if (nr == 10): # Om aktuell user har en sport i sin json-fil
            nr = 5
            sport = "fotboll" # Välj sporten från json-filen
        if (nr == 1):
            tts = gTTS(text='Hej' + name + ', vad vill du göra?', lang='sv')
        elif (nr == 2):
            tts = gTTS(text = 'Tjena' + name + 'vad vill du hitta på idag?', lang ='sv')
        elif (nr == 3):
            tts = gTTS(text='Vad kul att träffa dig ' + name + ', nu ska vi leka!', lang='sv')
        elif (nr == 4):
            tts = gTTS(text=name + ', det var ett fint namn!', lang='sv')
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

        if (answer == "ja"):
            tts = gTTS(text='Vad kul! Jag älskar ' + sport)
            tts.save("Ljudfiler/iLoveX.mp3")
            self.playSound("Ljudfiler/iLoveX.mp3")
        elif (answer == "nej"):
            tts = gTTS(text='Okej, hoppas du får spela det snart')
            tts.save("Ljudfiler/hopeToPlaySoon.mp3")
            self.playSound("Ljudfiler/hopeToPlaySoon.mp3")
        else:
            self.didntUnderstand()

    def playHello(self):
        self.funcName = "playHello"
        self.helloPhrasesFamiliarUser()
        audio = self.listenSpeech(4)
        answer = self.recognizedAudio(audio)
        self.playHelloName(answer)

    def helloPhrasesUnknownUser(self):
        nr = random.randint(1,4)

        if (nr == 1):
            tts = gTTS(text='Hej! Jag heter Kim, vad heter du?', lang='sv')
        if (nr == 2):
            tts = gTTS(text='Tjena polare! Mitt namn är Kim, vad är ditt?', lang='sv')
        if (nr == 3):
            tts = gTTS(text='Äntligen någon som vill leka! Jag heter Kim, kan du berätta vad du heter?', lang='sv')
        if (nr == 4):
            tts = gTTS(text='Hallå! Det är jag som är Kim, vad heter du?', lang='sv')

        tts.save("Ljudfiler/helloWhatsYourName.mp3")
        self.playSound("Ljudfiler/helloWhatsYourName.mp3")


    def whatToDo(self):
        self.funcName = "whatToDo"
        tts = gTTS(text='Vill du se schema, räkna matte, spela sten sax påse eller prata?', lang='sv')
        tts.save("Ljudfiler/whatToDo.mp3")
        self.playSound("Ljudfiler/whatToDo.mp3")
        audio = self.listenSpeech(4)
        answer = self.recognizedAudio(audio)
        if(answer == "upprepa"):
            self.whatToDo()
        else:
            self.handleKeyword(answer)


    def handleKeyword(self, message):
        self.funcName = "handleKeyword"
        keywords = self.stringSplitter(message)
        print("keywords: ", keywords)

        if any(("schema" in s for s in keywords) or ("kalender" in s for s in keywords)):
            self.start_Schedule()
            x=1
        elif any(("räkna" in s for s in keywords) or ("matte" in s for s in keywords)):
            self.startMath()
        elif any(("sten" in s for s in keywords) or ("sax" in s for s in keywords) or ("påse" in s for s in keywords) or ("spela" in s for s in keywords)):
            print('Startar RPS')
            self.startRPSVoice()
        elif any(("prata" in s for s in keywords)):
            self.startTalking()      #skicka till pratmetod
        elif any(("klocka" in s for s in keywords) or ("tid" in s for s in keywords)):
            x=1 #skicka till klockmetod
        elif any("hjälp" in s for s in keywords):
            x=1 #Skicka till infometod
        else:
            self.didntUnderstand()
            audio = self.listenSpeech(7)
            self.handleKeyword(self.recognizedAudio(audio))

    def overallKeyword(self, keyword):
        print('Overall keyword: ' + keyword)
        answer = self.stringSplitter(keyword)
        if any(("hejdå" in s for s in answer) or (
                ("hej" in s for s in answer) and ("då" in s for s in answer))):
            self.goodbye()
        elif (keyword == "tillbaka"):
            tts = gTTS(text='Okej, vi går tillbaka!', lang='sv')
            tts.save("Ljudfiler/goBack.mp3")
            self.playSound("Ljudfiler/goBack.mp3")
            self.whatToDo()
        elif (keyword == "hjälp"):
            self.help()
        elif (keyword == "klocka"):
            self.whatTime()
        elif (keyword == "app"):
            x=1 # Starta gui
        elif (keyword == "paus"):
            x=1 # Pausa interaktion
        elif(keyword == 'avsluta'):
            print('AVSLUTA')
            sys.exit('Shutting down from SC')
            print('After shut down from SC')


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

        if (answer == "upprepa"):
            self.help()

    def whatTime(self):
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute

        tts = gTTS(text='Klockan är ' + hour + ' ' + minute, lang='sv') # Behöver testas!!
        tts.save("Ljudfiler/clock.mp3")
        self.playSound("Ljudfiler/clock.mp3")
        time.sleep(1)
        self.whatToDo()


    def didntUnderstand(self):
        nr = random.randint(1, 5)
        if(nr == 1):
            tts = gTTS(text='Jag förstod inte, kan du säga igen!', lang='sv')
        if(nr == 2):
            tts = gTTS(text='Kan du upprepa det där?', lang='sv')
        if(nr == 3):
            tts = gTTS(text='Jag har persilja i öronen, du får säga igen', lang='sv')
        if(nr == 4):
            tts = gTTS(text='Kan du prata tydligare', lang='sv')
        if(nr == 5):
            tts = gTTS(text='Kan du upprepa', lang='sv')

        tts.save("Ljudfiler/didntUnderstand1.mp3")
        self.playSound("Ljudfiler/didntUnderstand1.mp3")


    def startTalking(self):
        self.funcName = "startTalking"
        tts = gTTS(text='Kul att du vill prata!', lang='sv')
        tts.save("Ljudfiler/whatToTalkAbout.mp3")
        self.playSound("Ljudfiler/whatToTalkAbout.mp3")
        self.smallTalk()

    def handleTalkKeyword(self, message):
        self.funcName = "handleTalkKeyword"
        keywords = self.stringSplitter(message)

        if any("skämt" in s for s in keywords):
            self.joke()        #Gå till skämtmetod
        elif any(("småprata" in s for s in keywords) or ("prata" in s for s in keywords)):
            self.smallTalk() #Gå till småpratmetod
        else:
            self.didntUnderstand()
            audio = self.listenSpeech(4)
            self.handleTalkKeyword(self.recognizedAudio(audio))

    def whatColor(self,string):
        #eventuellt kolla efter rött, blått etc.
        print(string)
        string = string.lower()
        if string == "röd":
            tts = gTTS(text='Ja, röd som tomater och kärleken!', lang='sv')
        elif string == "blå":
            tts = gTTS(text='Det är också min favoritfärg!', lang='sv')
        elif string == "gul":
            tts = gTTS(text='Gult rimmar med fult!', lang='sv')
        elif string == "grön":
            tts = gTTS(text='åh vad härligt, som en sommaräng!', lang='sv')
        elif string == "rosa":
            tts = gTTS(text='åh, nu blev jag sugen på sockervadd!', lang='sv')
        elif string == "brun":
            tts = gTTS(text='Är du helt säker på det, då ser det ju ut som... Chokladmousse!', lang='sv')
        elif string == "lila":
            tts = gTTS(text='Ja det är fint!', lang='sv')
        else:
            tts = gTTS(text='fin färg!', lang='sv')

        tts.save("Ljudfiler/favoriteColors.mp3")
        self.playSound("Ljudfiler/favoriteColors.mp3")
            

    def askQuestion(self, tts):
        self.funcName = "askQuestion"
        tts.save("Ljudfiler/askQuestion.mp3")
        self.playSound("Ljudfiler/askQuestion.mp3")
        audio = self.listenSpeech(4)
        string = self.recognizedAudio(audio)
        return string
    
    def smallTalk(self):
        #question = random.randint(1,5)
        question = 2
        if question == 1:
            tts = gTTS(text='Hur gammal är du?', lang='sv')
            string = self.askQuestion(tts)
            FileHandler().append(self.name,"age",string)
            
        elif question == 2:
            tts = gTTS(text='Vilken är din favoritfärg?', lang='sv')
            string = self.askQuestion(tts)
            self.whatColor(string)
            FileHandler().append(self.name, "color", string)

        elif question == 3:
            tts = gTTS(text='Vilken är din favoritsport?', lang='sv')
            string = self.askQuestion(tts)
            FileHandler().append(self.name, "sport", string)

        elif question == 4:
            self.wantToHearAJoke()

        elif question == 5:
            self.wantToContinueTalking()

        self.smallTalk()

    def wantToHearAJoke(self):
        self.funcName = "wantToHearAJoke"
        tts = gTTS(text='Vill du höra ett skämt?', lang='sv')
        tts.save("Ljudfiler/wantToHearAJoke.mp3")
        self.playSound("Ljudfiler/wantToHearAJoke.mp3")

        audio = self.listenSpeech(3)
        answer = self.recognizedAudio(audio)

        if(answer == "ja"):
            self.joke()
        elif(answer == "nej"):
            tts = gTTS(text='Okej, då slipper du.', lang='sv')
            tts.save("Ljudfiler/ok.mp3")
            self.playSound("Ljudfiler/ok.mp3")
        else:
            self.didntUnderstand()
            self.wantToHearAJoke()

    def wantToContinueTalking(self):
        self.funcName = "wantToContinueTalking"
        tts = gTTS(text='Vill du fortsätta prata eller göra något annat?', lang='sv')
        tts.save("Ljudfiler/wantToContinueTalking.mp3")
        self.playSound("Ljudfiler/wantToContinueTalking.mp3")

        audio = self.listenSpeech(3)
        answer = self.recognizedAudio(audio)

        if (answer == "ja"):
            self.smallTalk()
        elif (answer == "nej"):
            tts = gTTS(text='Okej, då gör vi något annat', lang='sv')
            tts.save("Ljudfiler/okLetsDoSomethingElse.mp3")
            self.playSound("Ljudfiler/okLetsDoSomethingElse.mp3")
        else:
            self.didntUnderstand()
            self.whatToDo()

    def joke(self):
        self.funcName = "joke"
        nr = random.randint(1, 5)
        if (nr == 1):
            tts = gTTS(text='Det var en gång en dansk, en norsk och Bellman som skulle tävla om vem som kunde vara inne i en svinstia i längst tid.'
                            'Först gick dansken in, men efter en minut kom han ut och stönade: Grisen fes!'
                            'Då gick norsken in och efter två minuter kom han ut, grön i ansiktet och stönade: Grisen fes!'
                            'Sedan var det Bellmans tur att gå in i svinstian. Efter tio minuter kom grisen ut och stönade: Bellman fes!', lang='sv')
        if (nr == 2):
            tts1 = gTTS(text = 'Vet du vad man får om man korsar en giraff och en igelkott? ')
            tts1.save("Ljudfiler/firstPartofJoke.mp3")
            self.playSound("Ljudfiler/firstPartofJoke.mp3")
            time.sleep(1)
            tts = gTTS(text = 'En tre meter lång tandborste!')
        if (nr == 3):
            tts = gTTS(text = 'Pappa frågar sin dotter, ser du bra med dina nya glasögon? Dotten svarade, visst mamma!')
        if (nr == 4):
            tts1 = gTTS(text='Vad sa marsgubbarna när de landade på jorden?')
            tts1.save("Ljudfiler/firstPartofJoke.mp3")
            self.playSound("Ljudfiler/firstPartofJoke.mp3")
            time.sleep(1)
            tts = gTTS(text = 'Hej jordgubbar!')
        if (nr == 5):
            tts1 = gTTS(text='Vad är en groda utan ben?')
            tts1.save("Ljudfiler/firstPartofJoke.mp3")
            self.playSound("Ljudfiler/firstPartofJoke.mp3")
            time.sleep(1)
            tts = gTTS(text='Hopplös!')

        tts.save("Ljudfiler/joke.mp3")
        self.playSound("Ljudfiler/joke.mp3")
        self.playSound("Ljudfiler/drumroll.mp3")   #Dab?

        self.postJoke()


    def postJoke(self):
        self.funcName = "postJoke"
        tts = gTTS(text='Vill du höra ett till skämt, fortsätta prata eller göra något annat?', lang='sv')
        tts.save("Ljudfiler/somethingElse.mp3")
        self.playSound("Ljudfiler/somethingElse.mp3")

        audio = self.listenSpeech(4)
        answer = self.recognizedAudio(audio)

        if (answer == "upprepa"):
            self.postJoke()
        else:
            self.postTalk(answer)

    def postTalk(self, message):
        self.funcName = "postTalk"
        keywords = self.stringSplitter(message)

        if any("skämt" in s for s in keywords):
            self.joke()
        elif any("prata" in s for s in keywords):
            self.smallTalk()
        elif any("annat" in s for s in keywords):
            self.whatToDo()
        else:
            self.didntUnderstand()
            audio = self.listenSpeech(4)
            self.postTalk(self.recognizedAudio(audio))


    def startRPSVoice(self):
        print('In startRPSVoice')
        self.funcName = "startRPSVoice"
        self.playRPSPhrases()
        print('After playRPSPhrases')
        tts1 = gTTS(text='Är du redo?', lang='sv')
        tts1.save("Ljudfiler/newReady.mp3")
        self.playSound("Ljudfiler/newReady.mp3")
        #time.sleep(3)
        audio = self.listenSpeech(5)
        answer = self.recognizedAudio(audio)
        if(answer == "ja"):
            tts2 = gTTS(text='Sten, sax, påse!', lang='sv')
            tts2.save("Ljudfiler/stenSaxPase.mp3")
            self.playSound("Ljudfiler/stenSaxPase.mp3")
            sign = random.randint(1, 3)
            print("sign:", sign)
            user = self.playerChoice()
            self.rockPaperScissors(sign,user)
            self.playAgain()
        elif(answer == "nej"):
            self.startRPSVoice()
        elif(answer == "tillbaka"):
            tts3 = gTTS(text='Okej, vi går tillbaka', lang='sv')  # Ta bort efter första inspelning
            tts3.save("Ljudfiler/goBack.mp3")
            self.playSound("Ljudfiler/goBack.mp3")
            self.whatToDo()
        elif(answer == "upprepa"):
            self.startRPSVoice()
        else:
            tts2 = gTTS(text='Jag förstod inte, vi testar igen!', lang='sv')  # Ta bort efter första inspelning
            tts2.save("Ljudfiler/tryAgain.mp3")
            self.playSound("Ljudfiler/tryAgain.mp3")
            self.startRPSVoice()

    def playerChoice(self):
        self.funcName = "playerChoice"
        tts1 = gTTS(text='Vad valde du?', lang='sv')
        tts1.save("Ljudfiler/playerChoice.mp3")
        self.playSound("Ljudfiler/playerChoice.mp3")
        audio = self.listenSpeech(3)
        answer = self.recognizedAudio(audio)
        if (answer == "sten"):
            return 1
        elif (answer == "sax"):
            return 2
        elif (answer == "påse"):
            return 3
        else:
            tts1 = gTTS(text='Jag förstod inte vad du sa, vi tar det igen.', lang='sv')
            tts1.save("Ljudfiler/playerChoiceUnclear.mp3")
            self.playSound("Ljudfiler/playerChoiceUnclear.mp3")
            self.playerChoice()
        
    def rockPaperScissors(self, sign, user):
        currentWins = FileHandler().read(self.name, "wins")
        if (currentWins == ""):
            currentWins = 0
        else:
            currentWins = int(currentWins)

        currentLosses = FileHandler().read(self.name, "losses")
        if (currentLosses == ""):
            currentLosses = 0
        else:
            currentLosses = int(currentLosses)
        
        if(sign == 1 and user == 1):
            tts = gTTS(text='Jag valde också sten, så det blev lika!', lang='sv')
        elif(sign == 1 and user == 2):
            tts = gTTS(text='Jag valde sten, så då vann jag!', lang='sv')
            currentLosses += 1
            FileHandler().append(self.name, "losses", str(currentLosses))
        elif(sign == 1 and user == 3):
            tts = gTTS(text='Jag valde sten, så du vann, grattis!', lang='sv')
            currentWins += 1
            FileHandler().append(self.name, "wins", str(currentWins))
        elif(sign == 2 and user == 1):
            tts = gTTS(text='Jag valde sax, så du vann, grattis!', lang='sv')
            currentWins += 1
            FileHandler().append(self.name, "wins", str(currentWins))
        elif (sign == 2 and user == 2):
            tts = gTTS(text='Jag valde också sax, så det blev lika!', lang='sv')
        elif (sign == 2 and user == 3):
            tts = gTTS(text='Jag valde sax, så då vann jag!', lang='sv')
            currentLosses += 1
            FileHandler().append(self.name, "losses", str(currentLosses))
        elif (sign == 3 and user == 1):
            tts = gTTS(text='Jag valde också påse, så då vann jag!', lang='sv')
            currentLosses += 1
            FileHandler().append(self.name, "losses", str(currentLosses))
        elif(sign == 3 and user == 2):
            tts = gTTS(text='Jag valde påse, så du vann, grattis!', lang='sv')
            currentWins += 1
            FileHandler().append(self.name, "wins", str(currentWins))
        elif (sign == 3 and user == 3):
            tts = gTTS(text='Jag valde också påse, så det blev lika!', lang='sv')
        tts.save("Ljudfiler/iChoseX.mp3")
        self.playSound("Ljudfiler/iChoseX.mp3")

    def playAgain(self):
        tts = gTTS(text='Vill du spela igen?', lang='sv')  # Ta bort efter första inspelning
        tts.save("Ljudfiler/playAgain.mp3")
        self.playSound("Ljudfiler/playAgain.mp3")

        play_again_answer = self.listenSpeech(3)
        if(self.recognizedAudio(play_again_answer) == "ja"):
            tts = gTTS(text='Vad kul!', lang='sv')               # Ta bort efter första inspelning
            tts.save("Ljudfiler/fun.mp3")
            self.playSound("Ljudfiler/fun.mp3")
            self.startRPSVoice()
        elif (self.recognizedAudio(play_again_answer) == "nej"):
            tts = gTTS(text='Okej, vi kan spela mer en annan gång', lang='sv') # Ta bort efter första inspelning
            tts.save("Ljudfiler/playAnotherTime.mp3")
            self.playSound("Ljudfiler/playAnotherTime.mp3")
            self.whatToDo()
        elif(self.recognizedAudio(play_again_answer) == "upprepa"):
            tts = gTTS(text='Okej, vi tar det igen', lang='sv') # Ta bort efter första inspelning
            tts.save("Ljudfiler/takeItAgain.mp3")
            self.playSound("Ljudfiler/takeItAgain.mp3")
            self.playAgain()
        else:
            self.didntUnderstand()
            self.playAgain()

    def playRPSPhrases(self):
        self.funcName = "playRPSPhrases"
        print('In playRPSPhrases')
        nr = random.randint(1, 10)
        if(nr == 1):
            tts = gTTS(text='Passa dig, jag känner mig vass idag!', lang='sv')
        elif(nr == 2):
            tts = gTTS(text='Jag märker om du fuskar!', lang='sv')
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


    def start_Schedule(self):
        # Switch from face screen to schedule screen
        self.funcName = "start_Schedule"
        FileHandler().append(self.name,"screen","schedule")

        tts = gTTS(text='Här är ditt schema! Säg nästa vecka eller förra veckan för att byta vecka.', lang='sv')
        tts.save('Ljudfiler/schedule_instruction.mp3')
        self.playSound('Ljudfiler/schedule_instruction.mp3')
        audio = self.listenSpeech(4)
        string = self.recognizedAudio(audio)
        words = self.stringSplitter(string)

        if any("upprepa" in s for s in words):
            self.start_Schedule()
        

    
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
        self.funcName = "startMath"
        print("mathtest start")
        ttsMath1 = gTTS(text='Vad vill du räkna?', lang='sv')
        ttsMath1.save("Ljudfiler/newCount.mp3")
        self.playSound("Ljudfiler/newCount.mp3")
        audio = self.listenSpeech(7)
        str_input = self.recognizedAudio(audio)
        print(str_input)

        temp = list()
        temp.extend(self.findNumbers(str_input))

        if len(temp) < 2:
            ttsMath2 = gTTS(text='Fler siffror tack.', lang='sv')
            ttsMath2.save("Ljudfiler/tooFewNumbers.mp3")
            self.playSound("Ljudfiler/tooFewNumbers.mp3")

        if len(temp) > 2:
            ttsMath3 = gTTS(text='Bara två siffror tack.', lang='sv')
            ttsMath3.save("Ljudfiler/fewerNumbersPlease.mp3")
            self.playSound("Ljudfiler/fewerNumbersPlease.mp3")

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
            
        tts = gTTS(text='Vill du räkna ett tal till?', lang='sv')
        tts.save("Ljudfiler/countAgain.mp3")
        self.playSound("Ljudfiler/countAgain.mp3")

        audio2 = self.listenSpeech(3)
        answer = self.recognizedAudio(audio2)

        if (answer == "ja"):
            self.startMath()
        elif (answer == "nej"):
            self.whatToDo()
        else:
            self.didntUnderstand()
            self.startMath()
   
