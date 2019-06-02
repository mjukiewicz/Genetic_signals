from GA import GA
from prepareData import prepareData
from classification import classification
import numpy as np

fs=256
raw_data=prepareData(['Subj1'],fs)
seconds=1

pierwszy=0
drugi=1

signal14_1=raw_data.prepared_data(seconds)[:,pierwszy,:]
signal8_1=raw_data.prepared_data(seconds)[:,10+pierwszy,:]
signal14_2=raw_data.prepared_data(seconds)[:,drugi,:]
signal8_2=raw_data.prepared_data(seconds)[:,10+drugi,:]

t=np.linspace(0,seconds,seconds*fs)
ref14=np.array([np.sin(2*np.pi*14*t),np.cos(2*np.pi*14*t)]).T
ref8=np.array([np.sin(2*np.pi*8*t),np.cos(2*np.pi*8*t)]).T
for i in range(10):
    dupa=GA(fs, seconds, signal14_1,signal14_2, signal8_1,signal8_2, ref14, ref8)
    ref14=dupa.run()
