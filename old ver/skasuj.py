import pandas as pd
from math import ceil
import numpy as np
import scipy.signal as ss
import matplotlib.pyplot as plt
import random
from sklearn.cross_decomposition import CCA
import itertools
from datetime import datetime

def createSubsetsForCV():
    allTrials=np.empty((0,15))
    setOfNums = np.arange(0,5)
    for sub in range(4):
        for subset in itertools.combinations(setOfNums, 3):
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

#trials=createSubsetsForCV()
#print(trials)
'''
for sub in range(4):
    print('----')
    results=[0,0,0]
    for subset in range(10):
        #for i in range(15):
        print(subset+(sub*10))
'''
data=np.genfromtxt("sig.txt", delimiter=",")
data1=np.genfromtxt("perf.txt", delimiter=",")

d1=np.array(data)
d2=np.array(data1)

n_components = 1
cca = CCA(n_components)

        #import pdb; pdb.set_trace()

cca.fit(d1,d2)
U, V = cca.transform(d1,d2)
print(abs(np.corrcoef(U.T, V.T)))
