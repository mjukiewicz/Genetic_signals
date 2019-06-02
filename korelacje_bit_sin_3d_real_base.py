from GA import GA
from prepareData import prepareData
from classification import classification
import numpy as np

fs=256
raw_data=prepareData(['Subj4'],fs)
for seconds in range(1,2):
    licz=0
    wynik=0
    for pierwszy in range(5):
        for drugi in range(5):
            if not pierwszy==drugi:
                signal14_1=raw_data.prepared_data(seconds)[:,pierwszy,:]
                signal8_1=raw_data.prepared_data(seconds)[:,10+pierwszy,:]
                signal14_2=raw_data.prepared_data(seconds)[:,drugi,:]
                signal8_2=raw_data.prepared_data(seconds)[:,10+drugi,:]

                ref14=np.concatenate((signal14_1,signal14_2),axis=1)
                ref8=np.concatenate((signal8_1,signal8_2),axis=1)

                idx_list1=list(range(0,5))
                idx_list2=list(range(10,15))
                idx_list1.remove(pierwszy)
                idx_list1.remove(drugi)
                idx_list2.remove(pierwszy+10)
                idx_list2.remove(drugi+10)
                set1=raw_data.prepared_data(seconds)[:,idx_list1,:]
                set2=raw_data.prepared_data(seconds)[:,idx_list2,:]

                wynik+=classification(ref14,ref8,set1,0)+\
                classification(ref14,ref8,set2,1)
                licz+=1

    print(wynik,wynik/(6*licz))
