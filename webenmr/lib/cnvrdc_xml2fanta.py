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

def convert(xml_rdc, ini_num, pdb_out, pdb_ref_n, tolerance, mb):  
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
        
    rdc_list = []
    
    rxml = etree.Element("status_rdc")
    
    for elt in xml_rdc.getiterator():
        if elt.tag == "selection":
            for elt1 in elt.getiterator():
                
                if elt1.tag == "cyana":
                    name_ang = alt1.get("angle")
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
                            
                if elt1.tag == "val_rdc":
                    rdc_val = elt1.text
                if elt1.tag == "tol":
                    tol = elt1.text
                if elt1.tag == "weight":
                    weight = elt1.text
                else:
                    weight = "1.0"
                if elt1.tag == "point":
                    point = elt1.text
                else:
                    point = "1"
            
            res1 = str(int(res1) - int(ini_num) + 1 )
            res2 = str(int(res2) - int(ini_num) + 1 )      
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
                    print "errore %s" %k1
                    num1 = 'XXX'
                    etree.SubElement(rxml, "Res1_not_found").text = "Res1 %s Atom1 %s Res2 %6s Atom2 %s " %(res1, atm1, res2, atm2)
                    
                if k1 in resMap: 
                    base1 = resMap[k1]
                else:
                    print "errore %s" %k1
                    base1 = 'XXX'
                    etree.SubElement(rxml, "Atom1_not_found").text = "Res1 %s Atom1 %s Res2 %s Atom2 %s" %(res1, atm1, res2, atm2)
                  
                print "NUM1"
                print num1
                print base1
               
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
                else:
                    print"**************************************************************************************************"
                    print "errore %s" %k2
                    num2 = 'XXX'
                    etree.SubElement(rxml, "Res2_not_found").text = "Res1 %s Atom1 %s Res2 %s Atom2 %s" %(res1, atm1, res2, atm2)
                    
                if k2 in resMap:                    
                    base2 = resMap[k2]
                else:
                    print "errore %s" %k2
                    base2 = 'XXX'
                    etree.SubElement(rxml, "Atom2_not_found").text = "Res1 %s Atom1 %s Res2 %s Atom2 %s " %(res1, atm1, res2, atm2)
                
                print "NUM2"
                print num2
                print base2
                
                #res1 = str(int(res1) - int(ini_num) + 1 )
                #res2 = str(int(res2) - int(ini_num) + 1 )
                if num1 != "XXX" and num2 != "XXX" :
                    print "TOLERANCE TOLERANCE"
                    print tolerance
                    print "-------------------"
                    if is_number(tolerance):
                        tol = tolerance
                    if len(atm1c) == 1 and len(atm2c) == 1:
                        out.append("%3d  %s  %3d  %s %9.3f    %2d%6.2f%10.3f%4s\n" %(int(res1), atm1c, int(res2), atm2c, float(rdc_val), float(weight), float(tol), float(point),  mb))
                    elif len(atm1c) == 1:
                        out.append("%3d  %s  %3d %3s%9.3f    %2d%6.2f%10.3f%4s\n" %(int(res1), atm1c, int(res2), atm2c, float(rdc_val), float(weight), float(tol), float(point), mb))
                    elif len(atm2c) == 1:
                        out.append("%3d %3s %3d  %s %9.3f    %2d%6.2f%10.3f%4s\n" %(int(res1), atm1c, int(res2), atm2c, float(rdc_val), float(weight), float(tol), float(point), mb))
                    else:
                        out.append("%3d %3s %3d %3s%9.3f    %2d%6.2f%10.3f%4s\n" %(int(res1), atm1c, int(res2), atm2c, float(rdc_val), float(weight), float(tol), float(point), mb))
    for i in out:
        print i[:-1]
        
    return etree.tostring(rxml, pretty_print=True), out
    
def convert_fin(xml_rdc, pdb_out, pdb_ref_n):
    
    info_rdc = {}
    for elt in xml_rdc.getiterator():
        if elt.tag == "rdc":
            info_rdc[elt.get("filename") + "_final.xml"] = elt.get("number")
            
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
        
    rdc_list = []
    
    rxml = etree.Element("status_rdc")
    
    tot_out = []
    m_c11 = ""
    m_c12 = ""
    m_c13 = ""
    m_c22 = ""
    m_c23 = ""
    
    for file, ini_num in info_rdc.items():
        print "aggiungo " + ini_num
        out = []
        f_xml = etree.parse(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), file))
        print "######################"
        print file
        for elt in f_xml.getiterator():
            
                if elt.tag == "matrix_rdc":
                    m_c11 += ("%s, " % elt.get("c11"))
                    m_c12 += ("%s, " % elt.get("c12"))
                    m_c13 += ("%s, " % elt.get("c13"))
                    m_c22 += ("%s, " % elt.get("c22"))
                    m_c23 += ("%s, " % elt.get("c23"))
            
                if elt.tag == "selection":
                    for elt1 in elt.getiterator():       
                        if elt1.tag == "sel1":
                            for elt2 in elt1.getiterator():
                                if elt2.tag == "resid":
                                    res1 = str(int(elt2.text) - int(ini_num) + 1)
                                if elt2.tag == "name":
                                    atm1 = elt2.text
                        if elt1.tag == "sel2":
                            for elt2 in elt1.getiterator():
                                if elt2.tag == "resid":
                                    res2 = str(int(elt2.text) - int(ini_num) + 1)
                                if elt2.tag == "name":
                                    atm2 = elt2.text
                                    
                        if elt1.tag == "val_rdc":
                            rdc_val = elt1.text
                        if elt1.tag == "tol":
                            tol = elt1.text
 
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
                            print "errore %s" %k1
                            num1 = 'XXX'
                            etree.SubElement(rxml, "Res1_not_found").text = "Res1 %s Atom1 %s Res2 %6s Atom2 %s " %(res1, atm1, res2, atm2)
                            
                        if k1 in resMap: 
                            base1 = resMap[k1]
                        else:
                            print "errore %s" %k1
                            base1 = 'XXX'
                            etree.SubElement(rxml, "Atom1_not_found").text = "Res1 %s Atom1 %s Res2 %s Atom2 %s " %(res1, atm1, res2, atm2)
                                                
                        
                        print "NUM1"
                        print num1
                        print base1
                    
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
                        else:
                            print"**************************************************************************************************"
                            print "errore %s" %k2
                            num2 = 'XXX'
                            etree.SubElement(rxml, "Res2_not_found").text = "Res1 %s Atom1 %s Res2 %s Atom2 %s " %(res1, atm1, res2, atm2)
                            
                        if k2 in resMap:                    
                            base2 = resMap[k2]
                        else:
                            print "errore %s" %k2
                            base2 = 'XXX'
                            etree.SubElement(rxml, "Atom2_not_found").text = "Res1 %s Atom1 %s Res2 %s Atom2 %s " %(res1, atm1, res2, atm2)
                        
                        print "NUM2"
                        print num2
                        print base2
                        
                        if num1 != "XXX" and num2 != "XXX" :
                            out.append("%s %s %s %s %s %s" % (num1, atm1, num2, atm2, rdc_val, tol))

        tot_out.append(out)
        
    print tot_out
    
    tot_rdc = 0
    fin_out = []
    gigj = ""
    dij = ""
    nu_rdc = 0
    num_datasets = 0
    loc_out = []
    
    for i in tot_out:
        num_datasets += 1
        loc_out.append("  dataset=%d, \n" % num_datasets )
        nu_NH = 0
        v_NH = []
        
        nu_CH = 0
        v_CH = []
        
        nu_PH = 0
        v_PH = []
        
        nu_CN = 0
        v_CN = []

        nu_CC = 0
        v_CC = []
            
        for p in i:
            s_spl=p.split()
            if (s_spl[1][0] == "N" and s_spl[3][0] == "H") or (s_spl[1][0] == "H" and s_spl[3][0] == "N"):
                nu_NH =+ 1
                v_NH.append(p)
                tot_rdc =+ 1
                
            if (s_spl[1][0] == "C" and s_spl[3][0] == "H") or (s_spl[1][0] == "H" and s_spl[3][0] == "C"):
                nu_CH =+ 1
                v_CH.append(p)
                tot_rdc =+ 1
                
            if (s_spl[1][0] == "P" and s_spl[3][0] == "H") or (s_spl[1][0] == "H" and s_spl[3][0] == "P"):
                nu_PH =+ 1
                v_PH.append(p)
                tot_rdc =+ 1
        
            if (s_spl[1][0] == "C" and s_spl[3][0] == "N") or (s_spl[1][0] == "N" and s_spl[3][0] == "C"):
                nu_CN =+ 1
                v_CN.append(p)
                tot_rdc =+ 1        
        
            if (s_spl[1][0] == "C" and s_spl[3][0] == "C"):
                nu_CC =+ 1
                v_CC.append(p)
                tot_rdc =+ 1
        
        if len(v_NH) >0:
            gigj += str(len(v_NH)) + "*-3.1631, "
        for p in v_NH:
            s_spl=p.split()
            num1  = s_spl[0]
            num2  = s_spl[2]
            rdc_val = s_spl[4]
            tol   = s_spl[5]
            dobsl = float(rdc_val) + float(tol)/2.0
            dobsu = float(rdc_val) - float(tol)/2.0
            dobs = float(rdc_val)
    
            nu_rdc += 1
            loc_out.append("  id(%d)=%s, jd(%d)=%s, dobsl(%d)=%3.6f, dobsu(%d)=%3.6f, \n" %(nu_rdc, num1, nu_rdc, num2, nu_rdc, dobsl, nu_rdc, dobsu ))
            #loc_out.append("  id(%d)=%s, jd(%d)=%s, dobs(%d)=%3.6f, \n" %(nu_rdc, num1, nu_rdc, num2, nu_rdc, dobs))

        if len(v_CH) >0:
            gigj += str(len(v_CH)) + "*7.8466, "
        for p in v_CH:
            s_spl=p.split()
            num1  = s_spl[0]
            num2  = s_spl[2]
            rdc_val = s_spl[4]
            tol   = s_spl[5]
            dobsl = float(rdc_val) + float(tol)/2.0
            dobsu = float(rdc_val) - float(tol)/2.0
            dobs = float(rdc_val)
            
            nu_rdc += 1
            loc_out.append("  id(%d)=%s, jd(%d)=%s, dobsl(%d)=%3.6f, dobsu(%d)=%3.6f, \n" %(nu_rdc, num1, nu_rdc, num2, nu_rdc, dobsl, nu_rdc, dobsu))
            #loc_out.append("  id(%d)=%s, jd(%d)=%s, dobs(%d)=%3.6f, \n" %(nu_rdc, num1, nu_rdc, num2, nu_rdc, dobs))

        if len(v_PH) >0:
            gigj += str(len(v_PH)) + "*12.6416, "
        for p in v_PH:
            s_spl=p.split()
            num1  = s_spl[0]
            num2  = s_spl[2]
            rdc_val = s_spl[4]
            tol   = s_spl[5]
            dobsl = float(rdc_val) - float(tol)/2.0
            dobsu = float(rdc_val) + float(tol)/2.0
            dobs = float(rdc_val)
    
            nu_rdc += 1
            loc_out.append("  id(%d)=%s, jd(%d)=%s, dobsl(%d)=%3.6f, dobsu(%d)=%3.6f, \n" %(nu_rdc, num1, nu_rdc, num2, nu_rdc, dobsl, nu_rdc, dobsu))
            #loc_out.append("  id(%d)=%s, jd(%d)=%s, dobs(%d)=%3.6f, \n" %(nu_rdc, num1, nu_rdc, num2, nu_rdc, dobs))

        if len(v_CN) >0:
            gigj += str(len(v_CN)) + "*-0.7955, "
        for p in v_CN:
            s_spl=p.split()
            num1  = s_spl[0]
            num2  = s_spl[2]
            rdc_val = s_spl[4]
            tol   = s_spl[5]
            dobsl = float(rdc_val) - float(tol)/2.0
            dobsu = float(rdc_val) + float(tol)/2.0
            dobs = float(rdc_val)
    
            nu_rdc += 1
            loc_out.append("  id(%d)=%s, jd(%d)=%s, dobsl(%d)=%3.6f, dobsu(%d)=%3.6f, \n" %(nu_rdc, num1, nu_rdc, num2, nu_rdc, dobsl, nu_rdc, dobsu))
            #loc_out.append("  id(%d)=%s, jd(%d)=%s, dobs(%d)=%3.6f, \n" %(nu_rdc, num1, nu_rdc, num2, nu_rdc, dobs))

        if len(v_CC) >0:
            gigj += str(len(v_CC)) + "*1.9734, "
        for p in v_CC:
            s_spl=p.split()
            num1  = s_spl[0]
            num2  = s_spl[2]
            rdc_val = s_spl[4]
            tol   = s_spl[5]
            dobsl = float(rdc_val) - float(tol)/2.0
            dobsu = float(rdc_val) + float(tol)/2.0
            dobs = float(rdc_val)
    
            nu_rdc += 1
            loc_out.append("  id(%d)=%s, jd(%d)=%s, dobsl(%d)=%3.6f, dobsu(%d)=%3.6f, \n" %(nu_rdc, num1, nu_rdc, num2, nu_rdc, dobsl, nu_rdc, dobsu))
            #loc_out.append("  id(%d)=%s, jd(%d)=%s, dobs(%d)=%3.6f, \n" %(nu_rdc, num1, nu_rdc, num2, nu_rdc, dobs))
            
    print gigj
    
    for i in loc_out:
        print i
    final_out = []
    final_out.append(" &align \n")
    final_out.append("  num_datasets=%d, \n" %num_datasets )
    final_out.append("  ndip=%d,dwt=%d*0.1, \n" %(nu_rdc, nu_rdc) )
    final_out.append("  gigj=%s \n" %gigj )
    final_out.append("  freezemol=.true., \n")
    final_out.append("  s11=%s s12=%s s13=%s s22=%s s23=%s \n" %("0.0", "0.0", "0.0", "0.0", "0.0") )
    #final_out.append("  s11=%s s12=%s s13=%s s22=%s s23=%s \n" %(m_c11, m_c12, m_c13, m_c22, m_c23) )
    final_out.extend(loc_out)
    final_out.append(" &end \n")
    #for i in final_out:
    #    print i
    open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "allRDC.in"),"w").writelines(final_out)
    
    return etree.tostring(rxml, pretty_print=True), out
    
    