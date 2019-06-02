from prepareData import prepareData
import numpy as np
import itertools

def createSubsetsForCV():
    allTrials=np.empty((0,15))
    setOfNums = np.arange(0,5)
    for subset in itertools.combinations(setOfNums, 3):
        subset=list(subset)
        for i in setOfNums:
            if not i in subset:
                subset.append(i)
        trials=np.concatenate((np.add(subset,0),
                               np.concatenate((np.add(subset,5),
                                               np.add(subset,10)),
                                              axis=0)), axis=0)
        allTrials=np.vstack([allTrials,trials])
    return allTrials.astype(int)

listOfSubjects=['SUBJ1']
seconds=1
fs=256

stim8 = np.genfromtxt('stim8.txt', delimiter=',')
stim14 = np.genfromtxt('stim14.txt', delimiter=',')
stim28 = np.genfromtxt('stim28.txt', delimiter=',')
'''
data=prepareData(listOfSubjects, seconds, fs)
dataEEG=data.readDataFromFiles()
'''
subsets=createSubsetsForCV()
print(subsets)
