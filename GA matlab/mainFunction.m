function result=mainFunction(numberOfMutations, numberOfSteps, data,dataLength, populationSize)

combinations=nchoosek(1:5,3);
combinationsToClassification=CTC(combinations);
score(1:10,1:3)=0;
scoreSin(1:10,1:3)=0;
% data = 256 x 15 x 7

for j=1:1:10
    for i=1:3:18
        fprintf('%d kombinacja %d elektroda\n', j, (i+2)/3)
        dataIn14=[data(:,combinations(j,1),(i+2)/3),     data(:,combinations(j,2),(i+2)/3),    data(:,combinations(j,3),(i+2)/3)];
        dataIn28=[data(:,combinations(j,1)+5,(i+2)/3),   data(:,combinations(j,2)+5,(i+2)/3),  data(:,combinations(j,3)+5,(i+2)/3)];
        dataIn8= [data(:,combinations(j,1)+10,(i+2)/3),  data(:,combinations(j,2)+10,(i+2)/3), data(:,combinations(j,3)+10,(i+2)/3)];

        dataIn=[dataIn14,dataIn28,dataIn8];
        [populationOut(:,:,i),fitness(:,i)]=generation(dataIn, numberOfMutations, numberOfSteps, dataLength, 14, populationSize);
        dataIn=[dataIn28,dataIn14,dataIn8];
        [populationOut(:,:,i+1),fitness(:,i+1)]=generation(dataIn, numberOfMutations, numberOfSteps, dataLength, 28, populationSize);
        dataIn=[dataIn8,dataIn14,dataIn28];
        [populationOut(:,:,i+2),fitness(:,i+2)]=generation(dataIn, numberOfMutations, numberOfSteps, dataLength, 8, populationSize);
    end
    %populationOut to powinna byc macierz 256x4x3 probki x 4perfekty x 3
    %bodzce
    perfectSin=createPerfectSin(dataLength);
    for i=1:1:2
        dataC14=data(:,combinationsToClassification(j,i),1:6);
        dataC28=data(:,combinationsToClassification(j,i)+5,1:6);
        dataC8= data(:,combinationsToClassification(j,i)+10,1:6);
        
        score(j,:)=score(j,:)+classificationGA(dataC14, dataC28, dataC8, populationOut);
        scoreSin(j,:)=scoreSin(j,:)+classificationGAperfect(dataC14, dataC28, dataC8, perfectSin);
    end
end

result(:,1)=100*sum(sum(score))/40
result(:,2)=100*sum(sum(scoreSin))/40