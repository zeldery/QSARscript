input_dir = 'C:/Users/phuc/Desktop/abc'
output_dir = 'C:/Users/phuc/Desktop/def'
ref_dir = 'C:/data/research/QSAR/data/mol_mopac_ok'

for file in os.listdir(input_dir):
    try:
        g = open(ref_dir + '/' + file,'r')
        f = open(input_dir + '/' + file,'r')
        h = open(output_dir + '/' +file,'w')
        temp = ''
        for i in range(4):
            temp = f.readline()
            h.write(temp)
        n = int(temp[:3])
        for i in range(n):
            temp = f.readline()
            h.write(temp)
        for i in range(n+4):
            temp = g.readline()
        temp = g.readline()
        while temp != '':
            h.write(temp)
            temp = g.readline()
        g.close()
        f.close()
        h.close()
    except OSError:
        print(file[:-4])
