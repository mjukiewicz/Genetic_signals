function [populationOut,fitnessOut ]=generation(dataIn,populationSize, numberOfMutation, numberOfSteps, dataLength)

population=createPopulation(populationSize,dataLength,dataIn);

for i=1:1:numberOfSteps
[population, bestFitness(i,1)]=getFitness(population, dataIn, populationSize,numberOfMutation);
end
plot(bestFitness); hold on
populationOut=population(:,end);
fitnessOut=bestFitness(end,1);

