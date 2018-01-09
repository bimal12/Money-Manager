"""Module that will contain all of the tkinter classes for the app"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename


class FinanceApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Finance App")
        # self.configure(background="blue")

        container = tk.Frame(self)
        container.lift()
        self.attributes('-topmost', True)

        frame = StartFrame(self)
        frame.tkraise()
        self.after_idle(self.attributes, '-topmost',False)

    def destroy_window(self):
        self.quit()
        print("Goodbye")
        self.destroy()


class StartFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        ttk.Label(parent, text="Welcome to the Finance App").grid(column=0,row=0, columnspan=2)
        # LabelBox(parent)


class LabelBox(ttk.LabelFrame):
    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text="Label in a Frame")
        self.grid(column=0, row=0, sticky='e')
        ttk.Label(self, text="Test Label").grid(column=0, row=0)


class CheckBox(tk.Frame):
    """Create check boxes for all the accounts that are present"""
    def __init__(self, parent, data):
        selection = tk.StringVar()
        # check_one = tk.Checkbutton(parent, text="Check", variable=selection)
        # check_one.select()
        # check_one.grid(column=0, row=1)
        self.var= {}
        self.check_o= {}
        for a in data:
            self.var[a] = tk.StringVar()
            self.check_o[a] = tk.Checkbutton(parent, text=str(a), variable=self.var[a], command=lambda b=a: self.cb(b))
            self.check_o[a].select()
            self.check_o[a].grid(column=0, row=data.index(a)+2)

    def cb(self, event):
        print("Value of {} is {} ".format(event, self.var[event].get()))


class DropDown(ttk.Combobox):
    def __init__(self, parent):
        number = tk.StringVar()
        ttk.Combobox.__init__(self,parent, width=12, textvariable=number, state='readonly')
        self['values'] = ('1', '2', '3')
        self.grid()

class AddTransactionButton(tk.Button):
    def __init__(self, parent):
        tk.Button.__init__(self, parent, text="Add Data")
        self.grid(column=1)


if __name__ == '__main__':
    app = FinanceApp()
    # app.protocol('WM_DELETE_WINDOW', app.destroyWindow())
    CheckBox(app, ['a','b','c'])
    a = DropDown(app)
    AddTransactionButton(app).grid(row=a.grid_info()['row'])
    print(a.grid_info()['row'])

    app.mainloop()


