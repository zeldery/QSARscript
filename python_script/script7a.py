import os
import shutil

max_file = 150

source = 'source'
result = 'result2'

cls_list = ['O6','O7','O8','O9']
outp_list = ['PCE','JscVoc']

def run(outp_ind,cls_ind,times):
    line = 'class_final_'+str(cls_ind)+str(outp_ind)+'{:0>2d}'.format(times)
    os.mkdir(line)
    shutil.copy2(source+'/'+'D1'+cls_list[cls_ind]+'Tr.csv',line)
    shutil.copy2(source+'/'+'D1'+cls_list[cls_ind]+'Ts.csv',line)
    shutil.copy2(source+'/'+cls_list[cls_ind]+'D1'+'Tr.csv',line)
    shutil.copy2(source+'/'+cls_list[cls_ind]+'D1'+'Ts.csv',line)
    shutil.copy2(source+'/'+'ga.py',line)
    shutil.copy2(source+'/'+'script7b.py',line)
    os.chdir(line)
    os.rename('D1'+cls_list[cls_ind]+'Tr.csv','inputTr.csv')
    os.rename('D1'+cls_list[cls_ind]+'Ts.csv','inputTs.csv')
    os.rename(cls_list[cls_ind]+'D1'+'Tr.csv','outputTr.csv')
    os.rename(cls_list[cls_ind]+'D1'+'Ts.csv','outputTs.csv')
    f = open('param.dat','w')
    f.write(line+'\n')
    f.write(str(cls_ind)+'\n')
    f.write(str(outp_ind)+'\n')
    f.write(str(times)+'\n')
    f.close()
    f = open('script','w')
    f.write('ipython script7b.py')
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
        outp_ind = j % len(outp_list)
        cls_ind = j // len(outp_list)
        if cls_ind >= len(cls_list):
            print('The job has completed')
            break
        run(outp_ind,cls_ind,times)
        i += 1
    f = open('total.dat','w')
    f.write(str(i) + '\n')
    f.close()
