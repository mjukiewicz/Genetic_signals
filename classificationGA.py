import numpy as np
import itertools
from prepareData import prepareData
from geneticFunctions import geneticFunctions
#import matplotlib.pyplot as plt

def compCorrCoefs(signal,EEGSignals):
    correlaton14 = abs(np.corrcoef(signal[0],EEGSignals))
    correlaton28 = abs(np.corrcoef(signal[1],EEGSignals))
    correlaton8 = abs(np.corrcoef(signal[2],EEGSignals))
    return correlaton14[0][1], correlaton28[0][1], correlaton8[0][1]

def compAcc(signal,ref):
    result=0
    for i in range(3,5):
        corr14, corr28, corr8 = compCorrCoefs(signal,ref[i])
        if corr14>corr8 and corr14>corr28 :
            result+=1
    for i in range(8,10):
        corr14, corr28, corr8 = compCorrCoefs(signal,ref[i])
        if corr28>corr8 and corr28>corr14:
            result+=1
    for i in range(13,15):
        corr14, corr28, corr8 = compCorrCoefs(signal,ref[i])
        if corr8>corr14 and corr8>corr28:
            result+=1
    return result

def classifyPrintAndCompute(bestIndvid,perfectSig, meanSig, EEGSignals):
    obtainGA=compAcc(bestIndvid,EEGSignals)
    obtainMean=compAcc(meanSig,EEGSignals)
    obtainPerfect=compAcc(perfectSig,EEGSignals)
    print("Skutecznosc klasyfikacji otrzymanych:", obtainGA)
    print("Skutecznosc klasyfikacji usrednionych:", obtainMean)
    print("Skutecznosc klasyfikacji idealnych:", obtainPerfect)
    return obtainGA, obtainMean, obtainPerfect

def main(numberOfSteps, numberOfInvids, numberOfMutations,meanSig, dataCut,numberOfGenes,learningSetSize,listOfStim,perfectSin):
    results=[0,0,0]
    oGenetic=geneticFunctions(numberOfGenes, numberOfSteps, numberOfInvids, learningSetSize, numberOfMutations)
    bestIndvids, bestIndvidsFitness = oGenetic.main(dataCut, listOfStim)
    results[0], results[1], results[2] = classifyPrintAndCompute(bestIndvids,perfectSin, meanSig, dataCut)
    return results

def crossValidationSet(numberOfGenes, learningSetSize, dataAll, rData,listOfStim):
    results=[0,0,0]
    dataCut = np.empty((15, numberOfGenes))
    test = np.arange(0,5)
    for sub in range(1):
        for subset in itertools.combinations(test, learningSetSize):
            subset=list(subset)
            for i in test:
                if not i in subset:
                    subset.append(i)
            trials=np.concatenate((np.add(subset,0+sub*15), np.concatenate((np.add(subset,5+sub*15), np.add(subset,10+sub*15)), axis=0)), axis=0)
            for i in range(len(trials)):
                dataCut[i]=dataAll[trials[i]]
            meanSig=rData.createMeanSig(dataCut)
            perfectSin=rData.createPerfectSin()
            resultsClass = main(100,120,100,meanSig, dataCut,numberOfGenes,learningSetSize,listOfStim,perfectSin)
            for i in range(len(resultsClass)):
                results[i]+=resultsClass[i]
    for i in results:
        print(100*i/40)
