import lib.db
import lib.gui as gui
import tkinter as tk
# import tkinter.ttk as ttk
# import datetime

import matplotlib
import sqlite3

matplotlib.use("TkAgg")
# import matplotlib.dates as mdates
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.figure import Figure
# import matplotlib.animation as animation
# from matplotlib import style


class Controller:
    def __init__(self, root):
        """Class that instantiates a view, and passes data and requests to/from
    the model and the view.

    The controller assumes the view offers the following methods:

    # * set_values(values)        used to initialize the view
    * clear() and .plot(x, y)   for clearing the canvas and plotting the
                                x, y data provided by the model, respectively.

    Controller provides the following method for external use by the view:

    * update_plot    Recalculates plot data, and updates view's plot.
    """
        self.view = gui.StartFrame(root, self)
        self.connection = sqlite3.Connection('data.db', detect_types=sqlite3.PARSE_DECLTYPES)

        #TODO Have methods as opposed to setting: Pull from db
        # self.view.update_option_menu(('1', '2r3', '3'))
        self.plot_data = 0
        # self.banks =['bank']
        # TODO put this into its own method
        dat = lib.db.get_data(self.connection, "SELECT name, bank from account")
        dit = list(", ".join(n) for n in dat)

        self.view.update_option_menu(['Add New Account']+dit)
        self.view.update_checkbox(dit)
        self.view.set_data(sorted(lib.db.BANKS), lib.db.DATE_FORMAT, lib.db.DATE_DELIMITER)


    def get_plt_data(self):
        # Interact with the model to get the data that you want and save it to a variable
        # self.plot_data = ([1,2,3,4],[1,2,3,4])
        for item in self.view.var:
            print(item)
        pass

    # Dont need this as only need to update when something changes, ie button pressed / check box
    def update_plot(self, i):
        print("Animate")
        tmp = lib.db.get_data(self.connection, "SELECT date, value FROM transactions")
        res = lib.db.sumtrans(tmp)
        # print(res[0])
        x_list = []
        y_list = []
        for x, y in sorted(res):
            x_list.append(x)
            y_list.append(float(y))

        self.plot_data = (x_list, y_list)
        self.view.update_graph(self.plot_data)


    def test(self,filename):
        print('Test: {}'.format(filename))


if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title("Test App")
    root.attributes('-topmost', True)
    app = Controller(root)

    # This line undoes the bringing the window to the front, but it prevents the window from always being there
    root.after(500, root.attributes, '-topmost', False)

    # ani = animation.FuncAnimation(app.view, app.animate, interval=1000)
    app.update_plot(0)
    root.mainloop()
