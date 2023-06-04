# Scan SVR

i = 0
nrun = 3000

gamma_list = [0.01,0.1,0.5]
C_list = [0.1,1,5]
eps_list = [0.01,0.05,0.2]

gamma_start = [0.005,0.05,0.2]
gamma_end = [0.05,0.2,1.0]
gamma_step = [0.005,0.025,0.05]

C_start = [0.05,0.5,2.0]
C_end = [0.5,2.0,10.0]
C_step = [0.05,0.25,0.5]

eps_start = [0.005,0.02,0.1]
eps_end = [0.02,0.1,0.5]
eps_step = [0.005,0.02,0.05]

import numpy as np
import pandas as pd
from sklearn.svm import SVR,SVC
from sklearn.model_selection import cross_val_score

from ga import GeneticAlgorithm

l = i%len(eps_list)
i = i // len(eps_list)
k = i%len(C_list)
i = i // len(C_list)
j = i%len(gamma_list)
i = i // len(gamma_list)

gamma = gamma_list[j]
C = C_list[k]
eps = eps_list[l]

x_train = pd.read_csv('D1O1Tr.csv',index_col = 0)
y_train = pd.read_csv('O1D1Tr.csv',index_col = 0)
x_test = pd.read_csv('D1O1Ts.csv',index_col = 0)
y_test = pd.read_csv('O1D1Ts.csv',index_col = 0)


ga = GeneticAlgorithm(x_train,y_train['PCE'],SVR(gamma = gamma,epsilon = eps,C = C),30,0.01,-1,0.5,0.0025,8,10)
ga.init()
ga.run(nrun)
dat = pd.DataFrame(columns = ['gamma','C','epsilon','NST','R2','Q2CV','Q2'])
current = 0
for chrom in np.arange(30):
    for gamma in np.arange(gamma_start[j],gamma_end[j],gamma_step[j]):
        for C in np.arange(C_start[k],C_end[k],C_step[k]):
            for eps in np.arange(eps_start[l],eps_end[l],eps_step[l]):
                dat.loc[current] = np.nan
                dat.iloc[current,0] = gamma
                dat.iloc[current,1] = C
                dat.iloc[current,2] = eps
                dat.iloc[current,3] = chrom
                model = SVR(gamma = gamma,epsilon = eps,C = C)
                model.fit(x_train.ix[:,ga.chromosome[chrom,:]==1],y_train['PCE'])
                dat.iloc[current,4] = model.score(x_train.ix[:,ga.chromosome[chrom,:]==1],y_train['PCE'])
                dat.iloc[current,6] = model.score(x_test.ix[:,ga.chromosome[chrom,:]==1],y_test['PCE'])
                dat.iloc[current,5] = cross_val_score(model,x_train.ix[:,ga.chromosome[chrom,:]==1],y_train['PCE']).mean()
                
                current += 1
dat.to_csv('temp1_'+str(j)+str(k)+str(l)+'.csv')
pd.DataFrame(ga.chromosome).to_csv('temp2_'+str(j)+str(k)+str(l)+'.csv')