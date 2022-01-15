'''
Created on 23 жовт. 2021

@author: Oliva
'''
#from pickle import TRUE
#from ecdsa.test_malformed_sigs import params
#from Tools.pynche.StripViewer import constant

class TemperatureValue(object):
    '''
    The temperature value
    '''
    T = 20
    CelsOrKelv = True
    CONSTANT_Shift = 273.15
    
    def __init__(self, Value, UnitCOrK):
        '''
        Constructor for temperature value
        '''
        self.T = Value
        self.CelsOrKelv = UnitCOrK

    def GetKelvinValue(self):
        '''
        Returns value in Kelvin
        '''
        return self.T

    def GetCelsiumValue(self):
        '''
        Returns value in Celsium
        '''
        return self.T - self.CONSTANT_Shift

class K45_Unit(object):
    '''
    Object of K45 
    '''
    SetOrScanState = True
    CelseOrKelvin = True
    CryoLiquidesLevelMeasureOn = True
    Treal    = TemperatureValue(20, True)
    Tset     = TemperatureValue(20, True)
    Tcur_set = TemperatureValue(20, True)
    D_T      = 1   # K/C
    D_t      = 0.1 # mS
    Ureal    = 10e-6  # V
    Kprop    = 10
    Kdiff    = 10
    L_Level  = 90 # %

    def __init__(self, SetOrScanState, CelseOrKelvin , CryoLiquidesLevelMeasureOn):
        '''
        Constructor
        '''
        self.SetOrScanState = SetOrScanState
        self.CelseOrKelvin  = CelseOrKelvin
        self.CryoLiquidesLevelMeasureOn = CryoLiquidesLevelMeasureOn