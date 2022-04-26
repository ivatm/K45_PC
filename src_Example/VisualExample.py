'''
Created on 11 січ. 2022

@author: Oliva
'''

# Python 3+
import tkinter as tk
from tkinter import ttk
from tkinter import *
from msilib.schema import CheckBox

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.minsize(500, 500)
        self.button = ttk.Button(self, text="Call toplevel!", command=lambda: self.SetOrScanState.set(not self.SetOrScanState.get()))
        self.button.pack(side="top")

        self.SetOrScanState = IntVar()
        self.SetOrScanState.set(1)
        self.SetScanSelection_Rb1 = Radiobutton(self, text = "Set", 
                                   variable = self.SetOrScanState, value = 0, command=lambda: print(self.SetOrScanState.get()))
        self.SetScanSelection_Rb1.place(x=20,y=20)
        
        self.SetScanSelection_Rb2 = Radiobutton(self, text = "Scan", 
                                   variable = self.SetOrScanState, value = 1,  command=lambda: print(self.SetOrScanState.get()))
        self.SetScanSelection_Rb2.place(x=20,y=40)

        CheckBoxExample = Checkbutton(self, variable = self.SetOrScanState)
        CheckBoxExample.place(x=40,y=20)


    def Create_InitCommunication(self):

        # THE CLUE
        self.wm_attributes("-disabled", True)

        # Creating the toplevel dialog
        self.toplevel_dialog = tk.Toplevel(self)
        self.toplevel_dialog.minsize(600, 400)

        # Tell the window manager, this is the child widget.
        # Interesting, if you want to let the child window 
        # flash if user clicks onto parent
        self.toplevel_dialog.transient(self)

        # This is watching the window manager close button
        # and uses the same callback function as the other buttons
        # (you can use which ever you want, BUT REMEMBER TO ENABLE
        # THE PARENT WINDOW AGAIN)
        self.toplevel_dialog.protocol("WM_DELETE_WINDOW", self.Close_InitCommunication)

        self.toplevel_dialog_label = ttk.Label(self.toplevel_dialog, text='Do you want to enable my parent window again?')
        self.toplevel_dialog_label.pack(side='top')

        self.toplevel_dialog_yes_button = ttk.Button(self.toplevel_dialog, text='Yes', command=self.Close_InitCommunication)
        self.toplevel_dialog_yes_button.pack(side='left', fill='x', expand=True)

        self.toplevel_dialog_no_button = ttk.Button(self.toplevel_dialog, text='No')
        self.toplevel_dialog_no_button.pack(side='right', fill='x', expand=True)
        

    def Close_InitCommunication(self):

        # IMPORTANT!
        self.wm_attributes("-disabled", False) # IMPORTANT!

        self.toplevel_dialog.destroy()

        # Possibly not needed, used to focus parent window again
        self.deiconify() 


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()