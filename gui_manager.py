import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QUrl

import data_manager as dmngt
import line_data_cls as lindat
import plot_manager as pltmngt
import gui_combobox as gcb

from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

class Dialog(QDialog):
    def slot_method(self):
        print('Call slot')
        return

    def plotlineclass_method (self):
        self.open_dataselect()
        if self.typeval != 0:
            self.generateLineClasses()
            if self.l_list:
                self.pltMngr.refreshAxis()
                self.pltMngr.multiPlot(self.l_list)
                
    def __init__(self):
        super(Dialog, self).__init__()
        self.pltMngr = pltmngt.PlotManager()
        self.datMngr = dmngt.dataManager()
        self.comboMngr = gcb.GenCombobox()

        self.defineDataLocations ()
        self.initUI()

    def open_dataselect(self):
        self.typeval = 0
        dialog = gcb.GenCombobox()
        dialog.initUI(1)
        self.typeval = dialog.exec_()
        self.pltMngr.defineDataType(self.typeval)
        
    def initUI (self):
        plotbutton = self.buttonGenerator('Select and Plot', self.plotlineclass_method)
        clearbutton = self.buttonGenerator('Clear Plot', self.pltMngr.refreshAxis)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(plotbutton)
        mainLayout.addWidget(clearbutton)
        mainLayout.addWidget(self.pltMngr.toolbar)
        mainLayout.addWidget(self.pltMngr.canvas) # add figure here
        self.setLayout(mainLayout)        
        self.setWindowTitle('QDialog - Prototype')
        
    def generateLineClasses (self):
        fname = self.returnFiles()
        if fname:
            fname_len = len(fname)
            self.l_list = [lindat.LineData() for k in range(fname_len)]
            i = 0
            for f in fname:
                x = self.getDataValues(f, self.typeval)[0]
                y = self.getDataValues(f, self.typeval)[1]
                self.l_list[i].fillValues(x, y)
                self.l_list[i].createLabels(f)
                i = i + 1
        else:
            self.l_list = None

    def returnFiles (self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog # optional        
        directory = os.getcwd()
        dialog = QFileDialog(self, 'Files', directory, ' ', options = options)
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter('*.txt')
        #dialog.setFileMode(QFileDialog.DirectoryOnly)
        self.setMultipleSidebarUrls(dialog)            
        if dialog.exec_() == QDialog.Accepted:
            fileNames = dialog.selectedFiles()
            if fileNames:
                return fileNames
            
    def getDataValues(self, filename, dattype): # 1-XPS, 2-Raman
        dat_vals = self.datMngr.retrieveData(filename, dattype)
        if dat_vals:
            return dat_vals

    def setMultipleSidebarUrls (self, dialogbox):
        places = self.datalocations
        urllist = []
        for plc in places:
            if os.path.exists(plc):
                urllist.append(QUrl.fromLocalFile(plc))
        dialogbox.setSidebarUrls(urllist)

    def defineDataLocations (self):
        xpsDataMac = '/Users/alex/Dropbox/Research/Paper - Sample J/plot_data/attempt_1'
        ramanDataMac = '/Users/alex/Documents/Documents/PhD/Raman_data'
        self.datalocations = [xpsDataMac, ramanDataMac]
        return

    def buttonGenerator (self, name, slot_func):
        button = QPushButton(name)
        button.clicked.connect(slot_func)
        return button
        

class AppWidg (QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Hello Owlrd'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 250

    def initUI(self, purpose):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #self.imageLoader()
        #self.buttonQuery('Do you like cookies?')
        #self.buttonGeneral('Open colour dialog','Open colour dialog', self.on_clickColor)
        #self.show()

        if purpose == 1: # 1-load path
            return self.openFileNameDialog()
        else:
            print('No Purpose currently, input purpose')
            
    def imageLoader(self):
        self.label = QLabel(self)
        self.pixmap = QPixmap('test.png')
        self.label.setPixmap(self.pixmap)
        self.resize(self.pixmap.width(), self.pixmap.height())
        self.show()

    def buttonQuery(self, buttontext):
        buttonReply = QMessageBox.question(self, 'Hello', buttontext, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('yeah')
        else:
            print('nah')

    def getDirectory(self):
        curr_dir = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if curr_dir:
            print (curr_dir)                        

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog # optional
        fileName, _ = QFileDialog.getOpenFileName(self, 'Return File Path', 'test', 'All Files (*);;Python Files (*.py)', options=options)
        if fileName:
            return fileName

    def buttonGeneral(self, buttontext, tooltext, func):
        button = QPushButton(buttontext, self)
        button.setToolTip(tooltext)
        button.move(10, 10)
        button.clicked.connect(func)
        return

    @pyqtSlot()
    def on_clickColor (self):
        self.openColorDialog()

    def openColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            print(color.name())
            return color.name()

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    #ex = App()
    #ex = AppWidg()
    dialog = Dialog()
    dialog.exec_()

    #sys.exit(app.exec_()) # Only need when self.show() is used?
