import matplotlib.pyplot as plt
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import key_press_handler

class PlotManager (QDialog):
    def __init__(self):
        super(PlotManager, self).__init__()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.ax = self.figure.add_subplot(111)
        return

    def defineDataType (self, datatype):
        self.typeval = datatype
        return

    def on_key_press (self, event):
        print(event)
        key_press_handler(event, self.canvas, self.toolbar)

    def quickClear(self):
        self.figure.clear()
        return

    def refreshAxis (self):
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.canvas.draw()

    def singlePlot(self, name,  x, y):
        lineplt, = self.ax.plot(x, y, label=name)
        #self.ax.plot(x, y, label=name)
        self.leg = self.ax.legend(loc = 'upper left', fancybox = True)
        return lineplt

    def enableToggling(self, lineclasslist):
        list_len = len(lineclasslist)
        self.lined = dict()
        for self.legline, self.origline in zip(self.leg.get_lines(), self.lines):
            self.legline.set_picker(5)
            self.lined[self.legline] = self.origline
        self.figure.canvas.mpl_connect('pick_event', self.onpick)

    def onpick(self, event):
        legline = event.artist
        origline = self.lined[legline]
        vis = not origline.get_visible()
        origline.set_visible(vis)
        if vis:
            legline.set_alpha(1.0)
        else:
            legline.set_alpha(0.2)
        self.figure.canvas.draw()

    def listCombiner(self, lineclasslist1, lineclasslist2):
        combined_list = lineclasslist1 + lineclasslist2
        return combined_list

    def multiPlot(self, lineclasslist):
#        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        list_len = len(lineclasslist)
        print(list_len)
        self.lines = []
        for i in range(list_len):
            self.lines.append(self.singlePlot(lineclasslist[i].lbl,
                            lineclasslist[i].x,
                            lineclasslist[i].y))
        self.enableToggling(lineclasslist)
        self.toolbar.update()
        self.toolbar.push_current()
        self.labelAxis(self.typeval)
        plt.tight_layout()
        self.canvas.draw()

    def randomPlot(self):
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.testx = range(10)
        self.testy = [0, 1, 2, 3, 4, 5, 4, 3, 2, 1]
        self.singlePlot('random', self.testx, self.testy)
        self.canvas.draw()
        self.toolbar.update()

    def labelAxis(self, plttype):
        if plttype == 1:
            print('label axis xps')
            self.ax.set_xlabel('Binding Energy (eV)')
            self.ax.set_ylabel('Intensity')
        elif plttype == 2:
            print('label axis raman')
            self.ax.set_xlabel('Raman Shift (cm^-1)')
            self.ax.set_ylabel('Intensity (a.u.)')
        else:
            print('no axis label')

if __name__ == '__main__':
    x = range(1,11)
    y = range(4,14)

    testMngr = plotManager()
    testMngr.basicPlot(x, y)

        

    
