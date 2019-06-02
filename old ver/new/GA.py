from prepareData import prepareData
from geneticAlgorithm import createOutputSignal
import numpy as np

listOfSubjects=['SUBJ1']
seconds=1
fs=256
numberOfGenes=seconds*fs
stim=[14,28,8];

populationSizeList=[10]#[150,200,300,500] #10,20,50,10
numberOfMutationsList=[10]#[10,20,50,70,100,150,200,300]

data=prepareData(listOfSubjects, seconds, fs)
dataEEG=data.readDataFromFiles()

#dataAfterGA = np.empty((fs, len(stim),4))
for i in range(len(stim)):
    dataAfterGA=createOutputSignal(stim[i], populationSizeList, numberOfMutationsList, dataEEG, numberOfGenes,fs)
    np.savetxt('stim'+str(stim[i])+'.txt', np.squeeze(dataAfterGA), delimiter=',')
