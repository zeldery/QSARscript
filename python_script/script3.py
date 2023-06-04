# The calculation code

import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score

source = 'source'
result = 'result'

gamma_list = [0.01,0.1,0.5]
C_list = [0.1,1,5]
eps_list = [0.01,0.05,0.2]
outp_list = ['PCE','JscVoc']

gamma_start = [0.005,0.05,0.2]
gamma_end = [0.05,0.2,1.0]
gamma_step = [0.005,0.025,0.05]

C_start = [0.05,0.5,2.0]
C_end = [0.5,2.0,10.0]
C_step = [0.05,0.25,0.5]

eps_start = [0.005,0.02,0.1]
eps_end = [0.02,0.1,0.5]
eps_step = [0.005,0.02,0.05]

if __name__ == '__main__':
    inp_train = pd.read_csv(source + '/D1O1Tr.csv',index_col = 0)
    outp_train = pd.read_csv(source + '/O1D1Tr.csv',index_col = 0)
    inp_test = pd.read_csv(source + '/D1O1Ts.csv',index_col = 0)
    outp_test = pd.read_csv(source + '/O1D1Ts.csv',index_col = 0)
    dat = pd.DataFrame(columns = ['output','gamma','C','epsilon','times','chromosome','R2','Q2CV','Q2'])
    current = 0
    for outp_ind in range(len(outp_list)):
        y_train = outp_train[outp_list[outp_ind]]
        y_test = outp_test[outp_list[outp_ind]]
        for eps_ind in range(len(eps_list)):
            for C_ind in range(len(C_list)):
                for gamma_ind in range(len(gamma_list)):
                    for times in range(10):
                        line = 'GAD1O1-'+str(outp_ind)+str(gamma_ind)+str(C_ind) + str(eps_ind) + str(times)
                        chromo = pd.read_csv(result +'/'+ line+'.csv',index_col = 0)
                        chromo = chromo.values
                        for chromo_ind in range(30):
                            x_train = inp_train.loc[:,chromo[chromo_ind,:]==1]
                            x_test = inp_test.loc[:,chromo[chromo_ind,:]==1]
                            for eps in np.arange(eps_start[eps_ind],eps_end[eps_ind],eps_step[eps_ind]):
                                for C in np.arange(C_start[C_ind],C_end[C_ind],C_step[C_ind]):
                                    for gamma in np.arange(gamma_start[gamma_ind],gamma_end[gamma_ind],gamma_step[gamma_ind]):
                                        model = SVR(gamma=gamma,C=C,epsilon = eps)
                                        model.fit(x_train,y_train)
                                        dat.loc[current] = np.nan
                                        dat.loc[current,'output'] = outp_list[outp_ind]
                                        dat.loc[current,'gamma'] = gamma
                                        dat.loc[current,'C'] = C
                                        dat.loc[current,'epsilon'] = eps
                                        dat.loc[current,'times'] = times
                                        dat.loc[current,'chromosome'] = chromo_ind
                                        dat.loc[current,'R2'] = model.score(x_train,y_train)
                                        dat.loc[current,'Q2'] = model.score(x_test,y_test)
                                        dat.loc[current,'Q2CV'] = cross_val_score(model,x_train,y_train,cv=10).mean()
                                        current = current + 1
    dat.to_csv('result.csv')