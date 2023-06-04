import os
import numpy as np
import pandas as pd
os.chdir('C:/data/research/QSAR/data')
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor

inp = pd.read_csv('csv_g09/D2Tr.csv',index_col=0)
outp = pd.read_csv('csv_output/O1D2Tr.csv',index_col=0)

inp_test = pd.read_csv('csv_g09/D2Ts.csv',index_col=0)
outp_test = pd.read_csv('csv_output/O1D2Ts.csv',index_col=0)
result = pd.DataFrame(columns=['File','chromosome','Output','LinearTrain','LinearTest','SVRTrain','SVRTest','MLPTrain','MLPTest'])

list_file = ['L2J','L2V','L2P','L2JV']
current = 0
for file in list_file:
    var = pd.read_csv('R_output/'+file+'.csv',index_col=0)
    for i in range(var.shape[0]):
        c_inp = inp.ix[:,var.iloc[i,:].dropna()]
        c_inp_test = inp_test.ix[:,var.iloc[i,:].dropna()]
        for j in [0,1,2,4]:
            result.loc[current] = np.nan
            print(current,' ',i,' ',j)
            result.ix[current,'File'] = file
            result.ix[current,'chromosome'] = i
            result.ix[current,'Output'] = ['PCE','Jsc','Voc','','JscVoc'][j]
            lr = LinearRegression()
            lr.fit(c_inp,outp.ix[:,j])
            result.ix[current,'LinearTrain'] = lr.score(c_inp,outp.ix[:,j])
            result.ix[current,'LinearTest' ] = lr.score(c_inp_test,outp_test.ix[:,j])
            svr_sample = SVR()
            tune_para = {'C':[0.1,0.2,0.3,0.5,1,1.2,1.5,2.0]}
            grid = GridSearchCV(svr_sample,tune_para)
            grid.fit(c_inp,outp.ix[:,j])
            svr = grid.best_estimator_
            result.ix[current,'SVRTrain'] = svr.score(c_inp,outp.ix[:,j])
            result.ix[current,'SVRTest'] = svr.score(c_inp_test,outp_test.ix[:,j])
            mlp_sample = MLPRegressor(max_iter = 100000)
            tune_para = {'hidden_layer_sizes':[5,6,7,8]}
            grid = GridSearchCV(mlp_sample,tune_para)
            grid.fit(c_inp,outp.ix[:,j])
            mlp = grid.best_estimator_
            result.ix[current,'MLPTrain'] = mlp.score(c_inp,outp.ix[:,j])
            result.ix[current,'MLPTest'] = mlp.score(c_inp_test,outp_test.ix[:,j])
            current += 1