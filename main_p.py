import lib.db
import lib.gui as gui
import lib.graphs
import tkinter as tk
import tkinter.ttk as ttk
import time

import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class Controller:
    def __init__(self, root):
        """Class that instantiates a view, and passes data and requests to/from
    the model and the view.

    The controller assumes the view offers the following methods:

    # * set_values(values)        used to initialize the view
    * clear() and .plot(x, y)   for clearing the canvas and plotting the
                                x, y data provided by the model, respectively.

    Controller provides the following method for external use by the view:

    * update_view    Recalculates plot data, and updates view's plot.
    """
        self.view = gui.StartFrame(root, self)
        # self.default_values = {'base': 1, 'exponent': 2}

        # TODO Have methods as opposed to setting:
        self.view.update_dropdown(('1','2r3','3'))
        self.view.update_checkbox(['a', 'b', 'c', 'd'])

        # Method for getting data from SQL for Check Boxes
        # self.view.var = ['a', 'b', 'c', 'd']
        # self.view.add_dropdown()
        # self.view.drop_data = ('1', 'two', '3')
        # self.view.drop.grid(row=6)
        # TODO Create method for updating checkbox
        # self.view.create_checkbox()
        # TODO Create Method for updating dropdown box
        # self.view.update_dropdown()
        # self.view.drop.grid()
        # self.view.add_trans_button()
        # self.initialize_view()
        print("Stuff")


if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title("Finance App")
    root.attributes('-topmost', True)
    app = Controller(root)
    # This line undoes the bringing the window to the front, but it prevents the window from always being there
    root.after(1000,root.attributes, '-topmost', False)

    root.mainloop()
