import numpy as np
import itertools
#from prepareData import prepareData
from geneticFunctions import geneticFunctions
from sklearn.cross_decomposition import CCA
import matplotlib.pyplot as plt
from datetime import datetime


class processing(object):
    def __init__(self,numberOfGenes, learningSetSize, listOfStim, data14,
                data22,data27,numberOfSteps, numberOfInvids, numberOfMutations, numberOfSubjects):
        self.numberOfGenes = numberOfGenes
        self.learningSetSize = learningSetSize
        self.listOfStim=listOfStim
        self.data14=data14
        self.data22=data22
        self.data27=data27
        self.numberOfSteps = numberOfSteps
        self.numberOfInvids = numberOfInvids
        self.numberOfMutations = numberOfMutations
        self.numberOfSubjects=numberOfSubjects

    def crossValidation(self):
        dataCut14 = np.empty((15, self.numberOfGenes))
        dataCut22 = np.empty((15, self.numberOfGenes))
        dataCut27 = np.empty((15, self.numberOfGenes))
        trials=self.createSubsetsForCV()
        for sub in range(self.numberOfSubjects):
            results=[0,0,0]
            for subset in range(10):
                for i in range(15):
                    dataCut14[i]=self.data14[trials[subset+(sub*10)][i]]
                    dataCut22[i]=self.data22[trials[subset+(sub*10)][i]]
                    dataCut27[i]=self.data27[trials[subset+(sub*10)][i]]
                oGenetic=geneticFunctions(self.numberOfGenes, self.numberOfSteps, self.numberOfInvids, self.learningSetSize, self.numberOfMutations)
                bestIndvids14, bestIndvidsFitness14 = oGenetic.main(dataCut14, self.listOfStim)
                oGenetic=geneticFunctions(self.numberOfGenes, self.numberOfSteps, self.numberOfInvids, self.learningSetSize, self.numberOfMutations)
                bestIndvids22, bestIndvidsFitness22 = oGenetic.main(dataCut22, self.listOfStim)
                oGenetic=geneticFunctions(self.numberOfGenes, self.numberOfSteps, self.numberOfInvids, self.learningSetSize, self.numberOfMutations)
                bestIndvids27, bestIndvidsFitness27 = oGenetic.main(dataCut27, self.listOfStim)

                learningSet=self.createLearningSets(bestIndvids14, bestIndvids22, bestIndvids27)
                results=np.add(results,self.classification(learningSet, np.vstack([dataCut14,dataCut22,dataCut27]),subset))
            self.writeResultsToFile(results, sub, self.numberOfSteps, self.numberOfInvids, self.numberOfMutations)

    def createLearningSets(self, data1, data2, data3):
        dataOut1=np.vstack([data1[0],data2[0],data3[0]])
        dataOut2=np.vstack([data1[1],data2[1],data3[1]])
        dataOut3=np.vstack([data1[2],data2[2],data3[2]])
        return np.vstack([dataOut1, dataOut2, dataOut3])

    def createSubsetsForCV(self):
        allTrials=np.empty((0,15))
        setOfNums = np.arange(0,5)
        for sub in range(self.numberOfSubjects):
            for subset in itertools.combinations(setOfNums, self.learningSetSize):
                subset=list(subset)
                for i in setOfNums:
                    if not i in subset:
                        subset.append(i)
                trials=np.concatenate((np.add(subset,0+sub*15),
                                       np.concatenate((np.add(subset,5+sub*15),
                                                       np.add(subset,10+sub*15)),
                                                      axis=0)), axis=0)
                allTrials=np.vstack([allTrials,trials])
        return allTrials.astype(int)

    def classification(self,learningSet,EEGSignals,subset):
        meanSig=self.createMeanSig(EEGSignals)
        perfectSig=self.createPerfectSin()

        plt.figure()
        for i in range(9):
            plt.subplot(9,1,i+1)
            plt.plot(learningSet[i])
        plt.savefig(str(subset)+".png")
        #print(np.corrcoef(learningSet[6],learningSet[7])[0][1])
        #print(np.corrcoef(learningSet[7],learningSet[8])[0][1])
        #print(np.corrcoef(learningSet[6],learningSet[8])[0][1])
        obtainGA=self.compAcc(learningSet,EEGSignals)
        obtainMean=self.compAcc(meanSig,EEGSignals)
        obtainPerfect=self.compAcc(perfectSig,EEGSignals)
        #print("Skutecznosc klasyfikacji otrzymanych:", obtainGA)
        #print("Skutecznosc klasyfikacji usrednionych:", obtainMean)
        #print("Skutecznosc klasyfikacji idealnych:", obtainPerfect)
        #return np.array([obtainGA, obtainGA, obtainGA])
        return np.array([obtainGA, obtainMean, obtainPerfect])

    def compCorrCoefs(self,learningSet,EEGSignals):
        n_components = 1
        cca = CCA(n_components)
        #print(EEGSignals.shape)
        '''
        correlation14 = abs(np.corrcoef(np.mean(learningSet[0:3].T, axis=1),np.mean(EEGSignals.T, axis=1))[0, 1])
        correlation28 = abs(np.corrcoef(np.mean(learningSet[3:6].T, axis=1),np.mean(EEGSignals.T, axis=1))[0, 1])
        correlation8 = abs(np.corrcoef(np.mean(learningSet[6:9].T, axis=1),np.mean(EEGSignals.T, axis=1))[0, 1])

        print(learningSet[0][0],learningSet[1][0],learningSet[2][0])
        for i in range(0,9,3):
            print(abs(np.corrcoef(learningSet[i].T,EEGSignals[int(i/3)].T)[0, 1]),
                  abs(np.corrcoef(learningSet[i+1].T,EEGSignals[int(i/3)].T)[0, 1]),
                  abs(np.corrcoef(learningSet[i+2].T,EEGSignals[int(i/3)].T)[0, 1]))
        print("---")
        '''

        cca.fit(learningSet[0:3].T,EEGSignals.T)
        U, V = cca.transform(learningSet[0:3].T,EEGSignals.T)
        correlation14 = abs(np.corrcoef(U.T, V.T)[0, 1])

        cca.fit(learningSet[3:6].T,EEGSignals.T)
        U, V = cca.transform(learningSet[3:6].T,EEGSignals.T)
        correlation28 = abs(np.corrcoef(U.T, V.T)[0, 1])

        cca.fit(learningSet[6:9].T,EEGSignals.T)
        U, V = cca.transform(learningSet[6:9].T,EEGSignals.T)
        correlation8 = abs(np.corrcoef(U.T, V.T)[0, 1])
        
        return correlation14, correlation28, correlation8

    def compAcc(self,learningSet,EEGSignals):
        result=0
        for i in range(3,5):
            corr14, corr28, corr8 = self.compCorrCoefs(learningSet,np.vstack((EEGSignals[i],EEGSignals[i+15],EEGSignals[i+30])))
            if corr14 == max([corr14, corr28, corr8]):
                result+=1
        for i in range(8,10):
            corr14, corr28, corr8 = self.compCorrCoefs(learningSet,np.vstack((EEGSignals[i],EEGSignals[i+15],EEGSignals[i+30])))
            if corr28 == max([corr14, corr28, corr8]):
                result+=1
        for i in range(13,15):
            corr14, corr28, corr8 = self.compCorrCoefs(learningSet,np.vstack((EEGSignals[i],EEGSignals[i+15],EEGSignals[i+30])))
            if corr8 == max([corr14, corr28, corr8]):
                result+=1
        return result


    def createPerfectSin(self):
        t=np.linspace(0,1,self.numberOfGenes)
        return np.vstack((np.tile(np.sin(2*np.pi*t*14),(3,1)),
                          np.tile(np.sin(2*np.pi*t*28),(3,1)),
                          np.tile(np.sin(2*np.pi*t*8),(3,1))))

    def createMeanSig(self, signals):
        meanSig=np.empty((0,self.numberOfGenes))
        for i in range(9):
            meanSig=np.append(meanSig, [np.mean(signals[5*i:5*i+self.learningSetSize],axis=0)], axis=0)
        return meanSig

    def writeResultsToFile(self,results, sub, numberOfSteps, numberOfInvids, numberOfMutations):
        textFile = open('results.txt', 'a')
        textFile.write(str(datetime.now())+", "+ str(numberOfSteps)+", "+str(numberOfInvids)+", "+str(numberOfMutations)+", "+str(sub)+", "+str(results[0])+", "+str(results[1])+", "+str(results[2])+'\n')
        textFile.close()
