function data=mutation(data, mutationNumbers)

for i=1:1:mutationNumbers
    element=randi(size(data,3));
   indvid=randi(size(data,2)); 
   point=randi(size(data,1)); 
   data(point,indvid,element)=rand(1);
end