import numpy as np
import pandas as pd
import os

class EVA:
    def __init__(self,sigma,L):
        self.sigma = sigma
        self.L = L
        self.const = 0.3989422804014327 # 1/sqrt(2pi)
        self.x = np.arange(L,4000+0.001,L)
        self.name = []
        self.dat = np.zeros((0,len(self.x)))
    def add(self,name,freq):
        self.name += [name]
        self.dat = np.concatenate((self.dat,np.zeros((1,len(self.x)))),axis = 0)
        for i in range(len(freq)):
            self.dat[-1,:] += self.const * np.exp( - (self.x - freq[i]) **2/(2*self.sigma**2))
    def to_df(self):
        return pd.DataFrame(self.dat,columns = self.x,index = self.name)
        
class EEVA:
    def __init__(self,sigma,L):
        self.sigma = sigma
        self.L = L
        self.const = 0.3989422804014327 # 1/sqrt(2pi)
        self.x = np.arange(-45,10+0.00001,L)
        self.name = []
        self.dat = np.zeros((0,len(self.x)))
    def add(self,name,energy):
        self.name += [name]
        self.dat = np.concatenate((self.dat,np.zeros((1,len(self.x)))),axis = 0)
        for i in range(len(energy)):
            self.dat[-1,:] += self.const * np.exp( - (self.x - energy[i]) **2/(2*self.sigma**2))
    def to_df(self):
        return pd.DataFrame(self.dat,columns = self.x,index = self.name)