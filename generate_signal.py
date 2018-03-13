import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import aseegg as ag
from math import sqrt
from os import listdir
from os.path import isfile, join

numberOfGenes = 256
numberOfSteps = 10
numberOfInvids = 40
files=[]

Subj=['SUBJ1','SUBJ2','SUBJ3','SUBJ4']
path="C:\\Users\\Marcin\\Dropbox\\SSVEP\\Bakardjian\\"

for i in Subj:
    files.extend([i+'\\' + f for f in listdir(path+i) if isfile(join(path+i+'\\',f))])


def read_data(filePath):
    data=pd.read_csv(filePath, delimiter=",", engine="python", header=None)
    syg=ag.pasmowozaporowy(data.T.loc[14],256,49,51)
    syg=ag.pasmowoprzepustowy(syg,256,1,50)
    return pd.Series(syg[5*256:6*256])


def get_fitness(indvid,stim):
    p=pd.Series()
    for i in range(15):
        correlaton = np.corrcoef(indvid,EEGSignals.T[i])
        p=p.set_value(i, abs(correlaton[0][1]))
    if stim == 14 and p[0]-p[5]<0 or stim == 14 and p[1]-p[6]<0 or stim == 14 and p[2]-p[7]<0:
        return -sqrt(float(p[0]-p[5])**2+float(p[1]-p[6])**2 +float(p[2]-p[7])**2)
    elif stim == 28 and p[0]-p[5]<0 or stim == 28 and p[1]-p[6]<0 or stim == 28 and p[2]-p[7]<0:
        return -sqrt(float(p[0]-p[5])**2+float(p[1]-p[6])**2 +float(p[2]-p[7])**2) 
    
    
    
    elif stim == 8 and p[5]-p[0]<0 or stim == 8 and p[6]-p[1]<0 or stim == 8 and p[7]-p[2]<0:
        return -sqrt(float(p[0]-p[5])**2+float(p[1]-p[6])**2+float(p[2]-p[7])**2)
    else:
        return sqrt(float(p[0]-p[5])**2+float(p[1]-p[6])**2+float(p[2]-p[7])**2)


def ch_generate(p1, p2):
    crossPoint1 = np.random.randint(1, numberOfGenes)
    ch1 = pd.concat([p1[0:crossPoint1], p2[crossPoint1:numberOfGenes]])
    ch2 = pd.concat([p2[0:crossPoint1], p1[crossPoint1:numberOfGenes]])
    ch = pd.concat([ch1,ch2],axis=1)
    return ch


def sorting(stim):
    fitness = pd.DataFrame(np.zeros((1, numberOfInvids)))
    for i in range(len(indvids.T)):
        fitness[i] = get_fitness(indvids[i],stim)
    allData = indvids.append(fitness, ignore_index=True)
    allData = allData.sort_values(allData.last_valid_index(), axis=1,
                                  ascending=False)
    allData = allData.drop(allData.last_valid_index())
    allData = allData.T.reset_index(drop=True).T
    return allData


def mutate():
    #mutateProb = np.random.random()
    for i in range(1000):#if mutateProb > 0.0:
        mutateInvid = np.random.randint(1, numberOfInvids)
        mutatePoint = np.random.randint(0, numberOfGenes)
        indvids[mutateInvid][mutatePoint] = (np.random.random()-0.5)*10

def compCorrCoef(signal,EEGSignals):
    correlaton14 = abs(np.corrcoef(signal[0],EEGSignals.T[i]))
    correlaton28 = abs(np.corrcoef(signal[1],EEGSignals.T[i]))
    correlaton8 = abs(np.corrcoef(signal[2],EEGSignals.T[i]))
    return correlaton14[0][1], correlaton28[0][1], correlaton8[0][1]

def compCorr(signal,ref):
    result=0
    for i in range(0,5):
        corr14, corr28, corr8 = compCorrCoef(signal,EEGSignals)
        if corr14>corr8 and corr14>corr28 :
            result+=1
            
    for i in range(5,10):
        corr14, corr28, corr8 = compCorrCoef(signal,EEGSignals)
        if corr28>corr8 and corr28>corr14:
            result+=1
            
    for i in range(10,15):
        corr14, corr28, corr8 = compCorrCoef(signal,EEGSignals)
        if corr8>corr14 and corr8>corr28:
            result+=1           
                
    return result

def classify():
    print("Skuteczność klasyfikacji otrzymanych:", compCorr(bestIndvid.T,EEGSignals))
    meanSig=pd.concat([pd.DataFrame(EEGSignals[0:3].mean()).T,
                       pd.DataFrame(EEGSignals[5:8].mean()).T,
                       pd.DataFrame(EEGSignals[10:13].mean()).T,
                       ], ignore_index=True)
    print("Skuteczność klasyfikacji uśrednionych:", compCorr(meanSig.T,EEGSignals))

    perfectSig=pd.concat([perfectSin14.T, perfectSin28.T, perfectSin8.T], ignore_index=True)
    print("Skuteczność klasyfikacji idealnych:", compCorr(perfectSig.T,EEGSignals))

t=np.linspace(0,3,numberOfGenes)
perfectSin14=pd.DataFrame(np.sin(2*np.pi*t*14))
perfectSin8=pd.DataFrame(np.sin(2*np.pi*t*8))
perfectSin28=pd.DataFrame(np.sin(2*np.pi*t*28))

EEGSignals=pd.DataFrame()
for fileName in files:
    print(fileName)
    data=read_data(path + fileName)
    EEGSignals=EEGSignals.append(data, ignore_index=True)

wyniki = pd.Series()
stim=[14,28,8]
bestIndvid=pd.DataFrame()
for s in stim:
    if s==14:
        x=pd.DataFrame(EEGSignals[0:3].mean())
    elif s==28:
        x=pd.DataFrame(EEGSignals[5:8].mean())
    elif s==8:
        x=pd.DataFrame(EEGSignals[10:13].mean())
        
    indvids = pd.concat([x.T]*numberOfInvids, ignore_index=True).T
    for i in range(numberOfSteps):
        indvids = sorting(s)
        new_indvids=indvids.loc[:numberOfGenes,:numberOfInvids/2-1]

        for j in range(int(numberOfInvids/4)):
            ch = ch_generate(new_indvids[j*2], new_indvids[1+j*2])
            new_indvids = new_indvids.T.append(ch.T, ignore_index=True).T
        indvids=new_indvids
        mutate()
        bestValue=get_fitness(indvids[0],s)
        wyniki=wyniki.set_value(i, bestValue)
        print('%s, step:%s/%s, fitness:%.2f,' % (datetime.datetime.now(), 
                i +(stim.index(s)*numberOfSteps), numberOfSteps*2, bestValue))

    bestIndvid=bestIndvid.append(indvids[0], ignore_index=True)
    plt.subplot(2,1,1)
    plt.plot(wyniki)
    plt.subplot(2,1,2)
    plt.plot(t,indvids[0])

plt.show()
classify()
