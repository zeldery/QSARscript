# Running script

import numpy as np
import pandas as pd
from sklearn.svm import SVR,SVC
from sklearn.model_selection import cross_val_score
import shutil
import os
from ga import GeneticAlgorithm

run_folder = '../temp'
result_folder = '../result'

x_train = pd.read_csv('inputTr.csv',index_col = 0)
y_train = pd.read_csv('outputTr.csv',index_col = 0)
x_test = pd.read_csv('inputTs.csv',index_col = 0)
y_test = pd.read_csv('outputTs.csv',index_col = 0)

f = open('param.dat','r')
line = f.readline()[:-1]
gamma = float(f.readline()[:-1])
C = float(f.readline()[:-1])
eps = float(f.readline()[:-1])
outp = f.readline()[:-1]
f.close()

f = open(run_folder + '/' + line + '.info','w')
f.close()

ga = GeneticAlgorithm(x_train,y_train[outp],SVR(gamma = gamma,epsilon = eps,C = C),30,0.01,-1,0.5,0.0025,8,10)
ga.init()
ga.run(10000)

os.remove(run_folder + '/' + line + '.info')
pd.DataFrame(ga.chromosome).to_csv(result_folder + '/' + line+'.csv')
os.chdir('..')
shutil.rmtree(line)