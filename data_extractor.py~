import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl

import gui_combobox as gcb
import data_manager as dmngt
import line_data_cls as lindat

class ExtractManager(QDialog):
    def __init__(self):
        super(ExtractManager, self).__init__()
        self.datMngr = dmngt.dataManager()
        self.defineDataLocations()
        self.l_list = []
        self.typeval = 0
        return

    def clearL_list(self):
        self.l_list = []
    
    def open_dataselect(self):
        if self.typeval == 0:
            dialog = gcb.GenCombobox()
            dialog.initUI(1)
            self.typeval = dialog.exec_()

    def generateLineClasses(self, fname):
        if fname:
            f_len = len(fname)
            self.l_list = []
            for f in fname:
                x = self.getDataValues(f, self.typeval)[0]
                y = self.getDataValues(f, self.typeval)[1]
                temp_line = lindat.LineData()
                temp_line.fillValues(x, y)
                temp_line.createLabels(f)
                self.l_list.append(temp_line)
                del temp_line

    def getDataValues(self, filename, dattype): # 1-XPS, 2-Raman
        dat_vals = self.datMngr.retrieveData(filename, dattype)
        if dat_vals:
            return dat_vals

    def returnFiles(self, parent):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog # optional
        directory = os.getcwd()
        dialog = QFileDialog(parent, 'Files', directory, ' ', options = options)
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter('*.txt')
        #dialog.setFileMode(QFileDialog.DirectoryOnly) 
        self.setMultipleSidebarUrls(dialog)
        if dialog.exec_() == QDialog.Accepted:
            fileNames = dialog.selectedFiles()
            if fileNames:
                return fileNames

    def setMultipleSidebarUrls (self, dialogbox):
        places = self.datalocations
        urllist = []
        for plc in places:
            if os.path.exists(plc):
                urllist.append(QUrl.fromLocalFile(plc))
        dialogbox.setSidebarUrls(urllist)
    
    def defineDataLocations (self):
        xpsDataMac = '/Users/alex/Dropbox/Research/Paper - Sample J/plot_data\
/attempt_1'
        ramanDataMac = '/Users/alex/Documents/Documents/PhD/Raman_data'
        self.datalocations = [xpsDataMac, ramanDataMac]
        return
