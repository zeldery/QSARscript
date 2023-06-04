import os
import shutil
import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score

from ga import GeneticAlgorithm

source = '../source'
result1 = '../result1'
result2 = '../result2'
temp = '../temp'

outp_list = ['PCE','JscVcc']

inp_train = pd.read_csv('D1O1Tr.csv',index_col = 0)
inp_test = pd.read_csv('D1O1Ts.csv',index_col = 0)
outp_train = pd.read_csv('O1D1Tr.csv',index_col = 0)
outp_test = pd.read_csv('O1D1Ts.csv',index_col = 0)

f = open('param.dat','r')
line = f.readline()[:-1]
outp_ind = int(f.readline()[:-1])
times = int(f.readline()[:-1])
f.close()

f = open(temp+'/'+line+'.info','w')
f.close()

dat = pd.read_csv(source+'/reg_param.csv',index_col = 0)
C = dat.loc[outp_ind,'C']
gamma = dat.loc[outp_ind,'gamma']
eps = dat.loc[outp_ind,'epsilon']

ga = GeneticAlgorithm(inp_train,outp_train[outp_list[outp_ind]],SVR(gamma = gamma,C = C,epsilon = eps),30,0.01,-1,0.5,0.0025,8,10)
ga.init()
ga.run(20000)

pd.DataFrame(ga.chromosome).to_csv(result1+'/'+line+'.csv')
new_dat = pd.DataFrame(index = np.arange(30),columns = ['output','times','chromosome','R2','Q2CV','Q2'])
new_dat['output'] = outp_list[outp_ind]
new_dat['times'] = times
model = SVR(gamma = gamma,C=C,epsilon = eps)
for i in range(30):
    new_dat.loc[i,'chromosome'] = i
    x_train = inp_train.loc[:,ga.chromosome[i,:]==1]
    x_test = inp_test.loc[:,ga.chromosome[i,:]==1]
    y_train = outp_train[outp_list[outp_ind]]
    y_test = outp_test[outp_list[outp_ind]]
    model.fit(x_train,y_train)
    new_dat.loc[i,'R2'] = model.score(x_train,y_train)
    new_dat.loc[i,'Q2'] = model.score(x_test,y_test)
    new_dat.loc[i,'Q2CV'] = cross_val_score(model,x_train,y_train).mean()
new_dat.to_csv(result2+'/'+line+'.csv')
os.remove(temp+'/'+line+'.info')
os.chdir('..')
shutil.rmtree(line)
