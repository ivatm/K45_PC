'''
Created on 11 Ñ�Ñ–Ñ‡. 2022

@author: Oliva
'''

# Python 3+
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from K45Unit import K45_Unit
from TitleConfigs import Titles

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
        if (hasattr(self.COMConnection, 'is_open') and (self.COMConnection.isOpen())):
            print("Againe \n\r")
            if (self.Regulator.VarsUpdate(self.COMConnection)):
                self.UpdateVariables()
                # Visual elements update
                self.UpdateVisuals()
        else:
            print("Wait for COM\n\r")


    
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
        #------------------------------------------------------------------------------------------------------
        self.Focused = None
        def SelectFocus(event):
            self.Focused = event.widget
            
        def ReleaseFocus(event):
            if  (hasattr(self.COMConnection, 'is_open')   and (self.COMConnection.isOpen())):
                self.Regulator.RemoteCommand(str(self.Focused).split(".")[-1], self.Focused.get() , self.COMConnection)

        def CommandSet():
            if  (hasattr(self.COMConnection, 'is_open')   and (self.COMConnection.isOpen())):
                ComStr = CommandEnter.get()
                ComStr = re.sub("[^0-9]", "", ComStr)
                self.Regulator.RemoteCommand("pure_command", ComStr , self.COMConnection)

        def ModeUpdate():
            if  (hasattr(self.COMConnection, 'is_open') and (self.COMConnection.isOpen())):
                if self.SetOrScanState.value > 0:
                    Value = 0
                else:
                    Value = 1

                self.Regulator.RemoteCommand("set_needed", str(Value) , self.COMConnection)
                self.SetOrScanState.value = Value
                SetScanSelection_Rb1.update()
                SetScanSelection_Rb2.update()
                


        # K45 Labels and titles -------------------------------------------------------------------------
        self.titeles = Titles(1);
        # K45 Visual variables --------------------------------------------------------------------------
        self.SetOrScanState = IntVar(name = 'SetOrScanState')
        self.SetOrScanState.value = 0
        self.CelseOrKelvin = IntVar(name = 'CelseOrKelvin')
        self.CelseOrKelvin.value = 1
        self.CryoLiquidesLevelMeasureOn = IntVar(name = 'CryoLiquidesLevelMeasureOn')
        self.CryoLiquidesLevelMeasureOn.value = 1
        self.Treal = DoubleVar(name = 'Treal')
        self.Treal.value = 2000
        self.Tset = DoubleVar(name = 'Tset')
        self.Tset.value = 0
        self.Tcur_set = DoubleVar(name = 'Tcur_set')
        self.Tcur_set.value = 2000
        self.D_T = DoubleVar(name = 'D_T')
        self.D_T.value = 100
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
        self.userCommand = StringVar(name = 'user_Command')
        self.userCommand = "*"
        
        self.VariableList = [self.Treal, self.Tset, self.Tcur_set, self.D_T, self.D_t, self.Kprop, self.Kdiff, self.L_Level]
        self.VariableListIndex = 0; 
        # SetOrScanState, CelseOrKelvin , CryoLiquidesLevelMeasureOn 
        self.Regulator = K45_Unit(bool(self.SetOrScanState.get()), bool(self.CelseOrKelvin.get()), bool(self.CryoLiquidesLevelMeasureOn.get()))
        

        # --------------------------------------------------------------------------
        K45MenuButton = Menu(self)
        K45MenuButton.add_command(label=self.titeles.Menu_Connection, command = self.Create_InitCommunication)
        K45MenuButton.add_command(label=self.titeles.Menu_Sensor)
        K45MenuButton.add_command(label=self.titeles.Menu_Exit, command=self.OnQuit)
        self.config(menu=K45MenuButton)
        

        # Mode Selection and system state --------------------------------------------------------------------------
        ModeFrame = LabelFrame(self, relief=RAISED, borderwidth = 1, text = self.titeles.Mode_Selection, name = "settingmode")
        ModeFrame.place(height=50, width=510, x=10, y=20)
        
        SetScanSelection_Rb1 = Radiobutton(ModeFrame, text = self.titeles.Set, variable = self.SetOrScanState, value = 0, name = "set_needed" , command = ModeUpdate)

        SetScanSelection_Rb2 = Radiobutton(ModeFrame, text = self.titeles.Scan, variable = self.SetOrScanState, value = 1, name = "scan_needed" , command = ModeUpdate)
        
        SetScanSelection_Rb1.place(x=20,y=5)
        SetScanSelection_Rb2.place(x=170,y=5)
        SetScanSelection_Rb1.update()
        SetScanSelection_Rb2.update()
        
        # PID configurations --------------------------------------------------------------------------
        PIDFrame = LabelFrame(self, relief=RAISED, borderwidth = 1, text = self.titeles.PID_Configs, name = "pid_configs")
        PIDFrame.place(height=100, width=510, x=10, y=80)
        
        PropPartLabel = Label(PIDFrame, text = self.titeles.Kprop)
        PropPartLabel.place(x=20,y=20)
        WorkStr = self.Kprop.value.__str__()
        KpropEntry = Entry(PIDFrame, name = "kprop")
        KpropEntry.insert(END, WorkStr)
        KpropEntry.place(x=20,y=40)
        KpropEntry.bind('<Button-1>', SelectFocus)
        KpropEntry.bind('<Return>', ReleaseFocus)

        
        DiffPartLabel = Label(PIDFrame, text = self.titeles.Kdiff)
        DiffPartLabel.place(x=170,y=20)
        WorkStr = self.Kdiff.value.__str__()
        KdiffEntry = Entry(PIDFrame, name = "kdiff")
        KdiffEntry.insert(END, WorkStr)
        KdiffEntry.place(x=170,y=40) 
        KdiffEntry.bind('<Button-1>', SelectFocus)
        KdiffEntry.bind('<Return>', ReleaseFocus)

        
        # On Scan mode variables --------------------------------------------------------------------------
        ScanFrame = LabelFrame(self, relief=RAISED, borderwidth = 1, text = self.titeles.Scan_configs, name = "scan_configs")
        ScanFrame.place(height=100, width=510, x=10, y=190)
        
        TimeStepLabel = Label(ScanFrame, text = self.titeles.Scan_time_step)
        TimeStepLabel.place(x=20,y=20)
        WorkStr = self.Regulator.GetTimeString( self.D_t.value)
        TimeStepEntry = Entry(ScanFrame, name = "d_t")
        TimeStepEntry.insert(END, WorkStr)
        TimeStepEntry.place(x=20,y=40)
        TimeStepEntry.bind('<Button-1>', SelectFocus)
        TimeStepEntry.bind('<Return>', ReleaseFocus)
        
        TemperatureStepLabel = Label(ScanFrame, text = self.titeles.Scan_temperature_step)
        TemperatureStepLabel.place(x=170,y=20)
        WorkStr = self.Regulator.GetTemperatureString(self.D_T.value, False)
        TemperatureStepEntry = Entry(ScanFrame, name = "d_T")
        TemperatureStepEntry.insert(END, WorkStr)
        TemperatureStepEntry.place(x=170,y=40) 
        TemperatureStepEntry.bind('<Button-1>', SelectFocus)
        TemperatureStepEntry.bind('<Return>', ReleaseFocus)
        
        # Current state of Temperature --------------------------------------------------------------------------
        TemperatureFrame = LabelFrame(self, relief=RAISED, borderwidth = 1, text = self.titeles.Temperatures, name="temperature")
        TemperatureFrame.place(height=100, width=510, x=10, y=300)
        
        TempRealLabel = Label(TemperatureFrame, text = self.titeles.Measured)
        TempRealLabel.place(x=20,y=20)
       
        WorkStr = self.Regulator.GetTemperatureString(self.Treal.value, True)
        TempRealLabel = tk.Label(TemperatureFrame, anchor="w", text = WorkStr, bg="white" , height=1, width=20 , name = "treal")
        TempRealLabel.place(x=20,y=40,width=125)
        
        TempSetLabel = Label(TemperatureFrame, text = self.titeles.Set_Temperaure)
        TempSetLabel.place(x=170,y=20)
        WorkStr = self.Regulator.GetTemperatureString(self.Tset.value, True)
        TempSetEntry = Entry(TemperatureFrame, name = "tset")
        TempSetEntry.insert(END, WorkStr)
        TempSetEntry.place(x=170,y=40)
        TempSetEntry.bind('<Button-1>', SelectFocus)
        TempSetEntry.bind('<Return>', ReleaseFocus)
        
        # Status frame --------------------------------------------------------------------------
        StatusFrame = LabelFrame(self, relief=RAISED, borderwidth = 1,  text = self.titeles.Status, name="status_frame")
        StatusFrame.place(height=100, width=510, x=10, y=410)

        # WorkStr = self.Regulator.GetTemperatureString(self.Treal.value, True)
        # CurrentValue = tk.Label(StatusFrame, anchor="w", text = WorkStr, bg="white" , height=1, width=20 , name = "treal")
        # CurrentValue.place(x=90,y=15)
        # 
        # BtnLeft = Button(StatusFrame, text="<")#, command=lambda : self.DecValNumber())
        # BtnLeft.pack(side="top")
        # BtnLeft.place(x=10, y=13)
        # 
        # BtnRight = Button(StatusFrame, text=">")#, command=lambda : self.IncValNumber())
        # BtnRight.pack(side="top")
        # BtnRight.place(x=240, y=13)

        CommandEnter = Entry(StatusFrame, textvariable=self.userCommand)
        CommandEnter.insert(END, "*")
        CommandEnter.place(x=10,width=95,y=15) 

        BtnRight = Button(StatusFrame, text="#", command=CommandSet)
        BtnRight.pack(side="top")
        BtnRight.place(x=110, y=13)

        ConnectionState = tk.Label(StatusFrame, anchor="c", text = self.titeles.ConnectionState, bg="light gray" , height=1, width=20, name = "connection_state" )
        ConnectionState.place(x=0,y=65,width=127)
        
        HeaterState = tk.Label(StatusFrame, anchor="c", text = self.titeles.HeaterState, bg="light gray" , fg = "green" , height=1, width=20,name = "heater_state" )
        HeaterState.place(x=128,y=65,width=127)
        
        CoolerState = tk.Label(StatusFrame, anchor="c", text = self.titeles.CoolerState, bg="light gray" , fg = "green" , height=1, width=20, name = "cooler_state" )
        CoolerState.place(x=256,y=65,width=127)
        
        DiodeState = tk.Label(StatusFrame, anchor="c", text = self.titeles.DiodeState, bg="light gray" , fg = "green", height=1, width=20, name = "contr_diod_state" )
        DiodeState.place(x=384,y=65,width=127)
        
        # Cryo liquides level --------------------------------------------------------------------------
        CryoLevelFrame = LabelFrame(self, relief=RAISED, borderwidth = 1,  text = self.titeles.CryoLevel, name="cryo_level")
        CryoLevelFrame.place(height=490, width=150, x=530, y=20)
        
        # Progress bar widget
        CryoLiquidesLevel = Progressbar(CryoLevelFrame, orient=VERTICAL, length=410,  mode='determinate', name="cryo_level_bar")
        CryoLiquidesLevel.place(x=60, y=30)
        FullTankShow   = tk.Label(CryoLevelFrame, text = "100 % ")
        FullTankShow.place(x=20,y=20)
        MiddleTankShow = tk.Label(CryoLevelFrame, text = " 50 % ")
        MiddleTankShow.place(x=20,y=220)
        EmptyTankShow  = tk.Label(CryoLevelFrame, text = "  0 % ")
        EmptyTankShow.place(x=20,y=430)
        
        # Timer for communication start
        self.COMConnection = None
        def background_task(Period, Handle):
            while not background_task.cancelled:
                Handle()
                time.sleep(Period)
        background_task.cancelled = False
        self.t = Thread(target=background_task, args = (1, self.CommunicationHandle))
        self.t.start()
        


    def Create_InitCommunication(self):
        
        # THE CLUE
        self.wm_attributes("-disabled", True)

        # Creating the toplevel dialog
        self.toplevel_dialog = tk.Toplevel(self)
        self.toplevel_dialog.minsize(400, 250)
        self.toplevel_dialog.title(self.titeles.Interface_Configuration)

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
        InputCOMPortLabel = Label(self.toplevel_dialog, text = self.titeles.COM_Port_Selection)
        InputCOMPortLabel.pack()
        InputCOMPortLabel.place(x=20,y=10)
        InputCOMPort = OptionMenu(self.toplevel_dialog, COMPort, *COMPortOptions)
        InputCOMPort.pack(anchor = NW)
        InputCOMPort.place(x=20,y=40)
        
        BoudRateOptions = [2400, 4800, 9600, 14400, 19200]
        BoudRate = IntVar()
        BoudRate.set( 9600)
        InputBoudRateLabel = Label(self.toplevel_dialog, text = self.titeles.Bauderate_Selection)
        InputBoudRateLabel.pack()
        InputBoudRateLabel.place(x=200,y=10)
        InputBoudRate = OptionMenu(self.toplevel_dialog, BoudRate, *BoudRateOptions)
        InputBoudRate.pack(anchor = SE)
        InputBoudRate.place(x=200,y=40)
        
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
                self.COMConnection = None
                print("Can't set COM Port:{}\n".format(str(e)))

    def Close_InitCommunication(self):
        # IMPORTANT!
        self.wm_attributes("-disabled", False) # IMPORTANT!
        self.toplevel_dialog.destroy()
        # Possibly not needed, used to focus parent window again
        self.deiconify() 

    def UpdateVariables(self):
        self.Treal.value = self.Regulator.Treal
        self.Tset.value = self.Regulator.Tset
        self.Tcur_set.value = self.Regulator.Tcur_set
        self.Ureal.value = self.Regulator.Ureal
        
        self.D_T.value = self.Regulator.D_T
        self.D_t.value = self.Regulator.D_t
        self.Kprop.value = self.Regulator.Kprop
        self.Kdiff.value = self.Regulator.Kdiff
        # -------------------------------------------------------------
        self.SetOrScanState.set(int(self.Regulator.SetOrScanState))
        self.CelseOrKelvin.value = self.Regulator.CelseOrKelvin
        self.CryoLiquidesLevelMeasureOn.value = self.Regulator.CryoLiquidesLevelMeasureOn
        # -------------------------------------------------------------

    def UpdateVisuals(self):
        
        if (self.Focused == None or ((self.Focused != self.nametowidget(".pid_configs.scan_needed")) and (self.Focused != self.nametowidget(".pid_configs.set_needed")))):
            if (self.SetOrScanState.value > 0):
                self.nametowidget(".settingmode.scan_needed").config(state = "active")
                self.nametowidget(".settingmode.set_needed").config(state = "normal")
            else:
                self.nametowidget(".settingmode.scan_needed").config(state = "normal")
                self.nametowidget(".settingmode.set_needed").config(state = "active")

        self.nametowidget(".settingmode.scan_needed").update()
        self.nametowidget(".settingmode.set_needed").update()


        if (self.Focused == None or self.Focused != self.nametowidget(".pid_configs.kprop")):
            WorkStr = self.Kprop.value.__str__()
            self.nametowidget(".pid_configs.kprop").delete(0, END)
            self.nametowidget(".pid_configs.kprop").insert(END, WorkStr)

        if (self.Focused == None or self.Focused != self.nametowidget(".pid_configs.kdiff")):
            WorkStr = self.Kdiff.value.__str__()
            self.nametowidget(".pid_configs.kdiff").delete(0, END)
            self.nametowidget(".pid_configs.kdiff").insert(END, WorkStr)

        if (self.Focused == None or self.Focused != self.nametowidget(".temperature.tset")):
            WorkStr = self.Regulator.GetTemperatureString(self.Tset.value, True)
            self.nametowidget(".temperature.tset").delete(0, END)
            self.nametowidget(".temperature.tset").insert(END, WorkStr)
        
        if (self.Focused == None or self.Focused != self.nametowidget(".temperature.treal")):
            WorkStr = self.Regulator.GetTemperatureString(self.Treal.value, True)
        
        self.nametowidget(".temperature.treal").config(text = WorkStr)

        if (self.Focused == None or self.Focused != self.nametowidget(".scan_configs.d_T")):
            WorkStr = self.Regulator.GetTemperatureString(self.D_T.value, False)
            self.nametowidget(".scan_configs.d_T").delete(0, END)
            self.nametowidget(".scan_configs.d_T").insert(END, WorkStr)

        if (self.Focused == None or self.Focused != self.nametowidget(".scan_configs.d_t")):
            WorkStr = self.Regulator.GetTimeString(self.D_t.value)
            self.nametowidget(".scan_configs.d_t").delete(0, END)
            self.nametowidget(".scan_configs.d_t").insert(END, WorkStr)
        
        #self.nametowidget(".cryo_level.cryo_level_bar")['value'] = self.L_Level
        if (not self.CryoLiquidesLevelMeasureOn.get()):
            self.nametowidget(".cryo_level.cryo_level_bar")['value'] = 0
            #self.nametowidget(".cryo_level").enable(False)
        else:
            self.nametowidget(".cryo_level.cryo_level_bar")['value'] = (self.Regulator.L_Level)
            # self.nametowidget(".cryo_level").enable(True)
            
        #if not (hasattr(self.COMConnection, 'is_open') and (self.COMConnection.isOpen())):
        if (hasattr(self.COMConnection, 'is_open') and (self.COMConnection.isOpen())):
            self.nametowidget(".status_frame.connection_state").config(fg="red")
            self.nametowidget(".status_frame.heater_state").config(fg="black")
            self.nametowidget(".status_frame.cooler_state").config(fg="black")
            self.nametowidget(".status_frame.contr_diod_state").config(fg="black")
        else:
            self.nametowidget(".status_frame.connection_state").config(fg="green")
            if (self.HeaterError):
                self.nametowidget(".status_frame.heater_state").config(fg="red")
            else:
                self.nametowidget(".status_frame.heater_state").config(fg="green")
            
            if (self.CoolerError):
                self.nametowidget(".status_frame.cooler_state").config(fg="red")
            else:
                self.nametowidget(".status_frame.cooler_state").config(fg="green")
            
            if (self.ControlDiodeError):
                self.nametowidget(".status_frame.contr_diod_state").config(fg="red")
            else:
                self.nametowidget(".status_frame.contr_diod_state").config(fg="green")
               
             
            if TRUE:#(self.CryoLiquidesLevelMeasureOn):
                self.nametowidget(".cryo_level.cryo_level_bar")["value"] = 75#.update(self.CryoLevel)
            else:
                self.nametowidget(".cryo_level.cryo_level_bar")["value"] = 0
            
            
if __name__ == "__main__":
    app = K45_Comm()
    app.mainloop()