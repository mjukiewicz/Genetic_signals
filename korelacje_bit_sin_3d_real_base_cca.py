from GA import GA
from prepareData import prepareData
from classification import classification
import numpy as np
from sklearn.cross_decomposition import CCA

def computeCorr(signal,signal_set):
    n_components = 1
    cca = CCA(n_components)
    cca.fit(signal,signal_set)
    U, V = cca.transform(signal,signal_set)
    return abs(np.corrcoef(U.T, V.T)[0, 1])

fs=256
raw_data=prepareData(['Subj4'],fs)
t=np.linspace(0,1,256)
ref14=np.array([np.sin(2*np.pi*14*t),np.cos(2*np.pi*14*t),np.sin(4*np.pi*14*t),np.cos(4*np.pi*14*t)]).T
ref8=np.array([np.sin(2*np.pi*8*t),np.cos(2*np.pi*8*t),np.sin(4*np.pi*8*t),np.cos(4*np.pi*8*t)]).T

licz=0
wynik=0
for pierwszy in range(5):
    signal14=raw_data.prepared_data(1)[:,pierwszy,:]
    signal8=raw_data.prepared_data(1)[:,10+pierwszy,:]
    if computeCorr(ref14, signal14)>computeCorr(ref8, signal14):
        print(computeCorr(ref14, signal14),computeCorr(ref8, signal14))
        wynik+=1
    if computeCorr(ref14, signal8)<computeCorr(ref8, signal8):
        print(computeCorr(ref14, signal8),computeCorr(ref8, signal8))
        wynik+=1


print(wynik,wynik/10)
