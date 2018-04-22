from prepareData import prepareData
from classificationGA import processing

import matplotlib.pyplot as plt

numberOfGenes = 256
learningSetSize = 3
listOfStim=(14,28,8)
electrodeSet=(14,22,27)
numberOfSteps=10
numberOfInvids=40
numberOfMutations=10
listOfSubjects =  ['SUBJ3']#,'SUBJ4']#,'SUBJ3','SUBJ4']


electrode14=prepareData(numberOfGenes, learningSetSize, 14, listOfSubjects)
electrode22=prepareData(numberOfGenes, learningSetSize, 22, listOfSubjects)
electrode27=prepareData(numberOfGenes, learningSetSize, 27, listOfSubjects)

data14=electrode14.readDataFromFiles()
data22=electrode22.readDataFromFiles()
data27=electrode27.readDataFromFiles()

for i in range(1):
    oProcess=processing(numberOfGenes, learningSetSize, listOfStim,
                        data14, data22, data27,numberOfSteps, numberOfInvids,
                        numberOfMutations, len(listOfSubjects))

    oProcess.crossValidation()
