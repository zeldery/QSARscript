import os
import shutil

max_file = 150
source = 'source_combine'
total = 'combine_result'

outp_list = ['PCE','JscVoc']
cls_list = ['O6','O7','O8','O9']

def run(gamma_ind,C_ind,outp_ind,cls_ind,times):
    line = 'combine-'+cls_list[cls_ind]+'-'+str(outp_ind)+str(gamma_ind)+str(C_ind) + str(times)
    os.mkdir(line)
    shutil.copy2(source+'/script6b.py',line)
    os.chdir(line)
    f = open('param.dat','w')
    f.write(line+'\n')
    f.write(str(cls_ind)+'\n')
    f.write(str(outp_ind)+'\n')
    f.write(str(C_ind)+'\n')
    f.write(str(gamma_ind)+'\n')
    f.write(str(times)+'\n')
    f.close()
    f = open('script','w')
    f.write('ipython script6b.py')
    f.close()
    os.system('submit ASB general -exec script')
    os.chdir('..')

if __name__ == '__main__':
    f = open('total_combine.dat','r')
    n = int(f.readline()[:-1])
    f.close()
    n_file = len(os.listdir(total))
    while n-n_file < max_file:
        i = n
        m = i%10
        i = i // 10
        l = i % 4
        i = i // 4
        k = i % 2
        i = i // 2
        j = i % 3
        i = i // 3
        if i >= 3:
            print('The job is done')
            break;
        run(i,j,k,l,m)
        n = n + 1
    f = open('total_combine.dat','w')
    f.write(str(n)+'\n')
    f.close()