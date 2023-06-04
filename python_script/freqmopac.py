mopac_execute = 'C:/Program Files/MOPAC/MOPAC2016.exe'
mopac_log_dir = 'C:/Users/phuc/Desktop/abc'
mopac_in_dir = 'C:/Users/phuc/Desktop/def'
mopac_out_dir = 'C:/Users/phuc/Desktop/xyz'

for file_name in os.listdir(mopac_log_dir):
    x = mopac.MopInfo()
    x.readmopout(mopac_log_dir+'/'+file_name)
    x.freq_calc = True
    x.writemopinp(mopac_in_dir + '/' +file_name[:-3] + 'mop')

for file_name in os.listdir(mopac_in_dir):
    root = file_name[:-4]
    os.system('"'+mopac_execute+'" '+mopac_in_dir+'/'+file_name)
    os.system('move ' + mopac_in_dir.replace('/','\\')+'\\'+root+'.out '+ mopac_out_dir.replace('/','\\'))