function [populationOut,fitnessOut ]=generation(dataIn, numberOfMutation, numberOfSteps, dataLength, stim, populationSize)

population=createPopulation(dataLength,stim, populationSize);

for i=1:1:numberOfSteps
    [population, bestFitness(i,1)]=getFitness(population, dataIn, numberOfMutation);
end
plot(bestFitness); 
populationOut=population(:,:,end);
fitnessOut=bestFitness(end,1); %tu trzeba sprawdzicz czy ma przekazywac ostatnie czy pierwsze elementy


