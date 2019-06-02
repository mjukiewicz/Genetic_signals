import numpy as np
import random
import matplotlib.pyplot as plt
from math import sqrt, pow, exp, atan
import scipy.stats as ss
import scipy.fftpack as sf
from sklearn.cross_decomposition import CCA

class GA():
    def __init__(self, fs,seconds, signal1, signal2, signal3=[]):
        self.n_genes=700
        self.n_pop=100
        self.players_in_tournament=40
        self.n_bits=7
        self.fs=fs
        self.seconds=seconds
        self.mutation_p=0.05
        self.crossover_p=0.75
        self.signal1=signal1
        self.signal2=signal2
        self.signal3=signal3
        self.results3d=[]
        self.n_generations=100

    def mutation(self, individual):
        if random.random()<self.mutation_p:
            point_of_mutation=random.randint(0,self.n_genes-1)
            individual[point_of_mutation]=abs(individual[point_of_mutation]-1)
        return individual

    def crossover(self,parent1,parent2):
        if random.random()<self.crossover_p:
            point_of_crossover=random.randint(0,len(parent1)-1)
            child1=np.append(parent1[:point_of_crossover],parent2[point_of_crossover:], axis=0)
            child2=np.append(parent2[:point_of_crossover],parent1[point_of_crossover:], axis=0)
        else:
            child1=parent1
            child2=parent2
        return child1, child2

    def create_population(self,size1,size2):
        return  np.asarray([[int(round(random.random(),0)) for x in range(size1)] for y in range(size2)])

    def tournament_selection(self,population,fitness):
        new_population=[]
        for i in range(len(fitness)):
            players_list=random.sample(range(len(fitness)), self.players_in_tournament)
            players_fitness=[fitness[players_list[j]] for j in range(len(players_list))]
            new_population.append(population[:,players_list[players_fitness.index(max(players_fitness))]])
        return np.asarray(new_population).T

    def bin2dec(self,bin_list):
        return sum([bin_list[i]*pow(2,len(bin_list)-i-1) for i in range(len(bin_list)-1,-1,-1)])

    def decode_indv(self,indv):
        signal=np.empty([self.fs*self.seconds])
        for i in range(0,len(indv),self.n_bits):
            if i%(self.n_bits*2)==0:
                const= self.bin2dec(indv[i:i+self.n_bits])/(-1+2**self.n_bits)
            else:
                phi= self.bin2dec(190*indv[i:i+self.n_bits]/(-1+2**self.n_bits))
                t=np.linspace(0,1,self.fs*self.seconds)
                signal=signal+const*np.sin(2*np.pi*t*((i+1)/self.n_bits)+phi)

        mmin=min(signal)
        mmax=max(signal)
        for i in range(len(signal)):
            signal[i]=(signal[i]-mmin)/(mmax-mmin)
        return signal.reshape(-1, 1)

    def computeCorr(self,signal,signal_set):
        n_components = 1
        cca = CCA(n_components)
        cca.fit(signal,signal_set)
        U, V = cca.transform(signal,signal_set)
        return np.corrcoef(U.T, V.T)[0, 1]

    def check_fitness(self,population):
        result=[]
        result1=[]
        max_wynik=0
        for i in range(self.n_pop):
            signal=self.decode_indv(population[:,i])
            corr1=self.computeCorr(signal,self.signal1)
            corr2=self.computeCorr(signal,self.signal2)
            if not self.signal3==[]:
                corr3=self.computeCorr(signal,self.signal3)
                wynik=sqrt(pow(corr2-1,2)+pow(corr3-1,2)+pow(corr1,2))
            else:
                wynik=sqrt(pow(corr2-1,2)+pow(corr1,2))
            #wynik=sqrt(3)-sqrt(pow(corr2,2)+pow(corr3,2)+pow(abs(corr1)-1,2))
            #wynik=corr1*atan(corr1/corr3) + corr1*atan(corr1/corr2)
            #wynik=0.5*corr1*(1-corr2)*(1-corr3)

            result.append(wynik)
            #if max_wynik<wynik:
            #    punkty=(corr1,corr2,corr3)
        #self.results3d.append(punkty)
        return result

    def run(self):
        result=[]
        population=self.create_population(self.n_pop,self.n_genes)
        for i in range(self.n_generations):
            fitness=self.check_fitness(population)
            population=self.tournament_selection(population,fitness)
            for j in range(0,self.n_pop,2):
                population[:,j],population[:,j+1]=self.crossover(population[:,j],population[:,j+1])
                population[:,j]=self.mutation(population[:,j])
                population[:,j+1]=self.mutation(population[:,j+1])
            result.append(max(fitness))
            print(i,max(fitness),np.mean(fitness))
        #self.plot_results(population, result)
        return self.decode_indv(population[:,0])

    def plot_results(self, population, result):
        t=np.linspace(0,1,self.fs*self.seconds)
        indv_float=self.decode_indv(population[:,0])
        plt.subplot(311)
        plt.plot(abs(sf.fft(indv_float)))
        plt.xlim([0,50])
        plt.subplot(312)
        plt.plot(t,indv_float)
        plt.plot(t,self.signal1, label='1')
        plt.plot(t,self.signal2, label='2')
        plt.plot(t,self.signal3, label='3')
        plt.legend()
        plt.subplot(313)
        plt.plot(result)
        plt.show()
        #fig = plt.figure()
        #from mpl_toolkits.mplot3d import Axes3D
        #ax=Axes3D(fig)
        #for i in range(len(self.results3d)):
        #    ax.scatter(self.results3d[i][0],self.results3d[i][1],self.results3d[i][2],color=(i/len(self.results3d),0,0), marker='o')
        #plt.show()
