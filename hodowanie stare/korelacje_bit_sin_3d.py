import numpy as np
import random
import matplotlib.pyplot as plt
from math import sqrt, pow, exp
import scipy.stats as ss
import scipy.fftpack as sf
import aseegg as ag

n_genes=700
n_pop=100
players_in_tournament=40
n_bits=7

def mutation(individual):
    if random.random()<0.05:
        point_of_mutation=random.randint(0,n_genes-1)
        individual[point_of_mutation]=abs(individual[point_of_mutation]-1)
    return individual

def crossover(parent1,parent2):
    if random.random()<0.75:
        point_of_crossover=random.randint(0,len(parent1)-1)
        child1=np.append(parent1[:point_of_crossover],parent2[point_of_crossover:], axis=0)
        child2=np.append(parent2[:point_of_crossover],parent1[point_of_crossover:], axis=0)
    else:
        child1=parent1
        child2=parent2
    return child1, child2

def create_population(size1,size2):
    return  np.asarray([[int(round(random.random(),0)) for x in range(size1)] for y in range(size2)])

def tournament_selection(population,fitness):
    new_population=[]
    for i in range(len(fitness)):
        players_list=random.sample(range(len(fitness)), players_in_tournament)
        players_fitness=[fitness[players_list[j]] for j in range(len(players_list))]
        new_population.append(population[:,players_list[players_fitness.index(max(players_fitness))]])
        #print(players_list[players_fitness.index(max(players_fitness))], max(players_fitness))
    return np.asarray(new_population).T

t=np.linspace(0,1,250)
signal14=ag.pasmowoprzepustowy(0.1*np.sin(2*np.pi*t*14)+[0.9*random.random() for x in range(250)],250,1,50)
signal8=ag.pasmowoprzepustowy(0.1*np.sin(2*np.pi*t*8)+[0.9*random.random() for x in range(250)],250,1,50)
signal12=ag.pasmowoprzepustowy(0.1*np.sin(2*np.pi*t*28)+[0.9*random.random() for x in range(250)],250,1,50)

def bin2dec(bin_list):
    return sum([bin_list[i]*pow(2,len(bin_list)-i-1) for i in range(len(bin_list)-1,-1,-1)])

def decode_indv(indv):
    signal=np.empty([250])
    for i in range(0,len(indv),n_bits):
        if i%(n_bits*2)==0:
            const= bin2dec(indv[i:i+n_bits])/127
        else:
            phi= bin2dec(indv[i:i+n_bits])
            signal=signal+const*np.sin(phi*t)

    mmin=min(signal)
    mmax=max(signal)
    for i in range(len(signal)):
        signal[i]=(signal[i]-mmin)/(mmax-mmin)
    return signal

dupa=[]
def check_fitness(population):
    result=[]
    result1=[]
    max_wynik=0
    for i in range(n_pop):
        signal=decode_indv(population[:,i])
        corr14=ss.pearsonr(signal,signal14)
        corr8=ss.pearsonr(signal,signal8)
        corr12=ss.pearsonr(signal,signal12)
        wynik=sqrt(3)-sqrt(pow(corr8[0],2)+pow(corr12[0],2)+pow(corr14[0]-1,2))
        result.append(wynik)
        if max_wynik<wynik:
            punkty=(corr8[0],corr14[0],corr12[0])
    dupa.append(punkty)
    return result
result=[]
population=create_population(n_pop,n_genes)
for i in range(1000):
    fitness=check_fitness(population)
    population=tournament_selection(population,fitness)
    for j in range(0,n_pop,2):
        population[:,j],population[:,j+1]=crossover(population[:,j],population[:,j+1])
        population[:,j]=mutation(population[:,j])
        population[:,j+1]=mutation(population[:,j+1])
    result.append(max(fitness))
    print(i,max(fitness),np.mean(fitness))
indv_float=decode_indv(population[:,0])
plt.subplot(311)
plt.plot(abs(sf.fft(indv_float)))
plt.xlim([0,50])
plt.subplot(312)
plt.plot(indv_float)
plt.plot(signal8)
plt.plot(signal12)
plt.plot(signal14)
plt.subplot(313)
plt.plot(result)
plt.show()
fig = plt.figure()
from mpl_toolkits.mplot3d import Axes3D
ax=Axes3D(fig)
for i in range(len(dupa)):
    ax.scatter(dupa[i][0],dupa[i][1],dupa[i][2],color=(i/len(dupa),0,0), marker='o')
plt.show()
