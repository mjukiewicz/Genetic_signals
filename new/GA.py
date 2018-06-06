from prepareData import prepareData
from sklearn.cross_decomposition import CCA
import numpy as np
from math import atan
from geneticAlgorithm import mutation
import matplotlib.pyplot as plt
import time

listOfSubjects=['SUBJ1']
seconds=1
fs=256
stim=14;
n_components = 1
cca = CCA(n_components)

populationSizeList=[10,20,50,100,150,200,300,500]
numberOfMutationsList=[10,20,50,70,100,150,200,300]

data=prepareData(listOfSubjects, seconds, fs)
dataEEG=data.readDataFromFiles()

for populationSize in populationSizeList:
    for numberOfMutations in numberOfMutationsList:
        start = time.clock()
        population=data.createPopulation(stim, populationSize)
        x, y=[],[0]
        maxFitness=9.33
        step=1
        popVar=0
        while True:
            fitness=np.zeros((1, populationSize))
            for j in range(3):
                for i in range(populationSize):
                    cca.fit(population[:,i,:],dataEEG[:,j,:])
                    U, V = cca.transform(population[:,i,:],dataEEG[:,j,:])
                    r1 = abs(np.corrcoef(U.T, V.T)[0, 1])

                    cca.fit(population[:,i,:],dataEEG[:,j,:])
                    U, V = cca.transform(population[:,i,:],dataEEG[:,j+5,:])
                    r2 = abs(np.corrcoef(U.T, V.T)[0, 1])

                    cca.fit(population[:,i,:],dataEEG[:,j,:])
                    U, V = cca.transform(population[:,i,:],dataEEG[:,j+10,:])
                    r3 = abs(np.corrcoef(U.T, V.T)[0, 1])

                    fitness[0,i]+= r1*atan(r1/r3) + r1*atan(r1/r2)

            SortedIndexes= np.argsort(-fitness)
            newPopulation = np.empty((seconds*fs,populationSize,4))
            for i in range(populationSize):
                newPopulation[:,i,:] = population[:,SortedIndexes[0,i],:]

            population=np.concatenate((newPopulation[:,0:int(populationSize/2),:], newPopulation[:,0:int(populationSize/2),:]),axis=1)
            maxFitness=9.33-fitness[0,SortedIndexes[0,0]]
            mutation(population,numberOfMutations)

            x.append(step)
            y.append(maxFitness)
            print("step: %d, fitness: %.6f, var: %.6f" %(step, maxFitness, popVar))
            if step==1:
                y.pop(0)
            elif step>50:
                popVar=np.var(y[-51:-1])
            if step>100 and popVar<0.000001:
                break
            step+=1
        #plt.plot(x,y)
        #plt.show()
        koniec = time.clock()
        czas_trwania = koniec - start
        tekst="step: "+str(step-1)+", fitness: "+str(round(maxFitness,6))+", time: "+str(round(czas_trwania,2))+", mutations:"+str(numberOfMutations)+", population:"+ str(populationSize)
        plik_tekstowy = open('test.txt', 'a')
        plik_tekstowy.writelines(tekst)
        plik_tekstowy.close()
