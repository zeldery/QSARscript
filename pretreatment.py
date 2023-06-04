'''
Pretreatment file
Process the data before regression or classification
First written by: Thien-Phuc Tu-Nguyen
Tested on Anaconda3 version 4.4 with respective packages
Last modified: June 2017 by Thien-Phuc Tu-Nguyen
'''

from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

class PreTreatment:
    def __init__(self):
        self.raw_input = None
        self.raw_output = None
        self.input = None
        self.output = None
        self.input_std = None
        self.output_std = None
        self.input_scaler = StandardScaler()
        self.output_scaler = StandardScaler()
    
    def set(self,inp,outp,good=False):
        self.raw_input = inp.copy()
        self.raw_output = outp.copy()
        if good:
            self.input = inp.copy()
            self.output = outp.copy()
        else:
            temp = pd.merge(inp,outp,left_index=True,right_index=True)
            self.input = temp.iloc[:,:inp.shape[1]]
            self.output = temp.iloc[:,inp.shape[1]:]
    
    def check(self,unity=True,corr=True,unity_criterion = 0.9,corr_criterion=0.9):
        if unity:
            be_ok = []
            for (name,serie) in self.input.iteritems():
                if serie.value_counts().max() / len(serie) < unity_criterion:
                    be_ok += [name]
            self.input = self.input[be_ok]
            be_ok = []
            for (name,serie) in self.output.iteritems():
                if serie.value_counts().max() / len(serie) < unity_criterion:
                    be_ok += [name]
            self.output = self.output[be_ok]
        if corr:
            n = self.input.shape[1]
            eliminated = []
            for i in range(n-1):
                for j in range(i+1,n):
                    if np.corrcoef(self.input.iloc[:,i],self.input.iloc[:,j])[0,1] >= corr_criterion:
                        eliminated += [j]
            self.input = self.input.drop(self.input.columns[eliminated],axis=1)
        self.input_std = self.input_scaler.fit_transform(self.input)
        self.input_std = pd.DataFrame(self.input_std,columns=self.input.columns,index = self.input.index)
        self.output_std = self.output_scaler.fit_transform(self.output)
        self.output_std = pd.DataFrame(self.output_std,columns=self.output.columns,index = self.output.index)
    
    def transform(self,inp,outp):
        return (self.input_scaler.transform(inp),self.output_scaler.transform(outp))
    
    def inverse_transform(self,inp,outp):
        return (self.input_scaler.inverse_transform(inp),self.output_scaler.inverse_transform(outp))
    
    def write(self,input_name,output_name):
        dat_inp = pd.DataFrame(np.nan,index = ['mean','scale'],columns = self.input_std.columns)
        dat_outp = pd.DataFrame(np.nan,index = ['mean','scale'],columns = self.output_std.columns)
        dat_inp.iloc[0,:] = self.input_scaler.mean_
        dat_inp.iloc[1,:] = self.input_scaler.scale_
        dat_outp.iloc[0,:] = self.output_scaler.mean_
        dat_outp.iloc[1,:] = self.output_scaler.scale_
        dat_inp.to_csv(input_name)
        dat_outp.to_csv(output_name)
    
    def read(self,input_name,output_name):
        dat_inp = pd.read_csv(input_name,index_col = 0)
        dat_outp = pd.read_csv(output_name,index_col = 0)
        self.input_scaler.mean_ = dat_inp.iloc[0,:]
        self.input_scaler.scale_ = dat_inp.iloc[1,:]
        self.output_scaler.mean_ = dat_outp.iloc[0,:]
        self.output_scaler.scale_ = dat_outp.iloc[1,:]
        