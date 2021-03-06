import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt

import data_extractor as dext
import data_fitting as datfit
import plot_manager as pmngt
import list_manager as lmngt

import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QWidget()
        self.setCentralWidget(self._main)
        self.hlayout = QHBoxLayout(self._main)
        self.vlayout1 = QVBoxLayout()
        self.vlayout2 = QVBoxLayout()
        
        self.pltchck = False

        self.extMngr = dext.ExtractManager()
        self.pltMngr = pmngt.PlotManager()
        self.lstMngr = lmngt.ListManager()
        self.fitMngr = datfit.DataFitManager()

        self.title = 'Plotcrastinator'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.sidePanelCheck = False

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        pltbtn = self.buttonGenerator('Select/Plot', self.pltbtnfunc)
        clrpltbtn = self.buttonGenerator('Clear', self.clrcanvasfunc)
        #rndmpltbtn = self.buttonGenerator('Random', self.rndmpltgen)

        #pltCanvas = self.pltMngr.canvas
        #pltCanvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.vlayout1.addWidget(pltCanvas)
        self.vlayout1.addWidget(self.pltMngr.toolbar)
        self.vlayout1.addWidget(self.pltMngr.canvas)
        self.vlayout1.addWidget(pltbtn)
        #self.vlayout1.addWidget(rndmpltbtn)
        self.vlayout1.addWidget(clrpltbtn)
        #self.vlayout1.setSizeConstraint(QLayout.SetFixedSize())

        self.hlayout.addLayout(self.vlayout1)
        self._main.setLayout(self.hlayout)

        #self.textboxMaker()
        #self.menubarMaker()

        #self.buttonMaker()
        #self.labelMaker()
        #self.statusBar().showMessage('In Progress')
        #self.dialogVal = self.dialogDouble()

    def buttonGenerator (self, name, slot_func):
        button = QPushButton(name, self)
        button.clicked.connect(slot_func)
        return button

    def textBoxGenerator(self):
        textbox = QLineEdit(self)
        return textbox
        
    def createSidePanel (self):
        if self.sidePanelCheck == False:
            self.fitbttn = self.buttonGenerator('Fit', self.fitfunc)
            self.fitbttn.setEnabled(False)
            self.rpltbtn = self.buttonGenerator('Replot', self.repltfunc)
            self.rpltbtn.setEnabled(False)
            
            self.lstMngr.generateLineList(self.extMngr.l_list)

            self.vlayout2.addWidget(self.lstMngr)
            self.vlayout2.addWidget(self.rpltbtn)
            self.vlayout2.addWidget(self.fitbttn)
            self.hlayout.addLayout(self.vlayout2)
            self._main.setLayout(self.hlayout)
            self.sidePanelCheck = True

    def removeSidePanel(self, panel):
        if self.sidePanelCheck == True:
            self.deleteItemsOfLayout(panel)
            self.hlayout.removeItem(panel)
            self._main.setLayout(self.hlayout)
            self.sidePanelCheck = False
        return

    def deleteItemsOfLayout (self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    deleteItemsOfLayout(item.layout())

    def dialogDouble(self):
        d, okPressed = QInputDialog.getDouble(self, 'Get double', 'Value', 0, 0.5, 100, 9.5)
        if okPressed:
            print(d)
            return d
        
    def labelMaker(self):
        self.label1 = QLabel('Pink', self)
        self.label1.move(50, 50)
        self.label2 = QLabel('Blue', self)
        self.label2.move(100,100)        

    def menubarMaker(self):
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('File')
        self.editMenu = self.menubar.addMenu('Edit')
        self.viewMenu = self.menubar.addMenu('View')
        self.toolsMenu = self.menubar.addMenu('Tools')
        
        self.exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        self.exitButton.setShortcut('Ctrl+Q')
        self.exitButton.setStatusTip('Exit application')
        self.exitButton.triggered.connect(self.close)
        self.fileMenu.addAction(self.exitButton)
        
        self.menubar.setNativeMenuBar(False)

    def textboxMaker(self):
        self.textbox = QLineEdit(self)
        self.textbox.move(30,30)
        self.textbox.resize(280,40)
                
    def guiProgress(self):
        self.statusBar().showMessage('In progress')

    def buttonRefresher(self):
        itm_slctd = len(self.lstMngr.selectedItems())
        if  itm_slctd < 1:
            self.fitbttn.setEnabled(False)
            self.rpltbtn.setEnabled(False)
        elif itm_slctd == 1:
            self.fitbttn.setEnabled(True)
            self.rpltbtn.setEnabled(True)
        else:
            self.fitbttn.setEnabled(False)
            self.rpltbtn.setEnabled(True)
        return

    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Hello text', 'Confirm: ' + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText('...')

    @pyqtSlot()
    def pltbtnfunc(self):
        self.extMngr.open_dataselect()
        if self.extMngr.typeval != 0:
            fname = self.extMngr.returnFiles(self)
            if len(self.extMngr.l_list) != 0 and fname:
                for lin in self.extMngr.l_list:
                    fname.append(lin.fpathname)
            self.extMngr.generateLineClasses(fname)
            if self.extMngr.l_list:
                self.pltMngr.refreshAxis()
                self.pltMngr.defineDataType(self.extMngr.typeval)
                self.pltMngr.quickClear()
        
                if len(self.fitMngr.f_list) == 0:
                    self.t_list = self.extMngr.l_list
                else:
                    self.t_list = self.extMngr.l_list + self.fitMngr.f_list
                self.lstMngr.generateLineList(self.t_list)

                self.pltMngr.multiPlot(self.t_list)
                self.lstMngr.generateLineList(self.t_list)
                
                self.pltchck = True
                self.createSidePanel()

                self.lstMngr.itemSelectionChanged.connect(self.buttonRefresher)

    @pyqtSlot()
    def rndmpltgen(self):
        testtext = 'what does this do'
        self.pltMngr.randomPlot()
        self.createSidePanel()
        print(testtext)

    @pyqtSlot()
    def clrcanvasfunc(self):
        self.pltMngr.refreshAxis()
        self.pltchck = False
        self.extMngr.typeval = 0
        self.extMngr.clearL_list()
        self.removeSidePanel(self.vlayout2)

    def testfitfunc(self):
        xarr = self.fitMngr.lst2arr(self.pltMngr.testx)
        yarr = self.fitMngr.lst2arr(self.pltMngr.testy)

        testparam, testcov = self.fitMngr.fitFunction(1, xarr, yarr)
        fitvals = self.fitMngr.gaus(xarr, *testparam)
        
        xlst = self.fitMngr.arr2list(self.pltMngr.testx)
        fitvalslst = self.fitMngr.arr2list(fitvals)
        
        self.pltMngr.singlePlot('fit', self.pltMngr.testx, fitvalslst)
        self.pltMngr.canvas.draw()
        print('test')

    @pyqtSlot()
    def repltfunc(self):
        l_list_len = len(self.extMngr.l_list)
        t_list_len = len(self.t_list)
        new_l_list_idx = []
        rows = [x.row() for x in self.lstMngr.selectedIndexes()]
        print(rows)
        new_l_list_idx = sorted(i for i in rows if i < l_list_len)
        new_l_list = [self.extMngr.l_list[i] for i in new_l_list_idx]
        self.extMngr.l_list = new_l_list
        if t_list_len > l_list_len:
            new_f_list_idx = sorted(i for i in rows if i > l_list_len)
            new_f_list = [self.fitMngr.f_list[i] for i in new_f_list_idx]
            self.fitMngr.f_list = new_f_list    

        slct_rws = [self.t_list[i] for i in rows]
        print(slct_rws)
        self.pltMngr.quickClear()
        self.pltMngr.multiPlot(slct_rws)
        self.lstMngr.generateLineList(slct_rws)
        self.t_list = slct_rws
        return

    @pyqtSlot()
    def fitfunc(self):
        print('real thing maybe')
        drow = self.lstMngr.currentRow()
        row_name = self.lstMngr.currentItem().text()
        xarr = self.fitMngr.lst2arr(self.extMngr.l_list[drow].x)
        yarr = self.fitMngr.lst2arr(self.extMngr.l_list[drow].y)

        self.fitMngr.fitFunctionPrepClass(2, xarr, yarr)
        self.fitMngr.fitFunctionMakeClass(row_name)

        self.t_list = self.extMngr.l_list + self.fitMngr.f_list
        self.pltMngr.quickClear()
        self.pltMngr.multiPlot(self.t_list)
        self.lstMngr.generateLineList(self.t_list)
        return    
        
    def chckpltbutton(self):
        if len(self.lstMngr.selectedItems()) != 0:
            print(self.lstMngr.currentItem().text())
            print(self.lstMngr.currentRow())
        if self.pltchck:
            print('yes there is a plot')
        else:
            print('no plot')

    def testBtnFunc(self):
        print('testing button')
        return
                

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    ex = App()
    ex.show()
    sys.exit(app.exec_()) # Only need when self.show() is used?



