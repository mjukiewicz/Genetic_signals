function perfect=createPopulation(dataLength,stim, populationSize)

t=1/256:1/256:(dataLength/256);
base(1,:)=(sin(2*pi*stim*t)+1)/2;
base(2,:)=(cos(2*pi*stim*t)+1)/2;
base(3,:)=(sin(4*pi*stim*t)+1)/2;
base(4,:)=(cos(4*pi*stim*t)+1)/2;

base=base';
for i=1:1:populationSize
    perfect(:,i,:)=base;    
end


