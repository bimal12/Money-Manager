import lib.db
import lib.gui as gui
import lib.graphs
import tkinter as tk
import tkinter.ttk as ttk

import matplotlib
import sqlite3
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style


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
        self.connection = sqlite3.Connection('data.db')
        # Have methods as opposed to setting: Pull from db
        self.view.update_option_menu(('1', '2r3', '3'))
        self.view.update_checkbox(['a', 'b', 'c', 'd'])

    def get_plt_data(self):
        # Interact with the model to get the data that you want and save it to a variable
        # self.plot_data = ([1,2,3,4],[1,2,3,4])
        for item in self.view.var:
            print(item)
        pass
        # self.view.create_graph()

    def update_plot(self):
        self.view.canvas.clear()
        self.view.canvas.add.plot(*self.plot_data)

    # Dont need this as only need to update when something changes, ie button pressed / check box
    def animate(self,i):
        print("Animate")
        # print(i)
        # print(j)
        # self.plot_data=([1,2,3,4],[i,i+1,i+2,i+1])
        tmp=lib.db.get_data(self.connection, "SELECT date, value FROM transactions")
        res = lib.db.sumtrans(tmp)
        xList = []
        yList = []
        for x, y in res:
            # print(type(x))
            xList.append(x)
            yList.append(float(y))
        self.plot_data=(xList,yList)
        # print(self.plot_data)
        # self.get_plt_data()
        self.update_plot()


if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title("Finance App")
    root.attributes('-topmost', True)
    app = Controller(root)

    # This line undoes the bringing the window to the front, but it prevents the window from always being there
    root.after(500, root.attributes, '-topmost', False)

    ani = animation.FuncAnimation(app.view, app.animate, interval=1000)

    # f = Figure(figsize=(4, 4), dpi=100)
    # b = f.add_subplot(1, 1, 1)
    # canvas = FigureCanvasTkAgg(f, root)
    # canvas.show()
    # canvas.get_tk_widget().grid(column=4, row=0, rowspan=9)
    root.mainloop()
