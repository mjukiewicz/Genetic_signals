
import numpy as np
from math import atan
import matplotlib.pyplot as plt
from prepareData import prepareData
from geneticFunctions import geneticFunctions

numberOfGenes = 256
numberOfLSig = 3


def Euklides(p,stim):
    sumVal1=0
    sumVal2=0
    if stim == 14:
        for shift in range(numberOfLSig-1):
            sumVal1+=p[0+shift]*180*atan(p[0+shift]/p[5+shift])/np.pi
            sumVal2+=p[0+shift]*180*atan(p[0+shift]/p[10+shift])/np.pi
    if stim == 28:
        for shift in range(numberOfLSig-1):
            sumVal1+=p[5+shift]*180*atan(p[5+shift]/p[0+shift])/np.pi
            sumVal2+=p[5+shift]*180*atan(p[5+shift]/p[10+shift])/np.pi
    if stim == 8:
        for shift in range(numberOfLSig-1):
            sumVal1+=p[10+shift]*180*atan(p[10+shift]/p[0+shift])/np.pi
            sumVal2+=p[10+shift]*180*atan(p[10+shift]/p[5+shift])/np.pi
    return sumVal1+sumVal2

def compCorrCoef(signal,EEGSignals):
    correlaton14 = abs(np.corrcoef(signal[0],EEGSignals))
    correlaton28 = abs(np.corrcoef(signal[1],EEGSignals))
    correlaton8 = abs(np.corrcoef(signal[2],EEGSignals))
    return correlaton14[0][1], correlaton28[0][1], correlaton8[0][1]

def compCorr(signal,ref):
    result=0
    for i in range(0,5):
        corr14, corr28, corr8 = compCorrCoef(signal,ref[i])
        if corr14>corr8 and corr14>corr28 :
            result+=1
    for i in range(5,10):
        corr14, corr28, corr8 = compCorrCoef(signal,ref[i])
        if corr28>corr8 and corr28>corr14:
            result+=1
    for i in range(10,15):
        corr14, corr28, corr8 = compCorrCoef(signal,ref[i])
        if corr8>corr14 and corr8>corr28:
            result+=1
    return result

def classifyPrint(bestIndvid,perfectSig, EEGSignals):
    print("Skuteczność klasyfikacji otrzymanych:", compCorr(bestIndvid,EEGSignals))
    meanSig=np.stack((np.mean(EEGSignals[0:numberOfLSig], axis=0),
                      np.mean(EEGSignals[5:5+numberOfLSig], axis=0),
                      np.mean(EEGSignals[10:10+numberOfLSig], axis=0)))
    plt.figure()
    plt.subplot(211)
    plt.plot(bestIndvid.T)
    plt.subplot(212)
    plt.plot(meanSig.T)
    print("Skuteczność klasyfikacji uśrednionych:", compCorr(meanSig,EEGSignals))
    print("Skuteczność klasyfikacji idealnych:", compCorr(perfectSig,EEGSignals))

def main(numberOfSteps, numberOfInvids, numberOfMutations):
    rData=prepareData(numberOfGenes)
    dataAll = rData.readDataFromFiles()
    perfectSin=rData.createPerfectSin()
    listOfStim=[14,28,8]
    for sub in range(1):
        bestIndvids = np.empty((3, numberOfGenes))
        bestIndvidsFitness = np.empty((3, numberOfSteps))
        for stim in range(len(listOfStim)):
            indvids=createPopulation(dataAll[stim*5+sub*15:numberOfLSig+stim*5+sub*15], numberOfInvids)
            indvids=mutate(4000, numberOfInvids, indvids)
            for step in range(numberOfSteps):
                indvids=generation(indvids,dataAll, listOfStim[stim], sub, numberOfInvids, numberOfMutations)
                bestIndvidsFitness[stim][step]=get_fitness(indvids[0],listOfStim[stim], dataAll[0+sub*15:15+sub*15])
            bestIndvids[stim] = indvids[0]

        classifyPrint(bestIndvids,perfectSin,dataAll[0+sub*15:15+sub*15])
        plt.figure()
        plt.plot(bestIndvidsFitness.T)
        plt.show()
main(80,40,100)

#dodac crossvalidation
