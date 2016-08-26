#!/usr/bin/env python

import shutil
import sys

#pdbline = 'ATOM     13 1HD2 ASN B 106      -8.312  14.565  12.150  1.00 13.00 \n'
#lineout = pdbline.split()
filename = sys.argv[1]
kat=0
nanr=[]
for line in open(filename):
	tmpln = line.split()
	if tmpln[0] == 'ATOM':
		kat+=1
		temp=[]
		temp.append(tmpln[2])		
		if len(tmpln[3])==3 or len(tmpln[3])==2:
			temp.append(int(tmpln[5]))		
			temp.append(float(tmpln[6]))		
			temp.append(float(tmpln[7]))		
			temp.append(float(tmpln[8]))
		elif len(tmpln[3])==5:		
			temp.append(int(tmpln[4]))		
			temp.append(float(tmpln[5]))		
			temp.append(float(tmpln[6]))		
			temp.append(float(tmpln[7]))
		nanr.append(temp)
file1 = open('inputpre','r')
filepre = file1.readline().strip()
xm=[]
ym=[]
zm=[]
for line in file1:
#VANNO LETTI
	stringa = line.split()
	xm.append(float(stringa[0]))
	ym.append(float(stringa[1]))
	zm.append(float(stringa[2]))
#VANNO LETTIi
file1.close()
#print len(xm)
nat=0
fileout = open('fort.68','w')
for line in open(filepre):
	rr = int(line.split()[0])
	ra = line.split()[2]
	met = int(line.split()[4])-1
	for r in nanr:
#		print r
		if  r[1] == rr and r[0] == ra:
	   		 
			d2=0
#	    		print a.coord[0], a.coord[1], a.coord[2]
                        d2 += (xm[met]-r[2])**2
                        d2 += (ym[met]-r[3])**2
                        d2 += (zm[met]-r[4])**2
			d = d2**(0.5)
			dm6 = d**(-6)
			fileout.write(str(dm6))
			fileout.write('  ')
			fileout.write(line.split()[6])
			fileout.write('\n')
fileout.close()
