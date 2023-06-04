import os
import shutil
import numpy as np
import pandas as pd
from sklearn.svm import SVR

max_file = 10

source = 'source'
result = 'result2'

outp_list = ['PCE','JscVoc']

def run(outp_ind,times):
    line = 'reg_final_'+str(outp_ind)+'{:0>2d}'.format(times)
    os.mkdir(line)
    shutil.copy2(source+'/D1O1Tr.csv',line)
    shutil.copy2(source+'/D1O1Ts.csv',line)
    shutil.copy2(source+'/O1D1Tr.csv',line)
    shutil.copy2(source+'/O1D1Ts.csv',line)
    shutil.copy2(source+'/ga.py',line)
    shutil.copy2(source+'/script8b.py',line)
    os.chdir(line)
    f = open('param.dat','w')
    f.write(line+'\n'+str(outp_ind)+'\n'+str(times)+'\n')
    f.close()
    f = open('script','w')
    f.write('ipython script8b.py')
    f.close()
    os.system('submit ASB general -exec script')
    os.chdir('..')

if __name__ == '__main__':
    f = open('total.dat','r')
    i = int(f.readline()[:-1])
    f.close()
    num = len(os.listdir(result))
    while i - num < max_file:
        times = i % 100
        j = i // 100
        if j > len(outp_list):
            print('The job has completed')
            break
        run(j,times)
        i += 1
    f = open('total.dat','w')
    f.write(str(i) + '\n')
    f.close()