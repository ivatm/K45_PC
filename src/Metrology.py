'''
Created on 12.11.2023

@author: aivashchenko
'''
# Python 3+
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from K45Unit import K45_Unit

class Metrology(tk.Tk):
    '''
    The class involves and calls all procedures to calibrate the measure/calibrating devices in K45 module
    '''
    
    Password = ""

    def __init__(self, K45_Comm):
        '''
        Constructor
        '''
        tk.Tk.__init__(self)
        self.title("Calibration")
        self.minsize(820, 550)
        self.configure(bg='light gray')


        self.NullValue = IntVar(self, name = "null_value")
        self.NullValue.value = 0
        self.K_1_Corr  = IntVar(self, name = "k1_corr_value")
        self.K_1_Corr.value = 1
        self.K_32_Corr = IntVar(self, name = "k32_corr_value")
        self.K_32_Corr.value = 1
        self.SetCoef   = IntVar(self, name = "SetCoef")
        
        self.I_10mkA_Code  = IntVar(self, name = "10mka_code_value")
        self.I_10mkA_Code.value = 0x1000
        self.I_25mkA_Code  = IntVar(self, name = "25mka_code_value")
        self.I_25mkA_Code.value = 0x2000
        self.I_100mkA_Code = IntVar(self, name = "100mka_code_value")
        self.I_100mkA_Code.value = 0x3000
        self.I_250mkA_Code = IntVar(self, name = "250mka_code_value")
        self.I_250mkA_Code.value = 0x4000
        self.SelectCurrent = IntVar(self, name = "SelectCurrent")
        self.SelectCurrent.set(1)
        #------------------------------------------------------------------------------------------------------
        
        def SelectCurrentCommand(NewValue):
            self.SelectCurrent.set(NewValue)
            print(self.SelectCurrent.get())

        def SetCoefCommand(NewValue):
            self.SetCoef.set(NewValue)
            print(self.SetCoef.get())
        #------------------------------------------------------------------------------------------------------

        ADCFrame = LabelFrame(self, relief=RAISED, borderwidth = 1,  text = "ADC Frame", name="adc_frame", style = "Red.TLabelframe" )
        ADCFrame.place(height=150, width=800, x=10, y=20)

        for i in range(10):
            ADCFrame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            ADCFrame.grid_columnconfigure(i, weight=1)


        NullCorrection = Label(ADCFrame, text = "Null correction -1..+1 мВ")
        NullCorrection.grid(column=0, row=0 )#place(x=10,y=0)
        ADCNullEnter = Entry(ADCFrame, name="null_correction")
        ADCNullEnter.insert(END, str(self.NullValue.value))
        ADCNullEnter.grid(column=0, row=1  )#place(x=10,width=95,y=20) 
        ADCNullEnter.bind('<Button-1>', SelectFocus)
        ADCNullEnter.bind('<Return>', ReleaseFocus)

        K1_Correction = Label(ADCFrame, text = "Correction K=1 -0.9..+1.1")
        K1_Correction.grid(column=1, row=0 )#place(x=320,y=0)
        K1_Enter = Entry(ADCFrame, name="k1_correction")
        K1_Enter.insert(END, str(self.K_1_Corr.value))
        K1_Enter.grid(column=1, row=1 )#place(x=320,width=95,y=20) 
        K1_Enter.bind('<Button-1>', SelectFocus)
        K1_Enter.bind('<Return>', ReleaseFocus)

        K32_Correction = Label(ADCFrame, text = "Correction K=32 -0.9..+1.1")
        K32_Correction.grid(column=2, row=0 )#place(x=600,y=0)
        K32_Enter = Entry(ADCFrame, name="k32_correction")
        K32_Enter.insert(END, str(self.K_32_Corr.value))
        K32_Enter.grid(column=2, row=1 )#place(x=600,width=95,y=20) 
        K32_Enter.bind('<Button-1>', SelectFocus)
        K32_Enter.bind('<Return>', ReleaseFocus)

        SetCoef1_Rb  = Radiobutton(ADCFrame, text = "K = 1",  variable = self.SetCoef, value = 0, name = "set_K_1",   command = lambda: SetCoefCommand(0))
        SetCoef32_Rb = Radiobutton(ADCFrame, text = "K = 32", variable = self.SetCoef, value = 1, name = "set_K_32" , command = lambda: SetCoefCommand(1))
        self.SetCoef.set(0)

        SetCoef1_Rb.grid(column=1, row=2 )#.place(x=320,y=45)
        SetCoef32_Rb.grid(column=2, row=2 )#.place(x=600,y=45)
        SetCoef1_Rb.update()
        SetCoef32_Rb.update()

        #------------------------------------------------------------------------------------------------------
        DACFrame = LabelFrame(self, relief=RAISED, borderwidth = 1,  text = "DAC Frame", name="dac_frame", style = "Red.TLabelframe")
        DACFrame.place(height=150, width=800, x=10, y=200)
        for i in range(10):
            DACFrame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            DACFrame.grid_columnconfigure(i, weight=1)

        DACCode_10mk = Label(DACFrame, text = "Set 10 mkA")
        DACCode_10mk.grid(column=0, row=0 )#.place(x=10,y=0)
        Code_10mkEnter = Entry(DACFrame, name="set_10mka")
        Code_10mkEnter.insert(END, str(self.I_10mkA_Code.value))
        Code_10mkEnter.grid(column=0, row=1 )#.place(x=10,width=95,y=20) 
        Code_10mkEnter.bind('<Button-1>', SelectFocus)
        Code_10mkEnter.bind('<Return>', ReleaseFocus)

        DACCode_25mk = Label(DACFrame, text = "Set 25 mkA")
        DACCode_25mk.grid(column=1, row=0 )#.place(x=210,y=0)
        Code_25mkEnter = Entry(DACFrame, name="set_25mka")
        Code_25mkEnter.insert(END, str(self.I_25mkA_Code.value))
        Code_25mkEnter.grid(column=1, row=1 )#.place(x=210,width=95,y=20) 
        Code_25mkEnter.bind('<Button-1>', SelectFocus)
        Code_25mkEnter.bind('<Return>', ReleaseFocus)

        DACCode_100mk = Label(DACFrame, text = "Set 100 mkA")
        DACCode_100mk.grid(column=2, row=0 )#.place(x=420,y=0)
        Code_100mkEnter = Entry(DACFrame, name="set_100mka")
        Code_100mkEnter.insert(END, str(self.I_100mkA_Code.value))
        Code_100mkEnter.grid(column=2, row=1 )#.place(x=420,width=95,y=20) 
        Code_100mkEnter.bind('<Button-1>', SelectFocus)
        Code_100mkEnter.bind('<Return>', ReleaseFocus)

        DACCode_250mk = Label(DACFrame, text = "Set 250 mkA")
        DACCode_250mk.grid(column=3, row=0 )#.place(x=660,y=0)
        Code_250mkEnter = Entry(DACFrame, name="set_250mka")
        Code_250mkEnter.insert(END, str(self.I_250mkA_Code.value))
        Code_250mkEnter.grid(column=3, row=1 )#.place(x=660,width=95,y=20) 
        Code_250mkEnter.bind('<Button-1>', SelectFocus)
        Code_250mkEnter.bind('<Return>', ReleaseFocus)

        SetCurrent_10mkA  = Radiobutton(DACFrame, text = "I = 10 mkA",  variable = self.SelectCurrent, value = 0, name = "select_10mka" ,  command = lambda: SelectCurrentCommand(0))
        SetCurrent_25mkA  = Radiobutton(DACFrame, text = "I = 25 mkA",  variable = self.SelectCurrent, value = 1, name = "select_20mka" ,  command = lambda: SelectCurrentCommand(1))
        SetCurrent_100mkA = Radiobutton(DACFrame, text = "I = 100 mkA", variable = self.SelectCurrent, value = 2, name = "select_100mka" , command = lambda: SelectCurrentCommand(2))
        SetCurrent_250mkA = Radiobutton(DACFrame, text = "I = 250 mkA", variable = self.SelectCurrent, value = 3, name = "select_250mka" , command = lambda: SelectCurrentCommand(3))

                
        SetCurrent_10mkA.grid(column=0, row=3 )#.place(x=10,y=45)
        SetCurrent_25mkA.grid(column=1, row=3 )#.place(x=210,y=45)
        SetCurrent_100mkA.grid(column=2, row=3 )#.place(x=420,y=45)
        SetCurrent_250mkA.grid(column=3, row=3 )#.place(x=660,y=45)
        SetCurrent_10mkA.update()
        SetCurrent_25mkA.update()
        SetCurrent_100mkA.update()
        SetCurrent_250mkA.update()
# ---------------------------------------------------------------------------------------------------------------------------------------        
        ButtonsFrame = Frame(self, relief=RAISED, borderwidth = 1,  name="buttons_frame" )
        ButtonsFrame.place(height=150, width=800, x=10, y=380)

        for i in range(2):
            ButtonsFrame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            ButtonsFrame.grid_columnconfigure(i, weight=1)

        BtnSend = Button(ButtonsFrame, text="Ok", command=AcceptConfig)
        #BtnSend.pack(side="top")
        BtnSend.grid(column=1, row=1 )#.place(width=70,x=120, y=9)

        BtnCancel = Button(ButtonsFrame, text="Cancel", command=CancelConfig)
        #BtnCancel.pack(side="top")
        BtnCancel.grid(column=2, row=1 )#.place(width=70,x=220, y=9)

# -----------------------------------------------------------------------------------------------------------------------------------------

        self.Focused = None
        def SelectFocus(event):
            self.Focused = event.widget
            
        def ReleaseFocus(event):
            if  (hasattr(K45_Comm.COMConnection, 'is_open') and (K45_Comm.COMConnection.isOpen()) and ((not hasattr(self, 'SensDataSender')) or (not self.SensDataSender.Transmitting))):
                Variable = str(self.Focused).split(".")[-1]
                if Variable == "null_value":
                    K45_Comm.Regulator.RemoteCalibrationCommand(0, self.Focused.get() , self.COMConnection)
                elif Variable == "k1_corr_value":
                    K45_Comm.Regulator.RemoteCalibrationCommand(1, self.Focused.get() , self.COMConnection)
                elif Variable == "k32_corr_value":
                    K45_Comm.Regulator.RemoteCalibrationCommand(2, self.Focused.get() , self.COMConnection)
                elif Variable == "10mka_code_value":
                    K45_Comm.Regulator.RemoteCalibrationCommand(3, self.Focused.get() , self.COMConnection)
                elif Variable == "25mka_code_value":
                    K45_Comm.Regulator.RemoteCalibrationCommand(4, self.Focused.get() , self.COMConnection)
                elif Variable == "100mka_code_value":
                    K45_Comm.Regulator.RemoteCalibrationCommand(5, self.Focused.get() , self.COMConnection)
                elif Variable == "250mka_code_value":
                    K45_Comm.Regulator.RemoteCalibrationCommand(6, self.Focused.get() , self.COMConnection)
                else:
                    pass

        def AcceptConfig():
            K45_Comm.Regulator.RemoteCalibrationCompletition(self.COMConnection)
            
        def CancelConfig():
            K45_Comm.Regulator.RemoteCalibrationStartCancel(self.COMConnection)


