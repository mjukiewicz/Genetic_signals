import pandas as pd
from math import ceil
import numpy as np
import scipy.signal as ss
import matplotlib.pyplot as plt
import random

import itertools

dataCut = np.empty((0, 256))
test = np.array([0, 1, 2, 3, 4])

for sub in range(4):
    for subset in itertools.combinations(test, 3):
        subset=list(subset)
        for i in test:
            if not i in subset:
                subset.append(i)
        trials=np.concatenate((np.add(subset,0+sub*15), np.concatenate((np.add(subset,5+sub*15), np.add(subset,10+sub*15)), axis=0)), axis=0)
        print(trials)
        #for i in range(len(trials)):
        #    dataCut=np.append(dataCut,dataAll[i], axis=0)
