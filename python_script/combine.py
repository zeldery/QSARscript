# Combine code

import numpy as np
import pandas as pd
dat = pd.DataFrame(columns=['gamma','C','epsilon','NST','R2','Q2CV','Q2'])
for i in range(3):
    for j in range(3):
        for k in range(3):
            temp = pd.read_csv('temp1_'+str(i)+str(j)+str(k)+'.csv',index_col=0)
            dat = pd.concat((dat,temp))
dat.index = np.arange(dat.shape[0])
gamma_list = np.concatenate((np.arange(0.005,0.05,0.005),np.arange(0.05,0.2,0.025),np.arange(0.2,1.0,0.05)))
C_list = np.concatenate((np.arange(0.05,0.5,0.05),np.arange(0.5,2.0,0.25),np.arange(2.0,10.0,0.5)))
eps_list = np.concatenate((np.arange(0.005,0.02,0.005),np.arange(0.02,0.1,0.02),np.arange(0.1,0.5,0.05)))


# gamma C
new_dat = pd.DataFrame(columns =['gamma','C','R2','Q2CV','Q2'])
current = 0
for gamma in gamma_list:
    for C in C_list:
        new_dat.loc[current] = np.nan
        temp = dat.ix[(dat['gamma'] - gamma) **2 <= 0.000001,:]
        temp = temp.ix[ (temp['C'] - C) **2 <= 0.000001,:]
        temp.index = np.arange(temp.shape[0])
        i = temp['Q2CV'].argmax()
        new_dat.iloc[current,0] = gamma
        new_dat.iloc[current,1] = C
        new_dat.iloc[current,2:] = temp.iloc[i,-3:]
        current += 1
fig = plot3d(gamma_list,C_list,new_dat.ix[:,[0,1,4]])
fig.show()

# gamma eps
new_dat = pd.DataFrame(columns =['gamma','eps','R2','Q2CV','Q2'])
current = 0
for gamma in gamma_list:
    for eps in eps_list:
        new_dat.loc[current] = np.nan
        temp = dat.ix[(dat['gamma'] - gamma) **2 <= 0.000001,:]
        temp = temp.ix[ (temp['epsilon'] - eps) **2 <= 0.000001,:]
        temp.index = np.arange(temp.shape[0])
        i = temp['Q2CV'].argmax()
        new_dat.iloc[current,0] = gamma
        new_dat.iloc[current,1] = eps
        new_dat.iloc[current,2:] = temp.iloc[i,-3:]
        current += 1
fig = plot3d(gamma_list,eps_list,new_dat.ix[:,[0,1,4]])
fig.show()

# C eps
new_dat = pd.DataFrame(columns =['C','eps','R2','Q2CV','Q2'])
current = 0
for C in C_list:
    for eps in eps_list:
        new_dat.loc[current] = np.nan
        temp = dat.ix[(dat['C'] - C) **2 <= 0.000001,:]
        temp = temp.ix[ (temp['epsilon'] - eps) **2 <= 0.000001,:]
        temp.index = np.arange(temp.shape[0])
        i = temp['Q2CV'].argmax()
        new_dat.iloc[current,0] = C
        new_dat.iloc[current,1] = eps
        new_dat.iloc[current,2:] = temp.iloc[i,-3:]
        current += 1
fig = plot3d(C_list,eps_list,new_dat.ix[:,[0,1,3]])
fig.show()