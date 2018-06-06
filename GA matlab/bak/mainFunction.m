function result=mainFunction(populationSize, numberOfMutations, numberOfSteps, data,dataLength)

combinations=nchoosek(1:5,3);
combinationsToClassification=CTC(combinations);
score(1:10,1:3)=0;
scoreSin(1:10,1:3)=0;
% data = 256 x 15 x 3
for j=1:1:10
    for i=1:3:9
        dataIn14=[data(:,combinations(j,1),(i+2)/3),     data(:,combinations(j,2),(i+2)/3),    data(:,combinations(j,3),(i+2)/3)];
        dataIn28=[data(:,combinations(j,1)+5,(i+2)/3),   data(:,combinations(j,2)+5,(i+2)/3),  data(:,combinations(j,3)+5,(i+2)/3)];
        dataIn8= [data(:,combinations(j,1)+10,(i+2)/3),  data(:,combinations(j,2)+10,(i+2)/3), data(:,combinations(j,3)+10,(i+2)/3)];
        
        dataIn=[dataIn14,dataIn28,dataIn8];
        [populationOut(:,i),fitness(:,i)]=generation(dataIn,populationSize, numberOfMutations, numberOfSteps, (i+2)/3, dataLength);
        
        dataIn=[dataIn28,dataIn14,dataIn8];
        [populationOut(:,i+1),fitness(:,i+1)]=generation(dataIn,populationSize, numberOfMutations, numberOfSteps, (i+2)/3, dataLength);
        
        dataIn=[dataIn8,dataIn14,dataIn28];
        [populationOut(:,i+2),fitness(:,i+2)]=generation(dataIn,populationSize, numberOfMutations, numberOfSteps, (i+2)/3, dataLength);
    end
%     figure()
%     plot(populationOut)
    perfectSin=createPerfectSin(dataLength);
    for i=1:1:2
        dataC14=[data(:,combinationsToClassification(j,i),1),    data(:,combinationsToClassification(j,i),2),    data(:,combinationsToClassification(j,i),3)];
        dataC28=[data(:,combinationsToClassification(j,i)+5,1),  data(:,combinationsToClassification(j,i)+5,2),  data(:,combinationsToClassification(j,i)+5,3)];
        dataC8= [data(:,combinationsToClassification(j,i)+10,1), data(:,combinationsToClassification(j,i)+10,2), data(:,combinationsToClassification(j,i)+10,3)];
        score(j,:)=score(j,:)+classificationGA(dataC14, dataC28, dataC8, populationOut);
        scoreSin(j,:)=scoreSin(j,:)+classificationGA(dataC14, dataC28, dataC8, perfectSin);
    end
end

result(:,1)=100*sum(sum(score))/60
result(:,2)=100*sum(sum(scoreSin))/60