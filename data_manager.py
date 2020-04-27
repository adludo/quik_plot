import os
from os import listdir
from os.path import isfile, join
import string
import csv

class dataManager ():
    def __init__(self):
        return

    def retrieveData (self, filename, datatype):
        if datatype == 1: # XPS Data
            f = open(filename)
            f_content = f.readlines()
            f_content = self.cleanXPSData(f_content)
            Benergy, datavals = self.sortXPSData(f_content)
            return Benergy, datavals
        elif datatype == 2: # Raman Data
            raman_shift, intensity = self.retrieveRamanData(filename)
            return raman_shift, intensity
        else:
            print ('no valid datatype entered')

    def cleanXPSData (self, inputdata):
        stripdata = [x.strip() for x in inputdata]
        del stripdata[0:7] # remove headers
        data_num = [line.split(',') for line in stripdata]
        data_num = [[t.replace('\t', ' ') for t in el] for el in data_num]
        data_num = [[[float(x) for x in te.split()] for te in el] for el in data_num]
        data_num = [el[0] for el in data_num]
        return data_num

    def sortXPSData (self, inputdata):
        # Store different parts of data in different lists
        # 1 - Binding Energy (x-axis)
        # 2 - Data Values (experimental)
        # Final - Envelope function
        # 2nd last - Background
        # In between - Fitted Voight functions
        dattyp_len = len(inputdata[0]) - 1
        fits = []
        envelope = [el[dattyp_len] for el in inputdata]
        datval_len = len(envelope)
        backgrnd = [el[dattyp_len - 1] for el in inputdata]
        Benergy = [el[0] for el in inputdata]
        datvals = [el[1] for el in inputdata]
        return Benergy, datvals

    def retrieveRamanData(self, filename):
        ramanshift = []
        intensity = []
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter = '\t')
            for line in reader:
                ramanshift.append(float(line[0]))
                intensity.append(float(line[1]))
            return ramanshift, intensity

if __name__ == '__main__':
    testMngr = dataManager()
