from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PyQt5 import QtGui

class ListManager(QListWidget):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(self.ExtendedSelection)

    def basicList(self):
        self.addItem('test 1')
        self.addItem('test 2')

    def generalAdd2List(self, list_item):
        if list_item:
            for l in list_item:
                self.addItem(l)
        return            

    def lineClassToListStr(self, line_list):
        dat_list = []
        for l in line_list:
            dat_list.append(l.name)
        return dat_list

    def generateLineList(self, dclass_list):
        self.clear()
        dat_list = self.lineClassToListStr(dclass_list)
        self.generalAdd2List(dat_list)
        return

    def addFitLines(self, fclass_list):
        fdat_list = self.lineClassToListStr(fclass_list)
        self.generalAdd2List(fdat_list)
        return

    def selectChanged(self):
        print('slecteditems: ', self.selectedItems())

        
