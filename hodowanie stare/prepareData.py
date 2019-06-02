from os import listdir
from os.path import isfile, join
import numpy as np
import aseegg as ag


class prepareData(object):

    def __init__ (self,list_of_subjects, fs, seconds):
         self.notch_cut_off1=49
         self.notch_cut_off2=51
         self.bandpass_cut_off1=7
         self.bandpass_cut_off2=15
         self.list_of_subjects=list_of_subjects
         self.seconds=seconds
         self.fs=fs
         self.electrode_set=[15-1,21-1,23-1,28-1,17-1,30-1];
         #self.electrodeSet=[10-1,15-1,21-1,23-1,28-1,39-1];
         #self.electrode_set=[23-1]
         self.path="C:\\Users\\Marcin\\Dropbox\\SSVEP\\Bakardjian\\"
         self.data=self.read_data_from_files()

    def read_data_from_files(self):
        file_names=[]
        for Sub in self.list_of_subjects:
            file_names.extend([Sub+'\\' + f for f in listdir(self.path+Sub) if isfile(join(self.path+Sub+'\\',f))])

        data = np.empty((self.fs*self.seconds, 15, len(self.electrode_set)))
        for i in range(len(file_names)):
            dataRaw=np.genfromtxt(self.path+file_names[i], delimiter=",")
            dataRaw=dataRaw.T
            for j in range(len(self.electrode_set)):
                data[:,i,j]=self.filtering_data(dataRaw[self.electrode_set[j]])
            print("Wczytano dane dla pliku:", file_names[i])
        return data

    def filtered_data(self):
        return self.data

    def filtering_data(self,data):
        syg=ag.pasmowozaporowy(data, self.fs, self.notch_cut_off1,self.notch_cut_off2)
        syg=ag.pasmowoprzepustowy(syg, self.fs, self.bandpass_cut_off1,self.bandpass_cut_off2)
        return self.normalize_data(syg[self.fs*5+36:(5+self.seconds)*self.fs+36])

    def normalize_data(self,signal):
        minSignal=signal.min()
        maxSignal=signal.max()
        signal=(signal-minSignal)/(maxSignal-minSignal)
        return signal
