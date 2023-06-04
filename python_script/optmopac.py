mopac_execute = 'C:/Program Files/MOPAC/MOPAC2016.exe'
mopac_in_dir = 'C:/Users/phuc/Desktop/def'
mopac_out_dir = 'C:/Users/phuc/Desktop/ghi'
g09_in_dir = 'C:/Users/phuc/Desktop/abc'

import os
from file_convert import g09,mopac

for file_name in os.listdir(g09_in_dir):
    x = g09.G09Info()
    if file_name[-3:] == 'gjf':
        x.readg09inp(g09_in_dir + '/' + file_name)
    if file_name[-3:] == 'log':
        x.readg09out(g09_in_dir + '/' + file_name)
    y = mopac.MopInfo()
    y.g09convert(x)
    y.method = 'PM7'
    y.pdbout = True
    y.writemopinp(mopac_in_dir + '/' +file_name[:-3] + 'mop')

for file_name in os.listdir(mopac_in_dir):
    root = file_name[:-4]
    os.system('"'+mopac_execute+'" '+mopac_in_dir+'/'+file_name)
    os.system('move ' + mopac_in_dir.replace('/','\\')+'\\'+root+'.out '+ mopac_out_dir.replace('/','\\'))
    os.system('move ' + mopac_in_dir.replace('/','\\')+'\\'+root+'.pdb '+ mopac_out_dir.replace('/','\\'))
    os.remove(mopac_in_dir+'/'+root+'.arc')
    