#!/usr/bin/env python

from pylons import config, session
import os
import sys
from optparse import OptionParser
from lxml import etree
import math

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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

def findProt(resi,atm):
    rr = []
    rr.append("GLY:HA:1")
    rr.append("ALA:HB:3")
    rr.append("SER:HB:2")
    rr.append("VAL:HG1:3")
    rr.append("VAL:HG2:3")
    rr.append("VAL:HB:2")   
    rr.append("ASN:HB:2")
    rr.append("ASN:HD2:2")
    rr.append("GLN:HB:2")
    rr.append("GLN:HE2:2")
    rr.append("GLN:HG:2")
    rr.append("PRO:HB:2")
    rr.append("PRO:HD:2")
    rr.append("PRO:HG:2")
    rr.append("GLU:HB:2")
    rr.append("GLU:HG:2")
    rr.append("ASP:HB:2")
    rr.append("LEU:HB:2")
    rr.append("LEU:HD1:3")
    rr.append("LEU:HD2:3")
    rr.append("ILE:HD:3")
    rr.append("ILE:HG1:2")
    rr.append("ILE:HG2:3")
    rr.append("HIS:HB:2")
    rr.append("HID:HB:2")
    rr.append("HIE:HB:2")
    rr.append("MET:HB:2")
    rr.append("MET:HG:2")
    rr.append("MET:HE:3")
    rr.append("CYS:HB:2")
    rr.append("PHE:HB:2")
    rr.append("TYR:HB:2")
    rr.append("TRP:HB:2")
    rr.append("THR:HG2:3")
    rr.append("THR:HB:2")
    rr.append("LYS:HB:2")
    rr.append("LYS:HG:2")
    rr.append("LYS:HD:2")
    rr.append("LYS:HE:2")
    rr.append("LYS:HZ:3")
    rr.append("ARG:HB:2")
    rr.append("ARG:HG:2")
    rr.append("ARG:HD:2")
    rr.append("ARG:HH1:2")
    rr.append("ARG:HH2:2")
    rr.append("ARG:NH:1")
    ret = ""
    for i in rr:
        rrs = i.split(":")
        #print atm[0:-1]
        #print i
        if rrs[0] == resi and (atm[0:-1] in rrs[1] or atm[1:] in rrs[1]):
            ret = rrs[2]
        else:
            ret = "1"
    return ret

def convert(xml_pcs, ini_num, pdb_out, pdb_ref_n, tolerance, mb):  
    lpdb = open(pdb_out, 'r').readlines()
    out = []
    numMap = {}
    resMap = {}
    resnum = []
    resnumall = []
    nocorr = True
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
        
    pcs_list = []
    
    rxml = etree.Element("status_pcs")
    
    for elt in xml_pcs.getiterator():
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
                                
                    if elt1.tag == "val_pcs":
                        pcs_val = elt1.text
                    if elt1.tag == "molatm":
                        molatm = elt1.text
                    else:
                        molatm = "1"
                        
                    if elt1.tag == "tol":
                        tol = elt1.text
                    
                    if elt1.tag == "weight":
                        weight = elt1.text
                    else:
                        weight = "1.0"
                
                res1 = str(int(res1) - int(ini_num) + 1 )  
                print "----------------------------------------------------------------------------------------"
                print "Cerco %s %s " %(res1, atm1)
                # controllo il multiassegnamento
                
                num1 = ""
                num2 = ""
                base1 = ""
                base2 = ""
                
                igr1 = ""
                igr2 = ""
                nigr1 = ""
                nigr2 = ""
                atm1c = ""
                atm2c = ""
                tr_atm = 0
                res_name = ""
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
                    else:
                        print "####################################################################################################################"
                        print "errore %s" %k1
                        num1 = 'XXX'
                        etree.SubElement(rxml, "Res1_not_found").text = "Res1 %s Atom1 %s " %(res1, atm1)
                        
                    if k1 in resMap: 
                        base1 = resMap[k1]
                    else:
                        print "errore %s" %k1
                        base1 = 'XXX'
                        etree.SubElement(rxml, "Atom1_not_found").text = "Res1 %s Atom1 %s " %(res1, atm1)
                                                             
                    print "NUM1"
                    print num1
                    print base1
                    
                    #res1 = str(int(res1) - int(ini_num) + 1 )
                
                    if num1 != "XXX":
                        if is_number(tolerance):
                            tol = tolerance
                        if len(atm1c) == 1 :
                            out.append("%4d XXX  %s   %9.3f    %2d%6.2f%10.3f\n" %(int(res1), atm1c, float(pcs_val), int(molatm), float(tol), float(weight)))
                        else:
                            out.append("%4d XXX  %-3s %9.3f    %2d%6.2f%10.3f\n" %(int(res1), atm1c, float(pcs_val), int(molatm), float(tol), float(weight)))
    for i in out:
        print i[:-1]
        
    return etree.tostring(rxml, pretty_print=True), out
        
def convert_fin(xml_pcs, pdb_out, pdb_ref_n):
    
    file = ""
    ini_num_v = 1
    for elt in xml_pcs.getiterator():
        if elt.tag == "pcs":
            file = elt.get("filename") + "_final.xml"
            ini_num_v = int(elt.get("number"))
            
    lpdb = open(pdb_out, 'r').readlines()
    out = []
    numMap = {}
    resMap = {}
    resnum = []
    resnumall = []
    nocorr = True
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
 
    print "REF"
    for i in ref:
        print i.replace("\n","").split()
        
    pcs_list = []
    
    rxml = etree.Element("status_pcs")
    
    tot_out = []
    
    out = []
    print file
    f_xml = etree.parse(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), file))
    print "######################"
    print f_xml
    for elt in f_xml.getiterator():
            
            if elt.tag == "metal":
                metal = elt.text
            if elt.tag == "euler":
                theta = elt.get("theta")
                phi = elt.get("phi")
                omega = elt.get("omega")
            if elt.tag == "aniso":
                a1 = elt.get("dchiax")
                a2 = elt.get("dchirh")
                
            if elt.tag == "selection":
                for elt1 in elt.getiterator():       
                    if elt1.tag == "sel1":
                        for elt2 in elt1.getiterator():
                            if elt2.tag == "resid":
                                res1 = str(int(elt2.text) - int(ini_num_v) + 1) 
                            if elt2.tag == "name":
                                atm1 = elt2.text
                    
                    if elt1.tag == "val_pcs":
                        pcs_val = elt1.text
                    if elt1.tag == "tol":
                        tol = elt1.text

                print "----------------------------------------------------------------------------------------"
                print "Cerco %s %s " %(res1, atm1)
                # controllo il multiassegnamento
                
                num1 = ""
                
                base1 = ""
                 
                igr1 = ""
                
                nigr1 = ""
                atm1c = ""
                atm2c = ""
                
                tr_atm = 0
                res_name = ""
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
                    mltprot = findProt(res_name, atm1)        
                    print res1
                    print atm1                        
                    
                    k1 = '%s:%s' % (res1, atm1c)
                    
                    

                    print k1
                    
                    if k1 in numMap:
                        num1 = numMap[k1]
                    else:
                        print "errore %s" %k1
                        num1 = 'XXX'
                        etree.SubElement(rxml, "Res1_not_found").text = "Res1 %s Atom1 %s  " %(res1, atm1)
                        
                    if k1 in resMap: 
                        base1 = resMap[k1]
                    else:
                        print "errore %s" %k1
                        base1 = 'XXX'
                        etree.SubElement(rxml, "Atom1_not_found").text = "Res1 %s Atom1 %s  " %(res1, atm1)
                                                               
                    print "NUM1"
                    print num1
                    print base1
                    
                    if num1 != "XXX"  :
                        tot_out.append("%s %s %s %s %s" % (num1, atm1, pcs_val, tol, mltprot ))

    print tot_out
    print len(tot_out)
    
    tot_pcs = 0
    fin_out = []
    nu_pcs = 0
    num_datasets = 0
    loc_out = []
    for i in tot_out:
        tot_pcs += 1    
        s_spl=i.split()
        num1  = s_spl[0]
        pcs_val = s_spl[2]
        tol   = s_spl[3]
        mltprot = s_spl[4]
        #dobsl = float(pcs_val) + float(tol)/2.0
        #dobsu = float(pcs_val) - float(tol)/2.0
        #iprot(1)=27, obs(1)=-0.140, wt(1)=0.150, tolpro(1)=.500, mltpro(1)=1
        loc_out.append("  iprot(%d)=%s, obs(%d)=%s, wt(%d)=%s, tolpro(%d)=%s, mltpro(%d)=%s, \n" %(tot_pcs, num1, tot_pcs, pcs_val, tot_pcs, "1.0", tot_pcs, tol, tot_pcs, mltprot ))

    print len(loc_out)
    final_out = []
    final_out.append(" &pcshf \n")
    final_out.append("  nmpmc='%s', \n"%metal[0:3]) 
    final_out.append("  nprot=%d, \n" %tot_pcs )
    final_out.append("  optkon=30, \n")
    final_out.append("  nfe=1, \n")
    final_out.append("  opttet(1)=%s, \n" %theta )
    final_out.append("  optphi(1)=%s, \n" %phi )
    final_out.append("  optomg(1)=%s, \n" %omega )
    final_out.append("  opta1(1)=%s, \n" %a1)
    final_out.append("  opta2(1)=%s, \n" %a2)
    final_out.extend(loc_out)
    final_out.append(" &end \n")
    #for i in final_out:
    #    print i
    open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "PCS.in"),"w").writelines(final_out) 
    return etree.tostring(rxml, pretty_print=True), out
