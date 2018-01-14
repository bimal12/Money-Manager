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
    """ Main View from which all other widgets will be properties of."""

    def __init__(self, parent, controller, **options):
        tk.Frame.__init__(self, parent, **options)
        self.grid(column=0, row=0)
        self.parent = parent
        self.controller = controller
        tk.Label(self, text="Welcome to the Finance App").grid(column=0, row=0, columnspan=2)
        self.add_option_menu()
        self.add_trans_button()
        self.check_box = {}
        self.var = list()
        self.var_check = {}

        self.create_checkbox()
        self.create_graph()

    def create_checkbox(self):  # This currently resets checkboxes
        """Creates the checkbox widget from row (2) onwards"""
        for a in self.var:
            # Could store variable and box as tuple?
            self.var_check[a] = tk.StringVar()
            self.check_box[a] = tk.Checkbutton(self, text=str(a), variable=self.var_check[a],
                                               command=lambda b=a: self.cb(b))
            self.check_box[a].select()
            self.check_box[a].grid(column=0, row=self.var.index(a) + 2, sticky='W', padx=1)

    def update_checkbox(self, data=None):
        """Method for updating the checkboxes with new data"""
        if data is not None:
            self.var = list(data)
        self.create_checkbox()
        self.update_option_menu()

    def cb(self, event):
        print("Value of {} is {} ".format(event, self.var_check[event].get()))

    def add_option_menu(self):
        """Creates the Option Menu under the checkboxes"""
        self.dd = tk.StringVar()
        self.drop_data = []
        self.drop = ttk.OptionMenu(self, variable=self.dd, *self.drop_data)
        self.drop.grid()
        # self.drop['values'] = self.drop_data
        # self.drop.grid()

    def update_option_menu(self, data=None):
        """Updates the Option Menu with the new list"""
        if data is not None:
            self.drop_data = tuple(data)
        self.dd.set('')
        self.drop['menu'].delete(0, 'end')
        for item in self.drop_data:
            self.drop['menu'].add_command(label=item, command=tk._setit(self.dd, item))
        self.drop.grid(row=2 + len(self.var))
        self.update_button()

    def add_trans_button(self):
        """Creates Add Data button next to the Option Menu"""
        self.button = tk.Button(self, text="Add Data", command=self.get_account)
        # The line above with lambda may need to be edited when adding accounts
        self.button.grid(column=1, row=self.drop.grid_info()['row'])

    def update_button(self):
        """Updates the position of the button when Option Menu moves"""
        self.button.grid(row=self.drop.grid_info()['row'])

    def get_account(self):
        print(self.dd.get())
        if self.dd.get() is not '':
            self.var.append(self.dd.get())
            self.update_checkbox()
            win = tk.Toplevel()
            message = 'This is the child window'
            tk.Label(win, text=message).grid()
            win.grab_set()

    def create_graph(self):
        self.figure = Figure(figsize=(8, 5), dpi=100)
        # self.([1, 2, 3, 4], [1, 2, 3, 4], label="TSB")
        self.canvas = FinanceGraph(self.figure, self.parent)
        self.parent.grid_rowconfigure(0,weight=1)
        self.parent.grid_columnconfigure(4, weight=1)
        # self.canvas.add.xticks(rotation='vertical')
        # self.canvas.add.plot([1, 2, 3, 4], [1, 2, 4, 4], label="TSB")
        # self.canvas.grid()

    def clear(self):
        self.canvas.clear()


# Create a seperate class for the graph camvas
class FinanceGraph(FigureCanvasTkAgg):
    """Creates the Canvas Figure that the view uses """
    def __init__(self, figure, parent, **options):
        FigureCanvasTkAgg.__init__(self, figure, parent, **options)
        self.figure = figure
        self.add = figure.add_subplot(111)

        self.show()
        self.get_tk_widget().grid(column=4, row=0, rowspan=9, sticky='nsew', pady=20)
        # self.figure.subplot.bottom : 0.15
        # self.get_tk_widget().rowconfigure(parent,weight=1)
        # self.toolbar = NavigationToolbar2TkAgg(self, parent)
        # self.toolbar.update()

    def clear(self):
        """Erase the plot."""
        self.add.clear()
        # self.figure.canvas.draw()


if __name__ == '__main__':
    root = tk.Tk()
    app = StartFrame(root, controller=None)

    root.mainloop()
