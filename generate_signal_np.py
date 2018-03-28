import aseegg as ag
from os import listdir
from os.path import isfile, join
import numpy as np
from math import ceil, atan

numberOfGenes = 256
numberOfLSig = 3

def readDataFromFiles():
    Subjs=['SUBJ1']#,'SUBJ2','SUBJ3','SUBJ4']
    path="C:\\Users\\Marcin\\Dropbox\\SSVEP\\Bakardjian\\"
    fileNames=[]
    for Sub in Subjs:
        fileNames.extend([Sub+'\\' + f for f in listdir(path+Sub) if isfile(join(path+Sub+'\\',f))])
    data = np.empty((0, numberOfGenes))
    for files in fileNames:
        oneElectrode=prepareData(path+files)
        data=np.append(data, [oneElectrode], axis=0)
    return data

def prepareData(filePath):
    data=np.genfromtxt(filePath, delimiter=",")
    data=data.T
    syg=ag.pasmowozaporowy(data[14],256,49,51)
    syg=ag.pasmowoprzepustowy(syg,256,1,50)
    return syg[5*256:6*256]

def createAdamEve(data):
    firstFamily = np.empty((0, numberOfGenes))
    for i in range(0,3):
        for j in range(i,3):
            firstFamily=np.append(firstFamily, [np.add(data[i],data[j])/2], axis=0)
    firstFamily=np.append(firstFamily, [np.mean(data, axis=0)], axis=0)
    return firstFamily

def createPopulation(data,InitialPopSize):
    family=createAdamEve(data)
    familySize=family.shape[0]
    roundPopSize=ceil((InitialPopSize-familySize)/familySize)
    family=np.repeat(family,roundPopSize+1,axis=0)
    if InitialPopSize%familySize!=0:
        family=family[:InitialPopSize]
    return family

def mutate(numberOfMut, numberOfInvids, indvids):
    for i in range(numberOfMut):
        mutateInvid = np.random.randint(0, numberOfInvids-1)
        mutatePoint = np.random.randint(0, numberOfGenes-1)
        indvids[mutateInvid][mutatePoint] = (np.random.random()-0.5)*(2*indvids[mutateInvid].std()+indvids[mutateInvid].mean())
    return indvids

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

def get_fitness(indvid,stim, EEGSignals):
    p=np.empty((0, 15))
    for i in range(15):
        correlaton = np.corrcoef(indvid,EEGSignals[i])
        p=np.append(p,abs(correlaton[0][1]))
    return Euklides(p,stim)

def sorting(indvids, data, stim):
    fitness = np.empty((0, 15))
    #import pdb; pdb.set_trace()
    for i in range(indvids.shape[0]):
        fitness = np.append(fitness,get_fitness(indvids[i],stim, data))
    indvids=np.column_stack([indvids,fitness])
    indvids=np.array(sorted(indvids, key=lambda x :x[-1]))
    indvids=np.delete(indvids, -1, axis=1)
    return indvids

def main(numberOfSteps, numberOfInvids, numberOfMutations):
    dataAll = readDataFromFiles()
    listOfStim=[14,28,8]
    indvids=createPopulation(dataAll[0:numberOfLSig], numberOfInvids)
    print(indvids.shape)
    #tu moze byc mutacja poczatkowa
    for step in range(numberOfSteps):
        indvids=sorting(indvids,dataAll[0:15],14)
        indvids=mutate(numberOfMutations, numberOfInvids, indvids)
        print(get_fitness(indvids[-1], 14, indvids))
    #print(indvids.shape)
main(100,100,100)
