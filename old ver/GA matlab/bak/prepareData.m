function daneOut=prepareData(subj)

Fs = 256;  % Sampling Frequency

N   = 4;   % Order
Fc1 = 49;  % First Cutoff Frequency
Fc2 = 51;  % Second Cutoff Frequency
h  = fdesign.bandstop('N,F3dB1,F3dB2', N, Fc1, Fc2, Fs);
Hd = design(h, 'butter');

Fc1 = 8;   % First Cutoff Frequency
Fc2 = 42;  % Second Cutoff Frequency
h  = fdesign.bandpass('N,F3dB1,F3dB2', N, Fc1, Fc2, Fs);
Hd1 = design(h, 'butter');

path=strcat('C:\Users\Marcin\Dropbox\SSVEP\Bakardjian\',subj,'\');
for trial=1:1:15
    nazwa=dir(path);
    imprt=importdata(strcat(path,nazwa(trial+2,1).name));
    disp(strcat(path,nazwa(trial+2,1).name))
    dane(:,trial)=imprt(1:6300,10);
    dane(:,trial+15)=imprt(1:6300,23);
    dane(:,trial+30)=imprt(1:6300,39);
end

for i=1:1:45
    daneNotch(:,i)=filtfilt(Hd.sosMatrix,Hd.ScaleValues,dane(:,i));
    daneFiltered(:,i)=filtfilt(Hd1.sosMatrix,Hd1.ScaleValues,daneNotch(:,i));
end

daneCut=daneFiltered(1+5*256:8*256,:);

for i=1:1:45
    daneNormalized(:,i)=(daneCut(:,i)-min(daneCut(:,i)))/(max(daneCut(:,i))-min(daneCut(:,i)));
end

daneOut(:,:,1)=daneNormalized(:,1:15);
daneOut(:,:,2)=daneNormalized(:,16:30);
daneOut(:,:,3)=daneNormalized(:,31:45);
