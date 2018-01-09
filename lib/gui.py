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


# class FinanceApp(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#
#         tk.Tk.wm_title(self, "Finance App")
#         # self.configure(background="blue")
#
#         container = tk.Frame(self)
#         container.lift()
#         self.attributes('-topmost', True)
#
#         # frame = StartFrame(self)
#         # frame.tkraise()
#         self.after_idle(self.attributes, '-topmost',False)
#
#     def destroy_window(self):
#         self.quit()
#         print("Goodbye")
#         self.destroy()


class StartFrame(tk.Frame):
    def __init__(self, parent, controller, **options):
        tk.Frame.__init__(self, parent, **options)
        self.grid(column=0, row=0)
        self.parent = parent
        self.controller = controller
        tk.Label(self, text="Welcome to the Finance App").grid(column=0,row=0, columnspan=2)
        self.drop_data = ()
        self.check_box = {}
        self.var = list()
        self.var_check = {}

        self.add_dropdown()
        self.create_checkbox()


    @property
    def var(self):
        return self.__var

    @var.setter
    def var(self,data):
        self.__var = data
        self.create_checkbox()
        print(data)

    def create_checkbox(self):

        for a in self.var:
            # Could store variable and box as tuple?
            self.var_check[a] = tk.StringVar()
            self.check_box[a] = tk.Checkbutton(self, text=str(a), variable=self.var_check[a], command=lambda b=a:self.cb(b))
            self.check_box[a].select()
            self.check_box[a].grid(column=0, row=self.var.index(a)+2, sticky='n')

    def cb(self, event):
        print("Value of {} is {} ".format(event, self.var_check[event].get()))


    def update_check(self):
        pass

    def add_dropdown(self):
        self.dd = tk.StringVar()
        self.drop = ttk.OptionMenu(self, variable=self.dd, *self.drop_data)
        self.drop.grid()
        # self.drop['values'] = self.drop_data
        # self.drop.grid()

    def update_dropdown(self):
        self.dd.set('')
        self.drop['menu'].delete(0,'end')
        for item in self.drop_data:
            self.drop['menu'].add_command(label=item, command=tk._setit(self.dd, item))


    def add_trans_button(self):
        self.button = tk.Button(self, text="Add Data", command=self.get_account)
        # self.drop_down = dropdown
        # The line above with lambda may need to be edited when adding accounts
        self.button.grid(column=1, row=self.drop.grid_info()['row'])

    def get_account(self):
        print(self.dd.get())
        self.var.append(self.dd.get())
        self.var = self.var
#
# class LabelBox(ttk.LabelFrame):
#     def __init__(self, parent):
#         ttk.LabelFrame.__init__(self, parent, text="Label in a Frame")
#         self.grid(column=0, row=0, sticky='e')
#         ttk.Label(self, text="Test Label").grid(column=0, row=0)

#
# class DropDown(ttk.Combobox):
#     def __init__(self, parent, data):
#         number = tk.StringVar()
#         ttk.Combobox.__init__(self,parent, width=12, textvariable=number, state='readonly')
#         self['values'] = data
#         self.grid()

#
# class AddTransactionButton(tk.Button):
#     def __init__(self, parent, dropdown):
#         tk.Button.__init__(self, parent, text="Add Data", command=lambda: self.get_account(dropdown))
#         self.drop_down = dropdown
#         # The line above with lambda may need to be edited when adding accounts
#         self.grid(column=1, row=dropdown.grid_info()['row'])
#
#     @staticmethod
#     def get_account(drop):
#         print(drop.get())


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

    # app.mainloop()


