#!/usr/bin/env python
'''
This program attempts to convert XPLOR Pseudocontact shift restraints in AMBER format
XPLOR:
assign ( resid 200  and name OO ) ( resid 200  and name Z ) ( resid 200  and name X ) (resid 200  and name Y ) ( resid  13  and name C )   0.2400  0.2000 
assign ( resid 200  and name OO ) ( resid 200  and name Z ) ( resid 200  and name X ) ( resid 200  and name Y ) ( resid  13  and name CA ) 0.4300  0.2000 
assign ( resid 200  and name OO ) ( resid 200  and name Z ) ( resid 200  and name X ) (  resid 200  and name Y )( resid  13  and name CB ) 0.1000  0.2000 


AMBER:
&pcshf
nprot=205,
nme=1,
nmpcm='FE ',
optphi(1)=0.38847,
opttet(1)=0.407499,
optomg(1)=0.0251676,
opta1(1)=-71.233,
opta2(1)=1214.511,
optkon=30,
iprot(1)=26, obs(1)=1.140, wt(1)=1.000, tolpro(1)=1.00, mltpro(1)=1,
iprot(2)=28, obs(2)=2.740, wt(2)=1.000, tolpro(2)=.500, mltpro(2)=1,
iprot(3)=30, obs(3)=1.170, wt(3)=1.000, tolpro(3)=.500, mltpro(3)=1,

...
iprot(205)=1215, obs(205)=.730, wt(205)=1.000, tolpro(205)=.500,
mltpro(205)=1,

'''

import sys
import os
import commands
from optparse import OptionParser
from xml_parser import *
from normalize_tbl import normalize
from constants import convtable

molteplicity={'ALA:H' : 1, 'ALA:HA' : 1, 'GLY:H' :1, 'SER:H' : 1, 'SER:HA' : 1, 'SER:HG' : 1, 'THR:H' : 1, 'THR:HA' : 1,
              'THR:HB' : 1, 'THR:HG1' : 1, 'LEU:H' : 1, 'LEU:HA' : 1, 'LEU:HG' : 1, 'ILE:H' : 1, 'ILE:HA' : 1,
              'ILE:HB' : 1, 'VAL:H' : 1, 'VAL:HA' : 1, 'VAL:HB' : 1, 'ASN:H' : 1, 'ASN:HA' : 1, 'GLN:H' : 1,
              'GLN:HA' : 1, 'ARG:H' : 1, 'ARG:HA' : 1, 'ARG:HE' : 1, 'HID:H' : 1, 'HID:HA' : 1, 'HID:HD1' : 1,
              'HID:HE1' : 1, 'HID:HD2' : 1, 'HIE:H' : 1, 'HIE:HA' : 1, 'HIE:HD2' : 1, 'HIE:HE1' : 1, 'HIE:HE2' :1,
              'HIP:H' : 1, 'HIP:HA' : 1, 'HIP:HD1' : 1, 'HIP:HD2' : 1, 'HIP:HE1' : 1, 'HIP:HE2' : 1, 'TRP:H' : 1,
              'TRP:HA' : 1, 'TRP:HD1' : 1, 'TRP:HE1' : 1, 'TRP:HZ2' : 1, 'TRP:HH2' : 1, 'TRP:HZ3' : 1, 'TRP:HE3' : 1,
              'PHE:H' : 1, 'PHE:HA' : 1, 'PHE:HD1' : 1, 'PHE:HE2' : 1, 'PHE:HZ' : 1, 'PHE:HE2' : 1, 'PHE:HD2' : 1,
              'TYR:H' : 1, 'TYR:HA' : 1, 'TYR:HD1' : 1, 'TYR:HE1' : 1, 'TYR:HH' : 1, 'TYR:HE2' : 1, 'TYR:HD2' : 1,
              'GLU:H' : 1, 'GLU:HA' : 1, 'ASP:H' : 1, 'ASP:HA' : 1, 'LYS:H' : 1, 'LYS:HA' : 1, 'PRO:HA' : 1, 'CYS:H' : 1,
              'CYS:HA' : 1, 'CYS:HG' : 1, 'CYX:H' : 1, 'CYX:HA' : 1, 'MET:H' : 1, 'MET:HA' : 1,
              'GLY:HA2' : 2, 'GLY:HA3' : 2, 'SER:HB2' : 2, 'SER:HB3' : 2, 'LEU:HB2' : 2, 'LEU:HB3' : 2,
              'ILE:HG12' : 2, 'ILE:HG13' : 2, 'ASN:HB2' : 2, 'ASN:HB3' : 2, 'ASN:HD21' : 2, 'ASN:HD22' : 2,
              'GLN:HB2' : 2, 'GLN:HB3' : 2, 'GLN:HG2' : 2, 'GLN:HG3' : 2, 'GLN:HE21' : 2, 'GLN:HE22' : 2,
              'ARG:HB2' : 2,  'ARG:HB3' : 2, 'ARG:HG2' : 2, 'ARG:HG3' : 2, 'ARG:HD2' : 2, 'ARG:HD3' : 2,
              'ARG:HH21' : 2, 'ARG:HH22' : 2, 'ARG:HH11' : 2, 'ARG:HH12' : 2, 'HID:HB2' : 2, 'HID:HB3' : 2,
              'HIE:HB2' : 2, 'HIE:HB3' : 2, 'HIP:HB2' : 2, 'HIP:HB3' : 2, 'TRP:HB2' : 2, 'TRP:HB3' : 2,
              'PHE:HB2' : 2, 'PHE:HB3' : 2, 'TYR:HB2' : 2, 'TYR:HB3' : 2, 'GLU:HB2' : 2, 'GLU:HB3' : 2,
              'GLU:HG2' : 2, 'GLU:HG3' : 2, 'ASP:HB2' : 2, 'ASP:HB3' : 2, 'LYS:HB2' : 2, 'LYS:HB3' : 2,
              'LYS:HG2' : 2, 'LYS:HG3' : 2, 'LYS:HD2' : 2, 'LYS:HD3' : 2, 'LYS:HE2' : 2, 'LYS:HE3' : 2,
              'PRO:HB2' : 2, 'PRO:HB3' : 2, 'PRO:HG2' : 2, 'PRO:HG3' : 2, 'PRO:HD2' : 2, 'PRO:HD3' : 2,
              'CYS:HB2' : 2, 'CYS:HB3' : 2, 'CYX:HB2' : 2, 'CYX:HB3' : 2, 'MET:HB2' : 2, 'MET:HB3' : 2,
              'MET:HG2' : 2, 'MET:HG3' : 2, 
              'ALA:HB1' : 3, 'ALA:HB2' : 3, 'ALA:HB3' :3, 'THR:HG21' : 3, 'THR:HG22' : 3, 'THR:HG23' :3,
              'LEU:HD11' : 3, 'LEU:HD12' : 3, 'LEU:HD13' : 3, 'LEU:HD21' : 3, 'LEU:HD22' : 3, 'LEU:HD23' : 3,
              'ILE:HG21' : 3, 'ILE:HG22' : 3,  'ILE:HG23' : 3, 'ILE:HD11' : 3, 'ILE:HD12' : 3, 'ILE:HD13' : 3,
              'VAL:HG11' : 3, 'VAL:HG12' : 3, 'VAL:HG13' : 3, 'VAL:HG21' : 3,  'VAL:HG22' : 3, 'VAL:HG23' : 3,
              'LYS:HZ1' : 3, 'LYS:HZ2' : 3, 'LYS:HZ3' : 3, 'MET:HE1' : 3, 'MET:HE2' : 3, 'MET:HE3' : 3
              }


def searchres(nres, lpdb):
    for l in lpdb:
        if l.strip().lower().startswith('atom'):
            s=l.split()
            if int(nres)==int(s[4]):
                return s[3]
            
def convert(pdb, new, tensor_file, wd):

    if new.calculation.protocol.xpcs:
        
        if len(new.calculation.protocol.xpcs)==1:
            xfile=new.calculation.protocol.xpcs.attrib_.xpcs_file
        else:
            xfile=new.calculation.protocol.xpcs[0].attrib_.xpcs_file
         
        nxfile=os.path.join(wd, 'pcs_web_enmr_normalized.tbl')
        xfile=os.path.join(wd, xfile)
        try:
            normalize(xfile, nxfile, new, wd)
        except:
            sys.exit('%s: unable to normalize %s tbl file\n' % (sys.argv[0], xfile))
        #cmd='python /opt/python_wrapper/wrapper_xml/normalize_tbl.py -w %s -t %s -o %s' % (wd, xfile, nxfile)
        #outx=commands.getoutput(cmd)
        #if outx:
            #sys.exit(outx)
        
    else:
        sys.exit('%s: PCS not found\n' % sys.argv[0])
                        
    try:
        lpdb=open(pdb, 'r').readlines()
    except IOError, (errno, strerror):
        sys.exit('%s: IOError(%s): %s %s\n' % (sys.argv[0], errno, pdb, strerror))
    
    out = [' &pcshf\n']
    
    numMap = {}
    
    for l in lpdb:
        if l.strip().lower().startswith('atom'):
            ls=l.split()
            k='%s:%s' % (ls[4],ls[2])
            numMap[k]=ls[1]
            
    cmd=' /opt/local_prog/xplor-nih-2.22/bin/xplor tensor.inp'
    outx=commands.getoutput(cmd)
    outx=outx.split('\n')
    fphi=False
    fa1=False
    fa2=False
    for l in outx:
        if l.strip().startswith('PHI='):
            if not fphi:
                fphi=True
                sl=l.split()
                phi=float(sl[1])
                theta=float(sl[3])
                omega=float(sl[5])
                #print phi, theta, omega
        if l.strip().startswith('A1 ='):
            if not fa1:
                fa1=True
                a1=float(l.split()[2][:-1])
                
        if l.strip().startswith('A2 ='):
            if not fa2:
                fa2=True
                a2=float(l.split()[2][:-1])
    
    try:
        xp=open(nxfile,'r').readlines()
    except IOError, (errno, strerror):
        sys.exit('%s: IOError(%s): %s %s\n' % (sys.argv[0], errno, nxfile, strerror))

    out.append(' nprot=%d,\n' % len(xp))
    out.append(' nfe=1,\n')
    i=0
    first=True
    pream=True
    for l in xp:
        if l.strip().startswith('assign'):
            i=i+1
            ls=l.split()
            if first:
                first=False
                tf=open(tensor_file).readlines()
                for lt in tf:
                    lst=lt.split()
                    if int(lst[2])==int(ls[3]):
                        metal=lst[11]
                        break
                    elif int(lst[8])==int(ls[3]):
                        metal=lst[5]
                        break
             
            
            res=searchres(ls[31], lpdb)  
            kk='%s:%s' % (res, ls[34])
            if convtable.has_key(kk):
                ls[34]=convtable[kk].split(':')[1]
            if molteplicity.has_key(kk):
                mlt=molteplicity[kk]
            else:
                mlt=1
            
            k='%s:%s' % (ls[31], ls[34])
            #print numMap
            #print k
            natm=numMap[k]
            if pream:
                pream=False
                out.append(" nmpmc='%s'\n" % metal)
                out.append(' optphi(1)=%f,\n' % phi)
                out.append(' opttet(1)=%f,\n' % theta)
                out.append(' optomg(1)=%f,\n' % omega)
                out.append(' opta1(1)=%f,\n' % a1)
                out.append(' opta2(1)=%f,\n' % a2)
                out.append(' optkon=30,\n')
            out.append(' iprot(%d)=%s, obs(%s)=%1.3f, wt(%d)=%1.3f, tolpro(%d)=.500, mltpro(%d)=%d,\n' %
                       (i, natm, i, float(ls[36]), i, float(ls[37]), i, i, mlt))

    out.append('/')
    return out

if __name__ == '__main__':
   
    usage = "usage: %prog -w working_directory -t tensor_filename -p pdb_filename -o out_filename"
  
    parser = OptionParser(usage)
    parser.add_option("-w", "--wdir", dest="wd",
                    help="Working directory", metavar="WORKDIR")
  
    parser.add_option("-t", "--tensorfile", dest="tensorfile",
                    help="TBL filename", metavar="FILE")
    
    parser.add_option("-p", "--pdbfile", dest="pdbfile",
                    help="TBL filename", metavar="FILE")
  
    parser.add_option("-o", "--outfile", dest="outfile",
                    help="Output filename", metavar="FILE")
  
    (options, args) = parser.parse_args()
    
        
    if not options.wd:
        parser.error("Working directory is required")
    
    wd=os.path.abspath(options.wd)+'/'
    
    
    if options.tensorfile:
        tensorfile=os.path.join(wd, options.tensorfile)
    else:
        parser.error("TBL tensors filename is required")
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
    out=convert(pdbfile, new, tensorfile, wd)
    fout=open(outfile,'w')
    fout.writelines(out)
    fout.close()