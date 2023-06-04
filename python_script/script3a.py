import os
import shutil

max_file = 150
source = 'source_combine'
total = 'combine_result'

def run(outp_ind,eps_ind,C_ind,gamma_ind,times):
    line = 'combine-'+str(outp_ind)+str(eps_ind)+str(C_ind)+str(gamma_ind)+str(times)
    os.mkdir(line)
    shutil.copy2(source+'/script3b.py',line)
    os.chdir(line)
    f = open('param.dat','w')
    f.write(line+'\n')
    f.write(str(outp_ind)+'\n')
    f.write(str(eps_ind)+'\n')
    f.write(str(C_ind)+'\n')
    f.write(str(gamma_ind)+'\n')
    f.write(str(times)+'\n')
    f.close()
    f = open('script','w')
    f.write('ipython script3b.py')
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
        l = i % 3
        i = i // 3
        k = i % 3
        i = i // 3
        j = i % 3
        i = i // 3
        if i >= 2:
            print('The job is done')
            break;
        run(i,j,k,l,m)
        n = n + 1
    f = open('total_combine.dat','w')
    f.write(str(n)+'\n')
    f.close()