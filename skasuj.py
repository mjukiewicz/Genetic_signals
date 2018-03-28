import pandas as pd
from math import ceil
import numpy as np
import scipy.signal as ss
import matplotlib.pyplot as plt
import random


data=np.array([[5,2,8],
              [2,3,6],
              [3,4,5]])
print(data.shape)
data=np.array(sorted(data, key=lambda x :x[-1]))
print(np.delete(data, -1, axis=1))
