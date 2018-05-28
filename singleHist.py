import numpy
import matplotlib
from matplotlib import pyplot
from scipy.interpolate import interp1d

class SingleHist(object):
  cntrate =  [0, 13.8, 34.9, 88.1, 218.3, 545.1, 1327.8, 2045.7, 3116.0, 4583.2, 6794.6, 9599.2, 11267.5, 12777.0, 14888.9, 16880.1, 18946.2, 20924.9, 22883.1, 24741.8, 26473.3, 27984.8, 29127.5]  # [Kc/s]
  corfactor = [1.00, 1.00, 0.99, 0.99, 1.00, 1.01, 1.04, 1.07, 1.11, 1.20, 1.28, 1.44, 1.54, 1.71, 1.85, 2.06, 2.31, 2.63, 3.03, 3.52, 4.14, 4.94, 5.97]
  spcmEff = 0.58 # Quantum efficiency of SPCM
  coupEff = 0.10 # Coupling efficiency into SPCM
  
  
  def __init__(self, fname): 
    self.fname = fname
    self.d = numpy.genfromtxt(fname, skip_header=0, skip_footer=0, delimiter='\t') # data

  def make_hist(self):
    self.h, self.e = numpy.histogram(self.d,self.binR)
      

  def plot_hist(self):
    if 'hreal' not in dir(self):
      self.get_atomNum()
    
    print("Bin width: {0}".format(self.binWidth))
#    pyplot.plot(self.e[0:self.histBinNum]+0.5*self.binWidth,self.hreal[0:self.histBinNum])
    pyplot.bar(self.e[0:self.histBinNum]+0.5*self.binWidth,self.hreal[0:self.histBinNum],width=12.0)
    pyplot.xlabel('Probe Time [$\mu s$]', fontsize=18)
    pyplot.xticks(fontsize=16)
    pyplot.yticks(fontsize=16)
    pyplot.tight_layout()
    pyplot.show()

  def get_photNum(self):
    self.hsingle = self.h/self.repeatNum
    self.hreal = self.hsingle * self.f(1000*self.hsingle/self.binWidth)
    self.photNum = sum(self.hreal[int(self.startT/self.binWidth):int(self.endT/self.binWidth)])/(self.spcmEff*self.coupEff)
#    print(self.photNum)    

  def get_atomNum(self, refPhotN):
    self.get_photNum()
    if refPhotN is None: # average in the saturated region
      self.atomNum = self.bratio*((sum(self.hreal[int(self.avrStartT/self.binWidth):int(self.endT/self.binWidth)])*(self.endT-self.startT)/(self.endT-self.avrStartT))/(self.spcmEff*self.coupEff)-self.photNum)
    else: # subtract from the reference transimission
      self.atomNum = self.bratio*(refPhotN - self.photNum)

  @classmethod
  def get_modcount(cls):
     cls.f = interp1d(cls.cntrate,cls.corfactor)
    
  @classmethod
  def set_parameters(cls, startT, endT, avrStartT, binR, binWidth, repeatNum, histBinNum, bratio):
     cls.startT = startT
     cls.endT = endT
     cls.avrStartT = avrStartT
     cls.binWidth = binWidth
     cls.repeatNum = repeatNum 
     cls.binR = binR
     cls.histBinNum = histBinNum
     cls.bratio = bratio
