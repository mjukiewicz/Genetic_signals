from random import randint, random
from sklearn.cross_decomposition import CCA
import numpy as np
from math import atan
from time import clock

def mutation(data, numbersOfMutations):
    for i in range(numbersOfMutations):
        element=randint(0,data.shape[2]-1)
        indvid=randint(0,data.shape[1]-1)
        point=randint(0,data.shape[0]-1)
        data[point,indvid,element]=random()
    return data

def computeCorrCoef(data1, data2):
    n_components = 1
    cca = CCA(n_components)
    cca.fit(data1, data2)
    U, V = cca.transform(data1, data2)
    return abs(np.corrcoef(U.T, V.T)[0, 1])

def sortPopulation(fitness,numberOfGenes,populationSize,population):
    SortedIndexes= np.argsort(-fitness)
    newPopulation = np.empty((numberOfGenes,populationSize,4))
    for i in range(populationSize):
        newPopulation[:,i,:] = population[:,SortedIndexes[0,i],:]

    return np.concatenate((newPopulation[:,0:int(populationSize/2),:],
                           newPopulation[:,0:int(populationSize/2),:]),axis=1), 3*np.pi-fitness[0,SortedIndexes[0,0]]

def singleGeneration(populationSize, population, dataEEG, numberOfMutations, numberOfGenes, stim):
    fitness=np.zeros((1, populationSize))
    if stim==14:
        dataStimuli=dataEEG[:,0:5,:]
        dataNoStimuli1=dataEEG[:,5:10,:]
        dataNoStimuli2=dataEEG[:,10:15,:]
    if stim==28:
        dataStimuli=dataEEG[:,5:10,:]
        dataNoStimuli1=dataEEG[:,0:5,:]
        dataNoStimuli2=dataEEG[:,10:15,:]
    if stim==8:
        dataStimuli=dataEEG[:,10:15,:]
        dataNoStimuli1=dataEEG[:,0:5,:]
        dataNoStimuli2=dataEEG[:,5:10,:]
    for j in range(3):
        for i in range(populationSize):
            r1=computeCorrCoef(population[:,i,:],dataStimuli[:,j,:])
            r2=computeCorrCoef(population[:,i,:],dataNoStimuli1[:,j,:])
            r3=computeCorrCoef(population[:,i,:],dataNoStimuli2[:,j,:])
            fitness[0,i]+= r1*atan(r1/r3) + r1*atan(r1/r2)

    population, maxFitness=sortPopulation(fitness,numberOfGenes,populationSize,population)

    return mutation(population,numberOfMutations), maxFitness

def createPopulation(seconds, fs, stim, populationSize):
    base = np.empty((4, seconds*fs))
    perfect = np.empty((seconds*fs,populationSize,4))

    t=np.linspace(0,seconds,fs)
    base[0,:]=(np.sin(2*np.pi*stim*t)+1)/2;
    base[1,:]=(np.cos(2*np.pi*stim*t)+1)/2;
    base[2,:]=(np.sin(4*np.pi*stim*t)+1)/2;
    base[3,:]=(np.cos(4*np.pi*stim*t)+1)/2;

    base=base.T
    for i in range(populationSize):
        perfect[:,i,:]=base;

    return perfect

def createOutputSignal(stim, populationSizeList, numberOfMutationsList, dataEEG, numberOfGenes, fs):
    for populationSize in populationSizeList:
        for numberOfMutations in numberOfMutationsList:
            start = clock()
            population=createPopulation(int(numberOfGenes/fs), fs,stim, populationSize)
            y=[]
            step=1
            popVar=0
            while True:
                population,maxFitness=singleGeneration(populationSize, population, dataEEG, numberOfMutations, numberOfGenes, stim)
                print("step: %d, fitness: %.6f, var: %.6f" %(step, maxFitness, popVar))
                y.append(maxFitness)
                if step>50:
                    popVar=np.var(y[-51:-1])
                if step>100 and popVar<0.000001 or step>10000: #0.000001
                    break
                step+=1
            koniec = clock()
            czas_trwania = koniec - start
            tekst="stim: "+ str(stim)+ ", step: "+str(step-1)+", fitness: "+str(round(maxFitness,6))+", time: "+str(round(czas_trwania,2))+", mutations:"+str(numberOfMutations)+", population:"+ str(populationSize)+"\n"
            plik_tekstowy = open('test.txt', 'a')
            plik_tekstowy.writelines(tekst)
            plik_tekstowy.close()

    return population[:,0,:]
