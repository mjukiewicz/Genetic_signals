function data=mutation(data, mutationNumbers)

for i=1:1:mutationNumbers
   indvid=randi(size(data,2)); 
   point=randi(size(data,1)); 
   data(point,indvid)=rand(1);
end