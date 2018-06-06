% function dataOut=sort3d(data3d, data1d)
clear
t=1/256:1/256:1;
data3d(1,:,1:10)=repmat(sin(2*pi*t*10),10,1)';
data3d(2,:,1:10)=repmat(2*sin(2*pi*t*10),10,1)';
data3d(3,:,1:10)=repmat(3*sin(2*pi*t*10),10,1)';
data3d(4,:,1:10)=repmat(4*sin(2*pi*t*10),10,1)';
data3d(5,:,1:10)=repmat(5*sin(2*pi*t*10),10,1)';
data3d(6,:,1:10)=repmat(6*sin(2*pi*t*10),10,1)';

data1d=1:6;

dataOut=[];
[M,I] = sort(data1d,'descend');
for i=1:1:length(data1d)
    dataOut(i,:,:)=data3d(I(1,i),:,:);
end