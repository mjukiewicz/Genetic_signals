clearvars -except dane

subj='SUBJ1';
seconds=1;
fs=256;
dataLength=seconds*fs;
populationSize=100;
numberOfmutation=200;
numberOfSteps=1000;
stim=14;

population=createPopulationGA(dataLength,stim, populationSize);
dane=prepareData(subj);
figure()
xlim([0 numberOfSteps])
hold on
for step=1:1:numberOfSteps
    fitness(1,1:size(population,2))=0;
    
    for j=1:1:3
        for i=1:1:size(population,2)
            [~,~,r1]=canoncorr(squeeze(population(:,i,:)),squeeze(dane(:,j,:)));
            [~,~,r2]=canoncorr(squeeze(population(:,i,:)),squeeze(dane(:,j+5,:)));
            [~,~,r3]=canoncorr(squeeze(population(:,i,:)),squeeze(dane(:,j+10,:)));
            r1=max(abs(r1));
            r2=max(abs(r2));
            r3=max(abs(r3));
            
            fitness(1,i)=fitness(1,i) + r1*atan(r1/r3) + r1*atan(r1/r2);
        end
    end
    fprintf('%f %f\n',r1,r3);
    
    newPop=[];
    [M,I] = sort(fitness,'descend');
    for i=1:1:length(fitness)
        newPop(:,i,:)=population(:,I(1,i),:);
    end
    
    population=[newPop(:,1:(populationSize/2),:), newPop(:,1:(populationSize/2),:)];
    maxFitness(1,step)= M(1,1);
    population=mutationGA(population,numberOfmutation);
    plot(maxFitness);drawnow
    
end

figure()
plot(abs(fft(population(:,1,1))))