function perfect=createPerfectSin(dataLength)

t=1/256:1/256:(dataLength/256);

perfect(1,:)=sin(2*pi*14*t);
perfect(2,:)=sin(2*pi*28*t);
perfect(3,:)=sin(2*pi*8*t);
perfect(4,:)=cos(2*pi*14*t);
perfect(5,:)=cos(2*pi*28*t);
perfect(6,:)=cos(2*pi*8*t);

perfect(7,:)=sin(4*pi*14*t);
perfect(8,:)=sin(4*pi*28*t);
perfect(9,:)=sin(4*pi*8*t);
perfect(10,:)=cos(4*pi*14*t);
perfect(11,:)=cos(4*pi*28*t);
perfect(12,:)=cos(4*pi*8*t);

perfect=perfect';

