import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

numberOfGenes = 32  
numberOfSteps=100000
ind=[4,8,16,32,64,128,256,512]

def get_fitness(indvid):
    return indvid.sum()

def child_generate(parent1,parent2):
    crossPoint=np.random.randint(1,numberOfGenes)
    child1=pd.concat([parent1[0:crossPoint],parent2[crossPoint:numberOfGenes]])
    child2=pd.concat([parent2[0:crossPoint],parent1[crossPoint:numberOfGenes]])
    return child1,child2

def sorting():
    fitness=pd.DataFrame(np.zeros((1,numberOfInvids)))
    for i in range(len(indvids.T)):
        fitness[i]=get_fitness(indvids[i])
    allData=indvids.append(fitness, ignore_index=True)
    allData=allData.sort_values(allData.last_valid_index(), axis=1, ascending=False)
    allData=allData.drop(allData.last_valid_index())
    allData=allData.T.reset_index(drop=True).T
    return allData

def mutate():
    mutateProb=np.random.random()
    if mutateProb>0.9:
        mutateInvid=np.random.randint(0,numberOfInvids)
        mutatePoint=np.random.randint(0,numberOfGenes)
        indvids[mutateInvid][mutatePoint]=np.random.random()

k=1
for numberOfInvids in ind:
    
    indvids = pd.DataFrame(np.random.rand(numberOfGenes,numberOfInvids))        
    wyniki=[]
    for i in range(numberOfSteps):
        indvids=sorting()
        for j in range(int(numberOfInvids/2)):
            indvids=indvids.T.drop(indvids.T.index[-1]).T
        for j in range(int(numberOfInvids/4)):
            child1,child2=child_generate(indvids[j*2],indvids[1+j*2])
            indvids=indvids.T.append(child1.T, ignore_index=True)
            indvids=indvids.append(child2.T, ignore_index=True).T
        mutate()
        wyniki.append(get_fitness(indvids[0])/numberOfGenes)
        print(100*i*k/(8*numberOfSteps))

    k+=1
    plt.plot(wyniki,label=numberOfInvids)
    plt.legend()
plt.show()