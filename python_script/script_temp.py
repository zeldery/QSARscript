# Create the scripting file
list_file = ['O6','O7','O8','O9']
source = 'source'

import os
import shutil
for file in list_file:
    os.mkdir(file)
    for file2 in os.listdir(source):
        shutil.copy2(source+'/'+file2,file)
    shutil.copy2('D1O3Tr.csv',file)
    shutil.copy2('D1O3Ts.csv',file)
    shutil.copy2(file+'D1Tr.csv',file)
    shutil.copy2(file+'D1Ts.csv',file)
    os.chdir(file)
    f = open('script_all','w')
    f.write('submit ASB general -exec script0\n')
    f.write('submit ASB general -exec script1\n')
    f.write('submit ASB general -exec script2\n')
    f.write('submit ASB general -exec script3\n')
    f.write('submit ASB general -exec script4\n')
    f.write('submit ASB general -exec script5\n')
    f.write('submit ASB general -exec script6\n')
    f.write('submit ASB general -exec script7\n')
    f.write('submit ASB general -exec script8\n')
    f.close()
    os.rename(file+'D1Tr.csv','O3D1Tr.csv')
    os.rename(file+'D1Ts.csv','O3D1Ts.csv')
    os.chdir('..')