import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui


class GenCombobox (QDialog):
    def __init__ (self, parent = None):
        QDialog.__init__(self, parent)
        
    def initUI(self, boxtype):
        if boxtype is not None:
            self.typeval = 0
            self.initLabels()
            
            self.initComboItemsPlot(boxtype)
        
            self.btn = QPushButton()
            self.btn.setText('Accept')
            self.btn.clicked.connect(self.accept)
            self.initLayoutPlot()
        else:
            print('No boxtype specified')

        
    def initLayoutPlot (self):
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.verticalLayout = QtWidgets.QVBoxLayout()
        self.layout.horizontalLayout = QtWidgets.QHBoxLayout()
        self.layout.verticalLayout.addLayout(self.layout.horizontalLayout)
        self.layout.verticalLayout.addWidget(self.combo)
        self.layout.verticalLayout.addWidget(self.lbl)
        self.layout.verticalLayout.addWidget(self.btn)
        self.setLayout(self.layout.verticalLayout)
        
    def initComboItemsPlot(self, boxtype):
        typelist = self.plotTypeList(boxtype)
        tlist_len = len(typelist)
        typevals = range(tlist_len)

        self.typed = dict()
        self.combo = QComboBox()
        self.combo.setMinimumWidth(200)
        for t, tval in zip(typelist, typevals):
            self.combo.addItem(t)
            self.typed[t] = tval
        self.combo.activated[str].connect(self.onActivated)
        print(self.typed)

    def plotTypeList(self, boxtype):
        if boxtype == 1:
            type0 = 'Select Type'
            type1 = 'XPS (CasaXPS Output)'
            type2 = 'Raman Spectroscopy'

            typeplot = []
            typeplot = [type0, type1, type2]
            return typeplot
        elif boxtype == 2:  
            typeplot = boxtype
            return typeplot

    def initLabels (self):
        self.lbl = QLabel('Select Type')
        self.lbl.setAlignment(Qt.AlignCenter)
        myFont = QtGui.QFont()
        myFont.setBold(True)
        self.lbl.setFont(myFont)
        
    def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()
        self.typeval = self.typed[text]

    def validate(self):
        if self.typeval != 0:
            retval = True
        else:
            self.lbl.setText('Select Type')
            retval = False
        return retval

    def accept(self):
        print(self.validate())
        if self.validate():
            print('Accepted')
            self.done(self.typeval) # return execution val here

if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = QDialog()
    ex = GenCombobox()
    ex.initUI(test, 1)
    test.exec_()
    #sys.exit(app.exec_())

