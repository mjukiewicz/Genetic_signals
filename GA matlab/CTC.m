function out=CTC(in)

set=[1,2,3,4,5];
out=[];
for i=1:1:length(in)
    part = setdiff(set,in(i,:));
    out=[out;part];
end
