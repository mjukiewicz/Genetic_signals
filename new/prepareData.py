from os import listdir
from os.path import isfile, join
import numpy as np
import aseegg as ag


class prepareData(object):

    def __init__ (self,listOfSubjects, seconds, fs):
         self.notchCutOff1=49
         self.notchCutOff2=51
         self.bandpassCutOff1=5
         self.bandpassCutOff2=50
         self.listOfSubjects=listOfSubjects
         self.seconds=seconds
         self.fs=fs
         self.electrodeSet=[10-1,15-1,21-1,23-1,28-1,39-1];
         self.path="C:\\Users\\Marcin\\Dropbox\\SSVEP\\Bakardjian\\"

    def readDataFromFiles(self):
        fileNames=[]
        for Sub in self.listOfSubjects:
            fileNames.extend([Sub+'\\' + f for f in listdir(self.path+Sub) if isfile(join(self.path+Sub+'\\',f))])

        data = np.empty((self.fs*self.seconds, 15, len(self.electrodeSet)))
        for i in range(len(fileNames)):
            dataRaw=np.genfromtxt(self.path+fileNames[i], delimiter=",")
            dataRaw=dataRaw.T
            for j in range(len(self.electrodeSet)):
                data[:,i,j]=self.filteringData(dataRaw[self.electrodeSet[j]])
            print("Wczytano dane dla pliku:", fileNames[i])
        return data

    def filteringData(self,data):
        syg=ag.pasmowozaporowy(data, self.fs, self.notchCutOff1,self.notchCutOff2)
        syg=ag.pasmowoprzepustowy(syg, self.fs, self.bandpassCutOff1,self.bandpassCutOff2)
        return self.normalizeData(syg[5*self.fs:(5+self.seconds)*self.fs])

    def normalizeData(self,signal):
        minSignal=signal.min()
        maxSignal=signal.max()
        signal=(signal-minSignal)/(maxSignal-minSignal)
        return signal

    def createPopulation(self, stim, populationSize):
        base = np.empty((4, self.seconds*self.fs))
        perfect = np.empty((self.seconds*self.fs,populationSize,4))

        t=np.linspace(0,self.seconds,self.fs)
        base[0,:]=(np.sin(2*np.pi*stim*t)+1)/2;
        base[1,:]=(np.cos(2*np.pi*stim*t)+1)/2;
        base[2,:]=(np.sin(4*np.pi*stim*t)+1)/2;
        base[3,:]=(np.cos(4*np.pi*stim*t)+1)/2;

        base=base.T
        for i in range(populationSize):
            perfect[:,i,:]=base;

        return perfect
