# Regression

import os
import shutil

source = 'source'
run_folder = 'temp'
result_folder = 'result'

max_run = 10

#gamma_list = np.concatenate((np.arange(0.005,0.05,0.005),np.arange(0.05,0.2,0.025),np.arange(0.2,1.0,0.05)))
#C_list = np.concatenate((np.arange(0.05,0.5,0.05),np.arange(0.5,2.0,0.25),np.arange(2.0,10.0,0.5)))
#eps_list = np.concatenate((np.arange(0.005,0.02,0.005),np.arange(0.02,0.1,0.02),np.arange(0.1,0.5,0.05)))


gamma_list = [0.01,0.1,0.5]
C_list = [0.1,1,5]
outp_list = ['PCE','JscVoc']
cls_list = ['O6','O7','O8','O9']

gamma_start = [0.005,0.05,0.2]
gamma_end = [0.05,0.2,1.0]
gamma_step = [0.005,0.025,0.05]

C_start = [0.05,0.5,2.0]
C_end = [0.5,2.0,10.0]
C_step = [0.05,0.25,0.5]

def run(gamma_ind,C_ind,outp_ind,cls_ind,times):
    line = 'GAD1'+cls_list[cls_ind]+'-'+str(outp_ind)+str(gamma_ind)+str(C_ind) + str(times)
    os.mkdir(line)
    shutil.copy2(source + '/' + 'D1'+cls_list[cls_ind]+'Tr.csv',line)
    shutil.copy2(source + '/' + 'D1'+cls_list[cls_ind]+'Ts.csv',line)
    shutil.copy2(source + '/'+cls_list[cls_ind]+'D1Tr.csv',line)
    shutil.copy2(source + '/'+cls_list[cls_ind]+'D1Ts.csv',line)
    shutil.copy2(source + '/' + 'ga.py',line)
    shutil.copy2(source + '/' + 'script5.py',line)
    os.chdir(line)
    os.rename('D1'+cls_list[cls_ind]+'Tr.csv','inputTr.csv')
    os.rename('D1'+cls_list[cls_ind]+'Ts.csv','inputTs.csv')
    os.rename(cls_list[cls_ind]+'D1Tr.csv','outputTr.csv')
    os.rename(cls_list[cls_ind]+'D1Ts.csv','outputTs.csv')
    gamma = gamma_list[gamma_ind]
    C = C_list[C_ind]
    outp = outp_list[outp_ind]
    f = open('param.dat','w')
    f.write(line+'\n')
    f.write(str(gamma)+'\n')
    f.write(str(C)+'\n')
    f.write(outp+'\n')
    f.close()
    f = open('script','w')
    f.write('python script5.py')
    f.close()
    os.system('submit ASB general -exec script')
    os.chdir('..')
    
if __name__ == '__main__':
    n = len(os.listdir(result_folder))
    f = open('total.dat','r')
    total = int(f.readline()[:-1])
    f.close()
    while total - n < max_run:
        i = total
        m = i % 10
        i = i // 10
        l = i%len(C_list)
        i = i // len(C_list)
        k = i%len(gamma_list)
        i = i // len(gamma_list)
        j = i % len(outp_list)
        i = i // len(outp_list)
        if i >= len(cls_list):
            print('The run has complete')
            break
        run(k,l,j,i,m)
        total += 1
    f = open('total.dat','w')
    f.write(str(total)+'\n')
    f.close()
    