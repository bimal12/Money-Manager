"""Module that will contain all of the tkinter classes for the app"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import lib.graphs


class StartFrame(tk.Frame):
    def __init__(self, parent, controller, **options):
        tk.Frame.__init__(self, parent, **options)
        self.grid(column=0, row=0)
        self.parent = parent
        self.controller = controller
        tk.Label(self, text="Welcome to the Finance App").grid(column=0,row=0, columnspan=2)
        self.add_dropdown()
        self.add_trans_button()
        self.check_box = {}
        self.var = list()
        self.var_check = {}

        self.create_checkbox()


    def create_checkbox(self):
        for a in self.var:
            # Could store variable and box as tuple?
            self.var_check[a] = tk.StringVar()
            self.check_box[a] = tk.Checkbutton(self, text=str(a), variable=self.var_check[a], command=lambda b=a:self.cb(b))
            self.check_box[a].select()
            self.check_box[a].grid(column=0, row=self.var.index(a)+2, sticky='W', padx=1)

    def update_checkbox(self, data=None):
        if data is not None:
            self.var = list(data)
        self.create_checkbox()
        self.update_dropdown()

    def cb(self, event):
        print("Value of {} is {} ".format(event, self.var_check[event].get()))

    def add_dropdown(self):
        self.dd = tk.StringVar()
        self.drop_data = []
        self.drop = ttk.OptionMenu(self, variable=self.dd, *self.drop_data)
        self.drop.grid()
        # self.drop['values'] = self.drop_data
        # self.drop.grid()

    def update_dropdown(self, data=None):
        if data is not None:
            self.drop_data = tuple(data)
        self.dd.set('')
        self.drop['menu'].delete(0,'end')
        for item in self.drop_data:
            self.drop['menu'].add_command(label=item, command=tk._setit(self.dd, item))
        self.drop.grid(row=2+len(self.var))
        self.update_button()


    def add_trans_button(self):
        self.button = tk.Button(self, text="Add Data", command=self.get_account)
        # The line above with lambda may need to be edited when adding accounts
        self.button.grid(column=1, row=self.drop.grid_info()['row'])

    def update_button(self):
        self.button.grid(row=self.drop.grid_info()['row'])

    def get_account(self):
        print(self.dd.get())
        if self.dd.get() is not '':
            self.var.append(self.dd.get())
            self.update_checkbox()
        # self.var = self.var


if __name__ == '__main__':
    root = tk.Tk()
    app = StartFrame(root,controller=None)
    root.mainloop()

    # app = FinanceApp()
    # # app.protocol('WM_DELETE_WINDOW', app.destroyWindow())
    # CheckBox(app, ['a','b','c','d'])
    # data = ('1', '2', '3')
    # a = DropDown(app, data)
    # AddTransactionButton(app, a)
    # f = Figure(figsize=(4, 4), dpi=100)
    # b = f.add_subplot(1, 1, 1)
    # canvas = FigureCanvasTkAgg(f, app)
    # canvas.show()
    # canvas.get_tk_widget().grid(column=4, row=0, rowspan=9)
    # print(a.grid_info()['row'])
    #

