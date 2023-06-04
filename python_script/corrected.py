BTD_list = 'C:/Users/phuc/Desktop/New folder (2)/outputDye'
TPA_list = 'C:/Users/phuc/Desktop/New folder (2)/temp'
BTD_inp = 'C:/data/research/QSAR/data/BTD_opt_inp'
TPA_inp = 'C:/data/research/QSAR/data/TPA_opt_inp'
destination = 'C:/Users/phuc/Desktop/New folder (2)/rerun'

import os
import shutle
from file_convert import g09

for file in os.listdir(BTD_list):
    file_name = file[:-4]+'.gjf'
    x = g09.G09Info()
    x.readg09inp(BTD_inp+'/'+file_name)
    x.processor = 16
    x.chk = '/scratch/chemusvn/' +  file_name[:-4]+'_super.chk'
    x.mem = '5Gb'
    x.run_type = 'opt(max_cycles=500)'
    x.method = 'RB3LYP'
    x.basis_set = '6-31+G(d)'
    x.modified = ''
    x.writeg09inp(destination+'/'+file_name)

for file in os.listdir(TPA_list):
    file_name = file[:-4]+'.gjf'
    x = g09.G09Info()
    x.readg09inp(TPA_inp+'/'+file_name.lower())
    x.processor = 16
    x.chk = '/scratch/chemusvn/' +  file_name[:-4]+'_super.chk'
    x.mem = '5Gb'
    x.run_type = 'opt(max_cycles=500)'
    x.method = 'RB3LYP'
    x.basis_set = '6-31+G(d)'
    x.modified = ''
    x.writeg09inp(destination+'/'+file_name)