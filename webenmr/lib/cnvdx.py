#!/usr/bin/env python
'''
This program attempts to convert XPLOR pseudo restraints into AMBER restraints.


XPLOR:
assign ( resid 99 and name N ) ( resid 99 and name CA ) ( resid 99 and name C ) ( resid 100  and name N )  1.00 -40.00 20.00 2 

AMBER:
#
#  1 GUA H3'  1 GUA Q5'        5.50
 &rst iat=  27, -1, r3= 4.394, r4= 4.894,
 igr1= 0, 0, 0, 0, igr2= 4, 5, 0, 0,
 r1= 1.300, r2= 1.800, r3= 4.394, r4= 4.894,
 rk2= 0.00, rk3= 32.000, &end
'''


import os
import sys
from optparse import OptionParser
from lxml import etree
import math

def stup_cyana(resi,atm):
    rr = []
    rr.append("GLY:HA")
    rr.append("ALA:HB")
    rr.append("SER:HB")
    rr.append("VAL:HG1")
    rr.append("VAL:HG2")
    rr.append("ASN:HB")
    rr.append("ASN:HD2")
    rr.append("GLN:HB")
    rr.append("GLN:HE2")
    rr.append("GLN:HG")
    rr.append("PRO:HB")
    rr.append("PRO:HD")
    rr.append("PRO:HG")
    rr.append("GLU:HB")
    rr.append("GLU:HG")
    rr.append("ASP:HB")
    rr.append("LEU:HB")
    rr.append("LEU:HD1")
    rr.append("LEU:HD2")
    rr.append("ILE:HG")
    rr.append("ILE:HG1")
    rr.append("ILE:HG2")
    rr.append("HIS:HB")
    rr.append("HID:HB")
    rr.append("HIE:HB")
    rr.append("MET:HB")
    rr.append("MET:HG")
    rr.append("MET:HE")
    rr.append("CYS:HB")
    rr.append("PHE:HB")
    rr.append("TYR:HB")
    rr.append("TRP:HB")
    rr.append("THR:HG")
    rr.append("THR:HG2")
    rr.append("LYS:HB")
    rr.append("LYS:HG")
    rr.append("LYS:HD")
    rr.append("LYS:HE")
    rr.append("LYS:HZ")
    rr.append("ARG:HB")
    rr.append("ARG:HG")
    rr.append("ARG:HD")
    rr.append("ARG:HH1")
    rr.append("ARG:HH2")
    rr.append("ARG:NH")
    ret = ""
    for i in rr:
        rrs = i.split(":")
        #print atm[0:-1]
        #print i
        if rrs[0] == resi and atm[0:-1] == rrs[1]:
            ret = atm[-1] + atm[0:-1]
    return ret
            

def convert(xml_noe, ini_num, pdb_out, pdb_ref_n,nocorr):  
    lpdb = open(pdb_out, 'r').readlines()
    out = []
    numMap = {}
    resMap = {}
    resnum = []
    resnumall = []
    nocorr = True
    res_num_corr = int(ini_num) - 1
    #for l in lpdb:
    #    if l.startswith('ATOM'):
    #        #k <- resid number : atom name 
    #        k='%s:%s' % (l[22:26], l[12:17].replace(" ",""))
    #        numMap[k] = l[6:11]
    #        resMap[k] = l[17:21].replace(" ","")
    for l in lpdb:
        if l.strip().startswith('ATOM'):
            ls=l.split()
            k='%s:%s' % (ls[4],ls[2])
            #numMap["numero_residuo: numero_atomo" ] = nome_atomo
            numMap[k] = ls[1]
            #resMap["numero_residuo: numero_atomo"] = nome_residuo
            resMap[k] = ls[3]
            #resnumall -> numero_residuo nome_residuo
            resnumall.append('%s %s' %(ls[4], ls[3]))
            #pdb_ref -> numero_residuo nome_atomo_prima_della_coversione nome_atomo_dopo_della_coversione
    print "NUMMAP"
    for i in numMap:
        print i
    
            
    lref = open(pdb_ref_n, 'r').readlines()
    set = {}
    ref = [set.setdefault(ek,ek) for ek in lref if ek not in set]
    set = {}
    resnum = [set.setdefault(ek,ek) for ek in resnumall if ek not in set]
    #print 'REFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf'
    #print ref
    #refd = {}
    #sd = []
    print "REF"
    for i in ref:
        print i.replace("\n","").split()
    #    sd.append(i.split()[1])
    #    sd.append(i.split()[2])
    #    refd[i.split()[0]] = sd
    #    sd = []
        
    noe_list = []
    
    rxml = etree.Element("status_dih")
    #find max number
    num_resid = []
    for dd in numMap:
        num_resid.append(int(dd.split(":")[0]))
            
    for elt in xml_noe.getiterator():
        ang_err = True
        if elt.tag == "selection":
            name_ang = ""
            for elt1 in elt.getiterator():
                if elt1.tag == "cyana":
                    name_ang = elt1.get("angle")
                    if elt1.get("ERROR"):
                        etree.SubElement(rxml, "Angle_not_found").text = name_ang
                        ang_err = False
                else:
                    name_ang = ""
                if elt1.tag == "sel1":
                    for elt2 in elt1.getiterator():
                        if elt2.tag == "resid":
                            res1 = elt2.text
                        if elt2.tag == "name":
                            atm1 = elt2.text
                if elt1.tag == "sel2":
                    for elt2 in elt1.getiterator():
                        if elt2.tag == "resid":
                            res2 = elt2.text
                        if elt2.tag == "name":
                            atm2 = elt2.text
                if elt1.tag == "sel3":
                    for elt2 in elt1.getiterator():
                        if elt2.tag == "resid":
                            res3 = elt2.text
                        if elt2.tag == "name":
                            atm3 = elt2.text
                if elt1.tag == "sel4":
                    for elt2 in elt1.getiterator():
                        if elt2.tag == "resid":
                            res4 = elt2.text
                        if elt2.tag == "name":
                            atm4 = elt2.text
                            
                if elt1.tag == "ang":
                    d = elt1.text
                if elt1.tag == "d_ang":
                    dd = elt1.text
            
            if ang_err:
                if (int(res1) - res_num_corr ) < 1 or (int(res2) - res_num_corr ) < 1 or (int(res3) - res_num_corr ) < 1 or (int(res4) - res_num_corr ) < 1:
                    ang_err = False
                    etree.SubElement(rxml, "Out_of_range").text = "%s %s %s %s %s %s %s %s" %(res1, atm1, res2, atm2, res3, atm3, res4, atm4)
                if ((int(res1) - res_num_corr ) not in num_resid) or ((int(res2) - res_num_corr ) not in num_resid) or ((int(res3) - res_num_corr ) not in num_resid) or ((int(res4) - res_num_corr ) not in num_resid):
                    ang_err = False
                    etree.SubElement(rxml, "Out_of_range").text = "%s %s %s %s %s %s %s %s" %(res1, atm1, res2, atm2, res3, atm3, res4, atm4)
                
            if ang_err:      
                up = float(d)+float(dd)
                dn = float(d)-float(dd)
                #correction of residues ini_num
                
                print "Cerco %s %s %s %s %s %s %s %s %s" %(res1, atm1, res2, atm2, res3, atm3, res4, atm4, name_ang)
                res1 = str(int(res1) - res_num_corr )
                res2 = str(int(res2) - res_num_corr )
                res3 = str(int(res3) - res_num_corr )
                res4 = str(int(res4) - res_num_corr )
                
                print "-------------------------------------With %d subtracted-----------------------------------------------" %res_num_corr
                print "Cerco %s %s %s %s %s %s %s %s" %(res1, atm1, res2, atm2, res3, atm3, res4, atm4)
                # controllo il multiassegnamento
                
                num1 = ""
                num2 = ""
                base1 = ""
                base2 = ""
                
                igr1 = ""
                igr2 = ""
                nigr1 = ""
                nigr2 = ""
                tr_atm = 0
                res_name = ""
                if not atm1.endswith('#'):
                    print "ATM1 " + atm1
                    for at in resnum:
                        if res1 == at.split()[0]:
                            for atr in ref:
                                tr_atm = 0
                                if ( atm1 == atr.split()[1] ) and (at.split()[1] == atr.split()[0] ):
                                    print "Trovato " + atr.split()[2] + " Convertito da " + atm1
                                    atm1c = atr.split()[2]
                                    tr_atm = 1
                                    
                                elif tr_atm == 0:
                                    atm1c = atm1
                                    res_name = at.split()[1]
                                    
                    if atm1c == atm1 and tr_atm == 0:
                        print "provo cyana ", res1, " ", res_name ," ", atm1
                        atm1c = stup_cyana(res_name, atm1)
                        print "result cyana ",atm1c
                        if atm1c == "":
                            atm1c = atm1
                            
                    print res1
                    print atm1                        
                    
                    k1 = '%s:%s' % (res1, atm1c)
    
                    print k1
                    
                    if k1 in numMap:
                        num1 = numMap[k1]
                    else:
                        print "####################################################################################################################"
                        print "errore %s" %k1
                        num1 = 'XXX'
                        
                        etree.SubElement(rxml, "Res1_not_found").text = "Res1 %s  Atom1 %s Res2 %s Atom2 %s Res3 %s Atom3 %s Res4 %s Atom4  %s" %(res1, atm1, res2, atm2, res3, atm3, res4, atm4)
                        
                    if k1 in resMap: 
                        base1 = resMap[k1]
                    else:
                        print "errore %s" %k1
                        base1 = 'XXX'
                        etree.SubElement(rxml, "Atom1_not_found").text = "Res1 %s  Atom1 %s Res2 %s Atom2 %s Res3 %s Atom3 %s Res4 %s Atom4  %s" %(res1, atm1, res2, atm2, res3, atm3, res4, atm4)
                                            
                    
                    print "NUM1"
                    print num1
                    print base1
                
    
                if not atm2.endswith('#'):
                    print "ATM2 " + atm2
                    for at in resnum:
                        if res2 == at.split()[0]:
                            for atr in ref:
                                tr_atm = 0
                                if ( atm2 == atr.split()[1] ) and (at.split()[1] == atr.split()[0] ):
                                    print "Trovato " + atr.split()[2] + " Convertito da " + atm2
                                    atm2c = atr.split()[2]
                                    tr_atm = 1
                                    
                                elif tr_atm == 0 :
                                    atm2c = atm2
                                    res_name = at.split()[1]
                                    
                    if atm2c == atm2 and tr_atm == 0:
                        print "provo cyana ", res2, " ", res_name ," ", atm2
                        atm2c = stup_cyana(res_name, atm2)
                        print "result cyana ",atm2c
                        if atm2c == "":
                            atm2c = atm2
                            
                    k2 = '%s:%s' % (res2, atm2c)
          
                    print k2
                    
                    if k2 in numMap:
                        num2 = numMap[k2]
                    else:
                        print"**************************************************************************************************"
                        print "errore %s" %k2
                        num2 = 'XXX'
                        etree.SubElement(rxml, "Res2_not_found").text = "Res1 %s  Atom1 %s Res2 %s Atom2 %s Res3 %s Atom3 %s Res4 %s Atom4  %s" %(res1, atm1, res2, atm2, res3, atm3, res4, atm4)
                        
                    if k2 in resMap:                    
                        base2 = resMap[k2]
                    else:
                        print "errore %s" %k2
                        base2 = 'XXX'
                        etree.SubElement(rxml, "Atom2_not_found").text = "Res1 %s  Atom1 %s Res2 %s Atom2 %s Res3 %s Atom3 %s Res4 %s Atom4  %s" %(res1, atm1, res2, atm2, res3, atm3, res4, atm4)
                    
                    print "NUM2"
                    print num2
                    print base2
                    
                if not atm3.endswith('#'):
                    print "ATM3 " + atm3
                    for at in resnum:
                        if res3 == at.split()[0]:
                            for atr in ref:
                                tr_atm = 0
                                if ( atm3 == atr.split()[1] ) and (at.split()[1] == atr.split()[0] ):
                                    print "Trovato " + atr.split()[2] + " Convertito da " + atm3
                                    atm3c = atr.split()[2]
                                    tr_atm = 1
                                    
                                elif tr_atm == 0 :
                                    atm3c = atm3
                                    res_name = at.split()[1]
                                    
                    if atm3c == atm3 and tr_atm == 0:
                        print "provo cyana ", res3, " ", res_name ," ", atm3
                        atm3c = stup_cyana(res_name, atm3)
                        print "result cyana ",atm3c
                        if atm3c == "":
                            atm3c = atm3
                            
                    k3 = '%s:%s' % (res3, atm3c)
          
                    print k3
                    
                    if k3 in numMap:
                        num3 = numMap[k3]
                    else:
                        print"**************************************************************************************************"
                        print "errore %s" %k3
                        num3 = 'XXX'
                        etree.SubElement(rxml, "Res3_not_found").text = "Res1 %s  Atom1 %s Res2 %s Atom2 %s Res3 %s Atom3 %s Res4 %s Atom4  %s" %(res1, atm1, res2, atm2, res3, atm3, res4, atm4)
                        
                    if k3 in resMap:                    
                        base3 = resMap[k3]
                    else:
                        print "errore %s" %k3
                        base3 = 'XXX'
                        etree.SubElement(rxml, "Atom3_not_found").text = "Res1 %s  Atom1 %s Res2 %s Atom2 %s Res3 %s Atom3 %s Res4 %s Atom4  %s" %(res1, atm1, res2, atm2, res3, atm3, res4, atm4)
                    
                    print "NUM3"
                    print num3
                    print base3                    
                    
                if not atm4.endswith('#'):
                    print "ATM4 " + atm4
                    for at in resnum:
                        if res4 == at.split()[0]:
                            for atr in ref:
                                tr_atm = 0
                                if ( atm4 == atr.split()[1] ) and (at.split()[1] == atr.split()[0] ):
                                    print "Trovato " + atr.split()[2] + " Convertito da " + atm4
                                    atm4c = atr.split()[2]
                                    tr_atm = 1
                                    
                                elif tr_atm == 0 :
                                    atm4c = atm4
                                    res_name = at.split()[1]
                                    
                    if atm4c == atm4 and tr_atm == 0:
                        print "provo cyana ", res4, " ", res_name ," ", atm4
                        atm4c = stup_cyana(res_name, atm4)
                        print "result cyana ",atm4c
                        if atm4c == "":
                            atm4c = atm4
                            
                    k4 = '%s:%s' % (res4, atm4c)
          
                    print k4
                    
                    if k4 in numMap:
                        num4 = numMap[k4]
                    else:
                        print"**************************************************************************************************"
                        print "errore %s" %k4
                        num4 = 'XXX'
                        etree.SubElement(rxml, "Res4_not_found").text = "Res1 %s  Atom1 %s Res2 %s Atom2 %s Res3 %s Atom3 %s Res4 %s Atom4  %s" %(res1, atm1, res2, atm2, res3, atm3, res4, atm4)
                        
                    if k4 in resMap:                    
                        base4 = resMap[k4]
                    else:
                        print "errore %s" %k4
                        base4 = 'XXX'
                        etree.SubElement(rxml, "Atom4_not_found").text = "Res1 %s  Atom1 %s Res2 %s Atom2 %s Res3 %s Atom3 %s Res4 %s Atom4  %s" %(res1, atm1, res2, atm2, res3, atm3, res4, atm4)
                    
                    print "NUM4"
                    print num4
                    print base4
                    
                    if num1 != "XXX" and num2 != "XXX" and num3 != "XXX" and num4 != "XXX" : 
                        #if dn > 0:
                        #    dns = dn + 1
                        #else:
                        #    dns = dn -1
                        #if up > 0:
                        #    ups = up + 1
                        #else:
                        #    ups = up -1   
                        out.append("#\n#  (%s %s %s) - (%s %s %s) - " % (res1, base1, atm1, res2, base2, atm2))
                        out.append("(%s %s %s) - (%s %s %s)  %s\n" % (res3, base3, atm3, res4, base4, atm4, name_ang ))
                        out.append(" &rst iat=  %s, %s, %s, %s, \n" % (num1, num2, num3, num4))
                        out.append(" r1= %3.1f, r2= %3.1f, r3= %3.1f, r4= %3.1f,\n" % (dn - 30, dn, up, up + 30))
                        out.append(" rk2= 32.00, rk3= 32.00, &end\n")
                
#for i in out:
#    print i[:-1]
    print "INI ###################### atomi non convertiti nei DIH ##########################"
    print etree.tostring(rxml, pretty_print=True)
    print "END ######################atomi non convertiti nei DIH ##########################"
    return etree.tostring(rxml, pretty_print=True), out



def convert_old(xfile, pdb):
    
    try:
        lpdb=open(pdb, 'r').readlines()
    except IOError, (errno, strerror):
        sys.exit('%s: IOError(%s): %s %s\n' % (sys.argv[0], errno, pdb, strerror))
    
    out = []
    numMap = {}
    baseMap={}
    
    for l in lpdb:
        if l.strip().startswith('ATOM'):
            ls=l.split()
            k='%s:%s' % (ls[4],ls[2])
            numMap[k]=ls[1]
            baseMap[k]=ls[3]
            
    try:
        xp=open(xfile,'r').readlines()
    except IOError, (errno, strerror):
        sys.exit('%s: IOError(%s): %s %s\n' % (sys.argv[0], errno, xfile, strerror))
    
    for l in xp:
        if l.strip().startswith('assign'):
            ls = l.split()    
            res1 = ls[3]
            atm1 = ls[6]
            k='%s:%s' % (res1, atm1)
            num1 = numMap[k]
            base1 = baseMap[k]
            
            res2 = ls[10]
            atm2 = ls[13]
            k='%s:%s' % (res2, atm2)
            num2 = numMap[k]
            base2 = baseMap[k]
            
            res3 = ls[17];
            atm3 = ls[20];
            k='%s:%s' % (res3, atm3)
            num3 = numMap[k]
            base3 = baseMap[k]
            
            res4 = ls[24];
            atm4 = ls[27];
            k='%s:%s' % (res4, atm4)
            num4 = numMap[k]
            base4 = baseMap[k]
            
            up = float(ls[30]) + float(ls[31])
            dn = float(ls[30]) - float(ls[31])
            
            out.append("#\n#  (%s %s %s) - (%s %s %s) - " % (res1, base1, atm1, res2, base2, atm2))
            out.append("(%s %s %s) - (%s %s %s)\n" % (res3, base3, atm3, res4, base4, atm4))
            out.append(" &rst iat=  %s, %s, %s, %s, \n" % (num1, num2, num3, num4))
            out.append(" r1= %3.1f, r2= %3.1f, r3= %3.1f, r4= %3.1f,\n" % (dn - 10, dn, up, up + 10))
            out.append(" rk2= 10.00, rk3= 10.00, ir6=1, &end\n")
    return out

