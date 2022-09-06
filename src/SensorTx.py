'''
Created on 10.07.2022
@author: Iva
'''
import time
from future.backports.test.pystone import TRUE


class SensorTransmitter(object):
    '''
    class transmits the needed Sensors file to K45 Module via UART (COM) port
    '''
    IndexTMH  = 0    # The string number to be transmitted
    TMHLength = 0   # Total length of TMH. By default it is 0? after Sensor charackteristik is loaded it will be inited

    keSendSensor     = 100
    keSensorComplete = 101


    '''
    Sensor data transmition
    '''
    def DataSensorLineSend(self, COMConnection, Regulator):
        if (not COMConnection.isOpen() or not self.SensorReady or not self.Transmitting):
            return False
        else:
            try:
                if (self.IndexTMH < self.TMHLength):
                    strCommand = ord('b') + ord('e') + ord('g') + self.keSendSensor + self.AllTMH[self.IndexTMH] + ord('e') + ord('n') + ord('d')
                    COMConnection.write(strCommand)
                    self.IndexTMH = self.IndexTMH + 1

                else:
                    # The transmition complete
                    strCommand = ord('b') + ord('e') + ord('g') + self.keSensorComplete + ord('e') + ord('n') + ord('d')
                    self.TransmittingComplete = True
                    COMConnection.write(strCommand)

                out = []
                # let's wait one until the buffer fulfiling
                LimitCounter = 0
                while (COMConnection.inWaiting() < self.ReadBufferLength) and (LimitCounter < 100):
                    time.sleep(0.1)
                    LimitCounter = LimitCounter + 1 
                
                if (LimitCounter >= 99):
                    UnitEvailable = False
                    return UnitEvailable
                
                # All string recept   
                while COMConnection.inWaiting() > 0:
                    out += COMConnection.read(1)
                   
                if out != '':
                    #print(out)
                    Regulator.receivedProcessing( out)

                UnitEvailable = True
                return UnitEvailable
            except Exception as e:
                #print("Can't set COM Port:{}\n".format(str(e)))
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
        