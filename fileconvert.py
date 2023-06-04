'''
Chemical File Convert
Convert output and input file of Gaussian 09 and MOPAC program
First written by: Thien-Phuc Tu-Nguyen
Tested on Anaconda3 version 4.4 with respective packages
Last modified: July 2017 by Thien-Phuc Tu-Nguyen
'''


class G09Info:
    
    def __init__(self):
        # Run attributes:
        self.processor = 0
        self.chk = ''
        self.mem = ''
        self.run_type = ''
        self.method = ''
        self.basis_set = ''
        self.modified = ''
        self.title = ''
        self.add_info = ''
        # Energy search
        self.energy_search_str = ''
        # Molecule information
        self.charge = 0
        self.spin = 1
        self.atom = []
        self.x = []
        self.y = []
        self.z = []
        # Properties information
        self.energy = 0
        self.occupied = []
        self.unoccupied = []
        self.dipole = 0
        self.wave = []
        self.os = []
        self.freq = []
        self.inten = []
        self.xxx = 0
        self.yyy = 0
        self.zzz = 0
        self.xyy = 0
        self.xxy = 0
        self.xxz = 0
        self.xzz = 0
        self.yzz = 0
        self.yyz = 0
        self.xyz = 0
        self.octapole = 0
        self.zero_correction = 0
        self.energy_correction = 0
        self.enthalpy_correction = 0
        self.gibbs_correction = 0
        self.zero_sum = 0
        self.energy_sum = 0
        self.enthalpy_sum = 0
        self.gibbs_sum = 0
        
    def readg09inp(self,file_name):
        f = open(file_name,'r')
        line = f.readline()
        while line != '\n' and line != ' \n':
            line = line[:-1]
            if line.lower().find('%nproc') != -1:
                self.processor = int(line.split('=')[1])
            if line.lower().find('%mem') != -1:
                self.mem = line.split('=')[1]
            if line.lower().find('%chk') != -1:
                self.chk = line.split('=')[1]
            if line.find('#') != -1:
                self.modified = line.split('#')[1]
            line = f.readline()
        line = f.readline()
        self.title = line[:-1]
        line = f.readline()
        line = f.readline()
        line = line[:-1]
        self.charge = int(line.split()[0])
        self.spin = int(line.split()[1])
        self.x = []
        self.y = []
        self.z = []
        self.atom = []
        line = f.readline()
        while line != '' and line != '\n' and line != ' \n':
            line = line[:-1]
            temp = line.split()
            self.atom += [temp[0]]
            if len(temp) == 4:
                self.x += [float(temp[1])]
                self.y += [float(temp[2])]
                self.z += [float(temp[3])]
            if len(temp) == 5:
                self.x += [float(temp[2])]
                self.y += [float(temp[3])]
                self.z += [float(temp[4])]
            line = f.readline()
        self.add_info = ''
        line = f.readline()
        while line != '':
            self.add_info += line
            line = f.readline()
        f.close()
    
    def readg09out(self,file_name):
        f = open(file_name,'r')
        finish_tag = False
        temp = None
        while not finish_tag:
            temp = f.readline()
            if temp == '':
                finish_tag = True
            if temp.find('Dipole moment (field-independent basis, Debye)') != -1:
                temp = f.readline()
                self.dipole = float(temp[84:-1])
                temp = f.readline()
            if temp.find(' Alpha  occ. eigenvalues --') != -1:
                self.occupied = []
                self.unoccupied = []
                values = temp[27:-1]
                temp = f.readline()
                while temp.find(' Alpha  occ. eigenvalues --') != -1:
                    values += temp[27:-1]
                    temp = f.readline()
                for number in values.split():
                    if len(number) == 20:
                        self.occupied += [float(number[:10])]
                        self.occupied += [float(number[10:])]
                    elif len(number) == 30:
                        self.occupied += [float(number[:10])]
                        self.occupied += [float(number[10:20])]
                        self.occupied += [float(number[20:])]
                    else:
                        self.occupied += [float(number)]
                values = temp[27:-1]
                while temp.find(' Alpha virt. eigenvalues --') != -1:
                    values += temp[27:-1]
                    temp = f.readline()
                for number in values.split():
                    self.unoccupied += [float(number)]
            if temp.find(' Excited State') != -1:
                self.wave += [float(temp.split()[6])]
                self.os += [float(temp.split()[8][2:])]
                temp = f.readline()
            if temp.find('SCF Done:  E('+self.energy_search_str+')') != -1:
                value = temp[(temp.find('=')+1):-1]
                self.energy = float(value.split()[0])
                temp = f.readline()
            if temp.find(' Frequencies --') != -1:
                temp = temp.split()[2:]
                for num in temp:
                    self.freq += [float(num)]
                temp = f.readline()
                temp = f.readline()
                temp = f.readline()
                temp = temp.split()[3:]
                for num in temp:
                    self.inten += [float(num)]
                temp = f.readline()
            if temp.find('Octapole moment (field-independent basis, Debye-Ang**2):') != -1:
                temp = f.readline()
                self.xxx = float(temp[6:28])
                self.yyy = float(temp[34:52])
                self.zzz = float(temp[58:78])
                self.xyy = float(temp[84:-1])
                temp = f.readline()
                self.xxy = float(temp[6:28])
                self.xxz = float(temp[34:52])
                self.xzz = float(temp[58:78])
                self.yzz = float(temp[84:-1])
                temp = f.readline()
                self.yyz = float(temp[6:28])
                self.xyz = float(temp[34:52])
                self.octapole = (self.xxx + self.xyy + self.xzz) **2
                self.octapole += (self.xyy + self.yzz + self.xxy) **2
                self.octapole += (self.zzz + self.xxz + self.yyz) **2
                self.octapole = self.octapole ** 0.5
            if temp.find('Zero-point correction=') != -1:
                self.zero_correction = float(temp[42:58])
                temp = f.readline()
                self.energy_correction = float(temp[42:58])
                temp = f.readline()
                self.enthalpy_correction = float(temp[42:58])
                temp = f.readline()
                self.gibbs_correction = float(temp[42:58])
                temp = f.readline()    
                self.zero_sum = float(temp[46:])
                temp = f.readline() 
                self.energy_sum = float(temp[46:])
                temp = f.readline() 
                self.enthalpy_sum = float(temp[46:])
                temp = f.readline() 
                self.gibbs_sum = float(temp[46:])
                temp = f.readline()                 
            if temp.find(' 1\\1\\') != -1 or temp.find(' 1|1|') != -1:
                sep = temp[2]
                next_line = f.readline()
                while next_line.find('@') == -1:
                    temp = temp[:-1] + next_line[1:]
                    next_line = f.readline()
                temp = temp[:-1] + next_line[1:-1]
                temp = temp[5:-1]
                info = temp.split(sep*2)
                # Basic infomation of the run
                temp = info[0].split(sep)
                self.run_type = temp[1]
                self.method = temp[2]
                self.basis_set = temp[3]
                # The title
                self.title = info[2]
                # The coordination
                sub_info = info[3].split(sep)
                self.charge = int(sub_info[0].split(',')[0])
                self.spin = int(sub_info[0].split(',')[1])
                del sub_info[0]
                self.atom = []
                self.x = []
                self.y = []
                self.z = []
                for atom in sub_info:
                    temp = atom.split(',')
                    self.atom += [temp[0]]
                    if len(temp) == 4:
                        self.x += [float(temp[1])]
                        self.y += [float(temp[2])]
                        self.z += [float(temp[3])]
                    if len(temp) == 5:
                        self.x += [float(temp[2])]
                        self.y += [float(temp[3])]
                        self.z += [float(temp[4])]
        f.close()
    
    def writeg09inp(self,file_name):
        f = open(file_name,'w')
        if self.processor != 0:
            f.write('%nprocshared='+str(self.processor)+'\n')
        if self.chk != '':
            f.write('%chk='+self.chk+'\n')
        if self.mem != '':
            f.write('%mem='+self.mem+'\n')
        f.write('#{} {}/{} {}\n'.format(self.run_type,self.method,self.basis_set,self.modified))
        f.write('\n')
        f.write(self.title+'\n')
        f.write('\n')
        f.write(str(self.charge)+' '+str(self.spin)+'\n')
        for i in range(len(self.atom)):
            f.write('{:2s} {:14.8f} {:14.8f} {:14.8f}\n'.format(self.atom[i],self.x[i],self.y[i],self.z[i]))
        f.write('\n')
        f.write(self.add_info)
        f.close()
    
class MopInfo:
    def __init__(self):
        # Run information
        self.method = 'PM7'
        self.single = False
        self.freq_calc = False
        self.pdbout = False
        self.title = ''
        # Geometry
        self.atom = []
        self.x = []
        self.y = []
        self.z = []
        # Result
        self.energy = 0.0
        self.heat_formation = 0.0
        self.ionization = 0.0
        self.occupied = []
        self.unoccupied = []
        self.area = 0.0
        self.volume = 0.0
        self.dipole = 0.0
        self.freq = []
        
    def writemopinp(self,file_name):
        f = open(file_name,'w')
        f.write(self.method)
        if self.single:
            f.write(' 1SCF')
        if self.freq_calc:
            f.write(' FORCE FREQCY')
        if self.pdbout:
            f.write(' PDBOUT')
        f.write('\n' + self.title + '\n\n')
        for i in range(len(self.atom)):
            f.write('{:>3} {:12.8f} {:12.8f} {:12.8f}\n'.format(self.atom[i],self.x[i],self.y[i],self.z[i]))
        f.close()
    
    def readmopout(self,file_name):
        filled_level = 0
        f = open(file_name,'r')
        temp = f.readline()
        self.freq = []
        while temp != '':
            if temp.find('TOTAL ENERGY') != -1:
                self.energy = float(temp.split()[3])
            if temp.find('COSMO AREA') != -1:
                self.area = float(temp.split()[3])
            if temp.find('COSMO VOLUME') != -1:
                self.volume = float(temp.split()[3])
            if temp.find('FINAL HEAT OF FORMATION') != -1:
                self.heat_formation = float(temp.split()[8])
            if temp.find('IONIZATION POTENTIAL') != -1:
                self.ionization = float(temp.split()[3])
            if temp.find('NO. OF FILLED LEVELS') != -1:
                filled_level = int(temp.split()[-1])
            if temp.find('CARTESIAN COORDINATES')!= -1 and filled_level != 0:
                temp = f.readline()
                temp = f.readline()
                self.atom = []
                self.x = []
                self.y = []
                self.z = []
                while temp != '\n':
                    temp = temp.split()
                    self.atom += [temp[1]]
                    self.x += [float(temp[2])]
                    self.y += [float(temp[3])]
                    self.z += [float(temp[4])]
                    temp = f.readline()
            if temp.find('DIPOLE') != -1 and temp.find('CHARGES') == -1:
                temp = f.readline()
                temp = f.readline()
                temp = f.readline()
                self.dipole = float(temp.split()[4])
            if temp.find('VIBRATION')!= -1 and temp.find('ENERGY CONTRIBUTION') != -1:
                temp = f.readline()
                self.freq += [float(temp.split()[1])]
                temp = f.readline()
            if temp.find('EIGENVALUES') != -1:
                temp = f.readline()
                raw = ''
                while temp != '\n':
                    raw += temp[:-1]
                    temp = f.readline()
                self.occupied = []
                self.unoccupied = []
                values = []
                for x in raw.split():
                    values += [float(x)]
                self.occupied = values[:filled_level]
                self.unoccupied = values[filled_level:]
            temp = f.readline()
        f.close()
    
    def g09convert(self,original):
        self.atom = original.atom
        self.x = original.x
        self.y = original.y
        self.z = original.z
        self.title = original.title
        