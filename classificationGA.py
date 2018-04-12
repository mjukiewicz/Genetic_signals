import numpy as np

def compCorrCoefs(signal,EEGSignals):
    correlaton14 = abs(np.corrcoef(signal[0],EEGSignals))
    correlaton28 = abs(np.corrcoef(signal[1],EEGSignals))
    correlaton8 = abs(np.corrcoef(signal[2],EEGSignals))
    return correlaton14[0][1], correlaton28[0][1], correlaton8[0][1]

def compAcc(signal,ref):
    result=0
    for i in range(3,5):
        corr14, corr28, corr8 = compCorrCoefs(signal,ref[i])
        if corr14>corr8 and corr14>corr28 :
            result+=1
    for i in range(8,10):
        corr14, corr28, corr8 = compCorrCoefs(signal,ref[i])
        if corr28>corr8 and corr28>corr14:
            result+=1
    for i in range(13,15):
        corr14, corr28, corr8 = compCorrCoefs(signal,ref[i])
        if corr8>corr14 and corr8>corr28:
            result+=1
    return result

def classifyPrintAndCompute(bestIndvid,perfectSig, meanSig, EEGSignals):
    obtainGA=compAcc(bestIndvid,EEGSignals)
    obtainMean=compAcc(meanSig,EEGSignals)
    obtainPerfect=compAcc(perfectSig,EEGSignals)
    print("Skuteczność klasyfikacji otrzymanych:", obtainGA)
    print("Skuteczność klasyfikacji uśrednionych:", obtainMean)
    print("Skuteczność klasyfikacji idealnych:", obtainPerfect)
    return obtainGA, obtainMean, obtainPerfect
