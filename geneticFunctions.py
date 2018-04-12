
import numpy as np
from math import ceil, atan

class geneticFunctions(object):

    def __init__(self,numberOfGenes, numberOfSteps, numberOfInvids, learningSetSize, numberOfMutations):
        self.numberOfGenes = numberOfGenes
        self.numberOfSteps = numberOfSteps
        self.numberOfInvids = numberOfInvids
        self.learningSetSize = learningSetSize
        self.numberOfMutations = numberOfMutations

    def createPopulation1(self,data):
        firstIndivd= np.empty((0, self.numberOfGenes))
        while firstIndivd.shape[0]<self.numberOfInvids:
            dupa=np.mean(data, axis=0, keepdims=True)
            firstIndivd=np.append(firstIndivd,dupa, axis=0)
        return firstIndivd

    def createAdamEve(self,data):
        firstFamily = np.empty((0, self.numberOfGenes))
        for i in range(0,3):
            for j in range(i,3):
                firstFamily=np.append(firstFamily, [np.add(data[i],data[j])/2], axis=0)
        firstFamily=np.append(firstFamily, [np.mean(data, axis=0)], axis=0)
        return firstFamily

    def createPopulation(self,data):
        family=self.createAdamEve(data)
        familySize=family.shape[0]
        roundPopSize=ceil((self.numberOfInvids-familySize)/familySize)
        while family.shape[0]<=self.numberOfInvids:
            family=np.append(family,family,axis=0)
        if self.numberOfInvids!=family.shape[0]:
            family=family[:self.numberOfInvids]
        return family

    def mutate(self,numberOfMut, indvids):
        for i in range(numberOfMut):
            mutateInvid = np.random.randint(1, self.numberOfInvids)
            mutatePoint = np.random.randint(0, self.numberOfGenes)
            indvids[mutateInvid][mutatePoint] = np.random.random()
        return indvids

    def get_fitness(self,indvid,stim, EEGSignals):
        p=np.empty((0, 15))
        for i in range(15):
            correlaton = np.corrcoef(indvid,EEGSignals[i])
            p=np.append(p,abs(correlaton[0][1]))
        return self.Euklides(p,stim)

    def Euklides(self,p,stim):
        sumVal1=0
        sumVal2=0
        if stim == 14:
            for shift in range(self.learningSetSize-1):
                sumVal1+=p[0+shift]*180*atan(p[0+shift]/p[5+shift])/np.pi
                sumVal2+=p[0+shift]*180*atan(p[0+shift]/p[10+shift])/np.pi
        if stim == 28:
            for shift in range(self.learningSetSize-1):
                sumVal1+=p[5+shift]*180*atan(p[5+shift]/p[0+shift])/np.pi
                sumVal2+=p[5+shift]*180*atan(p[5+shift]/p[10+shift])/np.pi
        if stim == 8:
            for shift in range(self.learningSetSize-1):
                sumVal1+=p[10+shift]*180*atan(p[10+shift]/p[0+shift])/np.pi
                sumVal2+=p[10+shift]*180*atan(p[10+shift]/p[5+shift])/np.pi
        return sumVal1+sumVal2

    def sorting(self,indvids, data, stim):
        fitness = np.empty((0, 15))
        for i in range(indvids.shape[0]):
            fitness = np.append(fitness,self.get_fitness(indvids[i],stim, data))
        indvids=np.column_stack([indvids,fitness])
        indvids=np.array(sorted(indvids, key=lambda x :x[-1], reverse=True))
        indvids=np.delete(indvids, -1, axis=1)
        return indvids

    def ch_generate(self,p1, p2):
        crossPoint1 = np.random.randint(1, self.numberOfGenes)
        ch1=np.concatenate((p1[0:crossPoint1], p2[crossPoint1:self.numberOfGenes]))
        ch2=np.concatenate((p2[0:crossPoint1], p1[crossPoint1:self.numberOfGenes]))
        ch = np.vstack([ch1,ch2])
        return ch

    def generation(self,indvids,dataAll,stim):
        indvids=self.sorting(indvids,dataAll[0:15],stim)
        indvids=self.mutate(self.numberOfMutations, indvids)
        new_indvids=indvids[:int(indvids.shape[0]/2)]
        for j in range(int(self.numberOfInvids/4)):
            ch = self.ch_generate(indvids[j*2], indvids[1+j*2])
            new_indvids=np.vstack([new_indvids,ch])
        return new_indvids

    def main(self,dataAll,listOfStim):
        bestIndvids = np.empty((3, self.numberOfGenes))
        bestIndvidsFitness = np.empty((3, self.numberOfSteps))
        for stim in range(len(listOfStim)):
            indvids=self.createPopulation(dataAll[0:self.learningSetSize])
            indvids=self.mutate(4000, indvids)
            for step in range(self.numberOfSteps):
                indvids=self.generation(indvids,dataAll, listOfStim[stim])
                bestIndvidsFitness[stim][step]=self.get_fitness(indvids[0],listOfStim[stim], dataAll[0:15])
            bestIndvids[stim] = indvids[0]
        return bestIndvids, bestIndvidsFitness
