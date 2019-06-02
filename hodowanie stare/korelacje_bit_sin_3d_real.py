from GA import GA
from prepareData import prepareData
from classification import classification

fs=256
seconds=1

raw_data=prepareData(['Subj1'],fs, seconds)
signal14=raw_data.filtered_data()[:,0,:]
signal28=raw_data.filtered_data()[:,5,:]
signal8=raw_data.filtered_data()[:,10,:]

dupa=GA(fs, seconds, signal14,signal8)
ref14=dupa.run()
#dupa=GA(fs, seconds, signal28,signal8, signal14)
#ref28=dupa.run()
dupa=GA(fs, seconds, signal8,signal14)
ref8=dupa.run()

wynik=classification(ref14,ref8,signal14,signal8,raw_data.filtered_data()[:,1:5,:],0)+classification(ref14,ref8,signal14,signal8,raw_data.filtered_data()[:,11:,:],1)#+classification(ref14,ref28,ref8,raw_data.filtered_data()[:,11:,:],2)

print(wynik,wynik/8)
