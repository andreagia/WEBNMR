#!/usr/bin/env python
'''
This program attempts to convert XPLOR restraints into AMBER restraints.

XPLOR:
assign  (resid  1 and  name  HA )(resid  2  and name  HD1  ) 2.40  0.60  0.60
assign  (resid  1 and  name  HA )(resid  2  and name  HD2  ) 2.90  1.10  1.10

AMBER:
#  1 GUA H2'1  1 GUA H8        5.50
 &rst iat=  29, 13, r3= 3.663, r4= 4.163,
 r1= 1.300, r2= 1.800, r3= 3.663, r4= 4.163,
 rk2= 0.00, rk3= 32.000, &end

'''


import os
import sys
from optparse import OptionParser
from lxml import etree
import math
import pprint

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
            

def convert(xml_noe, ini_num, pdb_out, pdb_ref_n, nocorr):
    if xml_noe.find("lol").text == "True":
        lol = True
    else:
        lol = False
    std_aa = ["GLY","ALA","SER", "VAL", "THR", "ASN", "GLN", "PRO", "GLU", "ASP", "LEU", "ILE", "HIS", "HIP", "HID", "HIE", "MET", "CYS", "CYX", "PHE", "TYR", "TRP", "LYS", "ARG"]
    
    print "#### lpdb ", pdb_out
    lpdb = open(pdb_out, 'r').readlines()
    out = []
    numMap = {}
    resMap = {}
    resnum = []
    resnumall = []
    print "############ NOCORR ##################"
    print nocorr
    print "######################################"    
    res_num_corr = int(ini_num) - 1
    #nocorr = True
    #for l in lpdb:
    #    if l.startswith('ATOM'):
    #        #k <- resid number : atom name 
    #        k='%s:%s' % (l[22:26], l[12:17].replace(" ",""))
    #        numMap[k] = l[6:11]
    #        resMap[k] = l[17:21].replace(" ","")
    mapres = {}
    rnadna = []
    rnadna.append("DA5")
    rnadna.append("DA")
    rnadna.append("DA3")
    rnadna.append("DAN")
    rnadna.append("RA5")
    rnadna.append("RA3")
    rnadna.append("RA")
    rnadna.append("RAN")
    rnadna.append("DT5")
    rnadna.append("DT")
    rnadna.append("DT3")
    rnadna.append("DTN")
    rnadna.append("RU5")
    rnadna.append("RU")
    rnadna.append("RU3")
    rnadna.append("RUN")
    rnadna.append("DG5")
    rnadna.append("DG")
    rnadna.append("DG3")
    rnadna.append("DGN")
    rnadna.append("RG5")
    rnadna.append("RG")
    rnadna.append("RG3")
    rnadna.append("RGN")
    rnadna.append("DC5")
    rnadna.append("DC")
    rnadna.append("DC3")
    rnadna.append("DCN")
    rnadna.append("RC5")
    rnadna.append("RC")
    rnadna.append("RC3")
    rnadna.append("RCN")
    for l in lpdb:
        if l.strip().startswith('ATOM'):
            ls=l.split()
            k='%s:%s' % (ls[4],ls[2])
            if ls[3] in rnadna:
                print "Residue DNA RNA"
                if "*" in ls[2] or ls[2][0].isdigit():
                    newda = ls[2].replace("*","'")
                    if newda[0].isdigit():
                        newda = newda[1:] + newda[0]
                    k='%s:%s' % (ls[4],newda)
                
                
            #numMap["numero_residuo: numero_atomo" ] = nome_atomo
            numMap[k] = ls[1]
            #resMap["numero_residuo: numero_atomo"] = nome_residuo
            resMap[k] = ls[3]
            #resnumall -> numero_residuo nome_residuo
            resnumall.append('%s %s' %(ls[4], ls[3]))
            
            mapres[str(int(ls[4]))] = ls[3]
            
            #pdb_ref -> numero_residuo nome_atomo_prima_della_coversione nome_atomo_dopo_della_coversione
    print "INI############NUMMAP#################"
    for i in numMap:
        print i
    print "END############NUMMAP###################"
    print "###########MAPRES##########"
    print mapres
    print "###########################"
    print "PDB_REF_N"
    print pdb_ref_n
    lref = open(pdb_ref_n, 'r').readlines()
    set = {}
    ref = [set.setdefault(ek,ek) for ek in lref if ek not in set]
    set = {}
    resnum = [set.setdefault(ek,ek) for ek in resnumall if ek not in set]
    #print 'REFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf'
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
    
    rxml = etree.Element("status_noe")
    for elt in xml_noe.getiterator():
            if elt.tag == "selection":
                for elt1 in elt.getiterator():
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
                    if elt1.tag == "D":
                        d = elt1.text
                    if elt1.tag == "D_minus":
                        dm = elt1.text
                    if elt1.tag == "D_plus":
                        dp = elt1.text
                d = float(d)
                dp = float(dp)
                dm = float(dm)
                #correction of residues ini_num

                res1 = str(int(res1) - res_num_corr )
                res2 = str(int(res2) - res_num_corr )
                
                print "NOE da xml " + res1 + " " + atm1 + " " + res2 + " " + atm2 + " numero sottratto " + str(res_num_corr)
                # modifico per Val gli atomi HG# -> CB
                
                if atm1 == "H$" and (res1 in mapres.keys() ):
                    if mapres[res1] == "TYR" or mapres[res1] == "PHE":
                        atm1 = "H%"
                        
                if atm1 == "HG#" and (res1 in mapres.keys() ):
                    if mapres[res1] == "VAL":
                        atm1 = "CB"
                    vl1 = 2.2
                elif atm1 == "HD#" and (res1 in mapres.keys()):
                    if mapres[res1] == "LEU":
                        atm1 = "CG"
                        print " modifico per Leu gli atomi HD# -> CG"
                    vl1 = 2.2
                elif atm1[0] == "Q" and atm1[1] == "Q":
                    if mapres[res1] == "LEU":
                        atm1 = "CG"
                    if mapres[res1] == "VAL":
                        atm1 = "CB"
                    vl1 = 2.2
                else:
                    vl1 = 0.0

                if atm2 == "H$" and (res2 in mapres.keys() ):
                    if mapres[res2] == "TYR" or mapres[res2] == "PHE":
                        atm2 = "H%"
                        
                if atm2 == "HG#" and (res2 in mapres.keys() ):
                    if mapres[res2] == "VAL":
                        atm2 = "CB"
                    vl2 = 2.2
                elif atm2 == "HD#" and (res2 in mapres.keys()):
                    if mapres[res2] == "LEU":
                        atm2 = "CG"
                        print " modifico per Leu gli atomi HD# -> CG"                       
                    vl2 = 2.2
                # modifico per Val e Leu gli atomi QQ*
                elif atm2[0] == "Q" and atm2[1] == "Q":
                    if mapres[res2] == "LEU":
                        atm2 = "CG"
                    if mapres[res2] == "VAL":
                        atm2 = "CB"
                    vl2 = 2.2
                else:
                    vl2 = 0.0
                    
 
                        
                print "----------------------------------------------------------------------------------------"
                print "Cerco %s %s %s %s " %(res1, atm1, res2, atm2)
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
                atm1c = ""
                atm2c = ""
                if not atm1.endswith('#'):
                    print "ATM1 " + atm1
                    for at in resnum:                       
                        if res1 == at.split()[0]:
                            for atr in ref:
                                
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
                        
                    elif res_name not in std_aa and (atm1[0] == "H" and atm1[-1].isdigit() ):
                        atm1c = atm1[-1] + atm1[:-1]
                        k1 = '%s:%s' % (res1, atm1c)
                        if k1 in numMap:
                            num1 = numMap[k1]
                        else:
                            print "####################################################################################################################"
                            print "errore numMap %s" %k1
                            num1 = 'XXX'
                            etree.SubElement(rxml, "Res1_not_found").text = "Res1 %s Atom1 %s Res2 %6s Atom2 %s Distances %6s %6s %6s" %(res1, atm1, res2, atm2, d, dm, dp) 
                    else:
                        print "####################################################################################################################"
                        print "errore numMap %s" %k1
                        num1 = 'XXX'
                        etree.SubElement(rxml, "Res1_not_found").text = "Res1 %s Atom1 %s Res2 %6s Atom2 %s Distances %6s %6s %6s" %(res1, atm1, res2, atm2, d, dm, dp)
                        
                    if k1 in resMap: 
                        base1 = resMap[k1]
                    else:
                        print "errore resMap%s" %k1
                        base1 = 'XXX'
                        etree.SubElement(rxml, "Atom1_not_found").text = "Res1 %s Atom1 %s Res2 %s Atom2 %s Distances %6s %6s %6s" %(res1, atm1, res2, atm2, d, dm, dp)
                                            
                    
                    print "NUM1"
                    print num1
                    print base1
                
                if  atm1.endswith('#') or atm1.endswith('%'):
                    if atm1.endswith('#'):
                        print "ATM#1 " + atm1
                        nall1 = []
                        nall1.append(atm1[:-1].strip() + '1')
                        nall1.append(atm1[:-1].strip() + '2')
                        nall1.append(atm1[:-1].strip() + '3')
                        nall1.append('1' + atm1[:-1].strip())
                        nall1.append('2' + atm1[:-1].strip())
                        nall1.append('3' + atm1[:-1].strip())
                    if atm1.endswith('%'):
                        print "ATM#1 " + atm1
                        nall1 = []
                        nall1.append('HE1')
                        nall1.append('HE2')
                        nall1.append('HD1')
                        nall1.append('HD2')
                        nall1.append('1HE')
                        nall1.append('2HE')
                        nall1.append('1HD')
                        nall1.append('2HD')


                    # the VAL QB are HB
                    #nall1.append(atm1[:-1].strip())
                    
                    nallt1 =[]
                    #solo per AA standard
                    if res_name in std_aa:
                        for ik in nall1:
                            for at in resnum:                       
                                if res1 == at.split()[0]:
                                    for atr in ref:
                                        
                                        if ( ik == atr.split()[1] ) and (at.split()[1] == atr.split()[0] ):
                                            print "Trovato " + atr.split()[2] + " Convertito da " + atm1
                                            nallt1.append(atr.split()[2])
                        print "NALLLLLLLLLLLLLLLLNALLLLLLLLLLLLLLLLLLLLLNALLLLLLLLLLLLLLLLLLLLLLNALLLLLLLLLLLLLLLLLL"
                    else:
                        # se non ho un AA standard cerco le possibili coppie numero nome nome numero nel file di amber 
                        for at in numMap:
                            if res1 == at.split(":")[0] and at.split(":")[1]  in nall1:
                                print "Trovato " + at.split(":")[1]
                                nallt1.append(at.split(":")[1])
                        
                    print nallt1
                    igr1 = ""
                    nigr1 = ''
                    if len(nallt1) > 0:
                        k1 = '%s:%s' % (res1, nallt1[0])
                    else:
                        k1 = 'NO:NO'
                        
                    if k1 in resMap: 
                        nigr1 = resMap[k1] + " "
                    else:
                        print "errore resMap %s" %k1
                        base1 = 'XXX'
                        etree.SubElement(rxml, "Atom1_not_found").text = "Res1 %s Atom1 %s Res2 %s Atom2 %s Distances %6s %6s %6s" %(res1, atm1, res2, atm2, d, dm, dp)
                        
                    for ik in nallt1:
                        k1 = '%s:%s' % (res1, ik)
                        print k1
                        if k1 in numMap :
                            igr1 = igr1 + numMap[k1]+ ", "
                            nigr1 = nigr1 + ik + " "
                        else:
                            print "errore numMap %s" %k1
                            igr1.join("XXX, ")
                            etree.SubElement(rxml, "Res1_not_found").text = "Res1 %s Atom1 %s Res2 %6s Atom2 %s Distances %6s %6s %6s" %(res1, atm1, res2, atm2, d, dm, dp)
                    
                    print "IGR1"
                    print igr1
                    print nigr1
                    
                tr_atm = 0
                res_name = ""
                if not atm2.endswith('#'):
                    print "ATM2 " + atm2
                    for at in resnum:
                        if res2 == at.split()[0]:
                            for atr in ref:
                                
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
                    elif res_name not in std_aa and (atm2[0] == "H" and atm2[-1].isdigit() ):
                        atm2c = atm2[-1] + atm2[:-1]
                        k2 = '%s:%s' % (res2, atm2c)
                        if k2 in numMap:
                            num1 = numMap[k2]
                        else:
                            print "####################################################################################################################"
                            print "errore numMap %s" %k2
                            num1 = 'XXX'
                            etree.SubElement(rxml, "Res1_not_found").text = "Res1 %s Atom1 %s Res2 %6s Atom2 %s Distances %6s %6s %6s" %(res1, atm1, res2, atm2, d, dm, dp)
                    else:
                        print"**************************************************************************************************"
                        print "errore %s" %k2
                        num2 = 'XXX'
                        etree.SubElement(rxml, "Res2_not_found").text = "Res1 %s Atom1 %s Res2 %s Atom2 %s Distances %6s %6s %6s" %(res1, atm1, res2, atm2, d, dm, dp)
                        
                    if k2 in resMap:                    
                        base2 = resMap[k2]
                    else:
                        print "errore %s" %k2
                        base2 = 'XXX'
                        etree.SubElement(rxml, "Atom2_not_found").text = "Res1 %s Atom1 %s Res2 %s Atom2 %s Distances %6s %6s %6s" %(res1, atm1, res2, atm2, d, dm, dp)
                    
                    print "NUM2"
                    print num2
                    print base2
                    
                    
                if  atm2.endswith('#') or atm2.endswith('%') :
                    if atm2.endswith('#'):
                        print "ATM#2 " + atm2
                        nall2 = []
                        nall2.append(atm2[:-1].strip() + '1')
                        nall2.append(atm2[:-1].strip() + '2')
                        nall2.append(atm2[:-1].strip() + '3')
                        nall2.append('1' + atm2[:-1].strip())
                        nall2.append('2' + atm2[:-1].strip())
                        nall2.append('3' + atm2[:-1].strip())
                    if atm2.endswith('%'):
                        print "ATM#2 " + atm2
                        nall2 = []
                        nall2.append('HE1')
                        nall2.append('HE2')
                        nall2.append('HD1')
                        nall2.append('HD2')
                        nall2.append('1HE')
                        nall2.append('2HE')
                        nall2.append('1HD')
                        nall2.append('2HD')
                    
                    ## the VAL QB are HB
                    #nall2.append(atm2[:-1].strip())
                    
                    print nall2
                    nallt2 = []
                    #solo per AA standard
                    if res_name in std_aa:
                        for ik in nall2:
                            for at in resnum:                       
                                if res2 == at.split()[0]:
                                    for atr in ref:
                                        #print ik + " " + atr.split()[1] + "  " + at.split()[1] + "  " + atr.split()[0]
                                        if ( ik == atr.split()[1] ) and (at.split()[1] == atr.split()[0] ):
                                            print "Trovato " + atr.split()[2] + " Convertito da " + atm2
                                            nallt2.append(atr.split()[2])
                        print "NALLLLLLLLLLLLLLLLNALLLLLLLLLLLLLLLLLLLLLNALLLLLLLLLLLLLLLLLLLLLLNALLLLLLLLLLLLLLLLLL"
                    else:
                        # se non ho un AA standard cerco le possibili coppie numero nome nome numero nel file di amber 
                        for at in numMap:
                            if res2 == at.split(":")[0] and at.split(":")[1]  in nall2:
                                print "Trovato " + at.split(":")[1]
                                nallt2.append(at.split(":")[1])
                                
                    print nallt2
                    igr2 = ""
                    nigr2 = ''
                    if len(nallt2) > 0:
                        k2 = '%s:%s' % (res2, nallt2[0])
                    else:
                        k2 = 'NO:NO'
                        
                    if k2 in resMap: 
                        nigr2 = resMap[k2] + " "
                    else:
                        print "errore %s" %k2
                        base2 = 'XXX'
                        etree.SubElement(rxml, "Atom2_not_found").text = "Res1 %s Atom1 %s Res2 %s Atom2 %s Distances %6s %6s %6s" %(res1, atm1, res2, atm2, d, dm, dp)
                    for ik in nallt2:
                        k2 = '%s:%s' % (res2, ik)
                        print k2
                        if k2 in numMap :
                            igr2 = igr2 + numMap[k2]+ ", "
                            nigr2 = nigr2 + ik + " "
                        else:
                            print "errore %s" %k2
                            igr2.join("XXX, ")
                            etree.SubElement(rxml, "Res2_not_found").text = "Res1 %s Atom1 %s Res2 %6s Atom2 %s Distances %6s %6s %6s" %(res1, atm1, res2, atm2, d, dm, dp)
                    print "IGR2"
                    print igr2
                    print nigr2
                    
                #if nocorr == False:
                #    out.append("#NOCORR = FALSE")
                    
                d_cor = d
                
                if (len(igr1) > 0 and len(igr2) >0 ):
                    if nocorr == False:
                        
                        if vl1 > 0:
                            d =   d * math.exp(math.log(float((len(igr2.split(","))-1)))/6.0) + vl1
                            dp = dp * math.exp(math.log(float((len(igr2.split(","))-1)))/6.0) + vl1
                            dm = dm * math.exp(math.log(float((len(igr2.split(","))-1)))/6.0) + vl1
                            
                        elif vl2 > 0:
                            d =   d * math.exp(math.log(float((len(igr1.split(","))-1)))/6.0) + vl2
                            dp = dp * math.exp(math.log(float((len(igr1.split(","))-1)))/6.0) + vl2
                            dm = dm * math.exp(math.log(float((len(igr1.split(","))-1)))/6.0) + vl2
                        
                        else:   
                            d =   d * math.exp(math.log((float((len(igr2.split(","))-1)*float((len(igr1.split(","))-1)))))/6.0)
                            dp = dp * math.exp(math.log((float((len(igr2.split(","))-1)*float((len(igr1.split(","))-1)))))/6.0)
                            dm = dm * math.exp(math.log((float((len(igr2.split(","))-1)*float((len(igr1.split(","))-1)))))/6.0) 
                            
                    if lol:
                        dn = d
                        up = d + 100.0
                        mark_l = "LOL"
                    else:
                        up = d + dp
                        dn = d - dm
                        mark_l = ""
                        
                    if (igr2 != 'XXX') and (nigr2 != 'XXX') and (nigr1 != 'XXX') and (igr1 != 'XXX'):
                        out.append("#\n#  %s %s   %s %s %2.2f %s \n" % (res1, nigr1, res2, nigr2, float(d_cor), mark_l))
                        out.append(" &rst iat= -1, -1,")
                        out.append(" r1= %2.2f, r2= %2.2f, r3= %2.2f, r4= %2.2f,\n" % (dn - 0.5, dn, up, up + 0.5))
                        out.append(" igr1= %s "%igr1)
                        out.append(" igr2= %s "%igr2)
                        #out.append(" ir6=1, &end\n")
                        out.append(" rk2= 0.00, rk3= 50.000, ir6=1, &end\n")
                        
                if  len(num1) > 0 and len(igr2 ) > 0 :
                    if nocorr == False:
                        if vl1 > 0:
                            d =   d * math.exp(math.log(float((len(igr2.split(","))-1)))/6.0) + vl1
                            dp = dp * math.exp(math.log(float((len(igr2.split(","))-1)))/6.0) + vl1
                            dm = dm * math.exp(math.log(float((len(igr2.split(","))-1)))/6.0) + vl1
                        else:
                            d =   d * math.exp(math.log(float((len(igr2.split(","))-1)))/6.0)
                            dp = dp * math.exp(math.log(float((len(igr2.split(","))-1)))/6.0)
                            dm = dm * math.exp(math.log(float((len(igr2.split(","))-1)))/6.0)  
                            
                    if lol:
                        dn = d
                        up = d + 100.0
                        mark_l = "LOL"
                    else:
                        up = d + dp
                        dn = d - dm
                        mark_l = ""
                        
                    if (igr2 != 'XXX') and (num1 != 'XXX') and (nigr2 != 'XXX') and (base1 != 'XXX'):
                        out.append("#\n#  %s %s   %s %s %s %2.2f %s\n" % (res2, nigr2, res1, base1, atm1, float(d_cor), mark_l))
                        out.append(" &rst iat= %s, -1,"%num1)
                        out.append(" r1= %2.2f, r2= %2.2f, r3= %2.2f, r4= %2.2f,\n" % (dn - 0.5, dn, up, up + 0.5))
                        out.append(" igr1= 0, ")
                        out.append(" igr2= %s " % igr2)
                        #out.append(" ir6=1, &end\n")
                        out.append(" rk2= 0.00, rk3= 50.000, ir6=1, &end\n")
                        
                if ( len(num2) > 0 and len(igr1 ) >0 ) :
                    if nocorr == False:
                        if vl2 > 0:
                            d =   d * math.exp(math.log(float((len(igr1.split(","))-1)))/6.0) + vl2
                            dp = dp * math.exp(math.log(float((len(igr1.split(","))-1)))/6.0) + vl2
                            dm = dm * math.exp(math.log(float((len(igr1.split(","))-1)))/6.0) + vl2
                        else:
                            d =   d * math.exp(math.log(float((len(igr1.split(","))-1)))/6.0)
                            dp = dp * math.exp(math.log(float((len(igr1.split(","))-1)))/6.0)
                            dm = dm * math.exp(math.log(float((len(igr1.split(","))-1)))/6.0)
                            
                    if lol:
                        dn = d
                        up = d + 100.0
                        mark_l = "LOL"
                    else:
                        up = d + dp
                        dn = d - dm
                        mark_l = ""
                        
                    if (igr1 != 'XXX') and (num2 != 'XXX') and (nigr1 != 'XXX') and (base2 != 'XXX'):
                        out.append("#\n#  %s %s   %s %s %s %2.2f %s\n" % (res1, nigr1, res2, base2, atm2, float(d_cor), mark_l))
                        out.append(" &rst iat= -1, %s,"%num2)
                        out.append(" r1= %2.2f, r2= %2.2f, r3= %2.2f, r4= %2.2f,\n" % (dn - 0.5, dn, up, up + 0.5))
                        out.append(" igr1= %s "%igr1)
                        out.append(" igr2= 0,")
                        #out.append(" ir6=1, &end\n")
                        out.append(" rk2= 0.00, rk3= 50.000, ir6=1, &end\n")
                    
                if len(num1) > 0 and len(num2) > 0:
                    if nocorr == False:
                        print "VL1"
                        print vl1
                        print "VL2"
                        print vl2
                        if vl1 > 0 and vl2 > 0:
                                d =   d  + vl1 + vl2
                                dp = dp  + vl1 + vl2
                                dm = dm  + vl1 + vl2
                                
                        elif  vl1 > 0:
                                d =   d  + vl1 
                                dp = dp  + vl1 
                                dm = dm  + vl1
                                
                        elif  vl2 > 0:
                                d =   d  + vl2 
                                dp = dp  + vl2 
                                dm = dm  + vl2
                        
                    #if lol 
                    if lol:
                        dn = d
                        up = d + 100.0
                        mark_l = "LOL"
                    else:
                        up = d + dp
                        dn = d - dm
                        mark_l = ""
                        
                    if (num1 != 'XXX') and (num2 != 'XXX') and (base1 != 'XXX') and (base2 != 'XXX'):
                        out.append("#\n#  %s %s %s  %s %s %s %2.2f %s\n" % (res1, base1, atm1, res2, base2, atm2, float(d_cor), mark_l))
                        out.append(" &rst iat=  %s, %s, r1= %2.2f, r2= %2.2f,\n" % (num1, num2, dn - 0.5, dn))
                        out.append(" r3= %2.2f, r4= %2.2f,\n" % (up, up + 0.5))
                        #out.append(" ir6=1, &end\n")
                        out.append(" rk2= 0.00, rk3= 50.00, ir6=1, &end\n")      
                        noe_list.append("Res1 %6s Atom1 %5s Res1 %6s Atom2%5s Distances %6s %6s %6s" %(res1, atm1, res2, atm2, d, dm, dp))
    for i in out:
        print i[:-1]
    print "INI ###################### atomi non convertiti nei NOE ##########################"
    print etree.tostring(rxml, pretty_print=True)
    print "END ######################atomi non convertiti nei NOE ##########################"
    return etree.tostring(rxml, pretty_print=True), out

    #return out
        
