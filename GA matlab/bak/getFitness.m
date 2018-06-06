function [population, maxFitness]=getFitness(population, data, populationSize,numberOfmutation)

fitness(1,1:size(population,2))=0;

for j=1:1:3
    for i=1:1:size(population,2)
        [~,~,r1]=canoncorr(population(:,i),data(:,j));
        [~,~,r2]=canoncorr(population(:,i),data(:,j+3));
        [~,~,r3]=canoncorr(population(:,i),data(:,j+6));
%         if i==1 && j==2
%             [r1, r2, r3]
%         end
        r1=abs(r1);
        r2=abs(r2);
        r3=abs(r3);
        %fitness(1,i)=fitness(1,i) + r1*(atan(r1/r2) + atan(r1/r3)); 
        fitness(1,i)=fitness(1,i) + sqrt((r1-r2)^2+(r1-r3)^2);
%        fitness(1,i)=fitness(1,i) + r1^2 + (r2-1)^2 + (r3-1)^2;
    end
end

population(end+1,:)=fitness;
population=sortrows(population',-length(population))';

maxFitness=population(end,1);
population(end,:)=[];

% fitnessSum=sum(fitness);
% wheel=sort(fitness,'descend')/fitnessSum;

newPopulation=population(:,1:size(population,2)/2);

for i=1:2:size(population,2)/2
    %     wheelSum=0;
    %     wheelPoint=rand(1);
    %     for j=1:1:length(wheel)
    %         wheelSum=wheel(1,j)+wheelSum;
    %         if wheelPoint<wheelSum
    %             break
    %         end
    %     end
    %     wheelSum=0;
    %     wheelPoint=rand(1);
    %     for k=1:1:length(wheel)
    %         wheelSum=wheel(1,k)+wheelSum;
    %         if wheelPoint<wheelSum
    %             break
    %         end
    %     end
    crossPoint=randi(size(population,1));
    newPopulation(:,end+1)=medfilt1([population(1:crossPoint,i); population(crossPoint+1:end,i+1)],5);
    newPopulation(:,end+1)=medfilt1([population(1:crossPoint,i+1); population(crossPoint+1:end,i)],5);
%     newPopulation(:,end+1)=[population(1:crossPoint,i); population(crossPoint+1:end,i+1)];
%     newPopulation(:,end+1)=[population(1:crossPoint,i+1); population(crossPoint+1:end,i)];
end
if size(newPopulation)~=populationSize
    newPopulation(:,end)=[];
end
population=newPopulation;
population=mutation(newPopulation,numberOfmutation);

