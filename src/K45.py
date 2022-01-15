'''
Created on 23 жовт. 2021

@author: Oliva
'''

#import TxRx_K45
from tkinter import *
from tkinter.ttk import *
from tkinter.tix import LabelEntry
import time




def K45Connect():  
    top = Toplevel(root)
    COMPort = StringVar()
    InputCOMPort = LabelEntry(top, variable = COMPort, text = "COM Port")
    InputCOMPort.pack(anchor = NW)

    BoudRate = IntVar()
    InputBoudRate = LabelEntry(top, variable = BoudRate, text = "Boudrate")
    InputBoudRate.pack()
    top.update()

    top.mainloop()
    


    
if __name__ == '__main__':

    root = Tk( )
    root.title("K45")
    root.geometry("1000x500")

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

    # --------------------------------------------------------------------------
    K45MenuButton = Menu(root)
    K45MenuButton.add_command(label="Connection", command=K45Connect)
    K45MenuButton.add_command(label="Sensor")
    K45MenuButton.add_command(label="Quit!", command=root.quit)
    root.config(menu=K45MenuButton)

    # Mode Selection and system state --------------------------------------------------------------------------
    ModeFrame = LabelFrame(root, relief=RAISED, borderwidth = 1)
    ModeFrame.pack()
    ModeFrame.place(height=50, width=510, x=10, y=20)
    
    ModeLabel = Label(ModeFrame, text = "Mode selection")
    ModeLabel.pack(anchor=NW)
    
    
    SetScanSelection_Rb1 = Radiobutton(ModeFrame, text = "Set", variable = SetOrScanState, value = FALSE)
    SetScanSelection_Rb2 = Radiobutton(ModeFrame, text = "Scan", variable = SetOrScanState, value = TRUE)
    SetScanSelection_Rb1.pack()
    SetScanSelection_Rb2.pack()
    SetScanSelection_Rb1.place(x=0,y=20)
    root.update()
    WorkVar = SetScanSelection_Rb1.winfo_width()
    SetScanSelection_Rb2.place(x=SetScanSelection_Rb1.winfo_width(),y=20)
    

    # On Scan mode variables --------------------------------------------------------------------------
    ScanFrame = LabelFrame(root, relief=RAISED, borderwidth = 1)
    ScanFrame.pack()
    ScanFrame.place(height=100, width=510, x=10, y=80)
    
    ScanLabel = Label(ScanFrame, text = "Scan configs")
    ScanLabel .pack(anchor=NW)

    
    TimeStepLabel = Label(ScanFrame, text = "dt - Time Step")
    TimeStepLabel.pack()
    TimeStepLabel.place(x=0,y=20)
    TimeStepEntry = Entry(ScanFrame)
    TimeStepEntry.pack()
    TimeStepEntry.place(x=0,y=40)
    
    TemperatureStepLabel = Label(ScanFrame, text = "dT - Temperature Step")
    TemperatureStepLabel.pack()
    TemperatureStepEntry = Entry(ScanFrame)
    TemperatureStepEntry.pack()

    # Current state of Temperature --------------------------------------------------------------------------
    TemperatureFrame = LabelFrame(root, relief=RAISED, borderwidth = 1)
    TemperatureFrame.pack()
    TemperatureFrame.place(height=100, width=510, x=10, y=200)
    
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
    CryoLevelFrame = LabelFrame(root, relief=RAISED, borderwidth = 1)
    CryoLevelFrame.pack()
    CryoLevelFrame.place(height=300, width=150, x=550, y=20)
    CryoLevelFrameName = Label(CryoLevelFrame, text = "Level of Cryo Liquid")
    CryoLevelFrameName .pack(anchor=N)
    
    # Progress bar widget
    CryoLiquidesLevel = Progressbar(CryoLevelFrame, orient=VERTICAL, length=100, mode='determinate')
    #CryoLiquidesLevel.pack(pady = 10)
    CryoLiquidesLevel.pack(expand=True)
    CryoLiquidesLevel['value'] = 50

    #CryoLiquidesLevel = Scale( CryoLevelFrame, variable = L_Level, 
    #       from_ = 1, to = 100, 
    #       orient = VERTICAL)   
    L_Level = 55
    CryoLiquidesLevel.place(x=25,y=40)
    CryoLiquidesLevel.pack(anchor=CENTER)

    # Variables --------------------------------------------------------------------------
    DataFrame = LabelFrame(root, relief=RAISED, borderwidth = 1)
    DataFrame.pack()
    DataFrame.place(height=150, width=510, x=10, y=320)
    
    SensorVoltageLabel = Label(DataFrame, text = "Sensor Voltage")
    SensorVoltageLabel.pack( anchor = NW)
    SensorVoltageEntry = Entry(DataFrame)
    SensorVoltageEntry.pack( anchor = NW)
    
    KpropLabel = Label(DataFrame, text = "Kprop")
    KpropLabel.pack( anchor = NW)
    KpropEntry = Entry(DataFrame)
    KpropEntry.pack( anchor = NW)
    
    KdiffLabel = Label(DataFrame, text = "Kdiff")
    KdiffLabel.pack( anchor = NW)
    KdiffEntry = Entry(DataFrame)
    KdiffEntry.pack( anchor = NW)
    

    root.mainloop( )