"""Module that will contain all of the tkinter classes for the app"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename

import matplotlib

from lib import autocomplete

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates

from matplotlib import style

style.use("ggplot")


class StartFrame(tk.Frame):
    """ Main View from which all other widgets will be properties of."""

    def __init__(self, parent, controller, **options):
        tk.Frame.__init__(self, parent, **options)
        self.grid(column=0, row=0)
        self.parent = parent
        self.controller = controller
        tk.Label(self, text="Welcome to the Test App").grid(column=0, row=0, columnspan=2, sticky='n')
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

    # If add new account build the new account window, if the account already exits
    # ask for the CSV file and add the data automatically to the db
    def get_account(self):
        print(self.dd.get())
        if self.dd.get() == 'Add New Account':
            win = AddDataWindow(self)
            win.grab_set()
            print('here')
        elif self.dd.get() != '':
            filename = askopenfilename()
            if filename:
                self.var.append(self.dd.get())
                self.update_checkbox()

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

    def update_graph(self, plot_data):
        self.canvas.clear()
        self.canvas.add.stackplot(*plot_data)
        month_yr_fmt = mdates.DateFormatter('%Y %B')
        self.canvas.add.xaxis_date()
        self.canvas.add.xaxis.set_major_formatter(month_yr_fmt)
        a = self.canvas.add.xaxis.get_ticklabels()
        for b in a:
            b.set_rotation(90)
        self.figure.tight_layout()

    def set_data(self, banks, date_formats, date_delim):
        self.banks = banks
        self.date_fmts = date_formats
        self.date_del = date_delim
        # print("Set data")


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


class AddDataWindow(tk.Toplevel):
    """Creates the top level widget to be displayed when adding new data"""
    def __init__(self, parent):
        tk.Toplevel.__init__(self, height=10)
        # message = 'This is the child window'
        # tk.Label(self, text=message).grid()
        self.labels=[[],[],[],[]]

        self.parent = parent
        entry = autocomplete.AutocompleteEntry(parent.banks, self, listboxLength=6, width=32)
        tk.Label(self,text="Bank Name").grid(row=0, column=0, columnspan=2)
        tk.Label(self,text='Account Name').grid(row=0, column=3, columnspan=2,sticky='w')
        self.account = tk.StringVar()
        tk.Entry(self, textvariable=self.account).grid(row=1, column=3, columnspan=2,sticky='w')
        entry.grid(row=1, column=0,columnspan=2)
        for i in range(6):
            tk.Label(self,text="").grid(row=i+3)
        tk.Button(self,text="Cancel",command=self.close_window).grid(row=12, column=3)
        tk.Button(self, text='File', command=self.file_press).grid(row=1, column=2)
        # TODO Import the csv/ask for bank and then show the fields and try to parse
        # self.var = tk.StringVar()
        # self.drop = ttk.OptionMenu(self, variable=self.var, *parent.banks)
        # self.drop.grid(row=1, column=1)
        # self.button = tk.Button(self, text="Add Data", command=self.button_press)
        # self.button.grid()

    def file_press(self):
        self.filename = askopenfilename()
        # Need to clear existing labels first
        for item in self.labels:
            for label in item:
                label.grid_forget()
        self.labels=[[],[],[],[]]
        self.parent.controller.test(self.filename)
        self.data = []
        with open(self.filename, 'r') as in_file:
            for line in in_file:
                self.data.append(line.rstrip().rstrip(',').split(','))
        self.parent.add_data = self.data
        for num in range(len(self.data[0])):
            # print(num)
            self.labels[0].append(tk.Label(self, text='(Column '+str(num+1)+')'))
            self.labels[0][-1].grid(row=3, column=num)
            self.labels[1].append(tk.Label(self, text=self.data[0][num]))
            self.labels[1][-1].grid(row=4,column=num)
            self.labels[2].append(tk.Label(self, bg='grey', text=self.data[1][num]))
            self.labels[2][-1].grid(row=5, column=num)
            self.labels[3].append(tk.Label(self, bg='grey', text=self.data[2][num]))
            self.labels[3][-1].grid(row=6, column=num)

        fmt = tk.StringVar()
        self.date_f_menu = ttk.OptionMenu(self, fmt, 'Date Format', *self.parent.date_fmts.keys())
        self.date_f_menu.grid(row=7, column=0)
        # for item in self.parent.date_fmts.keys():
        #     self.date_f_menu['menu'].add_command(label=item, command=tk._setit(fmt, item))

        fmt2 = tk.StringVar()
        self.date_f_del = ttk.OptionMenu(self, fmt2, 'Date Delimiter', *self.parent.date_del.keys())
        self.date_f_del.grid(row=7, column=1)
        # for item in self.parent.date_del:
        #     self.date_f_del['menu'].add_command(label=item, command=tk._setit(fmt2, item))

        date_col = tk.StringVar()
        self.date_coll = ttk.OptionMenu(self, date_col, 'Date Column', *range(1,len(self.data[0])+1))
        self.date_coll.grid(row=7, column=2)

        val_col = tk.StringVar()
        self.val_coll = ttk.OptionMenu(self, val_col, 'Debit Column', *range(1,len(self.data[0])+1))
        self.val_coll.grid(row=7, column=3)

        self.var_swap = tk.StringVar()
        self.check_box_swap = tk.Checkbutton(self, text='Negative Debit', variable=self.var_swap)
        self.check_box_swap.grid(row=8, column=3)

        # Could store variable and box as tuple?
        self.var_check = tk.StringVar()
        self.check_box = tk.Checkbutton(self, text='Separate Debit/Credit Column', variable=self.var_check, command=self.deactivate)
        self.check_box.deselect()
        self.check_box.grid(row=8, column=4)

        val_col2 = tk.StringVar()
        self.val_coll2 = ttk.OptionMenu(self, val_col2, 'Credit Column',*range(1, len(self.data[0]) + 1))
        self.val_coll2.grid(row=7, column=4)
        self.val_coll2.configure(state='disabled')

        # todo add checkbox if sign reversed
        desc_col = tk.StringVar()
        self.desc_coll = ttk.OptionMenu(self, desc_col, 'Description Column', *range(1,len(self.data[0])+1))
        self.desc_coll.grid(row=7, column=5)

        tk.Button(self, text="OK", command=self.ok_press).grid(row=12, column=2)

            # self.button.grid()
        # win = AddDataWindow()
            # win.grab_set()

    def close_window(root):
        root.destroy()

    def deactivate(self):
        if self.var_check.get() == '0':
            self.val_coll2.configure(state=tk.DISABLED)
        elif self.var_check.get() == '1':
            self.val_coll2.configure(state=tk.ACTIVE)

    def ok_press(self):
        print('OK')

if __name__ == '__main__':
    root = tk.Tk()
    app = StartFrame(root, controller=None)

    root.mainloop()
