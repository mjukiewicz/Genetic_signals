from prepareData import prepareData
from classificationGA import classifyPrintAndCompute, crossValidationSet, main


numberOfGenes = 256
learningSetSize = 3
listOfStim=[14,28,8]
electrodeSet=[14,22,27]

rData=prepareData(numberOfGenes, learningSetSize, 14)
dataAll = rData.readDataFromFiles()


crossValidationSet(numberOfGenes, learningSetSize, dataAll, rData,listOfStim)
