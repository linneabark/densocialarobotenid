import time
import serial
from serial import Serial

class ArduinoHandler2main():
    ser = serial.Serial()   # set port, vill vi sätta baude rate?
    ser.port = '/dev/ttyACM1'
    ser.timeout = 5
#    ser.write_timeout = 5
    
    def read(self):
#        try:
        self.ser.open()
        character = ser.read(1)
        self.ser.close()
        return character
        #except SerialException:
        #    print('SerialException, no port found')

    def write(self, character):
        #try:
        self.ser.open()
        self.ser.write(character)
        self.ser.close()
        return character
#        except SerialException:
            #print('SerialException, no port found')


    def __init__(self):
        pass
