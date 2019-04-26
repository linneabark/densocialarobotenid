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

from mutagen.mp3 import MP3

#from main import Manager, MainScreen
from FileController import FileHandler
#from mathtest import MathVoice
#from main import Manager, MainScreen
from fractions import Fraction

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
        #MainScreen.moveMouth()
        audio = MP3(fileName)
        length = audio.info.length
        mixer.init()
        mixer.music.load(fileName)
        mixer.music.play()
        time.sleep(length-0.05*length)
        self.speaking = False
        FileHandler().append(self.name, "screen", "main")
        
    
    def mp3Exception(self):
        tts = gTTS(text= 'MP3, kan du prata tydligare?', lang='sv')
        tts.save("Ljudfiler/speakClear.mp3")
        self.playSound("Ljudfiler/speakClear.mp3")
        #time.sleep(2)
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
            # Metod som stänger av
        elif(answer == "nej"):
            tts = gTTS(text='Okej, då fortsätter vi leka!', lang='sv')
            self.fromWhatFunc()
        else:
            tts = gTTS(text='Säg igen', lang='sv')
            self.goodbye()
        tts.save("Ljudfiler/goodbye.mp3")
        self.playSound("Ljudfiler/goodbye.mp3")
        FileHandler().append(self.name,"screen","sleep")

           

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
        self.manager = manager
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
        tts = gTTS(text= 'Hej' + name + ', vad vill du göra?', lang='sv')
        tts.save("Ljudfiler/helloWhatToDo.mp3")
        self.playSound("Ljudfiler/helloWhatToDo.mp3")
        self.whatToDo()


    def playHello(self):
        self.funcName = "playHello"
        tts = gTTS(text= 'Hej! Jag heter Kim, vad heter du?', lang='sv')
        tts.save("Ljudfiler/helloWhatsYourName.mp3")
        self.playSound("Ljudfiler/helloWhatsYourName.mp3")

        #time.sleep(3)
        audio = self.listenSpeech(4)
        self.playHelloName(self.recognizedAudio(audio))



    def whatToDo(self):
        self.funcName = "whatToDo"
        #time.sleep(1)
        tts = gTTS(text='Vill du se schema, räkna matte, spela sten sax påse eller prata?', lang='sv')
        tts.save("Ljudfiler/whatToDo.mp3")
        self.playSound("Ljudfiler/whatToDo.mp3")
        #time.sleep(7)
        audio = self.listenSpeech(4)
        self.handleKeyword(self.recognizedAudio(audio))


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
        elif any("info" in s for s in keywords):
            x=1 #Skicka till infometod
        else:
            self.didntUnderstand()
            audio = self.listenSpeech(7)
            self.handleKeyword(self.recognizedAudio(audio))

    def overallKeyword(self, keyword):
        if (self.containsGoodbye(keyword)):
            self.goodbye()
        elif (keyword == "info"):
            x=1 # skicka till infometod
        elif (keyword == "klocka"):
            x=1 # skicka till klockmetod
        elif (keyword == "app"):
            x=1 # Starta gui
        elif (keyword == "paus"):
            x=1 # Pausa interaktion
        else:
            x=1 # break?

    def didntUnderstand(self):
        nr = random.randint(1, 10)
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
        keywords = self.stringSplitter(message)

        if any("skämt" in s for s in keywords):
            self.joke()        #Gå till skämtmetod
        elif any(("småprata" in s for s in keywords) or ("prata" in s for s in keywords)):
            self.smallTalk() #Gå till småpratmetod
        else:
            self.playSound("Ljudfiler/didntUnderstand.mp3")

            audio = self.listenSpeech(7)
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
        tts.save("Ljudfiler/askQuestion.mp3")
        self.playSound("Ljudfiler/askQuestion.mp3")
        audio = self.listenSpeech(4)
        string = self.recognizedAudio(audio)
        return string
    
    def smallTalk(self):
        #question = random.randint(1,4)
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
            tts = gTTS(text='Vill du höra ett skämt?', lang='sv')
            self.playSound("Ljudfiler/favoriteSport.mp3")

        tts2 = gTTS(text='Vill du fortsätta prata, höra ett skämt eller göra något annat?', lang='sv')
        tts2.save("Ljudfiler/continueTalking.mp3")
        self.playSound("Ljudfiler/continueTalking.mp3")
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

        #time.sleep(38)
        self.playSound("Ljudfiler/drumroll.mp3")   #Dab?

        tts = gTTS(text='Vill du höra ett till skämt, prata eller göra något annat?', lang='sv')
        tts.save("Ljudfiler/SomethingElse.mp3")
        self.playSound("Ljudfiler/SomethingElse.mp3")

        #time.sleep(5)
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
            #time.sleep(3)
            sign = random.randint(1, 3)
            print("sign:", sign)  
            self.rockPaperScissors(sign)
            #time.sleep(4)
            self.playAgain()
        elif(answer == "nej"):
            #time.sleep(2)
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
            tts2 = gTTS(text='Jag förstod inte, vi testar igen!', lang='sv')  # Ta bort efter första inspelning
            tts2.save("Ljudfiler/tryAgain.mp3")
            self.playSound("Ljudfiler/tryAgain.mp3")
            self.startRPSVoice()

        
    def rockPaperScissors(self, sign):
        if(sign == 1):
            tts = gTTS(text='Jag valde sten!', lang='sv')
        elif(sign == 2):
            tts = gTTS(text='Jag valde sax!', lang='sv')
        elif(sign == 3):
            tts = gTTS(text='Jag valde påse!', lang='sv')
        tts.save("Ljudfiler/iChoseX.mp3")
        self.playSound("Ljudfiler/iChoseX.mp3")

    def playAgain(self):
        tts = gTTS(text='Vill du spela igen?', lang='sv')  # Ta bort efter första inspelning
        tts.save("Ljudfiler/playAgain.mp3")
        self.playSound("Ljudfiler/playAgain.mp3")

        #time.sleep(3)
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
            #time.sleep(1)
            self.whatToDo()
        elif(self.recognizedAudio(play_again_answer) == "upprepa"):
            tts = gTTS(text='Okej, vi tar det igen', lang='sv') # Ta bort efter första inspelning
            tts.save("Ljudfiler/takeItAgain.mp3")
            self.playSound("Ljudfiler/takeItAgain.mp3")
            time.sleep(1)
            self.playAgain()
        else:
            self.didntUnderstand()
            self.playAgain()

    def playRPSPhrases(self):
        funcName = "playRPSPhrases"
        print('In playRPSPhrases')
        nr = random.randint(1, 10)
        if(nr == 1):
            tts = gTTS(text='Passa dig, jag känner mig vass idag!', lang='sv')
        elif(nr == 2):
            tts = gTTS(text='Jag märker om du fuskar!', lang='sv')
        elif(nr == 3):
            tts = gTTS(text='Jag är olympisk mästare på sten sax påse', lang='sv')
        elif(nr == 4):
            tts = gTTS(text='Hoppas du har dina turstrumpor på dig idag!', lang='sv')
        elif(nr == 5):
            tts = gTTS(text='Tvinga mig inte att krossa dig', lang='sv')
        else:
            tts = gTTS(text='Nu spelar vi!', lang='sv')
        tts.save("Ljudfiler/RPSPhrase.mp3")
        self.playSound("Ljudfiler/RPSPhrase.mp3")


   

    def start_Schedule(self):
        # Switch from face screen to schedule screen
        FileHandler().append(self.name,"screen","schedule")

        tts = gTTS(text='Här är ditt schema! Säg nästa vecka eller förra veckan för att byta vecka.', lang='sv')
        tts.save('Ljudfiler/schedule_instruction.mp3')
        self.playSound('Ljudfiler/schedule_instruction.mp3')
        time.sleep(5)
        audio = self.listenSpeech(4)
        string = self.recognizedAudio(audio)
        words = self.stringSplitter(string)
        

    
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
        funcName = "startMath"
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
   
