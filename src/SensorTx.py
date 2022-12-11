'''
Created on 10.07.2022
@author: Iva
'''
import time
#from future.backports.test.pystone import TRUE
from K45Unit import GetCheckSum 
from K45Unit import CheckSumCheck 


class SensorTransmitter(object):
    '''
    class transmits the needed Sensors file to K45 Module via UART (COM) port
    '''
    IndexTMH  = 0    # The string number to be transmitted
    TMHLength = 0   # Total length of TMH. By default it is 0? after Sensor charackteristik is loaded it will be inited
    ProgressDone = 0 # [%]

    SensorReceptionAnswerLength = 8  # Telegram length in case common data transmition: 3-Start + 1-Commant + 1-Ok/NoK + 1-CheckSum + 3-End

    keSendSensor     = 100
    keSensorComplete = 101

    CommandPlace = 3
    SubCommandPlace = 4

    keSimpleTelegram     = 0
    keSensorLineReceived = 1


    '''
    Sensor data transmition
    '''
    def DataSensorLineSend(self, COMConnection):
        if (not COMConnection.isOpen() or not self.SensorReady or not self.Transmitting):
            return False
        else:
            try:
                if (self.IndexTMH < self.TMHLength):
                    IndexByte1 = (self.IndexTMH >> 8) & 0xFF
                    IndexByte2 = self.IndexTMH & 0xFF
                    strCommand = ['b', 'e', 'g', self.keSendSensor, IndexByte1, IndexByte2, *self.AllTMH[self.IndexTMH]]
                    CheckSum = GetCheckSum(strCommand)
                    strCommand = [*strCommand,CheckSum, 'e', 'n', 'd']
                    #print("Sensor:String to send:") 
                    #print(strCommand)
                    strCommandOut = []
                    for SymByte in strCommand:
                        if (type(SymByte) != int):
                            SymByte = ord(SymByte)
                        strCommandOut = [*strCommandOut, SymByte]
                    #print("Sensor:ASCII telegram sent :" ) 
                    #print(strCommandOut)
                            
                    COMConnection.write(strCommandOut)
                    self.IndexTMH = self.IndexTMH + 1

                else:
                    # The transmition complete
                    strCommand = [ord('b'),ord('e'),ord('g'), self.keSensorComplete]
                    CheckSum = GetCheckSum(strCommand)
                    strCommand = [*strCommand,CheckSum, ord('e'), ord('n'), ord('d')]
                    COMConnection.write(strCommand)
                    #print("Sensor complete:")
                    #print(strCommand)

                    self.TransmittingComplete = True
                    self.Transmitting = False
                    
                if (self.TMHLength > 0):
                    self.ProgressDone = 100 * self.IndexTMH / self.TMHLength
                else:
                    self.ProgressDone = 0

                out = []
                # let's wait one until the buffer fulfilling
                LimitCounter = 0
                while (COMConnection.inWaiting() < self.SensorReceptionAnswerLength) and (LimitCounter < 99):
                    time.sleep(0.01)
                    LimitCounter = LimitCounter + 1 
                
                if (LimitCounter >= 100):
                    UnitEvailable = False
                    return UnitEvailable
                
                # All string recept   
                while COMConnection.inWaiting() > 0:
                    out += COMConnection.read(1)
                   
                if out != '':
                    #print(out)
                    return(self.receivedProcessing(out))

                UnitEvailable = True
                return UnitEvailable
            except Exception as e:
                print("Can't transmit:{}\n".format(str(e)))
                UnitEvailable = False
                return False

    '''
    Initialisation of Sensor transmition 
    '''
    def SensorTxInit(self):
        self.IndexTMH = 0
        self.TransmittingComplete = False
        if  (self.SensorReady):
            self.TMHLength = len(self.AllTMH)

    def receivedProcessing(self, inBuff):
        
        beg = ''.join([chr(n) for n in inBuff[:3]])
        
        end = ''.join([chr(n) for n in inBuff[(self.SensorReceptionAnswerLength - 3):]]) 
    
        
        if beg != "beg" or  end != "end":
            #print("Length = " + str(len(inBuff)))
            
            beg = ''
            for x in range(len(inBuff[:3])):
                beg += chr(inBuff[x])
            
            #print("beg = " + beg)
            # print("inBuff[22:24] = " + inBuff[22:25].decode("utf-8"))
            #print("Wrong data")
            return False

        elif (len(inBuff) == self.SensorReceptionAnswerLength) and (inBuff[self.CommandPlace] == self.keSensorLineReceived) and CheckSumCheck(inBuff):
            return True
        else:
                        #print("Length = " + str(len(inBuff)))
            
            beg = ''
            for x in range(len(inBuff[:3])):
                beg += chr(inBuff[x])
            
            #print("beg = " + beg)
            # print("inBuff[22:24] = " + inBuff[22:25].decode("utf-8"))
            #print("Wrong data")
            return False


    def __init__(self, SensorFileDef):
        '''
        Constructor
        The Constructor receives file description
        '''
        try:
            f = open(SensorFileDef,'r')
            self.AllTMH = f.readlines()
            self.SensorReady = True
            self.SensorTxInit()
        except Exception as e:
            self.SensorReady = False
        self.Transmitting = False
        self.TransmittingComplete = False
        
        #print("File length ", len(AllTMH))
        