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
from mathtest import MathVoice
from main import Manager, MainScreen
from FileController import FileHandler

class SpeechController():
    def __init__(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.funcName = ""
        self.speaking = False
        self.name = ""


    def stringSplitter(self, string):
        if(string == None):
            return [""]
        stringArray = string.split()
        i = 0
        for x in stringArray:
            stringArray[i] = stringArray[i].lower()
            i += 1
        return stringArray

    def playSound(self, fileName):
        self.speaking = True
        MainScreen.moveMouth()
        mixer.init()
        mixer.music.load(fileName)
        mixer.music.play()
        self.speaking = False
    
    def mp3Exception(self):
        tts = gTTS(text= 'Kan du prata tydligare?', lang='sv')
        tts.save("Ljudfiler/speakClear.mp3")
        self.playSound("Ljudfiler/speakClear.mp3")
        time.sleep(2)
        self.fromWhatFunc()
        

    def fromWhatFunc(self):
        print("Function name: ", self.funcName)
        '''if(self.funcName == "listenForTim"):
            self.listenForTim()'''
        if(self.funcName == "playHello"):
            self.playHello()
        elif(self.funcName == "handleKeywords"):
            self.handleKeywords()
        elif(self.funcName == "startTalking"):
            self.startTalking()
        elif(self.funcName == "startRPSVoice"):
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
        self.playSound("Ljudfiler/startRecording.mp3")
        with self.m as source:
            #audio = r.record(source, duration = 5)
            mixer.init()
            #while(mixer.get_busy()):
            #    print("hej")
            #if(mixer.Channel(1).get_busy()):
            #    print("Channel 1 busy")
            audio = self.r.listen(source, phrase_time_limit=time)
            self.playSound("Ljudfiler/stopRecording.mp3")
            return audio
            #self.tryListen(audio)

    def goodbye(self):  # Lägg till personliga fraser
        tts = gTTS(text='Vill du verkligen säga hejdå?', lang='sv')
        tts.save("Ljudfiler/goodbye.mp3")
        self.playSound("Ljudfiler/goodbye.mp3")

        audio = self.listenSpeech(5)
        answer = self.recognizedAudio(audio)

        if(answer == "ja"):
            tts = gTTS(text='Okej, det var kul att leka med dig. Ses snart igen!', lang='sv')
            tts.save("Ljudfiler/funToPlayWithYou.mp3")
            self.playSound("Ljudfiler/funToPlayWithYou.mp3")
            # Metod som stänger av
        elif(answer == "nej"):
            tts = gTTS(text='Okej, då fortsätter vi leka!', lang='sv')
            tts.save("Ljudfiler/continuePlay.mp3")
            self.playSound("Ljudfiler/continuePlay.mp3")
            time.sleep(3)
            self.fromWhatFunc()
        else:
            tts = gTTS(text='Säg igen', lang='sv')
            tts.save("Ljudfiler/sayAgain.mp3")
            self.playSound("Ljudfiler/sayAgain.mp3")
            self.goodbye()
           

    def containsHiMyAndName(self, stringArray):
        if any(("hej" in s for s in stringArray) and ("kim" in s for s in stringArray) and ("heter" in s for s in stringArray)):
               return True
        return False

    def detectName(self, stringArray):
        namePos = stringArray.index("heter") + 1
        self.name = stringArray[namePos]
        return self.name

   
    def listenForTim(self, manager):
        self.funcName = "listenForTim"
        audio = self.listenSpeech(5)
        string = self.recognizedAudio(audio)
        if(string == None):
            return
        stringArray = self.stringSplitter(string)
        print(stringArray)
        if(self.containsHiMyAndName(stringArray)):
                self.name = self.detectName(stringArray)
                FileHandler.create(self.name)
                print('Familiar user')
                return "familiarUser"
        elif any("hej" in s for s in stringArray):
                return "hej"
        elif any("spela" in s for s in stringArray):
            self.startRPSVoice()
                   
    def playHelloName(self, name):
        if(name == None):
            name = ""
        tts = gTTS(text= 'Hej' + name + 'vad vill du göra?', lang='sv')
        tts.save("Ljudfiler/helloWhatToDo.mp3")
        self.playSound("Ljudfiler/helloWhatToDo.mp3")
        self.whatToDo()


    def playHello(self):
        self.funcName = "playHello"
        tts = gTTS(text= 'Hej! Jag heter Kim, vad heter du?', lang='sv')
        tts.save("Ljudfiler/helloWhatsYourName.mp3")
        self.playSound("Ljudfiler/helloWhatsYourName.mp3")

        time.sleep(3)
        audio = self.listenSpeech(4)
        self.playHelloName(self.recognizedAudio(audio))



    def whatToDo(self):
        self.funcName = "whatToDo"
        time.sleep(1)
        tts = gTTS(text='Vill du se schema, räkna matte, spela sten sax påse eller prata?', lang='sv')
        tts.save("Ljudfiler/whatToDo.mp3")
        self.playSound("Ljudfiler/whatToDo.mp3")
        time.sleep(7)
        audio = self.listenSpeech(4)
        self.handleKeyword(self.recognizedAudio(audio))


    def handleKeyword(self, message):
        self.funcName = "handleKeyword"
        keywords = self.stringSplitter(message)
        print("keywords: ", keywords)

        if any(("schema" in s for s in keywords) or ("kalender" in s for s in keywords)):
            Manager.startSchedule()
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
        elif any("info" in s for s in keywords):
            x=1 #Skicka till infometod
        else:
            tts = gTTS(text='Kan du upprepa?', lang='sv')
            tts.save("Ljudfiler/didntUnderstand.mp3")
            self.playSound("Ljudfiler/didntUnderstand.mp3")

            audio = self.listenSpeech(7)
            self.handleKeyword(self.recognizedAudio(audio))

    def startTalking(self):
        self.funcName = "startTalking"
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
        question = random.randint(1,3)
        if question == 1:
            tts = gTTS(text='Hur gammal är du?', lang='sv')
            tts.save("Ljudfiler/howOld.mp3")
            self.playSound("Ljudfiler/howOld.mp3")
            time.sleep(3)
            audio = self.listenSpeech(4)
            string = self.recognizedAudio(audio)
            FileHandler().append(self.name,"age",string)
            
        elif question == 2:
            tts = gTTS(text='Vilken är din favoritfärg?', lang='sv')
            tts.save("Ljudfiler/favoriteColor.mp3")
            self.playSound("Ljudfiler/favoriteColor.mp3")
            time.sleep(3)
            audio = self.listenSpeech(4)
            string = self.recognizedAudio(audio)
            FileHandler().append(self.name, "color", string)

        elif question == 3:
            tts = gTTS(text='Vilken är din favoritsport?', lang='sv')
            tts.save("Ljudfiler/favoriteSport.mp3")
            self.playSound("Ljudfiler/favoriteSport.mp3")
            time.sleep(3)
            audio = self.listenSpeech(4)
            string = self.recognizedAudio(audio)
            FileHandler().append(self.name, "sport", string)

        tts = gTTS(text='Vill du fortsätta prata, höra ett skämt eller göra något annat?', lang='sv')
        tts.save("Ljudfiler/continueTalking.mp3")
        self.playSound("Ljudfiler/continueTalking.mp3")
        time.sleep(5)
        audio = self.listenSpeech(5)
        self.postTalk(self.recognizedAudio(audio))

    def joke(self):
        self.funcName = "joke"
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
        self.postTalk(self.recognizedAudio(audio))

    def postTalk(self, message):
        keywords = self.stringSplitter(message)

        if any("skämt" in s for s in keywords):
            self.joke()
        elif any("prata" in s for s in keywords):
            self.smallTalk()
        elif any("annat" in s for s in keywords):
            self.whatToDo()
        elif self.containsGoodbye(keywords):
            self.goodbye()
        else:
            tts = gTTS(text='Jag förstod inte, kan du säga igen?', lang='sv')
            tts.save("Ljudfiler/didntUnderstand.mp3")
            self.playSound("Ljudfiler/didntUnderstand.mp3")

            audio = self.listenSpeech(7)
            self.postTalk(self.recognizedAudio(audio))

    def containsGoodbye(self, message):
        answer = self.stringSplitter(message)
        if any(("hejdå" in s for s in answer) or (("hej" in s for s in answer) and ("då" in s for s in answer))):  
            return True
        else:
            return False

    def startRPSVoice(self):
        print('In startRPSVoice')
        self.funcName = "startRPSVoice"
        self.playRPSPhrases()
        print('After playRPSPhrases')
        tts1 = gTTS(text='Är du redo?', lang='sv')               # Ta bort efter första inspelning
        tts1.save("Ljudfiler/newReady.mp3")
        self.playSound("Ljudfiler/newReady.mp3")
        time.sleep(3)
        audio = self.listenSpeech(5)
        answer = self.recognizedAudio(audio)
        if(answer == "ja"):
            tts2 = gTTS(text='Sten, sax, påse!', lang='sv')               # Ta bort efter första inspelning
            tts2.save("Ljudfiler/stenSaxPase.mp3")
            self.playSound("Ljudfiler/stenSaxPase.mp3")
            time.sleep(3)
            sign = random.randint(1, 3)
            print("sign:", sign)  
            self.rockPaperScissors(sign)
            time.sleep(4)
            self.playAgain()
        elif(answer == "nej"):
            time.sleep(2)
            self.startRPSVoice()
        elif(answer == "tillbaka"):
            tts3 = gTTS(text='Okej, vi går tillbaka', lang='sv')  # Ta bort efter första inspelning
            tts3.save("Ljudfiler/goBack.mp3")
            self.playSound("Ljudfiler/goBack.mp3")
            self.whatToDo()
        elif(answer == "upprepa"):
            self.startRPSVoice()
        elif(self.containsGoodbye(answer)):
            self.goodbye()
        else:
            tts4 = gTTS(text='Fattar ej, vi testar igen!', lang='sv')  # Ta bort efter första inspelning
            tts4.save("Ljudfiler/tryAgain.mp3")
            self.playSound("Ljudfiler/tryAgain.mp3")

        
    def rockPaperScissors(self, sign):
        if(sign == 1):
            print('Jag valde sten')
            tts = gTTS(text='Jag valde sten!', lang='sv')               # Ta bort efter första inspelning
            tts.save("Ljudfiler/iChoseStone.mp3")
            self.playSound("Ljudfiler/iChoseStone.mp3")
        elif(sign == 2):
            print('Jag valde sax')
            tts = gTTS(text='Jag valde sax!', lang='sv')               # Ta bort efter första inspelning
            tts.save("Ljudfiler/iChoseScissors.mp3")
            self.playSound("Ljudfiler/iChoseScissors.mp3")
        elif(sign == 3):
            print('Jag valde påse')
            tts = gTTS(text='Jag valde påse!', lang='sv')               # Ta bort efter första inspelning
            tts.save("Ljudfiler/iChosePaper.mp3")
            self.playSound("Ljudfiler/iChosePaper.mp3")

    def playAgain(self):
        tts = gTTS(text='Vill du spela igen?', lang='sv')  # Ta bort efter första inspelning
        tts.save("Ljudfiler/playAgain.mp3")
        self.playSound("Ljudfiler/playAgain.mp3")

        time.sleep(3)
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
            time.sleep(1)
            self.whatToDo()
        else:
            tts = gTTS(text='Kan du upprepa', lang='sv')               # Ta bort efter första inspelning
            tts.save("Ljudfiler/canYouRepeat.mp3")
            self.playSound("Ljudfiler/canYouRepeat.mp3")
            self.playAgain()

    def playRPSPhrases(self):
        funcName = "playRPSPhrases"
        print('In playRPSPhrases')
        nr = random.randint(1, 10)
        if(nr == 1):
            tts = gTTS(text='Passa dig, jag känner mig vass idag!', lang='sv')  # Ta bort efter första inspelning
            tts.save("Ljudfiler/feelingSharp.mp3")
            self.playSound("Ljudfiler/feelingSharp.mp3")
            time.sleep(3)
        elif(nr == 2):
            tts = gTTS(text='Jag märker om du fuskar!', lang='sv')  # Ta bort efter första inspelning
            tts.save("Ljudfiler/iKnowIfYouCheat.mp3")
            self.playSound("Ljudfiler/iKnowIfYouCheat.mp3")
            time.sleep(3)
        elif(nr == 3):
            tts = gTTS(text='Jag är olympisk mästare på sten sax påse', lang='sv')  # Ta bort efter första inspelning
            tts.save("Ljudfiler/osChampion.mp3")
            self.playSound("Ljudfiler/osChampion.mp3")
            time.sleep(4)
        elif(nr == 4):
            tts = gTTS(text='Hoppas du har dina tur-strumpor på dig idag!', lang='sv')  # Ta bort efter första inspelning
            tts.save("Ljudfiler/luckySocks.mp3")
            self.playSound("Ljudfiler/luckySocks.mp3")
            time.sleep(4)
        elif(nr == 5):
            tts = gTTS(text='Tvinga mig inte att krossa dig', lang='sv')  # Ta bort efter första inspelning
            tts.save("Ljudfiler/crushYou.mp3")
            self.playSound("Ljudfiler/crushYou.mp3")
            time.sleep(3)
        else:
            tts = gTTS(text='Nu spelar vi!', lang='sv')  # Ta bort efter första inspelning
            tts.save("Ljudfiler/letsPlay.mp3")
            self.playSound("Ljudfiler/letsPlay.mp3")
            time.sleep(2)

    def startMath(self):
        self.funcName = "startMath"
        MathVoice.start_mathtest()


    def start_Schedule(self, manager):
        # Switch from face screen to schedule screen
        Manager.current = 'schedule'

        tts = gTTS(text='Här är ditt schema! Säg nästa vecka eller förra veckan för att byta vecka.', lang='sv')
        tts.save('Ljudfiler/schedule_instruction.mp3')
        self.playSound('Ljudfiler/schedule_instruction.mp3')

        demand = self.listenSpeech(4)
        words = self.stringSplitter(demand)

        if "nästa" in words:
            x = Manager.current
            def next_week(x):
                list = {
                    "schedule": 's2',
                    's2': 's3',
                    's3': 's4',
                    's4': 's5',
                    's5': 's6'
                }
                next_screen = list.get(x)
                return next_screen
            return next_week(x)

        elif "förra" in words:
            x = Manager.current
            def previous_week(x):
                list = {
                    "s2": 'schedule',
                    's3': 's2',
                    's4': 's3',
                    's5': 's4',
                    's6': 's5'
                }
                next_screen = list.get(x)
                return next_screen
            return(previous_week(x))
