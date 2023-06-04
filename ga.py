'''
Genetic Algorithm code
Variable selection for QSPR model
First written by: Thien-Phuc Tu-Nguyen
Tested on Anaconda3 version 4.4 with respective packages
Last modified: June 2017 by Thien-Phuc Tu-Nguyen
'''


import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

class GeneticAlgorithm:
    def __init__(self, inp = None, outp = None, regressor = None,n_chromosome=10,init_prob=0.01,n_cross=-1,cross_prob=0.5,mutation_prob=0.5,max_var=100000,cv=5):
        if regressor == None:
            self.regressor = LinearRegression()
        else:
            self.regressor = regressor
        self.n_chromosome = n_chromosome
        self.init_prob = init_prob
        if n_cross == -1:
            self.n_cross = n_chromosome//2
        else:
            self.n_cross = n_cross
        self.cross_prob = cross_prob
        self.mutation_prob = mutation_prob
        self.max_var = max_var
        self.cv = cv
        self.inp = inp
        self.outp = outp
        self.trace = []
    def init(self):
        self.n_var = self.inp.shape[1]
        self.chromosome = np.zeros((self.n_chromosome,self.n_var))
        for i in range(self.chromosome.shape[0]):
            new = np.random.binomial(1,self.init_prob,(1,self.n_var))
            while new.sum() > self.max_var or new.sum()==0 or not self.check(new):
                new = np.random.binomial(1,self.init_prob,(1,self.n_var))
            self.chromosome[i,:] = new
        self.result_table = pd.DataFrame({'NumVar':np.zeros(self.n_chromosome),'Score':np.zeros(self.n_chromosome)})
        self.result_table['Protected'] = False
        for i in range(self.n_chromosome):
            x = self.inp.loc[:,self.chromosome[i,:]==1]
            self.result_table.iloc[i,1] = cross_val_score(self.regressor,x,self.outp,cv=self.cv).mean()
            self.result_table.iloc[i,0] = self.chromosome[i,:].sum()
        self.rank()
        self.trace = []
    def check(self,new_chromosome):
        be_ok = True
        for i in range(self.n_chromosome):
            if np.absolute(new_chromosome - self.chromosome[i,:]).sum()==0:
                be_ok = False
        return be_ok
    def rank(self):
        self.result_table = self.result_table.sort_values(['Score','NumVar'],ascending = [False,False])
        self.chromosome = self.chromosome[self.result_table.index,:]
        self.result_table.index = pd.Index(np.arange(self.n_chromosome))
        self.result_table['Protected'] = False
        for i in range(self.n_chromosome):
            nvar = self.result_table.iloc[i,0]
            index = self.result_table.iloc[:,0] <= np.repeat(nvar,self.n_chromosome)
            if self.result_table.iloc[i,1] >= self.result_table.loc[index,'Score'].max():
                self.result_table.iloc[i,2] = True
    def add(self,new_chromosome):
        nvar = new_chromosome.sum()
        x = self.inp.loc[:,new_chromosome==1]
        score = cross_val_score(self.regressor,x,self.outp,cv=self.cv).mean()
        i = self.n_chromosome
        while i >= 1 and score >= self.result_table.iloc[i-1,1]:
            i -= 1
        if i < self.n_chromosome:
            j = self.n_chromosome - 1
            while j >= i and self.result_table.iloc[j,0] < nvar and self.result_table.iloc[j,2]:
                j -= 1
            if j >= i:
                for k in range(j,i,-1):
                    self.result_table.iloc[k,:] = self.result_table.iloc[k-1,:]
                    self.chromosome[k,:] = self.chromosome[k-1,:]
                self.result_table.iloc[i,0] = nvar
                self.result_table.iloc[i,1] = score
                self.result_table.index = pd.Index(np.arange(self.n_chromosome))
                self.chromosome[i,:] = new_chromosome
                for k in range(j,i,-1):
                    if self.result_table.iloc[k,0] >= nvar:
                        self.result_table.iloc[k,2] = False
                k = i-1
                while k>=0 and self.result_table.iloc[k,0] > nvar:
                    k -= 1
                if k < 0:
                    self.result_table.iloc[i,2] = True
                else:
                    self.result_table.iloc[i,2] = False
    def cross_over(self):
        choice = np.random.choice(self.n_chromosome,2)
        new = self.chromosome[choice,:]
        rand = np.random.binomial(1,self.cross_prob,self.n_var)
        new[:,rand == 1] = new[:,rand==1][[1,0],:]
        return new
    def mutation(self,i):
        new = np.array(self.chromosome[i,:])
        rand = np.random.binomial(1,self.mutation_prob,self.n_var)
        new[rand==1] = 1 - new[rand==1]
        return new
    def run(self,n_cycle):
        for i in range(n_cycle):
            for j in range(self.n_cross):
                new = self.cross_over()
                if 0 < new[0,:].sum() <= self.max_var and self.check(new[0,:]):
                    self.add(new[0,:])
                if 0 < new[1,:].sum() <= self.max_var and self.check(new[1,:]):
                    self.add(new[1,:])
            for j in range(self.n_chromosome):
                new = self.mutation(j)
                if 0 < new.sum() <= self.max_var and self.check(new):
                    self.add(new)
            self.trace += [self.result_table.loc[:,'Score'].mean()]
    
