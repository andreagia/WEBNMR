from lxml import etree
import os
import math
from pyparsing import *
import webenmr.lib.cnvx as cnvx
#import amber_md.lib.cnvpx as cnvpx
import webenmr.lib.cnvdx as cnvdx
from pylons import config, session

def check_noe_d_cyana(xmlin, cyana):
    print "#######XML_NOE_CYANA################"
    print etree.tostring(xmlin, pretty_print=True)
    print "####################################"
    lol = False
    for elt in xmlin.getiterator():
        if elt.tag == "noe":
            f_noe = elt.get('filename')
            ini_num = elt.get('number')
            if elt.get('lol') == "False":
                lol = False
            elif elt.get('lol') == "True":
                lol = True
            else:
                lol = False
            if elt.get('nocorr') == "False":
                nocorr = False
            elif elt.get('nocorr') == "True":
                nocorr = True
                
    print f_noe
    #check if NOE is Lower Limits
    #if f_noe.split(".")[-1] == "lol":
    #    lol = True
    noe_in = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), f_noe)
    xxx = open(noe_in,"r").readlines()
    #if os.path.exists(noe_in):
    #    os.remove(noe_in)
    root = etree.Element("noe")
    if lol:
        etree.SubElement(root, "lol").text = "True"
    else:
        etree.SubElement(root, "lol").text = "False"
    for t in xxx:
        if len(t) > 0:
            sd = t.split("#")[0].replace(">","").replace("<","")
            sf = sd.split()
            if len(sf) == 2 and sf[0].isdigit():
                resnu1 = sf[0]
                resna1 = sf[1]
                
            if len(sf) >= 5 and not sf[0].isdigit():
                if sf[1].isdigit():
                    atm1 = sf[0]  
                    resnu2 = sf[1]
                    resna2 = sf[2]
                    atm2 = sf[3]
                    
                    if atm1[0] == "Q" and atm1[1] != "Q":
                        atm1 = "H"+atm1[1:]+"#"
                    # moved to cnvx.py   
                    #if atm1[0] == "Q" and atm1[1] == "Q":
                        #if resna1 == "LEU":
                            #atm1 = "CG"
                        #if resna1 == "VAL":
                            #atm1 = "CB"
                            
                    if atm2[0] == "Q" and atm2[1] != "Q":
                        atm2 = "H"+atm2[1:]+"#"
                    # moved to cnvx.py
                    #if atm2[0] == "Q" and atm2[1] == "Q":
                        #if resna2 == "LEU":
                            #atm2 = "CG"
                        #if resna2 == "VAL":
                            #atm2 = "CB"
                            
                    val = sf[4]
                    print resnu1,resna1,atm1,resnu2,resna2,atm2,val
                    sel = etree.SubElement(root, "selection")
                    sel1 = etree.SubElement(sel, "sel1")
                    etree.SubElement(sel1, "resid").text = resnu1
                    etree.SubElement(sel1, "name").text = atm1
                    sel2 = etree.SubElement(sel, "sel2")
                    etree.SubElement(sel2, "resid").text = resnu2
                    etree.SubElement(sel2, "name").text = atm2
                    dist = etree.SubElement(sel, "D")
                    etree.SubElement(dist, "D").text = val
                    etree.SubElement(dist, "D_minus").text = str(float(val) - 1.8)
                    etree.SubElement(dist, "D_plus").text = "0"
                    
            if len(sf) >= 7 and sf[0].isdigit():
                print"7"
                print sd
                if sf[3].isdigit():
                    sel = etree.SubElement(root, "selection")
                    resnu1 = sf[0]
                    resna1 = sf[1]
                    atm1 = sf[2]
                    resnu2 = sf[3]
                    resna2 = sf[4]
                    atm2 = sf[5]
                    val = sf[6]

                    # moved to cnvx.py
                    #if atm1[0] == "Q" and atm1[1] == "Q":
                    #    if resna1 == "LEU":
                    #        atm1 = "CG"
                    #    if resna1 == "VAL":
                    #        atm1 = "CB"
                    if atm1[0] == "Q" and atm1[1] != "Q":
                         atm1 = "H"+atm1[1:]+"#"
                    if atm1[0] == "Q" and atm1[1] == "R":
                        atm1 = "H"+atm1[1:]+"$"

                    # moved to cnvx.py
                    #if atm2[0] == "Q" and atm2[1] == "Q":
                    #    if resna2 == "LEU":
                    #        atm2 = "CG"
                    #    if resna2 == "VAL":
                    #        atm2 = "CB"           
                    if atm2[0] == "Q" and atm2[1] != "Q":
                        atm2 = "H"+atm2[1:]+"#"
                    if atm2[0] == "Q" and atm2[1] == "R":
                        atm2 = "H"+atm2[1:]+"$"
                        
                    sel1 = etree.SubElement(sel, "sel1")
                    etree.SubElement(sel1, "resid").text = resnu1
                    etree.SubElement(sel1, "name").text = atm1
                    sel2 = etree.SubElement(sel, "sel2")
                    etree.SubElement(sel2, "resid").text = resnu2
                    etree.SubElement(sel2, "name").text = atm2
                    dist = etree.SubElement(sel, "D")
                    etree.SubElement(dist, "D").text = val
                    etree.SubElement(dist, "D_minus").text = "0"
                    etree.SubElement(dist, "D_plus").text = "0"               
    
    #print etree.tostring(root, pretty_print=True)
    pdb_out = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "out_leap.pdb")
    pdb_ref_n = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb.ref")
    
    #
    #xml_file = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "xml_noe")
    #xml_file_w = open(xml_file, 'w')
    #xml_file_w.write()
    #xml_file_w.close()
    
    print pdb_out
    print pdb_ref_n
    print etree.tostring(root, pretty_print=True)
    
    #nocorr = 0
    [ resu_vx, rst ]= cnvx.convert(root, ini_num, pdb_out, pdb_ref_n, nocorr)
    
    noe_out_rst = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_noe + "_noe_RST")
    print noe_out_rst
    noe_out_rst_file = open(noe_out_rst, 'w')
    noe_out_rst_file.writelines(rst)
    noe_out_rst_file.close()
    
    return resu_vx

def check_dih_d_cyana(xmlin, cyana):
    print "XML DIH INPUT"
    print etree.tostring(xmlin, pretty_print=True)
    
    for elt in xmlin.getiterator():
        if elt.tag == "dihedral":
            f_dih = elt.get('filename')
            ini_num = elt.get('number')
    
    print f_dih        
    noe_in = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_dih)
    xxx = open(noe_in,"r").readlines()
    #if os.path.exists(noe_in):
    #    os.remove(noe_in)
    root = etree.Element("dih")
    for t in xxx:
        if len(t) > 0:
            sd = t.split("#")[0].replace(">","").replace("<","")
            sf = sd.split()
            print sf
            if len(sf) >= 4 :
                if sf[0].isdigit():
                    sel = etree.SubElement(root, "selection")
                    resnu = sf[0]  
                    resna = sf[1]
                    ang = sf[2]
                    ang1 = sf[3]
                    ang2 = sf[4]
                    ang_ok = False
                    # check from cyana-dyana library angle assignment for any residues
                    
                    if ang == "PHI":
                        atm1 = "C"
                        atm2 = "N"
                        atm3 = "CA"
                        atm4 = "C"
                        resnu1 = str(int(resnu) - 1)
                        resnu2 = resnu
                        ang_ok = True
                        
                    if ang == "PSI":
                        atm1 = "N"
                        atm2 = "CA"
                        atm3 = "C"
                        atm4 = "N"
                        resnu1 = resnu
                        resnu2 = str(int(resnu) + 1)
                        ang_ok = True
                    
                    #chi1_rn = ["ALA","ILE","VAL","CYS","SER"]
                    if ang == "CHI1": 
                        if resna[0:3] == "ILE"  or resna[0:3] == "VAL":
                            atm1 = "N"
                            atm2 = "CA"
                            atm3 = "CB"
                            atm4 = "CG1"
                            
                        elif resna[0:3] == "SER":
                            atm1 = "N"
                            atm2 = "CA"
                            atm3 = "CB"
                            atm4 = "OG"
                         
                        elif resna[0:3] == "THR":
                            atm1 = "N"
                            atm2 = "CA"
                            atm3 = "CB"
                            atm4 = "OG1"
                            
                        elif resna[0:3] == "CYS":
                            atm1 = "N"
                            atm2 = "CA"
                            atm3 = "CB"
                            atm4 = "SG"   
                        else:
                            atm1 = "N"
                            atm2 = "CA"
                            atm3 = "CB"
                            atm4 = "CG"
                        
                        resnu1 = resnu
                        resnu2 = resnu
                        ang_ok = True
                            
                    if ang == "CHI2": 
                        if resna[0:3] == "ARG" or resna[0:3] == "GLN" or resna[0:3] == "GLU" or resna[0:3] == "LYS":
                            atm1 = "CA"
                            atm2 = "CB"
                            atm3 = "CG"
                            atm4 = "CD"
                            
                        elif resna[0:3] == "ASN" or resna[0:3] == "ASP":
                            atm1 = "CA"
                            atm2 = "CB"
                            atm3 = "CG"
                            atm4 = "OD1"
                            
                        elif resna[0:3] == "CYS":
                            atm1 = "CA"
                            atm2 = "CB"
                            atm3 = "SG"
                            atm4 = "HG"
                            
                        elif resna[0:2] == "HI":
                            atm1 = "CA"
                            atm2 = "CB"
                            atm3 = "CG"
                            atm4 = "ND1"
                            
                                                    
                        elif resna[0:3] == "LEU" or resna[0:3] == "PHE" or resna[0:3] == "TRP" or resna[0:3] == "TYR":
                            atm1 = "CA"
                            atm2 = "CB"
                            atm3 = "CG"
                            atm4 = "CD1"
                        
                        elif resna[0:3] == "MET":
                            atm1 = "CA"
                            atm2 = "CB"
                            atm3 = "CG"
                            atm4 = "SD"
                            
                        resnu1 = resnu
                        resnu2 = resnu
                        ang_ok = True
                        
                    if ang_ok:
                        ran1 = math.radians(float(ang1))
                        ran2 = math.radians(float(ang2))
                        rand = (ran2 - ran1)/2
                        ranf = ran1 + rand
                        attri_ang = {}
                        attri_ang["angle"] = ang
                        attri_ang["res"] = resna[0:3]
                        type = etree.SubElement(sel, "cyana", attrib = attri_ang)
                        sel1 = etree.SubElement(sel, "sel1")
                        etree.SubElement(sel1, "resid").text = resnu1
                        etree.SubElement(sel1, "name").text = atm1
                        sel2 = etree.SubElement(sel, "sel2")
                        etree.SubElement(sel2, "resid").text = resnu
                        etree.SubElement(sel2, "name").text = atm2
                        sel3 = etree.SubElement(sel, "sel3")
                        etree.SubElement(sel3, "resid").text = resnu
                        etree.SubElement(sel3, "name").text = atm3
                        sel4 = etree.SubElement(sel, "sel4")
                        etree.SubElement(sel4, "resid").text = resnu2
                        etree.SubElement(sel4, "name").text = atm4
                        
                        dist = etree.SubElement(sel, "angle")
                        etree.SubElement(dist, "C").text = "1"
                        etree.SubElement(dist, "ang").text = "%6.2f" % math.degrees(ranf)
                        etree.SubElement(dist, "d_ang").text = "%6.2f" % math.degrees(rand)
                        etree.SubElement(dist, "exp").text = "2"
                    else:
                        attri_ang = {}
                        attri_ang["angle"] = ang
                        attri_ang["ERROR"] = "Angle not found"
                        etree.SubElement(sel, "cyana", attrib = attri_ang)
                        
    #print etree.tostring(root, pretty_print=True)
    pdb_out = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "out_leap.pdb")
    pdb_ref_n = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb.ref")
    
    #
    #xml_file = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "xml_noe")
    #xml_file_w = open(xml_file, 'w')
    #xml_file_w.write()
    #xml_file_w.close()
    
    print pdb_out
    print pdb_ref_n
    print etree.tostring(root, pretty_print=True)
    
    nocorr = 0
    [ resu_vx, rst ]= cnvdx.convert(root, ini_num, pdb_out, pdb_ref_n, nocorr)
    
    print rst
    dih_out_rst = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_dih + "_dih_RST")
    print dih_out_rst
    dih_out_rst_file = open(dih_out_rst, 'w')
    dih_out_rst_file.writelines(rst)
    dih_out_rst_file.close()
    
    return resu_vx

def check_pcs_xplor(xmlin):
    print etree.tostring(xmlin, pretty_print=True)
    
    for elt in xmlin.getiterator():
        if elt.tag == "pcs":
            f_pcs = elt.get('filename')
            ini_num = elt.get('number')
            #nocorr = elt.get('nocorr')
    nocorr = 0
    print f_pcs      
    pcs_in = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_pcs )
    #if os.path.exists(pcs_in):
    #    os.remove(pcs_in)
        
    LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR = map(Suppress, "()[]{}|")
    bytes = Word(printables)
    assi = Suppress(Regex(r"[aA][sS][sS][iI][a-z A-Z]*[a-z A-Z]*")).setResultsName("selection")
    num = Word(nums+"."+"-")
    numf = Group( num.setResultsName("val_pcs") + num.setResultsName("tol") ).setResultsName("values")
    word = Word(alphanums+'"*#+%\'')
    sand = Regex(r"[aA][nN][dD]")
    sor =  Regex(r"[oO][rR]")
    cond = Suppress(sand | sor)
    name = Suppress(Regex(r"[nN][aA][mM][eE]")) + Word(alphanums+'"*#+%\'').setResultsName("name")
    resid = Suppress(Regex(r"[rR][eE][sS][iI][a-z A-Z]*")) + Word(nums).setResultsName("resid")
    
    seidvoid = Literal('"    "')
    seidn = Group('"' + word + '"')
    seid = seidvoid | seidn
    #seid =  ZeroOrMore(Word(alphanums+'"*#+% ') )
    
    segid = Suppress(Regex(r"[sS][eE][gG][iI]*[a-z A-Z]") + seid)
    trash = Suppress(LBRC + word + RBRC)
    
    simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + Optional(name) + Optional(cond)
    simpleString2 = OneOrMore(name + Optional(cond) )
    
    simpleString = simpleString1 | simpleString2
    
    display = LBRK + simpleString + RBRK
    string_ = Optional(display) + simpleString
    
    sexp = Forward()
    sexpList = Group(LPAR + ZeroOrMore(sexp) + RPAR)
    sexp << ( string_ | sexpList )
    
    pr = assi + Optional(trash) + sexp + sexp + sexp + sexp + sexp.setResultsName("sel1") + numf 
    
    file = open(pcs_in,"r")
    file_r = []
    for i in file:
        file_r.append(i.split('!')[0])
    #file_r = file.readlines()
    xxx = ''.join(i for i in file_r)
    
    #print xxx
    
    sexpr = pr.searchString(xxx)
    #pprint.pprint(sexpr.asList())
    
    def remove_item(xml):
        #remove xml entry of nasted braket
        join_char=''
        for i in xml.splitlines():
            if not ("<ITEM>" in i or "</ITEM>" in i):
                #print i
                join_char += i + "\n"
        return join_char
         
    xml_pcs = etree.fromstring(remove_item(sexpr.asXML("pcs")))
    
    pdb_out = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "out_leap.pdb")
    pdb_ref_n = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb.ref")  
    xml_file = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_pcs+".xml")
    xml_file_w = open(xml_file, 'w')
    xml_file_w.write(remove_item(sexpr.asXML("pcs")))
    xml_file_w.close()
    
    #print pdb_out
    #print pdb_ref_n
    print etree.tostring(xml_pcs, pretty_print=True)
    
    return remove_item(sexpr.asXML("pcs"))
    
def check_pcs_d_cyana(xmlin, cyana):
    print "XML PCS INPUT"
    print etree.tostring(xmlin, pretty_print=True)
    
    for elt in xmlin.getiterator():
        if elt.tag == "pcs":
            f_pcs = elt.get('filename')
            ini_num = elt.get('number')
    
    print "file pcs input"
    print f_pcs
    print cyana
    pcs_in = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_pcs)
    xxx = open(pcs_in,"r").readlines()
    #if os.path.exists(noe_in):
    #    os.remove(noe_in)
    root = etree.Element("pcs")
    for t in xxx:
        if len(t) > 0:
            sd = t.split("#")[0].replace(">","").replace("<","")
            sf = sd.split()
            print sf
            
            if not cyana:
                if len(sf) >= 4 :
                    atmnf = 0
                    if sf[0].isdigit():
                        sel = etree.SubElement(root, "selection")
                        resnu = sf[0]  
                        resna = sf[1]
                        atm1 = sf[2]
                        val_pcs = sf[3]
                        tol = sf[4]
                        wheight = sf[5]
                        tens  = sf[6]
                        
                        if atm1 == "H":
                            atm2 = "N"
                        elif atm1 == "HN":
                            atm2 = "N"                            
                        elif atm1 == "HA":
                            atm2 = "CA"
                        elif atm1 == "HA":
                            atm2 = "CA"                        
                        else:
                            atmnf = 1
                            print "ATOM %s whit not listed attacched atom"
                        
                        if atmnf == 0:    
                            sel1 = etree.SubElement(sel, "sel1")
                            etree.SubElement(sel1, "resid").text = resnu
                            etree.SubElement(sel1, "name").text = atm1
                            sel2 = etree.SubElement(sel, "sel2")
                            etree.SubElement(sel2, "resid").text = resnu
                            etree.SubElement(sel2, "name").text = atm2
                                                    
                            dist = etree.SubElement(sel, "values")
                            etree.SubElement(dist, "val_pcs").text = val_pcs
                            etree.SubElement(dist, "tol").text = tol

#Formato copiato da il sorgente di cyana
#C    ------------------------------------------------------------------
#C    GETDIP:     reads a file containing the pseudocontact shift
#C                constraints.
#C                Format is:
#C
#C                I3,1X,2A5,1X,F7.2,1X,I1,A1,f5.2,1x,f5.2,1x,I2
#C
#C                that corresponds to:
#C
#C   IRESDIP()    residue number;
#C   NAMRESDIP()  residue name;
#C   NAMATDIP()   atom name;
#C   PSHIFTOR()   pseudocontact shift (original);
#C   QQDIA        if letter 'd' the averaged experimental shift is compared
#C                to the averaged experimental shift (in this case weight
#C                is doubled);
#C   NPROT()      number of atoms whose calculated shifts must be averaged;
#C   TOLPROT()    tolerance on calculated shift;
#C   WPROT()      weight of the individual contraints (multiplies wdip).
#C
#C
#C                Mauro A. Cremonini 24/01/95
#C                Mauro A. Cremonini 07/02/96
#C
#C
#C   NUTE()      index counting the different tensors

            if cyana:
                if len(sf) >= 7 :
                    atmnf = 0
                    if sf[0].isdigit():
                        sel = etree.SubElement(root, "selection")
                        resnu = sf[0]  
                        resna = sf[1]
                        atm1 = sf[2]
                        val_pcs = sf[3]
                        molatm  = sf[4]
                        tol = sf[5]
                        weight = sf[6]
                        
                        if atmnf == 0:    
                            sel1 = etree.SubElement(sel, "sel1")
                            etree.SubElement(sel1, "resid").text = resnu
                            etree.SubElement(sel1, "name").text = atm1
                                                    
                            dist = etree.SubElement(sel, "values")
                            etree.SubElement(dist, "val_pcs").text = val_pcs
                            etree.SubElement(dist, "molatm").text = molatm
                            etree.SubElement(dist, "tol").text = tol
                            etree.SubElement(dist, "weight").text = weight
                    
    print etree.tostring(root, pretty_print=True)

    xml_pcs = etree.tostring(root, pretty_print=True)   
    xml_file = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_pcs+".xml")
    xml_file_w = open(xml_file, 'w')
    xml_file_w.write(xml_pcs)
    xml_file_w.close()
   
    return xml_pcs


def check_rdc_d_cyana(xmlin, cyana):
    print "XML DIH INPUT"
    print etree.tostring(xmlin, pretty_print=True)
    
    for elt in xmlin.getiterator():
        if elt.tag == "rdc":
            f_rdc = elt.get('filename')
            ini_num = elt.get('number')
    
    print "file rdc input"
    print f_rdc
    print cyana
    rdc_in = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), f_rdc)
    xxx = open(rdc_in,"r").readlines()
    #if os.path.exists(noe_in):
    #    os.remove(noe_in)
    root = etree.Element("rdc")
    for t in xxx:
        if len(t) > 0:
            sd = t.split("#")[0].replace(">","").replace("<","")
            sf = sd.split()
            print sf
            
            if not cyana:
                if len(sf) >= 4 :
                    atmnf = 0
                    if sf[0].isdigit():
                        sel = etree.SubElement(root, "selection")
                        resnu = sf[0]  
                        resna = sf[1]
                        atm1 = sf[2]
                        val_rdc = sf[3]
                        tol = sf[4]
                        wheight = sf[5]
                        if len(sf) >= 7 :
                            tens  = sf[6]
                        else:
                            tens = ""
                            
                        if atm1 == "H":
                            atm2 = "N"
                        elif atm1 == "HN":
                            atm2 = "N"                            
                        elif atm1 == "HA":
                            atm2 = "CA"
                        elif atm1 == "HA":
                            atm2 = "CA"                        
                        else:
                            atmnf = 1
                            print "ATOM %s whit not listed attacched atom"
                        
                        if atmnf == 0:    
                            sel1 = etree.SubElement(sel, "sel1")
                            etree.SubElement(sel1, "resid").text = resnu
                            etree.SubElement(sel1, "name").text = atm2
                            sel2 = etree.SubElement(sel, "sel2")
                            etree.SubElement(sel2, "resid").text = resnu
                            etree.SubElement(sel2, "name").text = atm1
                                                    
                            dist = etree.SubElement(sel, "values")
                            etree.SubElement(dist, "val_rdc").text = val_rdc
                            etree.SubElement(dist, "tol").text = tol

            if cyana:
                if len(sf) >= 8 :
                    atmnf = 0
                    if sf[0].isdigit():
                        sel = etree.SubElement(root, "selection")
                        resnu1 = sf[0]  
                        atm1 = sf[1]
                        resnu2 = sf[2]  
                        atm2 = sf[3]
                        
                        val_rdc = sf[4]
                        tol = sf[5]
                        weight = sf[6]
                        point = sf[7]
                        
                        sel1 = etree.SubElement(sel, "sel1")
                        etree.SubElement(sel1, "resid").text = resnu1
                        etree.SubElement(sel1, "name").text = atm1
                        sel2 = etree.SubElement(sel, "sel2")
                        etree.SubElement(sel2, "resid").text = resnu2
                        etree.SubElement(sel2, "name").text = atm2
                    
                        dist = etree.SubElement(sel, "values")
                        etree.SubElement(dist, "val_rdc").text = val_rdc
                        etree.SubElement(dist, "tol").text = tol
                        etree.SubElement(dist, "weight").text = weight
                        etree.SubElement(dist, "point").text = point
                    
    print etree.tostring(root, pretty_print=True)

    xml_rdc = etree.tostring(root, pretty_print=True)   
    xml_file = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), f_rdc+".xml")
    xml_file_w = open(xml_file, 'w')
    xml_file_w.write(xml_rdc)
    xml_file_w.close()
   
    return xml_rdc


def check_rdc_xplor(xmlin):
    print etree.tostring(xmlin, pretty_print=True)
    
    for elt in xmlin.getiterator():
        if elt.tag == "rdc":
            f_rdc = elt.get('filename')
            ini_num = elt.get('number')
            #nocorr = elt.get('nocorr')
    nocorr = 0
    print f_rdc      
    rdc_in = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_rdc )
    #if os.path.exists(rdc_in):
    #    os.remove(rdc_in)
        
    LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR = map(Suppress, "()[]{}|")
    bytes = Word(printables)
    assi = Suppress(Regex(r"[aA][sS][sS][iI][a-z A-Z]*[a-z A-Z]*")).setResultsName("selection")
    num = Word(nums+"."+"-")
    numf = Group( num.setResultsName("val_rdc") + num.setResultsName("tol") ).setResultsName("values")
    word = Word(alphanums+'"*#+%\'')
    sand = Regex(r"[aA][nN][dD]")
    sor =  Regex(r"[oO][rR]")
    cond = Suppress(sand | sor)
    name = Suppress(Regex(r"[nN][aA][mM][eE]")) + Word(alphanums+'"*#+%\'').setResultsName("name")
    resid = Suppress(Regex(r"[rR][eE][sS][iI][a-z A-Z]*")) + Word(nums).setResultsName("resid")
    
    seidvoid = Literal('"    "')
    seidn = Group('"' + word + '"')
    seid = seidvoid | seidn
    #seid =  ZeroOrMore(Word(alphanums+'"*#+% ') )
    
    segid = Suppress(Regex(r"[sS][eE][gG][iI]*[a-z A-Z]") + seid)
    trash = Suppress(LBRC + word + RBRC)
    
    simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + Optional(name) + Optional(cond)
    simpleString2 = OneOrMore(name + Optional(cond) )
    
    simpleString = simpleString1 | simpleString2
    
    display = LBRK + simpleString + RBRK
    string_ = Optional(display) + simpleString
    
    sexp = Forward()
    sexpList = Group(LPAR + ZeroOrMore(sexp) + RPAR)
    sexp << ( string_ | sexpList )
    
    pr = assi + Optional(trash) + sexp + sexp + sexp + sexp + sexp.setResultsName("sel1") + sexp.setResultsName("sel2") + numf 
    
    file = open(rdc_in,"r")
    file_r = []
    for i in file:
        file_r.append(i.split('!')[0])
    #file_r = file.readlines()
    xxx = ''.join(i for i in file_r)
    
    #print xxx
    
    sexpr = pr.searchString(xxx)
    #pprint.pprint(sexpr.asList())
    
    def remove_item(xml):
        #remove xml entry of nasted braket
        join_char=''
        for i in xml.splitlines():
            if not ("<ITEM>" in i or "</ITEM>" in i):
                #print i
                join_char += i + "\n"
        return join_char
             
    xml_rdc = etree.fromstring(remove_item(sexpr.asXML("rdc")))
    
    pdb_out = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "out_leap.pdb")
    pdb_ref_n = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb.ref")
    
    
    xml_file = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_rdc+".xml")
    xml_file_w = open(xml_file, 'w')
    xml_file_w.write(remove_item(sexpr.asXML("rdc")))
    xml_file_w.close()
    
    #print pdb_out
    #print pdb_ref_n
    print etree.tostring(xml_rdc, pretty_print=True)
    
    return remove_item(sexpr.asXML("rdc"))
             

def check_dih_xplor(xmlin):
    print etree.tostring(xmlin, pretty_print=True)
    
    for elt in xmlin.getiterator():
        if elt.tag == "dihedral":
            f_dih = elt.get('filename')
            ini_num = elt.get('number')
            #nocorr = elt.get('nocorr')
    nocorr = 0
    print f_dih      
    dih_in = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_dih )
    #if os.path.exists(dih_in):
    #    os.remove(dih_in)
        
    LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR = map(Suppress, "()[]{}|")
    bytes = Word(printables)
    assi = Suppress(Regex(r"[aA][sS][sS][iI][a-z A-Z]*[a-z A-Z]*")).setResultsName("selection")
    num = Word(nums+"."+"-")
    numf = Group(num.setResultsName("c") + num.setResultsName("ang") + num.setResultsName("d_ang") + num.setResultsName("exp")).setResultsName("angle")
    word = Word(alphanums+'"*#+%\'')
    sand = Regex(r"[aA][nN][dD]")
    sor =  Regex(r"[oO][rR]")
    cond = Suppress(sand | sor)
    name = Suppress(Regex(r"[nN][aA][mM][eE]")) + Word(alphanums+'"*#+%\'').setResultsName("name")
    resid = Suppress(Regex(r"[rR][eE][sS][iI][a-z A-Z]*")) + Word(nums).setResultsName("resid")
    
    seidvoid = Literal('"    "')
    seidn = Group('"' + Regex(r" *[a-z A-Z 0-9]") + '"')
    seid = seidvoid | seidn
    #seid =  ZeroOrMore(Word(alphanums+'"*#+% ') )
    
    segid = Suppress(Regex(r"[sS][eE][gG][iI]*[a-z A-Z]") + seid)
    trash = Suppress(LBRC + word + RBRC)
    
    simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + Optional(name) + Optional(cond)
    simpleString2 = OneOrMore(name + Optional(cond) )
    
    simpleString = simpleString1 | simpleString2
    
    display = LBRK + simpleString + RBRK
    string_ = Optional(display) + simpleString
    
    sexp = Forward()
    sexpList = Group(LPAR + ZeroOrMore(sexp) + RPAR)
    sexp << ( string_ | sexpList )
    
    pr = assi + Optional(trash) + sexp.setResultsName("sel1") + sexp.setResultsName("sel2") + sexp.setResultsName("sel3") + sexp.setResultsName("sel4") + numf 
    
    file = open(dih_in,"r")
    file_r = []
    for i in file:
        file_r.append(i.split('!')[0])
    #file_r = file.readlines()
    xxx = ''.join(i for i in file_r)
    
    #print xxx
    
    sexpr = pr.searchString(xxx)
    #pprint.pprint(sexpr.asList())
    
    def remove_item(xml):
        #remove xml entry of nasted braket
        join_char=''
        for i in xml.splitlines():
            if not ("<ITEM>" in i or "</ITEM>" in i):
                #print i
                join_char += i + "\n"
        return join_char
             
    xml_dih = etree.fromstring(remove_item(sexpr.asXML("dih")))
    
    pdb_out = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "out_leap.pdb")
    pdb_ref_n = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb.ref")
    
    xml_file = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "xml_dih")
    xml_file_w = open(xml_file, 'w')
    xml_file_w.write(remove_item(sexpr.asXML("dih")))
    xml_file_w.close()
    
    print pdb_out
    print pdb_ref_n
    print etree.tostring(xml_dih, pretty_print=True) 
    
    [resu_vx, out_rst]= cnvdx.convert(xml_dih, ini_num, pdb_out, pdb_ref_n,nocorr)
    dih_out_rst = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_dih + "_dih_RST")
    print dih_out_rst
    dih_out_rst_file = open(dih_out_rst, 'w')
    dih_out_rst_file.writelines(out_rst)
    dih_out_rst_file.close()
    return resu_vx



def check_noe_xplor(xmlin):
    print etree.tostring(xmlin, pretty_print=True)
    
    for elt in xmlin.getiterator():
        if elt.tag == "noe":
            f_noe = elt.get('filename')
            ini_num = elt.get('number')
            nocorr = elt.get('nocorr')
    #nocorr = 0
    print f_noe        
    noe_in = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_noe)
    #if os.path.exists(noe_in):
    #    os.remove(noe_in)
        
    LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR = map(Suppress, "()[]{}|")
    bytes = Word(printables)
    assi = Suppress(Regex(r"[aA][sS][sS][iI][a-z A-Z]*[a-z A-Z]*")).setResultsName("selection")
    num = Word(nums+".")
    numf = Group(num.setResultsName("D") + num.setResultsName("D_minus") + num.setResultsName("D_plus"))
    word = Word(alphanums+'"*#+%\'')
    sand = Regex(r"[aA][nN][dD]")
    sor =  Regex(r"[oO][rR]")
    cond = Suppress(sand | sor)
    name = Suppress(Regex(r"[nN][aA][mM][eE]")) + Word(alphanums+'"*#+%\'').setResultsName("name")
    resid = Suppress(Regex(r"[rR][eE][sS][iI][a-z A-Z]*")) + Word(nums).setResultsName("resid")
    
    seidvoid = Literal('"    "')
    seidn = Group('"' + Regex(r" *[a-z A-Z 0-9]") + '"')
    seid = seidvoid | seidn
    #seid =  ZeroOrMore(Word(alphanums+'"*#+% ') )
    
    segid = Suppress(Regex(r"[sS][eE][gG][iI]*[a-z A-Z]") + seid)
    trash = Suppress(LBRC + word + RBRC)
    
    simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + Optional(name) + Optional(cond)
    simpleString2 = OneOrMore(name + Optional(cond) )
    
    simpleString = simpleString1 | simpleString2
    
    display = LBRK + simpleString + RBRK
    string_ = Optional(display) + simpleString
    
    sexp = Forward()
    sexpList = Group(LPAR + ZeroOrMore(sexp) + RPAR)
    sexp << ( string_ | sexpList )
    optor =  sor + sexp.setResultsName("selQ1") + sexp.setResultsName("selQ2")
    
    pr = assi + Optional(trash) + sexp.setResultsName("sel1") + sexp.setResultsName("sel2") + numf + ZeroOrMore(optor)
    
    file = open(noe_in,"r")
    file_r = []
    for i in file:
        file_r.append(i.split('!')[0])
    #file_r = file.readlines()
    xxx = ''.join(i for i in file_r)
    
    #print xxx
    
    sexpr = pr.searchString(xxx)
    #pprint.pprint(sexpr.asList())
    
    def remove_item(xml):
        #remove xml entry of nasted braket
        join_char=''
        for i in xml.splitlines():
            if not ("<ITEM>" in i or "</ITEM>" in i):
                #print i
                join_char += i + "\n"
        return join_char
             
    xml_noe = etree.fromstring(remove_item(sexpr.asXML("noe")))
    sele = xml_noe.findall("selection")
    
    #covert or in QQG QQD atom
    for i in sele:
        selq1 = i.find("selQ1")
        selq2 = i.find("selQ2")
        sel1 = i.find("sel1")
        sel2 = i.find("sel2")
        
        if selq1 is not None:
            te = selq1.find("name").text
            if (te == "HG1#" or te == "HG2#")  and (sel1.find("name").text[0:2] == te[0:2] and sel1.find("name").text.find("#") > 0):
                #print selq1.find("name").text, sel1.find("name").text
                sel1.remove(sel1.find("name"))
                nsl1 = etree.SubElement(sel1, "name" )
                nsl1.text = "QQG"
                
            if (te == "HD1#" or te == "HD2#")  and (sel1.find("name").text[0:2] == te[0:2] and sel1.find("name").text.find("#") > 0):
                #print selq1.find("name").text, sel1.find("name").text
                sel1.remove(sel1.find("name"))
                nsl1 = etree.SubElement(sel1, "name" )
                nsl1.text = "QQD"
                
        if selq2 is not None:
            te = selq2.find("name").text
            if (te == "HG1#" or te == "HG2#")  and (sel2.find("name").text[0:2] == te[0:2] and sel2.find("name").text.find("#") > 0):
                #print selq2.find("name").text, sel2.find("name").text
                sel2.remove(sel2.find("name"))
                nsl2 = etree.SubElement(sel2, "name" )
                nsl2.text = "QQG"
                
            if (te == "HD1#" or te == "HD2#")  and (sel2.find("name").text[0:2] == te[0:2] and sel2.find("name").text.find("#") > 0):
                #print selq2.find("name").text, sel2.find("name").text
                sel2.remove(sel2.find("name"))
                nsl2 = etree.SubElement(sel2, "name" )
                nsl2.text = "QQD"   
    
    pdb_out = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "out_leap.pdb")
    pdb_ref_n = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb.ref")
         
    xml_file = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "xml_noe")
    xml_file_w = open(xml_file, 'w')
    xml_file_w.write(etree.tostring(xml_noe))
    xml_file_w.close()
    
    print pdb_out
    print pdb_ref_n
    #Xplor manage lol in tbl by defualt is disabled
    etree.SubElement(xml_noe, "lol").text = "False"
    print etree.tostring(xml_noe, pretty_print=True)   
    nocorr = 0
    [resu_vx, outx] = cnvx.convert(xml_noe, ini_num, pdb_out, pdb_ref_n, nocorr)
    
    noe_out_rst = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f_noe + "_noe_RST")
    print noe_out_rst
    noe_out_rst_file = open(noe_out_rst, 'w')
    noe_out_rst_file.writelines(outx)
    noe_out_rst_file.close()
    return resu_vx
    
