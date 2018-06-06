function score=classificationGA(dataC14, dataC28, dataC8, populationOUT)

set=[dataC14, dataC28, dataC8];
learningSet(:,:,1)=[populationOUT(:,1), populationOUT(:,4),populationOUT(:,7)];
learningSet(:,:,2)=[populationOUT(:,2), populationOUT(:,5),populationOUT(:,8)];
learningSet(:,:,3)=[populationOUT(:,3), populationOUT(:,6),populationOUT(:,9)];


score=0;
for j=1:1:3
    for i=1:3:9
        [~,~,r]=canoncorr(set(:,j:j+2),squeeze(learningSet(:,:,(i+2)/3)));
        result((i+2)/3,j)=max(r);
    end
end


    if max(result(1,:))==result(1,1)
        score(1,1)= 1;
    else
        score(1,1)= 0;
    end
    if max(result(2,:))==result(2,2)
        score(1,2)= 1;
    else
        score(1,2)= 0;
    end
    if max(result(3,:))==result(3,3)
        score(1,3)= 1;
    else
        score(1,3)= 0;
    end


% result