
import numpy as np
import itertools
#import matplotlib.pyplot as plt
from prepareData import prepareData
from geneticFunctions import geneticFunctions
from classificationGA import classifyPrintAndCompute


def main(numberOfSteps, numberOfInvids, numberOfMutations):
    meanSig=rData.createMeanSig(dataCut)
    oGenetic=geneticFunctions(numberOfGenes, numberOfSteps, numberOfInvids, learningSetSize, numberOfMutations)
    bestIndvids, bestIndvidsFitness = oGenetic.main(dataCut, listOfStim)
    resultGA, resultMean, resultPerfect = classifyPrintAndCompute(bestIndvids,perfectSin, meanSig, dataCut)
    results[0]+=resultGA
    results[1]+=resultMean
    results[2]+=resultPerfect

numberOfGenes = 256
learningSetSize = 3
listOfStim=[14,28,8]
results=[0,0,0]

rData=prepareData(numberOfGenes, learningSetSize, 14)
dataAll = rData.readDataFromFiles()
perfectSin=rData.createPerfectSin()


dataCut = np.empty((15, numberOfGenes))
test = np.array([0, 1, 2, 3, 4])
for sub in range(1):
    for subset in itertools.combinations(test, learningSetSize):
        subset=list(subset)
        for i in test:
            if not i in subset:
                subset.append(i)
        trials=np.concatenate((np.add(subset,0+sub*15), np.concatenate((np.add(subset,5+sub*15), np.add(subset,10+sub*15)), axis=0)), axis=0)
        for i in range(len(trials)):
            dataCut[i]=dataAll[trials[i]]

        main(100,120,100)

for i in results:
    print(100*i/60)
