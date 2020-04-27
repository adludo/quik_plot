import os

class LineData ():
    def __init__(self):
        return

    def fillValues (self, x, y):
        self.x = x
        self.y = y

    def createLabels (self, filename):
        self.name = os.path.basename(filename)
        self.lbl = self.name[:8]
        self.fpathname = filename

    def dispValues(self):
        print (self.x)
        print (self.y)

    def createFitLabels (self, data_name):
        self.name = 'Fit_' + data_name
        self.lbl = self.name[:8]
        

if __name__ == '__main__':
    test = LineData(1, 5)
    test.dispValues()
