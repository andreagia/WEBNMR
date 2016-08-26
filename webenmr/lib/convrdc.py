#!/usr/bin/env python
'''
This program attempts to convert XPLOR Pseudocontact shift restraints in AMBER format
XPLOR:
assign ( resid 200  and name OO ) ( resid 200  and name Z ) ( resid 200  and name X ) (resid 200  and name Y ) ( resid  13  and name C )   0.2400  0.2000 
assign ( resid 200  and name OO ) ( resid 200  and name Z ) ( resid 200  and name X ) ( resid 200  and name Y ) ( resid  13  and name CA ) 0.4300  0.2000 
assign ( resid 200  and name OO ) ( resid 200  and name Z ) ( resid 200  and name X ) (  resid 200  and name Y )( resid  13  and name CB ) 0.1000  0.2000 


AMBER:
&align
num_datasets=2,
   dcut= -1.0, freezemol= .false.,

   ndip= 10, dwt= 5*0.1, 5*0.1
   gigj= 5*-3.1631,5*-3.1631,
   dij= 5*1.041,5*1.041,
  s11= -4.236,-4.236
  s12= 56.860,56.860
  s13= -34.696,-34.696
  s22= -27.361,-27.361
  s23= -12.867,-12.867
  
  dataset=1,
   id(1)=20, jd(1)=19, dobsl(1)=-2.13, dobsu(1)=-2.13,
   id(2)=31, jd(2)=30, dobsl(2)= 1.10, dobsu(2)= 1.10,
   id(3)=43, jd(3)=42, dobsl(3)=-5.54, dobsu(3)=-5.54,
   ...
   ...
&end
'''

import sys
import os
import commands
from optparse import OptionParser
from xml_parser import *
from normalize_tbl import normalize
from constants import convtable

def searchres(nres, lpdb):
    for l in lpdb:
        if l.strip().lower().startswith('atom'):
            s=l.split()
            if int(nres)==int(s[4]):
                return s[3]

def searchC(outx):
    i=0
    c=[]
    while i<len(outx): 
        if outx[i].strip().startswith('XDIPO_RDC>frun'):
            while i<len(outx):
                i+=1
                if i>=len(outx):
                    break
                if outx[i].strip().startswith('C1='):
                    t=[]
                    l=outx[i].split()
                    for x in range(1,len(l),2):
                        t.append(l[x])
                    c.append(t)
                    break
        i+=1
    return c
                    
def convert(pdb, new, wd):
    
    if new.calculation.protocol.xrdc:
        xfiles=[]
        if len(new.calculation.protocol.xrdc)==1:
            xfiles.append(new.calculation.protocol.xrdc.attrib_.xrdc_file)
        else:
            for i in range(len(new.calculation.protocol.xrdc)):
                xfiles.append(new.calculation.protocol.xrdc[i].attrib_.xrdc_file)
    else:
        sys.exit('%s: RDC not found\n' % sys.argv[0])
    
    try:
        lpdb=open(pdb, 'r').readlines()
    except IOError, (errno, strerror):
        sys.exit('%s: IOError(%s): %s %s\n' % (sys.argv[0], errno, pdb, strerror))
        
    numMap = {}
        
    for l in lpdb:
        if l.strip().lower().startswith('atom'):
            ls=l.split()
            k='%s:%s' % (ls[4],ls[2])
            numMap[k]=ls[1]
            
    cmd=' /opt/local_prog/xplor-nih-2.22/bin/xplor tensor.inp'
    outx=commands.getoutput(cmd)
    outx=outx.split('\n')  
    #outx=open('xplor.outx').readlines()
    c=searchC(outx)
    
    out=[' &align\n']
    out.append('  num_datasets=%d,\n' % len(xfiles))
    out.append('  dcut=-1.0, freezemol=.false.,\n')
    out.append('  ndip=10,')
    out.append('  dcut=-1.0,dwt=92*0.1,\n')
    out.append('  gigj=92*-3.163,\n')
    out.append('  dij=92*1.01,\n')
    s11='  s11='
    s12='  s12='
    s13='  s13='
    s22='  s22='
    s23='  s23='
    for i in range(len(c)):
        s11='%s%s,' % (s11, c[i][0])
        s12='%s%s,' % (s12, c[i][1])
        s13='%s%s,' % (s13, c[i][2])
        s22='%s%s,' % (s22, c[i][3])
        s23='%s%s,' % (s23, c[i][4])
    
    out.append('%s\n' % s11)
    out.append('%s\n' % s12)
    out.append('%s\n' % s13)
    out.append('%s\n' % s22)
    out.append('%s\n' % s23)
      
    counter=0
    nrdc=0
    for xfile in xfiles:
        counter+=1
        nxfile=os.path.join(wd, 'rdc_%d_web_enmr_normalized.tbl' % counter)
        xfile=os.path.join(wd, xfile)
        try:
            normalize(xfile, nxfile, new, wd)
        except:
            sys.exit('%s: unable to normalize %s tbl file\n' % (sys.argv[0], xfile))
    
        try:
            xp=open(nxfile,'r').readlines()
        except IOError, (errno, strerror):
            sys.exit('%s: IOError(%s): %s %s\n' % (sys.argv[0], errno, nxfile, strerror))
        out.append('  dataset=%d,\n' % counter)    
        for l in xp:
            if l.strip().startswith('assign'):
                nrdc+=1
                ls=l.split()
                res=searchres(ls[31], lpdb)  
                kk='%s:%s' % (res, ls[34])
                if convtable.has_key(kk):
                    ls[34]=convtable[kk].split(':')[1]
                k='%s:%s' % (ls[31], ls[34])
                natm1=numMap[k]
                res=searchres(ls[38], lpdb)  
                kk='%s:%s' % (res, ls[41])
                if convtable.has_key(kk):
                    ls[41]=convtable[kk].split(':')[1]
                k='%s:%s' % (ls[38], ls[41])
                natm2=numMap[k]
                
                out.append('  id(%s)=%s, jd(%s)=%s, dobsl(%s)=%s, dobsu(%s)=%s, \n' % 
                           (nrdc, natm1, nrdc, natm2, nrdc, ls[43], nrdc, ls[43]))
    
    out[3]='  ndip=%d,' % nrdc
    out.append(' &end')
    return out

if __name__ == '__main__':
   
    usage = "usage: %prog -w working_directory  -p pdb_filename -o out_filename"
  
    parser = OptionParser(usage)
    parser.add_option("-w", "--wdir", dest="wd",
                    help="Working directory", metavar="WORKDIR")
  
    
    parser.add_option("-p", "--pdbfile", dest="pdbfile",
                    help="PDB filename", metavar="FILE")
  
    parser.add_option("-o", "--outfile", dest="outfile",
                    help="Output filename", metavar="FILE")
  
    (options, args) = parser.parse_args()
    
        
    if not options.wd:
        parser.error("Working directory is required")
    
    wd=os.path.abspath(options.wd)+'/'
    
    if options.pdbfile:
        pdbfile=os.path.join(wd, options.pdbfile)
    else:
        parser.error("PDB filename is required")
        
    if options.outfile:
        outfile=os.path.join(wd, options.outfile)
    else:
        parser.error("Output filename is required")
    
        
    xml_input=os.path.join(wd,'input.xml')
    doc = etree.parse(xml_input)
    ndoc = etree.tostring(doc)
    new=parse_node(etree.fromstring(ndoc))
    out=convert(pdbfile, new, wd)
    fout=open(outfile,'w')
    fout.writelines(out)
    fout.close()