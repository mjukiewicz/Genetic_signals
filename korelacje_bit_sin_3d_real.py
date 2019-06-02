from GA import GA
from prepareData import prepareData
from classification import classification
import numpy as np

fs=256
raw_data=prepareData(['Subj1'],fs)
seconds=1
for i in range(0,10):
    licz=0
    wynik=0
    for pierwszy in range(5):
        for drugi in range(5):
            if not pierwszy==drugi:
                signal14_1=raw_data.prepared_data(seconds)[:,pierwszy,:]
                signal8_1=raw_data.prepared_data(seconds)[:,10+pierwszy,:]
                signal14_2=raw_data.prepared_data(seconds)[:,drugi,:]
                signal8_2=raw_data.prepared_data(seconds)[:,10+drugi,:]

                t=np.linspace(0,seconds,seconds*fs)
                ref14=np.array([np.sin(2*np.pi*14*t),np.cos(2*np.pi*14*t)]).T
                ref8=np.array([np.sin(2*np.pi*8*t),np.cos(2*np.pi*8*t)]).T
                dupa=GA(fs, seconds, signal14_1,signal14_2, signal8_1,signal8_2, ref14, ref8)
                ref14=dupa.run()
                dupa=GA(fs, seconds, signal8_1,signal8_2, signal14_1,signal14_2, ref8, ref14)
                ref8=dupa.run()

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
print("200")
