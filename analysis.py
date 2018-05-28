# python analysis.py directory_name

from os import listdir
from os.path import isfile, isdir, join
import sys
import re
import numpy
import math
from matplotlib import pyplot
from scipy.optimize import curve_fit
from singleHist import SingleHist
from readWrite import ReadWrite

fitFlag = True
refFile = None # None: average photon number in saturated region; file: full transmitted signal
#refFile = "no_atom.txt"
#argLen = len(sys.argv);

initAtom = 5000;
binWidth = 20; # [us]
startT = 0; # Start time of histogram display [us]
endT= 1000;
histBinNum = 50; # End time of histogram display [us]
avrStartT = 400; # Start time of the range for average
binR = numpy.arange(startT,endT+binWidth,binWidth);
#repeatNum = 50;
bratio = 7/12; #3/4; #7/12;

refPhotNum = None # Photon numbers from the reference transmission file

argvstr = str(sys.argv[1]);
rw1 = ReadWrite(argvstr)

SingleHist.get_modcount()
SingleHist.set_parameters(startT, endT, avrStartT, binR, binWidth, int(rw1.repeat), histBinNum, bratio)

if refFile is not None:
    histRef = SingleHist(refFile)
    histRef.make_hist()
    histRef.get_photNum()
    refPhotNum = histRef.photNum
    print(refPhotNum)
    del histRef

#================ Iteration for all files in the directory ===================
#=============================================================================
if isdir(argvstr):
#  fig = pyplot.figure()
#  ax = fig.add_subplot(111)

  def fitFunc(t, n, gammaR):
    return n*(1-numpy.exp(-0.001*2*math.pi*gammaR*t))

  files = [f for f in listdir(argvstr) if isfile(join(argvstr, f))]
  datafiles = [m.group(0) for l in files for m in [rw1.fileReg.search(l)] if m]

  list_t = [0]
  list_num = [0]
  for f in datafiles:
    time = re.search(rw1.pumpTimeReg,f)
    pumpTime = int(time.group(0))  

    hist1 = SingleHist(join(argvstr,f))
    hist1.make_hist()
    hist1.get_atomNum(refPhotNum)
    print("{0:.1f}us: {1:.1f}".format(pumpTime-0.5, hist1.atomNum))
    list_t.append(pumpTime-0.5)
    list_num.append(hist1.atomNum)
    del hist1

  pyplot.plot(list_t,list_num, 'bo')
  pyplot.xlabel('Pump time ($\mu s$)', fontsize=18)
  pyplot.ylabel('Atom number', fontsize=18)
  pyplot.xticks(fontsize=16)
  pyplot.yticks(fontsize=18)

  if fitFlag:
    x = numpy.linspace(list_t[0],list_t[-1],101)
    if (int(rw1.wait)<=40):
      guessNum = initAtom 
    elif (int(rw1.wait)>=60):
      guessNum = int(initAtom*0.05)
    else:
      guessNum = int(initAtom*(1+int(rw1.wait)-40)*(0.05-1)/(60-40))

    if (int(rw1.power)==620):
      guessGamma = 12
    elif (int(rw1.power)==310):
      guessGamma = 5 
    else:
      guessGamma = 0.1 

    fitParams, fitCovariances = curve_fit(fitFunc, list_t, list_num, p0=(guessNum,guessGamma))
    atomnumstd = numpy.sqrt(numpy.diag(fitCovariances)[0])/fitParams[0]
    gammastd = numpy.sqrt(numpy.diag(fitCovariances)[1])/fitParams[1]
    rw1.showValues(fitParams[0], atomnumstd, fitParams[1], gammastd)
    pyplot.plot(x, fitFunc(x,fitParams[0], fitParams[1]), 'k')
    pyplot.title('$\Gamma_R$ / $2 \pi$ = {0:.3f}kHz'.format(fitParams[1]), fontsize=16)

  pyplot.tight_layout()
  pyplot.show()

  if fitFlag:
    rw1.writeFile(fitParams[0], atomnumstd, fitParams[1], gammastd)

#=============================================================================

elif isfile(argvstr):
  SingleHist.set_parameters(startT, endT, avrStartT, binR, binWidth, int(rw1.repeat), histBinNum, bratio)
  hist1 = SingleHist(argvstr)
  hist1.make_hist()
  hist1.get_atomNum(refPhotNum)
  print(hist1.atomNum)
  hist1.plot_hist()
  del hist1

#atomNum = sum(h[int(avrStartT/binWidth):])*(endT-startT)/(repeatNum*(endT-avrStartT))

#print('atom number: {0:.1f}'.format(atomNum))
#pyplot.plot(e[0:histBinNum]+0.5*binWidth,h[0:histBinNum])
#pyplot.hist(d, bins=binR, alpha=0.75, edgecolor='black', linewidth=1.2)


#pyplot.axhline(y=BG/2.5, color='black')
#ax.text(2.75,10,'Bin width\n{:.1f}ns'.format(1000*binWidth))
#pyplot.xlabel('Time ($\mu$s)', fontsize=20)
#pyplot.xticks(numpy.arange(0,500,100),fontsize=20)
#pyplot.xticks(numpy.arange(0,40,5),fontsize=20)
#pyplot.yticks(numpy.arange(0,3500,500),fontsize=20)
#pyplot.yticks(fontsize=20)
#pyplot.tight_layout()
#pyplot.show()

# savefig('dataFitted.png', bbox_inches=0)
