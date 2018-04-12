import time
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import aseegg as ag
from math import sqrt
from os import listdir
from os.path import isfile, join
import scipy.signal as ss

numberOfGenes = 256
numberOfLSig = 3
files=[]

Subj=['SUBJ1','SUBJ2','SUBJ3','SUBJ4'] #jakim cudem czasem pojawia sie minus?
path="C:\\Users\\Marcin\\Dropbox\\SSVEP\\Bakardjian\\"

for i in Subj:
    files.extend([i+'\\' + f for f in listdir(path+i) if isfile(join(path+i+'\\',f))])


def read_data(filePath):
    data=pd.read_csv(filePath, delimiter=",", engine="python", header=None)
    syg=ag.pasmowozaporowy(data.T.loc[14],256,49,51)
    syg=ag.pasmowoprzepustowy(syg,256,1,50)
    return pd.Series(syg[5*256:6*256])

def checkHighestP(p, stimS):
    result = 0
    for shift in range(numberOfLSig):
        vec=pd.Series([p[0+shift],p[5+shift],p[10+shift]]).max()
        if p[0+shift]==vec and stimS==14:
            result+=1
        elif p[5+shift]==vec and stimS==28:
            result+=1
        elif p[10+shift]==vec and stimS==8:
            result+=1
    return int(result/3)

def Euklides(p,stimSS):
    sumVal1=0
    sumVal2=0
    if stimSS == 14:
        for shift in range(numberOfLSig):
            sumVal1+=float(p[0+shift]-p[5+shift])**2
            sumVal2+=float(p[0+shift]-p[10+shift])**2
    if stimSS == 28:
        for shift in range(numberOfLSig):
            sumVal1+=float(p[5+shift]-p[0+shift])**2
            sumVal2+=float(p[5+shift]-p[10+shift])**2
    if stimSS == 8:
        for shift in range(numberOfLSig):
            sumVal1+=float(p[10+shift]-p[0+shift])**2
            sumVal2+=float(p[10+shift]-p[5+shift])**2

    return sqrt(sumVal1)+sqrt(sumVal2)

def get_fitness(indvid,stimS, EEGSignals):
    p=pd.Series()
    for i in range(15):
        correlaton = np.corrcoef(indvid,EEGSignals.T[i])
        p=p.set_value(i, abs(correlaton[0][1]))

    if checkHighestP(p, stimS):
        return Euklides(p,stimS)
    else:
        return -Euklides(p,stimS)


def ch_generate(p1, p2):
    crossPoint1 = np.random.randint(1, numberOfGenes)

    ch1 = pd.concat([p1[0:crossPoint1], p2[crossPoint1:numberOfGenes]])
    ch2 = pd.concat([p2[0:crossPoint1], p1[crossPoint1:numberOfGenes]])
    ch = pd.concat([pd.Series(ss.medfilt(ch1.as_matrix(), kernel_size=5)),
                    pd.Series(ss.medfilt(ch2.as_matrix(), kernel_size=5))],axis=1)
#    ch = pd.concat([pd.Series(ch1.as_matrix()),
#                 pd.Series(ch2.as_matrix())],axis=1)
    return ch.T


def sorting(stimS, numberOfInvids, indvids,EEGSignals):
    global srFit, zz
    fitness = pd.DataFrame(np.zeros((1, numberOfInvids)))
    for i in range(len(indvids.T)):
        #print(i,indvids.shape)
        fitness[i] = get_fitness(indvids[i],stimS, EEGSignals)

    allData = indvids.append(fitness, ignore_index=True)

    newData = pd.DataFrame()
    for i in range(int(numberOfInvids/2)):
        participant = pd.DataFrame()
        for j in range(5):
            randNumber = np.random.randint(0,numberOfInvids)
            participant = participant.append(allData[randNumber]).reset_index(drop=True)

        participant = participant.T
        participant = participant.sort_values(participant.last_valid_index(), axis=1,ascending=False)
        newData=newData.append(participant[participant.columns[0]])

    newData = newData.T.reset_index(drop=True)
    newData = newData.sort_values(newData.last_valid_index(), axis=1,
                                  ascending=False)

    newData = newData.T.reset_index(drop=True)
    srFit=srFit.set_value(zz, newData[256][0])#fitness.T.var())

    newData = newData.T.drop(allData.last_valid_index())
    newData = newData.reset_index(drop=True).T

    return newData


def mutate(numberOfMut, numberOfInvids, indvids):
    #mutateProb = np.random.random()
    for i in range(numberOfMut):
    #if mutateProb > 0.0:
        mutateInvid = np.random.randint(0, numberOfInvids-1)
        mutatePoint = np.random.randint(0, numberOfGenes-1)
        indvids[mutateInvid][mutatePoint] = (np.random.random()-0.5)*(2*indvids[mutateInvid].std()+indvids[mutateInvid].mean())
    return indvids

def compCorrCoef(signal,EEGSignals):
    correlaton14 = abs(np.corrcoef(signal[0],EEGSignals))
    correlaton28 = abs(np.corrcoef(signal[1],EEGSignals))
    correlaton8 = abs(np.corrcoef(signal[2],EEGSignals))
    return correlaton14[0][1], correlaton28[0][1], correlaton8[0][1]

def compCorr(signal,ref):
    result=0
    for i in range(0,5):
        corr14, corr28, corr8 = compCorrCoef(signal,ref.T[i])
        if corr14>corr8 and corr14>corr28 :
            result+=1

    for i in range(5,10):
        corr14, corr28, corr8 = compCorrCoef(signal,ref.T[i])
        if corr28>corr8 and corr28>corr14:
            result+=1

    for i in range(10,15):
        corr14, corr28, corr8 = compCorrCoef(signal,ref.T[i])
        if corr8>corr14 and corr8>corr28:
            result+=1

    return result

def classify(bestIndvid,EEGSignals):
    print("Skuteczność klasyfikacji otrzymanych:", compCorr(bestIndvid.T,EEGSignals))
    meanSig=pd.concat([pd.DataFrame(EEGSignals[0:numberOfLSig].mean()).T,
                       pd.DataFrame(EEGSignals[5:5+numberOfLSig].mean()).T,
                       pd.DataFrame(EEGSignals[10:10+numberOfLSig].mean()).T,
                       ], ignore_index=True)
    print("Skuteczność klasyfikacji uśrednionych:", compCorr(meanSig.T,EEGSignals))

    perfectSig=pd.concat([perfectSin14.T, perfectSin28.T, perfectSin8.T], ignore_index=True)
    print("Skuteczność klasyfikacji idealnych:", compCorr(perfectSig.T,EEGSignals))

t=np.linspace(0,numberOfGenes/256,numberOfGenes)
perfectSin14=pd.DataFrame(np.sin(2*np.pi*t*14))
perfectSin8=pd.DataFrame(np.sin(2*np.pi*t*8))
perfectSin28=pd.DataFrame(np.sin(2*np.pi*t*28))

def main(numberOfSteps, numberOfInvids, numberOfMutations):
    global srFit, zz
    AllEEGSignals=pd.DataFrame()
    for fileName in files:
        #print(fileName)
        data=read_data(path + fileName)
        AllEEGSignals=AllEEGSignals.append(data, ignore_index=True)

    stim=[14,28,8]
    for sub in range(len(Subj)):
        EEGSignals=AllEEGSignals[0:15].reset_index(drop=True)
        wyniki = pd.Series()
        srFit= pd.Series()

        bestIndvid=pd.DataFrame()
        for s in stim:
            if s==14:
                x=pd.DataFrame(EEGSignals[0:numberOfLSig].mean())
            elif s==28:
                x=pd.DataFrame(EEGSignals[5:5+numberOfLSig].mean())
            elif s==8:
                x=pd.DataFrame(EEGSignals[10:10+numberOfLSig].mean())

            indvids = pd.concat([x.T]*numberOfInvids, ignore_index=True).T
            indvids=mutate(4000, numberOfInvids, indvids)
            for zz in range(numberOfSteps):

                indvids = sorting(s, numberOfInvids, indvids,EEGSignals)
                start = time.clock()

                new_indvids=indvids.T
                for j in range(int(numberOfInvids/4)):
                    ch = ch_generate(new_indvids[j*2], new_indvids[1+j*2])
                    new_indvids = new_indvids.T.append(ch, ignore_index=True).T
                indvids=new_indvids
                print(time.clock()-start)
                indvids=mutate(numberOfMutations, numberOfInvids, indvids)
                bestValue=get_fitness(indvids[0],s,EEGSignals)

                wyniki=wyniki.set_value(zz, bestValue)

    #            print('%s, step:%s/%s, fitness:%.2f,' % (datetime.datetime.now(),
    #                    i +(stim.index(s)*numberOfSteps), numberOfSteps*numberOfLSig, bestValue))

            bestIndvid=bestIndvid.append(indvids[0], ignore_index=True)
#            plt.subplot(2,1,1)
#            plt.plot(wyniki, label=s)
#            plt.legend()
#            plt.subplot(2,1,2)
#            #plt.plot(t,indvids[0])
#            plt.plot(srFit)

            print(srFit.iloc[-1])
        classify(bestIndvid,EEGSignals)
        AllEEGSignals.drop(AllEEGSignals.index[0:15], inplace=True)
#    plt.show()


#for k in range(20, 510, 60):
#    print("---------------")
#    print(k)
#    start = time.clock()
main(20,20,20)
#    print(time.clock()-start)
