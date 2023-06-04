from file_convert import g09
import os

input_dir = 'C:/Users/phuc/Desktop/New folder (2)/good'
output_dir = 'C:/Users/phuc/Desktop/New folder (2)/uv'
for file_name in os.listdir(input_dir):
    x = g09.G09Info()
    x.readg09out(input_dir+'/'+file_name)
    x.processor = 16
    x.chk = '/scratch/chemusvn/' +  file_name[:-4]+'_super.chk'
    x.mem = '5Gb'
    x.run_type = 'td=(nstates=15)'
    x.modified = ''
    x.writeg09inp(output_dir+'/'+file_name[:-4]+'.gjf')
    