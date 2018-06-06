function score=classificationGAperfect(dataC14, dataC28, dataC8, populationOUT)

set=[dataC14, dataC28, dataC8];

learningSet(:,:,1)=[populationOUT(:,1), populationOUT(:,4),populationOUT(:,7),populationOUT(:,10)];
learningSet(:,:,2)=[populationOUT(:,2), populationOUT(:,5),populationOUT(:,8),populationOUT(:,11)];
learningSet(:,:,3)=[populationOUT(:,3), populationOUT(:,6),populationOUT(:,9),populationOUT(:,12)];


score=0;
[~,~,r]=canoncorr(squeeze(dataC14),squeeze(learningSet(:,:,1)));
result(1,1)=max(r);
[~,~,r]=canoncorr(squeeze(dataC14),squeeze(learningSet(:,:,2)));
result(1,2)=max(r);
[~,~,r]=canoncorr(squeeze(dataC14),squeeze(learningSet(:,:,3)));
result(1,3)=max(r);

[~,~,r]=canoncorr(squeeze(dataC28),squeeze(learningSet(:,:,1)));
result(2,1)=max(r);
[~,~,r]=canoncorr(squeeze(dataC28),squeeze(learningSet(:,:,2)));
result(2,2)=max(r);
[~,~,r]=canoncorr(squeeze(dataC28),squeeze(learningSet(:,:,3)));
result(2,3)=max(r);

[~,~,r]=canoncorr(squeeze(dataC8),squeeze(learningSet(:,:,1)));
result(3,1)=max(r);
[~,~,r]=canoncorr(squeeze(dataC8),squeeze(learningSet(:,:,2)));
result(3,2)=max(r);
[~,~,r]=canoncorr(squeeze(dataC8),squeeze(learningSet(:,:,3)));
result(3,3)=max(r);


    if max(result(1,:))==result(1,1)
        score(1,1)= 1;
    else
        score(1,1)= 0;
    end
%     if max(result(2,:))==result(2,2)
%         score(1,2)= 1;
%     else
%         score(1,2)= 0;
%     end
    if max(result(3,:))==result(3,3)
        score(1,3)= 1;
    else
        score(1,3)= 0;
    end

