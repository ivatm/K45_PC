'''
Created on 11 січ. 2022

@author: Oliva
'''

# Python 3+
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from K45Unit import K45_Unit
import serial
from serial.tools.list_ports_windows import iterate_comports
from _ast import List
import logging

'''
  Good examples for Timers
  https://question-it.com/questions/1025145/kak-sozdat-fonovyj-potok-pri-vyzove-intervalnoj-funktsii-v-python
  https://ru.stackoverflow.com/questions/848711/tkinter-%D0%B8-%D0%B7%D0%B0%D0%B2%D0%B5%D1%80%D1%88%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BE%D0%B9
 ''' 
from threading import Thread
import time

class K45_Comm(tk.Tk):
    
    def CommunicationHandle(self):
        if (hasattr(self.COMConnection, 'is_open')   and (self.COMConnection.isOpen())):
            print("Againe \n\r")
        #self.CommTimer.start();
    
    def OnQuit(self):
        self. t._target.cancelled = True
        # IMPORTANT!
        self.wm_attributes("-disabled", False) # IMPORTANT!
        self.destroy()
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("K45")
        self.protocol("WM_DELETE_WINDOW", self.OnQuit)
        self.minsize(1000, 700)

        # K45 Visual variables --------------------------------------------------------------------------
        self.SetOrScanState = BooleanVar(name = 'SetOrScanState')
        self.SetOrScanState.set(True)
        self.CelseOrKelvin = BooleanVar(name = 'CelseOrKelvin')
        self.CelseOrKelvin.value = True
        self.CryoLiquidesLevelMeasureOn = BooleanVar(name = 'CryoLiquidesLevelMeasureOn')
        self.CryoLiquidesLevelMeasureOn.value = True
        self.Treal = DoubleVar(name = 'Treal')
        self.Treal.value = 20
        self.Tset = DoubleVar(name = 'Tset')
        self.Tset.value = 0
        self.Tcur_set = DoubleVar(name = 'Tcur_set')
        self.Tcur_set.value = 20
        self.D_T = DoubleVar(name = 'D_T')
        self.D_T.value = 1
        self.D_t = DoubleVar(name = 'D_t')
        self.D_t.value = 1
        self.Ureal = DoubleVar(name = 'Ureal')
        self.Ureal.value = 0.6
        self.Kprop = IntVar(name = 'Kprop')
        self.Kprop.value = 10 
        self.Kdiff = IntVar(name = 'Kdiff')
        self.Kdiff.value = 10
        self.L_Level = IntVar(name = 'L_Level')
        self.L_Level.value = 50
        
        # SetOrScanState, CelseOrKelvin , CryoLiquidesLevelMeasureOn 
        Regulator = K45_Unit(self.SetOrScanState.get(), self.CelseOrKelvin.get(), self.CryoLiquidesLevelMeasureOn.get())
        
        # Timer for communication
        self.COMConnection = None
        def background_task(Period, Handle):
            while not background_task.cancelled:
                Handle()
                time.sleep(Period)
        background_task.cancelled = False
        self.t = Thread(target=background_task, args = (1, self.CommunicationHandle))
        self.t.start()
        
        # --------------------------------------------------------------------------
        K45MenuButton = Menu(self)
        K45MenuButton.add_command(label="Connection", command = self.Create_InitCommunication)
        K45MenuButton.add_command(label="Sensor")
        K45MenuButton.add_command(label="Quit!", command=self.OnQuit)
        self.config(menu=K45MenuButton)
        
        # Reception value procedure
        def SetValueToVariable( Variable, Value):
            #Variable.set(Value)
            print("SetOrScanState %d,\n"  % self.SetOrScanState.get())

        # Mode Selection and system state --------------------------------------------------------------------------
        ModeFrame = LabelFrame(self, relief=RAISED, borderwidth = 1, text = "Mode selection")
        ModeFrame.pack()
        ModeFrame.place(height=100, width=510, x=10, y=20)
        
        SetScanSelection_Rb1 = Radiobutton(ModeFrame, text = "Set", 
                                           variable = self.SetOrScanState, value = "True",
                                           command = lambda : SetValueToVariable( self.SetOrScanState, self.SetOrScanState.get()))
        SetScanSelection_Rb2 = Radiobutton(ModeFrame, text = "Scan", 
                                           variable = self.SetOrScanState, value = "False", 
                                           command = lambda : SetValueToVariable( self.SetOrScanState, self.SetOrScanState.get()))
        SetScanSelection_Rb1.pack()
        SetScanSelection_Rb2.pack()
        SetScanSelection_Rb1.place(x=20,y=20)
        SetScanSelection_Rb2.place(x=60,y=20)
        
        
        # On Scan mode variables --------------------------------------------------------------------------
        ScanFrame = LabelFrame(self, relief=RAISED, borderwidth = 1, text = "Scan configs")
        ScanFrame.pack()
        ScanFrame.place(height=100, width=510, x=10, y=125)
        
        TimeStepLabel = Label(ScanFrame, text = "dt - Time Step")
        TimeStepLabel.pack()
        TimeStepLabel.place(x=20,y=20)
        TimeStepEntry = Entry(ScanFrame)
        TimeStepEntry.pack()
        TimeStepEntry.place(x=20,y=40)
        
        TemperatureStepLabel = Label(ScanFrame, text = "dT - Temperature Step")
        TemperatureStepLabel.pack()
        TemperatureStepLabel.place(x=170,y=20)
        TemperatureStepEntry = Entry(ScanFrame)
        TemperatureStepEntry.pack()
        TemperatureStepEntry.place(x=170,y=40) 
        
        # Current state of Temperature --------------------------------------------------------------------------
        TemperatureFrame = LabelFrame(self, relief=RAISED, borderwidth = 1, text = "Temperature")
        TemperatureFrame.pack()
        TemperatureFrame.place(height=100, width=510, x=10, y=230)
        
        TempRealLabel = Label(TemperatureFrame, text = "Current Temperature")
        TempRealLabel.pack()
        TempRealLabel.place(x=20,y=20)
        TempRealEntry = Entry(TemperatureFrame)
        TempRealEntry.pack()
        TempRealEntry.place(x=20,y=40)
        
        TempSetLabel = Label(TemperatureFrame, text = "Set Temperature")
        TempSetLabel.pack()
        TempSetLabel.place(x=170,y=20)
        TempSetEntry = Entry(TemperatureFrame)
        TempSetEntry.pack()
        TempSetEntry.place(x=170,y=40)
        
        # Cryo liquides level --------------------------------------------------------------------------
        CryoLevelFrame = LabelFrame(self, relief=RAISED, borderwidth = 1,  text = "Level of Cryo Liquid")
        CryoLevelFrame.pack()
        CryoLevelFrame.place(height=310, width=150, x=550, y=20)
        
        # Progress bar widget
        CryoLiquidesLevel = Progressbar(CryoLevelFrame, orient=VERTICAL, length=200,  mode='determinate')
        CryoLiquidesLevel.place(x=60, y=30)
        
        L_Level = 55
        CryoLiquidesLevel['value'] = L_Level

    def Create_InitCommunication(self):
        
        # THE CLUE
        self.wm_attributes("-disabled", True)

        # Creating the toplevel dialog
        self.toplevel_dialog = tk.Toplevel(self)
        self.toplevel_dialog.minsize(400, 250)
        self.toplevel_dialog.title("COM Port Configuration")

        # Tell the window manager, this is the child widget.
        # Interesting, if you want to let the child window 
        # flash if user clicks onto parent
        self.toplevel_dialog.transient(self)

        # This is watching the window manager close button
        # and uses the same callback function as the other buttons
        # (you can use which ever you want, BUT REMEMBER TO ENABLE
        # THE PARENT WINDOW AGAIN)
        self.toplevel_dialog.protocol("WM_DELETE_WINDOW", self.Close_InitCommunication)


        COMPortList = list(iterate_comports())
        COMPortOptions = []
        for port  in sorted(COMPortList):
            COMPortOptions.append(port.device)
        
        COMPort = StringVar()
        COMPort.set( "COM1")
        InputCOMPortLabel = Label(self.toplevel_dialog, text = "COM Port Selection")
        InputCOMPortLabel.pack()
        InputCOMPortLabel.place(x=20,y=10)
        InputCOMPort = OptionMenu(self.toplevel_dialog, COMPort, *COMPortOptions)
        InputCOMPort.pack(anchor = NW)
        InputCOMPort.place(x=20,y=40)
        
        BoudRateOptions = [2400, 4800, 9600, 14400, 19200]
        BoudRate = IntVar()
        BoudRate.set( 9600)
        InputBoudRateLabel = Label(self.toplevel_dialog, text = "Boudrate Selection")
        InputBoudRateLabel.pack()
        InputBoudRateLabel.place(x=250,y=10)
        InputBoudRate = OptionMenu(self.toplevel_dialog, BoudRate, *BoudRateOptions)
        InputBoudRate.pack(anchor = SE)
        InputBoudRate.place(x=250,y=40)
        
        BtnOk = Button(self.toplevel_dialog, text="Ok", command=lambda : self.GetCommConfig(COMPort.get(), BoudRate.get()))
        BtnOk.pack(side="top")
        BtnOk.place(x=115, y=80)
        
    def GetCommConfig(self, COMPort, BoudRate ):
        if (self.COMConnection != None and self.COMConnection.isOpen() and (self.COMConnection.port == COMPort)):
            self.Close_InitCommunication() # Nothing to do
        else:
            try:
                LocalComConnection = serial.Serial(
                        port=COMPort,
                        baudrate=BoudRate,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS)
                
                if (LocalComConnection.isOpen()):
                    self.COMConnection = LocalComConnection
                    self.Close_InitCommunication()
                
            except Exception as e:
                #"{}: {} [{}]".format(port, desc, hwid))
                # self.COMConnection = None
                print("Can't set COM Port:{}\n".format(str(e)))

    def Close_InitCommunication(self):
        # IMPORTANT!
        self.wm_attributes("-disabled", False) # IMPORTANT!
        self.toplevel_dialog.destroy()
        # Possibly not needed, used to focus parent window again
        self.deiconify() 

if __name__ == "__main__":
    app = K45_Comm()
    app.mainloop()