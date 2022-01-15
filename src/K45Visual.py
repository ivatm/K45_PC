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

class K45_Comm(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("K45")
        self.minsize(1000, 700)

        # --------------------------------------------------------------------------
        SetOrScanState = BooleanVar()
        CelseOrKelvin = BooleanVar()
        CryoLiquidesLevelMeasureOn = BooleanVar()
        Treal = DoubleVar()
        Tset = DoubleVar()
        Tcur_set = DoubleVar()
        D_T = DoubleVar()
        D_t = DoubleVar()
        Ureal = DoubleVar()
        Kprop = IntVar()
        Kdiff = IntVar()
        L_Level = IntVar()
        
        # SetOrScanState, CelseOrKelvin , CryoLiquidesLevelMeasureOn 
        Regulator = K45_Unit(SetOrScanState.get(), CelseOrKelvin.get(), CryoLiquidesLevelMeasureOn.get())

        # --------------------------------------------------------------------------
        K45MenuButton = Menu(self)
        K45MenuButton.add_command(label="Connection", command = self.Create_InitCommunication)
        K45MenuButton.add_command(label="Sensor")
        K45MenuButton.add_command(label="Quit!", command=self.quit)
        self.config(menu=K45MenuButton)

        # Mode Selection and system state --------------------------------------------------------------------------
        ModeFrame = LabelFrame(self, relief=RAISED, borderwidth = 1, text = "Mode selection")
        ModeFrame.pack()
        ModeFrame.place(height=100, width=510, x=10, y=20)
        
        SetScanSelection_Rb1 = Radiobutton(ModeFrame, text = "Set", variable = SetOrScanState, value = FALSE)
        SetScanSelection_Rb2 = Radiobutton(ModeFrame, text = "Scan", variable = SetOrScanState, value = TRUE)
        SetScanSelection_Rb1.pack()
        SetScanSelection_Rb2.pack()
        SetScanSelection_Rb1.place(x=0,y=20)
        self.update()
        WorkVar = SetScanSelection_Rb1.winfo_width()
        SetScanSelection_Rb2.place(x=SetScanSelection_Rb1.winfo_width(),y=20)
        
        
        # On Scan mode variables --------------------------------------------------------------------------
        ScanFrame = LabelFrame(self, relief=RAISED, borderwidth = 1, text = "Scan configs")
        ScanFrame.pack()
        ScanFrame.place(height=100, width=510, x=10, y=125)
        
        TimeStepLabel = Label(ScanFrame, text = "dt - Time Step")
        TimeStepLabel.pack()
        TimeStepLabel.place(x=0,y=20)
        TimeStepEntry = Entry(ScanFrame)
        TimeStepEntry.pack()
        TimeStepEntry.place(x=0,y=40)
        
        TemperatureStepLabel = Label(ScanFrame, text = "dT - Temperature Step")
        TemperatureStepLabel.pack()
        TemperatureStepLabel.place(x=150,y=20)
        TemperatureStepEntry = Entry(ScanFrame)
        TemperatureStepEntry.pack()
        TemperatureStepEntry.place(x=150,y=40) 
        
        # Current state of Temperature --------------------------------------------------------------------------
        TemperatureFrame = LabelFrame(self, relief=RAISED, borderwidth = 1, text = "Temperature")
        TemperatureFrame.pack()
        TemperatureFrame.place(height=100, width=510, x=10, y=230)
        
        TempRealLabel = Label(TemperatureFrame, text = "Current Temperature")
        TempRealLabel.pack()
        TempRealLabel.place(x=0,y=20)
        TempRealEntry = Entry(TemperatureFrame)
        TempRealEntry.pack()
        TempRealEntry.place(x=0,y=40)
        
        TempSetLabel = Label(TemperatureFrame, text = "Set Temperature")
        TempSetLabel.pack()
        TempSetLabel.place(x=150,y=20)
        TempSetEntry = Entry(TemperatureFrame)
        TempSetEntry.pack()
        TempSetEntry.place(x=150,y=40)
        
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

        COMPort = StringVar()
        InputCOMPort = Entry(self.toplevel_dialog, variable = COMPort, text = "COM Port")
        InputCOMPort.pack(anchor = NW)
        InputCOMPort.place(x=0,y=40)
        
        BoudRate = IntVar()
        InputBoudRate = Entry(self.toplevel_dialog, variable = BoudRate, text = "Boudrate")
        InputBoudRate.pack()

    def Close_InitCommunication(self):

        # IMPORTANT!
        self.wm_attributes("-disabled", False) # IMPORTANT!

        self.toplevel_dialog.destroy()

        # Possibly not needed, used to focus parent window again
        self.deiconify() 

if __name__ == "__main__":
    app = K45_Comm()
    app.mainloop()