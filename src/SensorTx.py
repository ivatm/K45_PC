'''
Created on 10 ���. 2022 �.

@author: Iva
'''

class SensorTransmitter(object):
    '''
    class transmits the needed Sensors file to K45 Module via UART (COM) port
    '''


    def __init__(self, SensorFileDef):
        '''
        Constructor
        The Constructor receives file description
        '''
        