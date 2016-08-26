#!/usr/bin/env python
'''
This program attempts to convert XPLOR pseudo restraints into AMBER restraints.


XPLOR:
assign ( resid 2   and name HA   )( resid 2   and name HB#  ) 2.4 0.6 0.6
assign ( resid 2   and name HB#  )( resid 3   and name HD1  ) 3.4 1.6 1.6
assign ( resid 2   and name HB#  )( resid 3   and name HD2  ) 3.4 1.6 1.6
assign ( resid 3   and name HD#  )( resid 3   and name HG#  ) 2.4 0.6 0.6

AMBER:
#
#  1 GUA H3'  1 GUA Q5'        5.50
 &rst iat=  27, -1, r3= 4.394, r4= 4.894,
 igr1= 0, 0, 0, 0, igr2= 4, 5, 0, 0,
 r1= 1.300, r2= 1.800, r3= 4.394, r4= 4.894,
 rk2= 0.00, rk3= 32.000, &end
'''

import sys
import os
from optparse import OptionParser

def convert(xfile, pdb):
    
    try:
        lpdb=open(pdb, 'r').readlines()
    except IOError, (errno, strerror):
        sys.exit('%s: IOError(%s): %s %s\n' % (sys.argv[0], errno, pdb, strerror))
    
    out = []
    numMap = {}
    resMap = {}
    
    for l in lpdb:
        if l.strip().startswith('ATOM'):
            ls=l.split()
            k='%s:%s' % (ls[4],ls[2])
            numMap[k]=ls[1]
            resMap[ls[4]]=ls[3]
            
    try:
        xp=open(xfile,'r').readlines()
    except IOError, (errno, strerror):
        sys.exit('%s: IOError(%s): %s %s\n' % (sys.argv[0], errno, xfile, strerror))
    xx=0
    for l in xp:
        xx+=1
        if l.strip().startswith('assign'):
            ls = l.split()
            
            res1 = ls[3]
            res2 = ls[10]
            atm1 = ls[6]
            atm2 = ls[13]
            up = float(ls[15])+float(ls[17])
            dn = float(ls[15])-float(ls[16])       
            
            igr1=igr2=0
            val1=val2=0
            ile1=ile2=0
            ild1=ild2=0
            leu1=leu2=0
            gln1=gln2=0
            thr1=thr2=0
            arg1=arg2=0
            h5p1=h5p2=0
            
            if ls[6].endswith('#'):
                name1 = ls[6][:-1].strip()
                atm1=name1
                if len(name1)==3:
                    name1=ls[6][:-1]
                if len(name1)==4:
                    name1=ls[6][:-2]
                
                residue1 = resMap[res1]
                
                igr1 = 1
                if residue1 == "VAL" and name1 == "HG":
                    val1 = 1
                elif residue1 == "ILE" and name1 == "HG":
                    ile1 = 1
                elif residue1 == "ILE" and name1 == "HD":
                    ild1 = 1
                elif residue1 == "LEU" and name1 == "HD":
                    leu1 = 1
                elif residue1 == "GLN" and name1 == "HE":
                    gln1 = 1
                elif residue1 == "THR" and name1 == "HG":
                    thr1 = 1
                elif residue1 == "ARG" and name1 == "HH":
                    arg1 = 1
                elif name1 == "H5'":
                    h5p1 = 1
                    
            if ls[13].endswith('#'):
                name2 = ls[13][:-1].strip()
                atm2=name2
                
                if len(name2)==3:
                    name2=ls[13][:-1]
                if len(name2)==4:
                    name2=ls[13][:-2]
            
                residue2 = resMap[res2]
                
                igr2 = 1
                if residue2 == "VAL" and name2 == "HG":
                    val2 = 1
                elif residue2 == "ILE" and name2 == "HG":
                    ile2 = 1
                elif residue2 == "ILE" and name2 == "HD":
                    ild2 = 1
                elif residue2 == "LEU" and name2 == "HD":
                    leu2 = 1
                elif residue2 == "GLN" and name2 == "HE":
                    gln2 = 1
                elif residue2 == "THR" and name2 == "HG":
                    thr2 = 1
                elif residue2 == "ARG" and name2 == "HH":
                    arg2 = 1
                elif name2=="H5'":
                    h5p2 = 1
            k='%s:%s' % (res1,atm1)
            num1 = numMap.get(k, '0')
        
            k='%s:%s' % (res2,atm2)
            num2 = numMap.get(k, '0')
            
                
            
            
            ########## Output Generation
            if igr1 and igr2:
                atm1j = name1 + "1"
                pseud1 = name1 + "*"
                base1 = resMap[res1]
                atm2j = name2 + "1"
                pseud2 = name2 + "*"
                base2 = resMap[res2]
                out.append("#\n#  %d %s %s %s   %s %s %s\n" % (xx, res1, base1, pseud1, res2, base2, pseud2))
                out.append(" &rst iat=  ")
                out.append(" -1, -1,")
            elif igr1:
                atm1j = name1 + "1"
                base1 = resMap[res1]
                pseud1 = name1 + "*"
                base2 = resMap[res2]
                out.append("#\n# %d %s %s %s   %s %s %s\n" % (xx, res1, base1, pseud1, res2, base2, atm2))
                out.append(" &rst iat=  ")
                out.append(" -1, %s," % num2)
            elif igr2:
                base1 = resMap[res1]
                atm2j = name2 + "1"
                base2 = resMap[res2]
                pseud2 = name2 + "*"
                out.append("#\n#  %d %s %s %s   %s %s %s\n" % (xx, res1, base1, atm1, res2, base2, pseud2))
                out.append(" &rst iat=  ")
                out.append(" %s, -1," % num1)
                
            out.append(" r1= %2.2f, r2= %2.2f, r3= %2.2f, r4= %2.2f,\n" % (dn - 0.5, dn, up, up + 0.5))
            
            ###### ATOM NUMBERS
            out.append(" igr1=")
            if val1 or ile1 or leu1 or gln1 or ild1 or thr1 or arg1 or h5p1:
                atmo1 = name1 + "11"
                atmo2 = name1 + "12"
                atmo3 = name1 + "13"
                atmo4 = name1 + "21"
                atmo5 = name1 + "22"
                atmo6 = name1 + "23"
                k="%s:%s" % (res1, atmo1)
                numo1 = numMap.get(k, None)
                k="%s:%s" % (res1, atmo2)
                numo2 = numMap.get(k, None)
                k="%s:%s" % (res1, atmo3)
                numo3 = numMap.get(k, None)
                k="%s:%s" % (res1, atmo4)
                numo4 = numMap.get(k, None)
                k="%s:%s" % (res1, atmo5)
                numo5 = numMap.get(k, None)
                k="%s:%s" % (res1, atmo6)
                numo6 = numMap.get(k, None)
                nout=''
                if numo1:
                    nout='%s %s, ' % (nout, numo1)
                if numo2:
                    nout='%s %s, ' % (nout, numo2)
                if numo3:
                    nout='%s %s, ' % (nout, numo3)
                if numo4:
                    nout='%s %s, ' % (nout, numo4)
                if numo5:
                    nout='%s %s, ' % (nout, numo5)
                if numo6:
                    nout='%s %s, ' % (nout, numo6)
                out.append(nout)
                
                if h5p1 == 1:
                    k="%s:H5'" % res1
                    numo1 = numMap[k]
                    k="%s:H5''" % res1
                    numo2 = numMap[k]
                    out.append(" %s, %s," % (numo1, numo2))
            elif igr1:
                atm1a = name1 + "1"
                atm1b = name1 + "2"
                atm1c = name1 + "3"
                nout=''
                k='%s:%s' % (res1, atm1a)
                num1a = numMap.get(k, None)
            
                k='%s:%s' % (res1, atm1b)
                num1b = numMap.get(k, None)
                
                
                k='%s:%s' % (res1, atm1c)
                num1c=numMap.get(k, None)
                
                if num1a:
                    nout='%s %s, ' % (nout, num1a)
                if num1b:
                    nout='%s %s, ' % (nout, num1b)
                if num1c:
                    nout='%s %s, ' % (nout, num1c)
                out.append(nout)
                
            else:
                out.append(" 0,")
                
            out.append("\n igr2=")
            
            if val2 or ile2 or leu2 or gln2 or ild2 or thr2 or arg2 or h5p2:
                atmt1 = name2 + "11"
                atmt2 = name2 + "12"
                atmt3 = name2 + "13"
                atmt4 = name2 + "21"
                atmt5 = name2 + "22"
                atmt6 = name2 + "23"
                k='%s:%s' % (res2, atmt1)
                numt1 = numMap.get(k, None)            
                k='%s:%s' % (res2, atmt2)
                numt2 = numMap.get(k, None)
                k='%s:%s' % (res2, atmt3)
                numt3 = numMap.get(k, None)
                k='%s:%s' % (res2, atmt4)
                numt4 = numMap.get(k, None)
                k='%s:%s' % (res2, atmt5)
                numt5 = numMap.get(k, None)
                k='%s:%s' % (res2, atmt6)
                numt6 = numMap.get(k, None)
                nout=''
                if numt1:
                    nout='%s %s, ' % (nout, numt1)
                if numt2:
                    nout='%s %s, ' % (nout, numt2)
                if numt3:
                    nout='%s %s, ' % (nout, numt3)
                if numt4:
                    nout='%s %s, ' % (nout, numt4)
                if numt5:
                    nout='%s %s, ' % (nout, numt5)
                if numt6:
                    nout='%s %s, ' % (nout, numt6)
                out.append(nout)
               
                if h5p2:
                    k="%s:H5'" % res2
                    numt1 = numMap[k]
                    k="%s:H5''" % res2
                    numt2 = numMap[k]
                    out.append(" %s, %s," % (numt1, numt2))
            elif igr2:
                atm2a = name2 + "1"
                atm2b = name2 + "2"
                atm2c = name2 + "3"
                k='%s:%s' % (res2, atm2a)
                num2a = numMap.get(k, None)
            
                k='%s:%s' % (res2, atm2b)
                num2b = numMap.get(k, None)
                nout=''
                if num2a:
                    nout='%s %s, ' % (nout, num2a)
                if num2b:
                    nout='%s %s, ' % (nout, num2b)
                k='%s:%s' % (res2, atm2c)
                num2c = numMap.get(k, None)
                if num2c:
                    nout='%s %s, ' % (nout, num2c)
                out.append(nout)
                out.append("\n")
            else:
                out.append(" 0,")
            out.append("  &end\n")
            #out.append(" rk2= 0.00, rk3= 20.000, ir6=1, &end\n")
    return out
            



if __name__ == '__main__':
    
    usage = "usage: %prog -w working_directory  -x xplor_filename -p pdb_filename -o out_filename"
  
    parser = OptionParser(usage)
    parser.add_option("-w", "--wdir", dest="wd",
                    help="Working directory", metavar="WORKDIR")
  
    parser.add_option("-x", "--xplorfile", dest="xplorfile",
                    help="Xplor filename", metavar="FILE")
    
    parser.add_option("-p", "--pdbfile", dest="pdbfile",
                    help="PDB filename", metavar="FILE")
  
    parser.add_option("-o", "--outfile", dest="outfile",
                    help="Output filename", metavar="FILE")
  
    (options, args) = parser.parse_args()
    
        
    if not options.wd:
        parser.error("Working directory  is required")
    
    wd=os.path.abspath(options.wd)+'/'
    
    if options.xplorfile:
        xfile=os.path.join(wd, options.xplorfile)
    else:
        parser.error("PDB filename is required")
        
    if options.pdbfile:
        pdbfile=os.path.join(wd, options.pdbfile)
    else:
        parser.error("PDB filename is required")
        
    if options.outfile:
        outfile=os.path.join(wd, options.outfile)
    else:
        parser.error("Output filename is required")
    
    
    out=convert(xfile, pdbfile)
    fout=open(outfile,'w')
    fout.writelines(out)
    fout.close()