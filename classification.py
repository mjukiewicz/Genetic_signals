import scipy.stats as ss
from sklearn.cross_decomposition import CCA
import numpy as np

def computeCorr(signal,signal_set):
    n_components = 1
    cca = CCA(n_components)
    cca.fit(signal,signal_set)
    U, V = cca.transform(signal,signal_set)
    return np.corrcoef(U.T, V.T)[0, 1]

def classification(signal1GA,signal2GA,set,clss):
    results=[]
    t=np.linspace(0,int(len(signal1GA)/256),len(signal1GA))
    ref14=np.array([np.sin(2*np.pi*14*t),np.cos(2*np.pi*14*t)]).T
    ref8=np.array([np.sin(2*np.pi*8*t),np.cos(2*np.pi*8*t)]).T

    for i in range(3):
        corr11=computeCorr(set[:,i,:],signal1GA)**2
        corr21=computeCorr(set[:,i,:],signal2GA)**2
        corr12=computeCorr(set[:,i,:],ref14)**2
        corr22=computeCorr(set[:,i,:],ref8)**2
        corr13=computeCorr(signal1GA,ref14)**2
        corr23=computeCorr(signal1GA,ref8)**2
        #corr=(abs(corr11),abs(corr21))
        corr=(np.sign(corr11)*corr11+np.sign(corr12)*corr12+np.sign(corr13)*corr13,np.sign(corr21)*corr21+np.sign(corr22)*corr22+np.sign(corr23)*corr23)
        #print(corr)
        results.append(corr.index(max(corr)))
    return check_correct(results,clss)

def check_correct(results,clss):
    result=0
    for i in results:
        if i==clss:
            result+=1
        #print(i,clss,result)
    return result
