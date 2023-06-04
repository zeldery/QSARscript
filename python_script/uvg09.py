input_dir = 'C:/Users/phuc/Desktop/abc'
temp_dir = 'C:/Users/phuc/Desktop/def'
output_dir = 'C:/Users/phuc/Desktop/xyz'

for file in os.listdir(input_dir):
    x = mopac.MopInfo()
    x.readmopout(input_dir + '/'+file)
    f = open(temp_dir+'/'+file[:-3]+'gjf','w')
    f.write('# td=(nstates=15) PM6\n')
    f.write('\n'+file[:-4]+'\n\n0 1\n')
    for i in range(len(x.atom)):
        f.write('{:2s} {:14.8f} {:14.8f} {:14.8f}\n'.format(x.atom[i],x.x[i],x.y[i],x.z[i]))
    f.write('\n')
    f.close()

os.chdir(temp_dir)
for file in os.listdir(temp_dir):
    os.system('g09 '+file)
    os.system('move ' + temp_dir.replace('/','\\')+'\\'+file[:-4]+'.out '+output_dir.replace('/','\\'))