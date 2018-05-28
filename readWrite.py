import re

class ReadWrite(object):
# Regular expression for pump duration
  reg_ahead = "pump_"
  reg_body = "[0-9]{3}"
  reg_behind = "us\.txt"
# Regular expression to extract information from directory name
  dateReg = "201[0-9]{5}" # Date data taken e.g. 20171119
  dipoleReg = "[0-9]+(?=mW)" # Dipole laser power e.g. 35mW
  detuneReg = "(-|\+)[0-9]+\.*[0-9]+(?=GHz)" # Pump detuning e.g. -1.4GHz
  powerReg = "[0-9]+\.*[0-9]+(?=nW)" # Pump power e.g. 620nW
  waitReg = "[0-9]+\.*[0-9]+(?=ms)" # Wait time after MOT release e.g. 35ms
  repeatReg = "(?<=rpn)[0-9]+" # repeat number

  def __init__(self, argvstr):
#    self.argvstr = '20171114_bleach_35mW/620nW_-1.4GHz_30ms/'
    self.params = re.split('_|/',argvstr)
    self.fileReg=re.compile(self.reg_ahead + self.reg_body + self.reg_behind) # Choose only data files
    self.pumpTimeReg = re.compile("(?<="+self.reg_ahead+")"+self.reg_body+"(?="+self.reg_behind+")")
    self.date=''
    self.dipole=''
    self.detune=''
    self.power=''
    self.wait=''
    self.repeat=''
    self.pumpTime=0

    for p in self.params:
      if re.search(self.dateReg,p) is not None:
        self.date = re.search(self.dateReg,p).group(0)
      elif re.search(self.dipoleReg,p) is not None:
        self.dipole = re.search(self.dipoleReg,p).group(0)
      elif re.search(self.detuneReg,p) is not None:
        self.detune = re.search(self.detuneReg,p).group(0)
      elif re.search(self.powerReg,p) is not None:
        self.power = re.search(self.powerReg,p).group(0)
      elif re.search(self.waitReg,p) is not None:
        self.wait = re.search(self.waitReg,p).group(0)
      elif re.search(self.repeatReg,p) is not None:
        self.repeat = re.search(self.repeatReg,p).group(0)

  def showValues(self, atomNum, num_std, gamma_R, g_std):
    print("date: {0}".format(self.date))
    print("dipole: {0}".format(self.dipole))
    print("detune: {0}".format(self.detune))
    print("power: {0}".format(self.power))
    print("wait: {0}".format(self.wait))
    print("repeat: {0}".format(self.repeat))
    print("atom number: {0:.1f}".format(atomNum))
    print("atom number: standard deviation: {0:.5f}".format(num_std))
    print("gamma_R: {0:.3f}".format(gamma_R))
    print("gamma_R standard deviation: {0:.5f}".format(g_std))

  def writeFile(self, atomNum, num_std, gamma_R, g_std):
    answer = input("Do you want to write on a file? [Y]es/[N]o  ")
    if (answer=='y') or (answer=='Y'):
      self.f = open('alldata.txt', 'a')
      print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6:.1f}\t{7:.5f}\t{8:.3f}\t{9:.5f}\t ".format(self.date,self.dipole,self.detune,self.power,self.wait,self.repeat,atomNum,num_std,gamma_R,g_std),file=self.f)
      self.f.close()
      print("Written successfully!")
    

#f = open('alldata.txt', 'a')
#print("{0}\t{1}\t{2}".format(params[0],params[1],params[2]),file=f)

#f.close()
