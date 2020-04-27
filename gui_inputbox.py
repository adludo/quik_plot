import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class InputDialogManager(QDialog):
    def __init__(self):
        QWidget.__init__(self)
        self.domCheck = False
        self.paramCheck = False
        self.doubleCheck = False

    def initDomainLayout(self, inputlayout):
        self.domlayout = QHBoxLayout()
        self.domtext = []
        for i in range(2):
            self.domtext.append(QLineEdit())
            self.domtext[i].setValidator(QDoubleValidator())
            self.domtext[i].setFixedWidth(55)
            self.domlayout.addWidget(self.domtext[i])
        self.lbl.append(QLabel(self.lbltxt[3]))
        inputlayout.addRow(self.lbl[3], self.domlayout)

    def initParamLayout(self, inputlayout):
        for i in range(self.param_num):
            self.le.append(QLineEdit())
            self.le[i].setValidator(QDoubleValidator())
            self.lbl.append(QLabel(self.lbltxt[i]))
            inputlayout.addRow(self.lbl[i], self.le[i])

    def initUIFit(self, max_domain):
        layout = QFormLayout()
        self.param_num = 3
        self.t_dom = max_domain
        
        self.le = []
        self.lbltxt = ['Amplitude', 'Mean', 'Sigma', 'Domain']
        self.lbl = []
        
        self.initParamLayout(layout)            
        self.initDomainLayout(layout)

        self.btnDone = QPushButton('Done')
        layout.addRow(self.btnDone)
        
        self.btnDone.clicked.connect(self.return_accept)
        self.setLayout(layout)

    def getDomainVals(self):
        self.domvals = []
        for i in range(2):
            if self.domtext[i].text():
                dom_val = float(self.domtext[i].text())
                if self.t_dom[0] <= dom_val <= self.t_dom[1]:
                    self.domvals.append(dom_val)
                    if i == 1:
                        self.domCheck = True
                else:
                     print('Domain values outside limit')
                     self.domCheck = False
                     break
            else:
                self.domCheck = False
                print('Insert domain values')
                break

        print(self.domvals)
        if self.domvals and len(self.domvals) == 2:
            if self.domvals[0] > self.domvals[1]:
                self.domCheck = False
            else:
                self.domCheck = True
            
    def return_accept(self):
        self.paramlist = []
        for i in range(self.param_num):
            if self.le[i].text():
                self.paramlist.append(float(self.le[i].text()))
                if i == self.param_num - 1:
                    self.paramCheck = True
            else:
                self.paramCheck = False
                print('Insert parameter values')
                break

        self.getDomainVals()
        print(self.paramCheck)
        print(self.domCheck)
        if self.paramCheck and self.domCheck:
            print(self.paramCheck)
            print(self.domCheck)
            self.doubleCheck = True
            self.done(1)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InputDialogManager()
    ex.initUI()
    ex.show()
    sys.exit(app.exec_())
