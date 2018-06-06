function daneCut=prepareData(subj)

electrodeSet=[10,15,21,23,28,39]; %81

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
    for electrode=1:1:size(electrodeSet,2)
        dane(:,trial,electrode)=imprt(1:6300,electrodeSet(electrode));
    end
end

for j=1:1:size(electrodeSet,2)
    for i=1:1:size(dane,2)
        daneNotch(:,i,j)=filtfilt(Hd.sosMatrix,Hd.ScaleValues,dane(:,i,j));
        daneFiltered(:,i,j)=filtfilt(Hd1.sosMatrix,Hd1.ScaleValues,daneNotch(:,i,j));
    end
end

daneCut=daneFiltered(1+5*256:6*256,:,:);

% for j=1:1:size(electrodeSet,2)
%     for i=1:1:size(dane,2)
%         daneNormalized(:,i,j)=(daneCut(:,i,j)-min(daneCut(:,i,j)))/(max(daneCut(:,i,j))-min(daneCut(:,i,j)));
%     end
% end


