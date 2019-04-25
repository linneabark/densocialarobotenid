from gtts import gTTS
from speechController import SpeechController

class MathVoice():

    def subtraction(first_term, second_term):
        return first_term - second_term


    def addition(first_term, second_term):
        return first_term + second_term


    def multiplication(first_term, second_term):
        return first_term * second_term

    def division(first_term, second_term):
        return first_term / second_term


    def find_numbers(str_input):
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


    def start_mathtest(self):
        while True:
            ttsMath1 = gTTS(text='Vad vill du räkna ut? Ge mig två siffror och en operator.', lang='sv')
            ttsMath1.save("Ljudfiler/newCount.mp3")
            SpeechController.playSound("Ljudfiler/newCount.mp3")
            audio = SpeechController.listenSpeech(7)
            str_input = SpeechController.recognizedAudio(audio)
            print(str_input)

            temp = list()
            temp.extend(find_numbers(str_input))

            if len(temp) < 2:
                ttsMath2 = gTTS(text='Fler siffror tack.', lang='sv')
                ttsMath2.save("Ljudfiler/tooFewNumbers.mp3")
                SpeechController.playSound("Ljudfiler/tooFewNumbers.mp3")
                continue

            if len(temp) > 2:
                ttsMath3 = gTTS(text='Bara två termer tack.', lang='sv')
                ttsMath3.save("Ljudfiler/fewerNumbersPlease.mp3")
                SpeechController.playSound("Ljudfiler/fewerNumbersPlease.mp3")
                continue

            first_term = int(temp[0])
            second_term = int(temp[1])

            operator_count = 0
            operator_input = str_input.lower()
            operators = {
                'PLUS': ["plus", "addera", "lägg till"],
                'MINUS': ["minus"],
                'MULTIPLICATION': ["multiplicerat", "gånger"],
                'DIVISION' : ["delat med", "delat på", "dividerat med", "dividerat på"]
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
                ttsMath4 = gTTS(text='Bara en operator tack.', lang='sv')
                ttsMath4.save("Ljudfiler/tooManyOperators.mp3")
                SpeechController.playSound("Ljudfiler/tooManyOperators.mp3")
                continue
            elif operator_count < 1:
                ttsMath5 = gTTS(text='Kan jag få en operator?', lang='sv')
                ttsMath5.save("Ljudfiler/tooFewOperators.mp3")
                SpeechController.playSound("Ljudfiler/tooFewOperators.mp3")
                continue

            if actual_operator == 'MINUS':
                ttsMath6 = gTTS(text=str(subtraction(first_term, second_term)), lang='sv')
                ttsMath6.save("Ljudfiler/answerSubtraction.mp3")
                SpeechController.playSound("Ljudfiler/answerSubtraction.mp3")
                break
            elif actual_operator == 'PLUS':
                ttsMath7 = gTTS(text=str(addition(first_term, second_term)), lang='sv')
                ttsMath7.save("Ljudfiler/answerAddition.mp3")
                SpeechController.playSound("Ljudfiler/answerAddition.mp3")
                break
            elif actual_operator == 'MULTIPLICATION':
                ttsMath8 = gTTS(text=str(multiplication(first_term, second_term)), lang='sv')
                ttsMath8.save("Ljudfiler/answerMultiplication.mp3")
                SpeechController.playSound("Ljudfiler/answerMultiplication.mp3")
                break
            elif actual_operator == 'DIVISION':
                ttsMath9 = gTTS(text=str(division(first_term, second_term)), lang='sv')
                ttsMath9.save("Ljudfiler/answerDivision.mp3")
                SpeechController.playSound("Ljudfiler/answerDivision.mp3")
                break
            else:
                ttsMath10 = gTTS(text='Försök igen med två siffror och en operator.', lang='sv')
                ttsMath10.save("Ljudfiler/tryAgainMath.mp3")
                SpeechController.playSound("Ljudfiler/tryAgainMath.mp3")

            break