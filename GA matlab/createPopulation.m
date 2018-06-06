function perfect=createPopulation(dataLength,stim, populationSize)

t=1/256:1/256:(dataLength/256);
base(1,:)=sin(2*pi*stim*t);
base(2,:)=cos(2*pi*stim*t);
base(3,:)=sin(4*pi*stim*t);
base(4,:)=cos(4*pi*stim*t);

for i=1:1:populationSize
    perfect(:,:,i)=base;    
end


