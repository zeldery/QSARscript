import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

outp = pd.read_csv('../csv_output/O1.csv',index_col=0)

EEVA_sigma = [25,50,75,100,150]
EEVA_L = [25,50,80,100,200]
EVA_sigma = [1,2,4,6,10,15]
EVA_L = [1,2,5,8,10,20]

dat = pd.DataFrame(columns = ['Output','Components','EEVA sigma','EEVA L','EVA sigma','EVA L','Times','Train','Test'])
current = 0
for eeva_sigma in EEVA_sigma:
    for eeva_L in EEVA_L:
        for eva_sigma in EVA_sigma:
            for eva_L in EVA_L:
                inp1 = pd.read_csv('EEVA_'+str(eeva_sigma)+'_'+str(eeva_L)+'_std.csv',index_col=0)
                inp2 = pd.read_csv('EVA_'+str(eva_sigma)+'_'+str(eva_L)+'_std.csv',index_col=0)
                inp_all = pd.merge(inp1,inp2,left_index=True,right_index=True)
                common = pd.merge(outp,inp_all,left_index=True,right_index=True)
                y = common.ix[:,:5]
                x = common.ix[:,5:]
                for n_comp in [5,10,20]:
                    model = PLSRegression(n_components = n_comp,scale=False)
                    for outp_index in [0,1,2,4]:
                        for i in range(3):
                            x_train,x_test,y_train,y_test = train_test_split(x,y)
                            dat.loc[current] = np.nan
                            dat.ix[current,0] = ['PCE','Jsc','Voc','','JscVoc'][outp_index]
                            dat.ix[current,1] = n_comp
                            dat.ix[current,2] = eeva_sigma
                            dat.ix[current,3] = eeva_L
                            dat.ix[current,4] = eva_sigma
                            dat.ix[current,5] = eva_L
                            dat.ix[current,6] = i+1
                            model.fit(x_train,y_train.iloc[:,outp_index])
                            dat.ix[current,7] = model.score(x_train,y_train.iloc[:,outp_index])
                            dat.ix[current,8] = model.score(x_test,y_test.iloc[:,outp_index])
                            current += 1
        dat.to_csv('final2.csv')