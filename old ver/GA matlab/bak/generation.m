function [populationOut,fitnessOut ]=generation(dataIn,populationSize, numberOfMutation, numberOfSteps, stim,dataLength)

population=createPopulation(dataIn(:,stim:stim+2),populationSize,dataLength);
% population=mutation(population,numberOfMutation);

for i=1:1:numberOfSteps
[population, bestFitness(i,1)]=getFitness(population, dataIn, populationSize,numberOfMutation);
end
plot(bestFitness); hold on
populationOut=population(:,end);
fitnessOut=bestFitness(end,1);

