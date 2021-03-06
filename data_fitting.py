import pylab as plb
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp

import gui_inputbox as ginbx
import line_data_cls as lindat

class DataFitManager():
    def __init__(self):
        super().__init__()
        self.f_list = []

    def exampleFitData(self):
        x = range(10)
        y = [0,1,2,3,4,5,4,3,2,1]

        xarr = self.lst2arr(x)
        yarr = self.lst2arr(y)
        
        xfin = np.linspace(0, 10, 100) # last arg is how many points
        
        fitoptparam, fitcov = self.fitFunction(1, xarr, yarr)
        fitvals = self.gaus(xfin, *fitoptparam)
        fitvalslst = self.arr2list(fitvals)
        plt.plot(x, y)
        plt.plot(xfin, fitvalslst)
        plt.show()

    def lst2arr(self, listvals):
        arrayvals = ar(listvals)
        return arrayvals

    def arr2list(self, arrvals):
        listvals = arrvals.tolist()
        return listvals
        
    def gaus(self, x, a, x0, sigma):
        return a*exp(-(x-x0)**2/(2*sigma**2))

    def gausParams(self, x, y): # obsolete
        n = len(x)
        mean = sum(x*y)/n
        sigma = sum(y*(x-mean)**2)/n
        param = [1, mean, sigma]
        return param

    def tryGausFit(self, x, y):
        max_dom = [min(x), max(x)]
        param, domain = self.open_dialog(max_dom)
        if param and domain:
            print('all good for params')
            e_dom = self.getDomainCells(domain, x)
            new_x = x[e_dom[0]:e_dom[1]]
            new_y = y[e_dom[0]:e_dom[1]]
            self.n_dom = new_x
            try:                
                popt, pcov = curve_fit(self.gaus, new_x, new_y, p0 = param)
                return popt, pcov
            except StopIteration:
                popt = 0
                pcov = 0
                print('Fit does not work')
                return popt, pcov
        else:
            print('No input params')
            return None, None

    def voight(self):
        print('test')
        return


    def fitFunction(self, functype, x, y):
        if functype == 1:
            param = self.gausParams(x, y)
            popt, pcov = curve_fit(self.gaus, x, y, p0 = param)
            # optimised values and estimated covariance
            return popt, pcov
        
        elif functype == 2:
            popt, pcov = self.tryGausFit(x, y)
            return popt, pcov

        elif functype == 3:
            return
   
    def fitFunctionMakeClass(self, fitname):
        try:
            temp_line = lindat.LineData()
            temp_line.fillValues(self.n_dom, self.fitvalslst)
            temp_line.createFitLabels(fitname)
            self.f_list.append(temp_line)
            del temp_line
            return
        except:
            return

    def fitFunctionPrepClass(self, fittype, xarr, yarr):
        if fittype == 2:
            param, cov = self.fitFunction(fittype, xarr, yarr)
            try:
                fitvals = self.gaus(self.n_dom, *param)
                self.fitvalslst = self.arr2list(fitvals)
            except:
                return

    def clearFitList(self):
        self.f_list = []

    def clearFitValues(self):
        self.fitvalslst = []
        self.n_dom = []

    def open_dialog(self, max_domain):
        parambox = ginbx.InputDialogManager()
        parambox.initUIFit(max_domain)
        parambox.exec_()
        if parambox.doubleCheck == True:
            fitparam = parambox.paramlist
            fitdomain = parambox.domvals
            return fitparam, fitdomain
        else:
            fitparam = False
            fitdomain = False
            return fitparam, fitdomain

    def getDomainCells(self, inpt_dom, x):
        dom_min = inpt_dom[0]
        dom_max = inpt_dom[1]

        if x[0] < x[-1]:
            print('normal progression')
            lmin = next(v1[0] for v1 in enumerate(x) if v1[1] > dom_min)
            lmax = next(v2[0] for v2 in enumerate(x) if v2[1] > dom_max)
        else:
            print('reverse progression')
            lmin = next(v1[0] for v1 in enumerate(x) if v1[1] < dom_max)
            lmax = next(v2[0] for v2 in enumerate(x) if v2[1] < dom_min)

        element_domain = [lmin, lmax]
        return element_domain
            
if __name__ == '__main__':
    test = DataFitManager()
    fitvalues = test.exampleFitData()


