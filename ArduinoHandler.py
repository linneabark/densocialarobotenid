'''
Det som ibland behöver ändras är "ttyACM0" till ttyACM1(förmodligen) eftersom den
ibland ändrar sig när man kopplar ut och in den igen

9600 kommer behöva ändras till 115200 också tror jag då detta är vår "baud rate"
dvs hur ofta och snabbt data skickas, typ bit rate
'''
import time
import serial

class ArduinoHandler():

    # ttyACM0" eller ttyACM1
    channel = None

    # Denna kanske också behöver ändras
    baudRate = 115200

    # Metod för testning om ttyACM0 eller ttyACM1 ska användas
    # Kanske går att använda ser.name för att se vilken kanal som används
    # waitTime tror jag är hur lång tid den väntar på respons,
    # sätts när man skapar en ArduinoHandler
    def testChannel(self, waitTime):
        ser = serial.Serial('/dev/ttyACM0',self.baudRate)
        s = [0, 1]
        start = time.time()
        t = 0
        while (s[0] == None | t < 4):            #Denna kontroller behöver nog ändras, göra en metod som väntar TODO
            read_serial = ser.readline()
            s[0] = str(int(ser.readline(), 16))
            print([0])
            t += (time.time() - start)
        if(s[0]!= None):
            return serial.Serial('/dev/ttyACM0',self.baudRate, timeout = waitTime)
        else:
            return serial.Serial('/dev/ttyACM1',self.baudRate, timeout = waitTime)
        pass

    def __init__(self,waitTime):
        self.channel = self.testChannel(waitTime)

    '''
    Ska läsa från arduino där "2" är antalet bytes den läser
    '''
    def read(self):
        string = str(self.channel.read(2))
        return string

    '''
    Tänker att denna ska skriva till Arduino och returnera om skrivningen har lyckats
    Detta funkar förmodligen inte men det är en start
    '''
    # TODO
    def write(self,char):
        self.channel.write('b' + char)         # oklart om "b" ska vara där, såg i ett exempel
        string = self.read()
        if(string == "k"):
            return True
        else:
            return False


'''

ser = serial.Serial('/dev/ttyACM0', 9600)
s = [0, 1]
while True:
    read_serial = ser.readline()
    s[0] = str(int(ser.readline(), 16))
    print([0])
    print(read_serial)
'''