'''
Created on 13 лип. 2021

@author: Oliva
'''

import time
import serial

# ---------------------------------------------------------------------------------------------------------------------
def receivedProcessing(inBuff):
 
    beg = ''
    for x in range(len(inBuff[:3])):
        beg += chr(inBuff[x])
    
    end = ''
    for x in range(len(inBuff[22:])):
        end += chr(inBuff[22 + x])

    
    if (len(inBuff) != ReadBufferLength) or beg != "beg" or  end != "end":
        print("Length = " + str(len(inBuff)))
        
        beg = ''
        for x in range(len(inBuff[:3])):
            beg += chr(inBuff[x])
        
        print("beg = " + beg)
        print("inBuff[22:24] = " + inBuff[22:25].decode("utf-8"))
        print("Wrong data")
    else:

#   keTreal,      //   lTemperatureReal,
#   keTset,       //   lTemperatureSet,
#   keTcurSet,    //   lTemperatureCurrentSet,
#   keDeltaT,     //   lDelta_T,
#   keDeltat,     //   lDelta_t,
#   keKprop,      //   lKprop,
#//   keKint,       //   lKint,
#   keKdiff,      //   lKdiff,
#   keUreal,       //  sSensorData.iUcurrent,
#   keMaxVariableNum

# Treal set        
        Treal = (inBuff[4]  << 8) + inBuff[3]
        print("Treal =" + format(Treal/100, ".2f"))
# Tset set ---------------------------------------------------------------------------------------------------------------------
        Tset = (inBuff[6]  << 8) + inBuff[5]
        print("Tset =" + format(Tset/100, ".2f"))
# Tcur_set set ---------------------------------------------------------------------------------------------------------------------
        Tcur_set = (inBuff[8]  << 8) + inBuff[7]
        print("Tcur_set =" + format(Tcur_set/100, ".2f"))
# D_T ---------------------------------------------------------------------------------------------------------------------
        D_T = (inBuff[10]  << 8) + inBuff[9]
        print("D_T = " + format(D_T/100, ".2f"))
# D_t ---------------------------------------------------------------------------------------------------------------------
        D_t = (inBuff[12]  << 8) + inBuff[11]
        print("D_t = " + format(D_t/1000, ".2f"))
# Kprop ---------------------------------------------------------------------------------------------------------------------
        Kprop = (inBuff[14]  << 8) + inBuff[13]
        print("Kprop =" + format(Kprop, "d"))
# Kdiff ---------------------------------------------------------------------------------------------------------------------
        Kdiff = (inBuff[16]  << 8) + inBuff[15]
        print("Kdiff =" + format(Kdiff, "d"))
# Ureal ---------------------------------------------------------------------------------------------------------------------
        Ureal = (inBuff[19]  << 16) +(inBuff[18]  << 8) + inBuff[17]
        print("Ureal =" + format(Ureal/1000000, ".5f"))
# ---------------------------------------------------------------------------------------------------------------------
        if (inBuff[20]):
            print("Scan mode")
        else:
            print("Set mode")
# ---------------------------------------------------------------------------------------------------------------------
        print("Co processor states =" + "{0:b}".format(inBuff[21]))
# ---------------------------------------------------------------------------------------------------------------------

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM14',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ReadBufferLength = 25

#ser.open()
ser.isOpen()

print('Enter your commands below.\r\nInsert "exit" to leave the application.')

InStr=1
while 1 :
    # get keyboard input
    InStr = "qwe" #input('>> ')
        # Python 3 users
        # input = input(">> ")
    if InStr == "exit":
        ser.close()
        exit()
    else:
        
        data = [ord('b'),ord('e'),ord('g'),5,1,1,1,ord('e'),ord('n'),ord('d')]
        ser.write(data)

        out = []
        # let's wait one until the buffer fulfiling
        while ser.inWaiting() < ReadBufferLength:
            time.sleep(0.1)
            
        while ser.inWaiting() > 0:
            out += ser.read(1)
            
        if out != '':
            print(out)
            receivedProcessing(out)
            
            
    
    