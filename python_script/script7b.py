import os
import shutil
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score

from ga import GeneticAlgorithm

source = '../source'
result1 = '../result1'
result2 = '../result2'
temp = '../temp'

cls_list = ['O6','O7','O8','O9']
outp_list = ['PCE','JscVoc']


inp_train = pd.read_csv('inputTr.csv',index_col = 0)
inp_test = pd.read_csv('inputTs.csv',index_col = 0)
outp_train = pd.read_csv('outputTr.csv',index_col = 0)
outp_test = pd.read_csv('outputTs.csv',index_col = 0)

f = open('param.dat','r')
line = f.readline()[:-1]
cls_ind = int(f.readline()[:-1])
outp_ind = int(f.readline()[:-1])
times = int(f.readline()[:-1])
f.close()

f = open(temp+'/'+line+'.info','w')
f.close()

dat = pd.read_csv(source+'/'+'class_param.csv',index_col = 0)
ind = cls_ind*2 + outp_ind
gamma = dat.loc[ind,'gamma']
C = dat.loc[ind,'C']

ga = GeneticAlgorithm(inp_train,outp_train[outp_list[outp_ind]],SVC(gamma = gamma,C = C),30,0.01,-1,0.5,0.0025,8,10)
ga.init()
ga.run(20000)

pd.DataFrame(ga.chromosome).to_csv(result1+'/'+line+'.csv')
new_dat = pd.DataFrame(index = np.arange(30),columns = ['class','output','times','chromosome','R2','Q2CV','Q2'])
new_dat['class'] = cls_list[cls_ind]
new_dat['output'] = outp_list[outp_ind]
new_dat['times'] = times
model = SVC(gamma = gamma, C=C)
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