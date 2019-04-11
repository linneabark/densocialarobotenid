#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
from gtts import gTTS
from pygame import mixer
import speech_recognition as sr
#from kivy.core.audio import SoundLoader

class SpeechController():
    def __init__(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()

    def playVoice(string):
        switcher = {
            1: "",
            2: ""
            }
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
        #sound = SoundLoader.load("internetException.mp3")
        #if sound:
        #    sound.play()
        #sound.play()
        mixer.init()
        mixer.music.load("internetException.mp3")
        mixer.music.play()
        print("hej")

    def recognizedAudio(self,audio):
        string = self.r.recognize_google(audio, language="sv-SV")
        return string

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
            
    def listenSpeech(self):
        with self.m as source:
            #audio = r.record(source, duration = 5)
            audio = self.r.listen(source, phrase_time_limit=3)
            #self.r.snowboy_wait_for_hot_word()
            return audio
            #self.tryListen(audio)

















