function dataOut=createPopulation(data,populationSize,dataLength)

% dataOut=[];

% for i=1:1:3
%     for j=i:1:3
%         if i~=j
%             dataOut=[dataOut,(data(:,i)+data(:,j))/2];
%         end
%     end
% end
% 
% dataOut=[dataOut,mean(data,2)];
% 
% t=1/256:1/256:1;
% perfect(1,:)=sin(2*pi*14*t);
% perfect(2,:)=sin(2*pi*28*t);
% perfect(3,:)=sin(2*pi*8*t);
% 
% dataOut=[dataOut,perfect'];
% 
% while size(dataOut,2)<populationSize
%     dataOut=[dataOut,dataOut];
% end
% 
% while size(dataOut,2)~=populationSize
%     dataOut(:,end)=[];
% end

dataOut=rand(dataLength,populationSize);