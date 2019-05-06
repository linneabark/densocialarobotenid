import time
import serial


class ArduinoHandler2():
    ser = serial.Serial(port='/dev/ttyUSB0', bauderate=115200, bytesize=EIGHTBITS, timeout=15, write_timeout=15)   # set port, vill vi sätta baude rate?

    def read(self):
        try:
            self.ser.open()
            while ser.is_open:
                character = ser.read(8)
            self.ser.close()
            return character
        except SerialException:
            print('SerialException, no port found')

    def write(self, character):
        try:
            self.ser.open()
            while ser.is_open:
                ser.write(character)
            self.ser.close()
            return character
        except SerialException:
            print('SerialException, no port found')

        pass

    def __init__(self):
        pass
