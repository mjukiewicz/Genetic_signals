#wersja 1.7

import scipy.signal as sig
import numpy as np
from pylab import *

def gornoprzepustowy(sygnal,czestProbkowania,czestOdciecia):
    rzad=4
    czestOdciecia=czestOdciecia/(czestProbkowania*0.5)
    [b, a] = sig.butter(rzad,czestOdciecia,'high')
    wynik=sig.filtfilt(b,a,sygnal)
    return wynik

def dolnoprzepustowy(sygnal,czestProbkowania,czestOdciecia):
    rzad=4
    czestOdciecia=czestOdciecia/(czestProbkowania*0.5)
    [b, a] = sig.butter(rzad,czestOdciecia,'low')
    wynik=sig.filtfilt(b,a,sygnal)
    return wynik

def pasmowoprzepustowy(sygnal,czestProbkowania,czestOdciecia1,czestOdciecia2):
    rzad=4
    czestOdciecia1=czestOdciecia1/(czestProbkowania*0.5)
    czestOdciecia2=czestOdciecia2/(czestProbkowania*0.5)
    [b, a] = sig.butter(rzad,[czestOdciecia1,czestOdciecia2],'bandpass')
    wynik=sig.filtfilt(b,a,sygnal)
    return wynik

def pasmowozaporowy(sygnal,czestProbkowania,czestOdciecia1,czestOdciecia2):
    rzad=4
    czestOdciecia1=czestOdciecia1/(czestProbkowania*0.5)
    czestOdciecia2=czestOdciecia2/(czestProbkowania*0.5)
    [b, a] = sig.butter(rzad,[czestOdciecia1,czestOdciecia2],'bandstop')
    wynik=sig.filtfilt(b,a,sygnal)
    return wynik

def FFT(sygnal):
    dlugoscFFT=nastepnaPotega(len(sygnal))
    wynik=2*abs(np.fft.fft(sygnal*sig.hamming(len(sygnal))))/len(sygnal)
    return wynik

def rysujFFT(sygnal, show_plot=True):
    dlugoscFFT=nastepnaPotega(len(sygnal))
    wynik=2*abs(np.fft.fft(sygnal*sig.hamming(len(sygnal))))/len(sygnal)
    if len(sygnal)%256==0:
        f=np.linspace(0,256, len(sygnal))
    else:
        f=np.linspace(0,200, len(sygnal))
    plt.figure()
    plt.plot(f,wynik)
    plt.xlim([0,50])
    if show_plot:
        plt.show()

def spektrogram(data, Fs, colormap=cm.Accent,
                    show_plot=True, ylim=50):
    plt.figure()
    data_padded = (np.concatenate((np.zeros(200),data,np.zeros(200))))
    Pxx, freqs, bins, im =specgram(data_padded, NFFT=512,
                                   Fs=Fs, window=sig.hamming(512), noverlap=2*Fs-1, #noverlap=Fs-1,
                                   cmap=cm.jet)

    plt.ylim(0, ylim)
    plt.xlim(0, len(data)/Fs)

    if show_plot:
        plt.show()

def formatujPlik(sciezka):
    nazwapliku=''.join(["\\\\" if i=="\\" else i for i in sciezka])

    with open(nazwapliku, 'r') as plikWejsciowy:
        dane = plikWejsciowy.read().splitlines(True)
    with open(nazwapliku, 'w') as plikWyjsciowy:
        if dane[0][0]=='l':
            [plikWyjsciowy.writelines(linia) for linia in dane]
        elif dane[0][1]!=' ':
            plikWyjsciowy.writelines("lp, e1, e2, e3, e4, trigger\n")
            [plikWyjsciowy.writelines(linia.replace(',',', ')) for linia in dane]
        else:
            plikWyjsciowy.writelines("lp, e1, e2, e3, e4, e5, e6, e7, e8, a1, a2, a3\n")
            [plikWyjsciowy.writelines(linia.replace(',','.').replace('. ',', ')) for linia in dane if linia[0]!='%']

def nastepnaPotega(x):
    return 2**(x-1).bit_length()
