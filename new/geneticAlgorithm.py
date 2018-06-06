from random import randint, random

def mutation(data, numbersOfMutations):
    for i in range(numbersOfMutations):
        element=randint(0,data.shape[2]-1)
        indvid=randint(0,data.shape[1]-1)
        point=randint(0,data.shape[0]-1)
        data[point,indvid,element]=random()
    return data
