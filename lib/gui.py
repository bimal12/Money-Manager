"""Module that will contain all of the tkinter classes for the app"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename

class FinanceApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Finance App")
        self.configure(background="blue")

        container = tk.Frame(self)
        container.lift()
        self.attributes('-topmost', True)

        frame = StartFrame(self)
        frame.tkraise()
        self.after_idle(self.attributes, '-topmost',False)

    def destroyWindow(self):
        self.quit()
        self.destroy()


class StartFrame(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        frame1 = CheckBox(parent)
        # frame1.grid()
        frame1.tkraise()


class CheckBox(ttk.LabelFrame):
    def __init__(self,parent):
        ttk.LabelFrame.__init__(self,parent,text="Label in a Frame")
        self.grid(column=0, row=0, sticky='e')
        ttk.Label(self, text="Test Label").grid(column=0, row=0)


if __name__ == '__main__':
    app = FinanceApp()
    # app.protocol('WM_DELETE_WINDOW', app.destroyWindow())

    app.mainloop()


