'''
Created on 23 жовт. 2021

@author: Oliva
'''
#from pickle import TRUE
#from ecdsa.test_malformed_sigs import params
#from Tools.pynche.StripViewer import constant
from pickle import FALSE
import re
import time
import serial
from xml.sax import _false


class K45_Unit(object):
    '''
    Object of K45 
    '''
    SetOrScanState = False
    CelseOrKelvin = False
    CryoLiquidesLevelMeasureOn = False
    
    ReadBufferLength = 26
    D_T      = 100   # K/C
    D_t      = 0.1 # mS
    Kprop    = 10
    Kdiff    = 10
    
    Ureal    = 10e-6  # V
    Treal    = 2000
    Tset     = 2000
    Tcur_set = 2000
    L_Level  = 90 # %
    
    CoProcessorState = 0
    # ------------------------------------------------------------------------------------
    keTset_input             = 2
    keTstep_input            = 4
    ketime_step_input        = 5
    keKprop_input            = 6
    keKdiff_input            = 7
    keSet_ScanSelect         = 9
    keTemperatureUnitSwitch  = 11
    keSaveConfigs            = 12
    keADCCalibration         = 13
    keShowSensor             = 14
    keNop                    = 253  # Nothing to do
    keRestoreDefaults        = 254
    keExit                   = 255
    keUnknownCommand         = 0xFFFF

    
    # ------------------------------------------------------------------------------------
    UnitEvailable = False

    def __init__(self, SetOrScanState, CelseOrKelvin , CryoLiquidesLevelMeasureOn):
        '''
        Constructor
        '''
        self.SetOrScanState = SetOrScanState
        self.CelseOrKelvin  = CelseOrKelvin
        self.CryoLiquidesLevelMeasureOn = CryoLiquidesLevelMeasureOn
    
# -----------------------------------------------------------------------------------

    def receivedProcessing(self, inBuff):
        
        beg = ''.join([chr(n) for n in inBuff[:3]])
        
        end = ''.join([chr(n) for n in inBuff[23:26]]) 
    
        
        if (len(inBuff) != self.ReadBufferLength) or beg != "beg" or  end != "end":
            #print("Length = " + str(len(inBuff)))
            
            beg = ''
            for x in range(len(inBuff[:3])):
                beg += chr(inBuff[x])
            
            #print("beg = " + beg)
            # print("inBuff[22:24] = " + inBuff[22:25].decode("utf-8"))
            #print("Wrong data")
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
            self.Treal = (inBuff[4]  << 8) + inBuff[3]
            #print("Treal =" + format(self.Treal/100, ".2f"))
            # Tset set ---------------------------------------------------------------------------------------------------------------------
            self.Tset = (inBuff[6]  << 8) + inBuff[5]
            #print("Tset =" + format(self.Tset/100, ".2f"))
            # Tcur_set set ---------------------------------------------------------------------------------------------------------------------
            self.Tcur_set = (inBuff[8]  << 8) + inBuff[7]
            #print("Tcur_set =" + format(self.Tcur_set/100, ".2f"))
            # D_T ---------------------------------------------------------------------------------------------------------------------
            self.D_T = (inBuff[10]  << 8) + inBuff[9]
            #print("D_T = " + format(self.D_T/100, ".2f"))
            # D_t ---------------------------------------------------------------------------------------------------------------------
            self.D_t = (inBuff[12]  << 8) + inBuff[11]
            #print("D_t = " + format(self.D_t/1000, ".2f"))
            # Kprop ---------------------------------------------------------------------------------------------------------------------
            self.Kprop = (inBuff[14]  << 8) + inBuff[13]
            #print("Kprop =" + format(self.Kprop, "d"))
            # Kdiff ---------------------------------------------------------------------------------------------------------------------
            self.Kdiff = (inBuff[16]  << 8) + inBuff[15]
            #print("Kdiff =" + format(self.Kdiff, "d"))
            # Ureal ---------------------------------------------------------------------------------------------------------------------
            self.Ureal = (inBuff[19]  << 16) +(inBuff[18]  << 8) + inBuff[17]
            #print("Ureal =" + format(self.Ureal/1000000, ".5f"))
            # Ureal ---------------------------------------------------------------------------------------------------------------------
            self.CryoLevel = inBuff[20]
            #print("cryoLevel =" + format(self.CryoLevel,"3.0f") + " %")
            # ---------------------------------------------------------------------------------------------------------------------
            Modes = inBuff[21]
            self.SetOrScanState = (Modes & 0x1) > 0
            #if (self.SetOrScanState > 0):
                #print("Scan mode")
            #else:
                #print("Set mode")
            self.TempSetAchieved    = (Modes & 0x2) > 0
            self.CelsiumOrKelvin    = (Modes & 0x4) > 0
            self.CryoLevelMeasuring = (Modes & 0x8) > 0
            # ---------------------------------------------------------------------------------------------------------------------
            self.Status = inBuff[22]
            self.HeaterError = (self.Status & 0x2) > 0
            self.CoolerError = (self.Status & 0x4) > 0
            self.ControlDiodeError = (self.Status & 0x8) > 0
            #print("Status =" + "{0:b}".format(self.Status))
# -----------------------------------------------------------------------------------
    def VarsUpdate(self, COMConnection):
        if (not COMConnection.isOpen()):
            return FALSE
        else:
            try:
                data = [ord('b'),ord('e'),ord('g'),self.keNop,0,0,0,ord('e'),ord('n'),ord('d')]
                COMConnection.write(data)
             
                out = []
                # let's wait one until the buffer fulfiling
                LimitCounter = 0
                while (COMConnection.inWaiting() < self.ReadBufferLength) and (LimitCounter < 100):
                    time.sleep(0.1)
                    LimitCounter = LimitCounter + 1 
                
                if (LimitCounter >= 99):
                    UnitEvailable = False
                    return False
                
                # All string recept   
                while COMConnection.inWaiting() > 0:
                    out += COMConnection.read(1)
                   
                if out != '':
                    #print(out)
                    self.receivedProcessing( out)
                UnitEvailable = True
                return True
            except Exception as e:                
                #print("Can't set COM Port:{}\n".format(str(e)))
                UnitEvailable = False
                return False
    
    def SendCommand(self, Command, Value, COMConnection):
        if (not COMConnection.isOpen()):
            return FALSE
        else:
            data = [ord('b'),ord('e'),ord('g'),Command,0,0,0,ord('e'),ord('n'),ord('d')]
            WorkByte = Value & 0xFF
            data[4] = WorkByte
            WorkByte = (Value >> 8) & 0xFF
            data[5] = WorkByte
            COMConnection.write(data)
            

    def RemoteCommand(self, Variable, StrValue, COMConnection):
        StrValue = re.sub("[^0-9,.]", "", StrValue)

        if Variable == "set_needed" or Variable == "scan_needed":
            #case :
            self.SendCommand(self.keSet_ScanSelect, int(StrValue)  , COMConnection)
        elif Variable=="treal":
            #case :
            #print(Variable)
            #print(StrValue)
            pass

        elif Variable=="tset":
            #case 
            #print(Variable)
            #print(StrValue)
            self.SendCommand(self.keTset_input, round(float(StrValue)*100), COMConnection)
        elif Variable=="tcur_set":
            #case 
            #print(Variable)
            #print(StrValue)
            pass
        elif Variable=="d_T":
            #case 
            #print(Variable)
            #print(StrValue)
            pass
            self.SendCommand(self.keTstep_input, round(float(StrValue)*100), COMConnection)
        elif Variable=="d_t":
            #case 
            #print(Variable)
            #print(StrValue)
            self.SendCommand(self.ketime_step_input, round(float(StrValue)*1000), COMConnection)
        elif Variable=="kprop":
            #case 
            #print(Variable)
            #print(StrValue)
            self.SendCommand(self.keKprop_input, int(StrValue), COMConnection)
        elif Variable=="kdiff":
            #case 
            #print(Variable)
            #print(StrValue)
            pass
            self.SendCommand(self.keKdiff_input, int(StrValue), COMConnection)
        elif Variable=="ureal":
            #print(Variable)
            #print(StrValue)
            pass
        elif Variable=="pure_command":
            self.SendCommand(int(StrValue), 0, COMConnection)
        else:
            #print(Variable)
            #print(StrValue)
            pass

    def GetTemperatureString(self, TempIntegerValue, NeedConvertion):
        if self.CelseOrKelvin and NeedConvertion:
            TempIntegerValue = TempIntegerValue - 27315
        WorkString = TempIntegerValue/100
        WorkString = WorkString.__str__()
        if self.CelseOrKelvin:
            WorkString = WorkString + " oC"
        else:
            WorkString = WorkString + " K"
        
        return WorkString
    
    def GetTimeString(self, TimeIntegerValue):

        WorkString = float(TimeIntegerValue/1000)
        WorkString = WorkString.__str__()
        WorkString = WorkString + " S"
        
        return WorkString
        