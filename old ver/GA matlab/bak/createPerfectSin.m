function perfect=createPerfectSin(dataLength)

t=1/256:1/256:(dataLength/256);

for i=1:3:9
perfect(i,:)=sin(2*pi*14*t);
perfect(i+1,:)=sin(2*pi*28*t);
perfect(i+2,:)=sin(2*pi*8*t);
end

perfect=perfect';

