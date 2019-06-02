from os import listdir
from os.path import isfile, join
import numpy as np
import aseegg as ag

class prepareData(object):

    def __init__ (self,numberOfGenes, learningSetSize, electrodeNumber, listOfSubjects):
         self.electrodeNumber=electrodeNumber
         self.notchCutOff1=49
         self.notchCutOff2=51
         self.bandpassCutOff1=5
         self.bandpassCutOff2=50
         self.numberOfGenes=numberOfGenes
         self.learningSetSize = learningSetSize
         self.listOfSubjects=listOfSubjects
         self.path="C:\\Users\\Marcin\\Dropbox\\SSVEP\\Bakardjian\\"

    def readDataFromFiles(self):
        fileNames=[]
        for Sub in self.listOfSubjects:
            fileNames.extend([Sub+'\\' + f for f in listdir(self.path+Sub) if isfile(join(self.path+Sub+'\\',f))])
        data = np.empty((0, self.numberOfGenes))
        for files in fileNames:
            oneElectrode=self.filteringData(self.path+files)
            data=np.append(data, [oneElectrode], axis=0)
        print("Wczytano dane dla elektrody:", self.electrodeNumber)
        return data

    def filteringData(self,filePath):
        data=np.genfromtxt(filePath, delimiter=",")
        data=data.T
        syg=ag.pasmowozaporowy(data[self.electrodeNumber],self.numberOfGenes,
                               self.notchCutOff1,self.notchCutOff2)
        syg=ag.pasmowoprzepustowy(syg,self.numberOfGenes,
                                  self.bandpassCutOff1,self.bandpassCutOff2)
        return self.normalizeData(syg[5*self.numberOfGenes:6*self.numberOfGenes])

    def normalizeData(self,signal):
        minSignal=signal.min()
        maxSignal=signal.max()
        signal=(signal-minSignal)/(maxSignal-minSignal)
        return signal
