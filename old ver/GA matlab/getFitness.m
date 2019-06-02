function [population, maxFitness]=getFitness(population, data, numberOfmutation)

fitness(1,1:size(population,3))=0;

for j=1:1:3
    for i=1:1:size(population,3)
        [~,~,r1]=canoncorr(squeeze(population(:,:,i)'),data(:,j));
        [~,~,r2]=canoncorr(squeeze(population(:,:,i)'),data(:,j+3));
        [~,~,r3]=canoncorr(squeeze(population(:,:,i)'),data(:,j+6));
        r1=abs(r1);
        r2=abs(r2);
        r3=abs(r3);
%        fitness(1,i)=fitness(1,i) + r1*(atan(r1/r2) + atan(r1/r3)); 
%         fitness(1,i)=fitness(1,i) + sqrt((r1-r2)^2+(r1-r3)^2);
%        fitness(1,i)=fitness(1,i) + r1^2 + (r2-1)^2 + (r3-1)^2;
%         fitness(1,i)=fitness(1,i)+r1;

%       fitness(1,i)=fitness(1,i) + r1*atan(r1/r3); 
%         fitness(1,i)=fitness(1,i) + r1-r3;
%        fitness(1,i)=fitness(1,i) + r1^2 + (r3-1)^2;
         fitness(1,i)=fitness(1,i)+r1;
    end
end

newPop=[];
[M,I] = sort(fitness,'descend');
for i=1:1:length(fitness)
    newPop(:,:,i)=population(:,:,I(1,i));
end
population=newPop;
% population(end+1,:,:)=repmat(fitness,256,1);
% population=sortrows(population',-length(population))';
% 
maxFitness=M(1,1);
% population(:,:,end)=[];

% newPopulation=population(:,1:size(population,2)/2);

% for i=1:2:size(population,2)/2
%     crossPoint=randi(size(population,1));
%     newPopulation(:,end+1)=medfilt1([population(1:crossPoint,i); population(crossPoint+1:end,i+1)],5);
%     newPopulation(:,end+1)=medfilt1([population(1:crossPoint,i+1); population(crossPoint+1:end,i)],5);
% 
% end
% if size(newPopulation)~=populationSize
%     newPopulation(:,end)=[];
% end
% population=newPopulation;
population=mutation(population,numberOfmutation);

