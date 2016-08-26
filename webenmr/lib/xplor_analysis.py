from __future__ import division
import sys, re, glob, commands
import os, shutil, tarfile, copy, string
from lxml import etree
from pyparsing import *
from pylons import config
from subprocess import call
from webenmr.lib.Subprocess import shellCall
from webenmr.lib.BaseSecurity import BaseSecurity
os.environ['MPLCONFIGDIR'] = config['app_conf']['mpl_data']
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from matplotlib.patches import Patch
from pylab import *
from dicts.sorteddict import ValueSortedDict
from pyparsing import *

def metal_param(wd, atom_name, element, charge, res_name, eps, rvdw, type_name ):
    #Mass = {'Ru': '101.07', 'Re': '186.207', 'Rf': '261', 'Rg': '272', 'Ra': '226', 'Rb': '85.4678', 'Rn': '220', 'Rh': '102.90550', 'Be': '9.012182', 'Ba': '137.327',
    #        'Bh': '264', 'Bi': '208.98040', 'Bk': '247', 'Br': '79.904', 'Uuh': '292', 'H': '1.00794', 'P': '30.973762', 'Os': '190.23', 'Hg': '200.59', 'Ge': '72.64',
    #        'Gd': '157.25', 'Ga': '69.723', 'Uub': '285', 'Pr': '140.90765', 'Pt': '195.084', 'Pu': '244', 'C': '12.0107', 'Pb': '207.2', 'Pa': '231.03588', 'Pd': '106.42',
    #        'Xe': '131.293', 'Po': '210', 'Pm': '145', 'Hs': '277', 'Uuq': '289', 'Uup': '288', 'Ho': '164.93032', 'Hf': '178.49', 'Mo': '95.94', 'He': '4.002602',
    #        'Md': '258', 'Mg': '24.3050', 'K': '39.0983', 'Mn': '54.938045', 'O': '15.9994', 'Mt': '268', 'S': '32.065', 'W': '183.84', 'Zn': '65.409', 'Eu': '151.964',
    #        'Es': '252', 'Er': '167.259', 'Ni': '58.6934', 'No': '259', 'Na': '22.98976928', 'Nb': '92.90638', 'Nd': '144.242', 'Ne': '20.1797', 'Np': '237', 'Fr': '223',
    #        'Fe': '55.845', 'Fm': '257', 'B': '10.811', 'F': '18.9984032', 'Sr': '87.62', 'N': '14.0067', 'Kr': '83.798', 'Si': '28.0855', 'Sn': '118.710', 'Sm': '150.36',
    #        'V': '50.9415', 'Sc': '44.955912', 'Sb': '121.760', 'Sg': '266', 'Se': '78.96', 'Co': '58.933195', 'Cm': '247', 'Cl': '35.453', 'Ca': '40.078', 'Cf': '251',
    #        'Ce': '140.116', 'Cd': '112.411', 'Tm': '168.93421', 'Cs': '132.9054519', 'Cr': '51.9961', 'Cu': '63.546', 'La': '138.90547', 'Li': '6.941', 'Tl': '204.3833',
    #        'Lu': '174.967', 'Lr': '262', 'Th': '232.03806', 'Ti': '47.867', 'Te': '127.60', 'Tb': '158.92535', 'Tc': '98', 'Ta': '180.94788', 'Yb': '173.04', 'Db': '262',
    #        'Zr': '91.224', 'Dy': '162.500', 'Ds': '271', 'I': '126.90447', 'U': '238.02891', 'Y': '88.90585', 'Ac': '227', 'Ag': '107.8682', 'Uut': '284', 'Ir': '192.217',
    #        'Am': '243', 'Al': '26.9815386', 'As': '74.92160', 'Ar': '39.948', 'Au': '196.966569', 'At': '210', 'In': '114.818'}
    mass_d = {'ac': '227',
        'ag': '107.8682',
        'al': '26.9815386',
        'am': '243',
        'ar': '39.948',
        'as': '74.92160',
        'at': '210',
        'au': '196.966569',
        'b': '10.811',
        'ba': '137.327',
        'be': '9.012182',
        'bh': '264',
        'bi': '208.98040',
        'bk': '247',
        'br': '79.904',
        'c': '12.0107',
        'ca': '40.078',
        'cd': '112.411',
        'ce': '140.116',
        'cf': '251',
        'cl': '35.453',
        'cm': '247',
        'co': '58.933195',
        'cr': '51.9961',
        'cs': '132.9054519',
        'cu': '63.546',
        'db': '262',
        'ds': '271',
        'dy': '162.500',
        'er': '167.259',
        'es': '252',
        'eu': '151.964',
        'f': '18.9984032',
        'fe': '55.845',
        'fm': '257',
        'fr': '223',
        'ga': '69.723',
        'gd': '157.25',
        'ge': '72.64',
        'h': '1.00794',
        'he': '4.002602',
        'hf': '178.49',
        'hg': '200.59',
        'ho': '164.93032',
        'hs': '277',
        'i': '126.90447',
        'in': '114.818',
        'ir': '192.217',
        'k': '39.0983',
        'kr': '83.798',
        'la': '138.90547',
        'li': '6.941',
        'lr': '262',
        'lu': '174.967',
        'md': '258',
        'mg': '24.3050',
        'mn': '54.938045',
        'mo': '95.94',
        'mt': '268',
        'n': '14.0067',
        'na': '22.98976928',
        'nb': '92.90638',
        'nd': '144.242',
        'ne': '20.1797',
        'ni': '58.6934',
        'no': '259',
        'np': '237',
        'o': '15.9994',
        'os': '190.23',
        'p': '30.973762',
        'pa': '231.03588',
        'pb': '207.2',
        'pd': '106.42',
        'pm': '145',
        'po': '210',
        'pr': '140.90765',
        'pt': '195.084',
        'pu': '244',
        'ra': '226',
        'rb': '85.4678',
        're': '186.207',
        'rf': '261',
        'rg': '272',
        'rh': '102.90550',
        'rn': '220',
        'ru': '101.07',
        's': '32.065',
        'sb': '121.760',
        'sc': '44.955912',
        'se': '78.96',
        'sg': '266',
        'si': '28.0855',
        'sm': '150.36',
        'sn': '118.710',
        'sr': '87.62',
        'ta': '180.94788',
        'tb': '158.92535',
        'tc': '98',
        'te': '127.60',
        'th': '232.03806',
        'ti': '47.867',
        'tl': '204.3833',
        'tm': '168.93421',
        'u': '238.02891',
        'uub': '285',
        'uuh': '292',
        'uup': '288',
        'uuq': '289',
        'uut': '284',
        'v': '50.9415',
        'w': '183.84',
        'xe': '131.293',
        'y': '88.90585',
        'yb': '173.04',
        'zn': '65.409',
        'zr': '91.224'}

    type_tem = """
addAtomTypes {
{"%s" "%s" "sp3"}
}"""

    par_temp = """Amber Xplor PAR
MASS
%s      %s

BOND

ANGLE

NONB
 %s     %s   %s

   
    """
    try:
        emass = Mass[element.lower()]
    
    except Exception:
        emass = "10"
    
    mass_
    #par.append("nonbonded %s     %s     %s        %s      %s\n" %(type_name, eps, rvdw, eps, rvdw))
    if len(element.strip()) == 2:
        ele = element.strip()[0].upper() + element.strip()[1].lower()
    elif len(element.strip()) == 1:
        ele = element.strip()[0].upper()
        
    par = par %(ele, emass, type_name, eps, rvdw)
    
    type_fi = type_tem %( type_name, ele)
    
    path = wd
    #else:
    #    path = os.path.join("/tmp/", tmp_dir)
    block = []
    block.append('logFile %s\n' %os.path.join(path, 'leap.log'))
    block.append('me= createAtom %s %s %s\n' % ( atom_name, type_name, charge))
    block.append('set me element %s\n' % (element))
    block.append('set me  position { 0 0 0 }\n')
    block.append('r = createResidue %s\n' % res_name)
    block.append('add r me\n')
    block.append('%s = createUnit %s\n' % ( res_name, res_name))
    block.append('add %s r\n' % res_name)
    block.append('saveOff %s %s/%s.lib\n' % (res_name, path, res_name))
    block.append('quit\n')
    prmlib = os.path.join(path, "leapmet.in" )
    prmpar = os.path.join(path, "%s.par" % res_name)
    type_name = os.path.join(path, "%s.typ" % res_name)
    #if os.path.exists(prmlib):
    #    os.remove(prmlib)
    #if os.path.exists(prmpar):
    #    os.remove(prmpar)

    fito = open(prmlib, 'w')
    fito.writelines(block)
    fito.close()
    fito = open(prmpar, 'w')
    fito.writelines(par)
    fito.close()
    fito = open(type_name, 'w')
    fito.writelines(type_fi)
    fito.close()

    os.environ["AMBER_HOME"] = config['app_conf']['amber_home']
    #os.environ["AMBER_HOME"] = "/home/pylons/amber_tools/data/amber_prog/amber10"
    amber_h_exe = os.path.join(config['app_conf']['amber_home'], "bin")
    print amber_h_exe

    cmd = "%s/tleap -f %s "%(amber_h_exe, prmlib)


def check_noe_xplor(noe_in, diz):
    
    #remove alla betwenn {data}
    file_r = []
    for i in noe_in:
        file_r.append(i.split('!')[0].replace("\n", ""))
    xxx1 = ''.join(i + " " for i in file_r)
    
    xxx = re.sub(r'\{.*?\}', '',xxx1)
    #print xxx
    
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
    seid = seidvoid | seidn | Regex(r" *[a-z A-Z 0-9]")
    #seid =  ZeroOrMore(Word(alphanums+'"*#+% ') )
    
    segid = Suppress(Regex(r"[sS][eE][gG][iI]*[a-z A-Z]")) + seid.setResultsName("segid")
    trash = Suppress(LBRC + word + RBRC)
    
    simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + name
    simpleString2 =  resid + cond + name + Optional(cond) + Optional(segid)
    simpleString3 =  resid + cond + Optional(segid) + Optional(cond) + name
    simpleString4 =  name  + cond + Optional(segid) + Optional(cond) + resid
    simpleString5 =  Optional(segid) + Optional(cond) + name + cond + resid
    simpleString6 =  name + cond + resid + Optional(cond) + Optional(segid)
    
    simpleString = (simpleString1 ^ simpleString2 ^ simpleString3 ^ simpleString4 ^ simpleString5 ^ simpleString6)
    
    display = LBRK + simpleString + RBRK
    string_ = Optional(display) + simpleString
    
    sexp = Forward()
    sexpList = Group(LPAR + ZeroOrMore(sexp) + RPAR)
    sexp << ( string_ | sexpList )
    #optor =  sor + sexp.setResultsName("selQ1") + sexp.setResultsName("selQ2")
    
    pr = assi + Optional(trash) + sexp.setResultsName("sel1") + sexp.setResultsName("sel2") + numf #+ ZeroOrMore(optor)
    
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
    noe_o = []  
    xml_noe = etree.fromstring(remove_item(sexpr.asXML("noe")))
    sele = xml_noe.findall("selection")
    #print sele
    print diz
    for i in sele:
        resid1 = i.xpath("sel1/resid")[0].text.strip()
        name1 = i.xpath("sel1/name")[0].text.strip()
        try:
            segid1 = i.xpath("sel1/segid")[0].text.strip()
        except:
            segid1 = ""
    
        resid2 = i.xpath("sel2/resid")[0].text.strip()
        name2 = i.xpath("sel2/name")[0].text.strip()
        try:
            segid2 = i.xpath("sel2/segid")[0].text.strip()
        except:
            segid2 = ""
        
        d = i.xpath("D/D")[0].text.strip()
        dp = i.xpath("D/D_plus")[0].text.strip()
        dm = i.xpath("D/D_minus")[0].text.strip()
        try:
            noe_o.append("assign ( resid  %s and name %s ) ( resid  %s and name %s )    %s  %s  %s\n" %(diz["%s_%s" %(resid1, segid1)], name1, diz["%s_%s" %(resid2, segid2)], name2, d, dm, dp ))
        except:
            print "problem on NOE TBL"
            print diz
            print resid1,name1, segid1, resid2, name2, segid2
            

    #xml_file = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "xml_noe")
    #
    #xml_file_w = open(xml_file, 'w')
    #xml_noe.attrib["prog"] = "xplor"
    #xml_file_w.write(etree.tostring(xml_noe))
    #xml_file_w.close()
    print etree.tostring(xml_noe, pretty_print=True)   
  
    return noe_o    
  

def check_aco_xplor(aco_in, diz):
        
    #remove alla betwenn {data}
    file_r = []
    for i in aco_in:
        file_r.append(i.split('!')[0].replace("\n", ""))
    xxx1 = ''.join(i + " " for i in file_r)
    
    xxx = re.sub(r'\{.*?\}', '',xxx1)
    print xxx
    
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
    seid = seidvoid | seidn | Regex(r" *[a-z A-Z 0-9]")
    #seid =  ZeroOrMore(Word(alphanums+'"*#+% ') )
    
    segid = Suppress(Regex(r"[sS][eE][gG][iI]*[a-z A-Z]")) + seid.setResultsName("segid")
    trash = Suppress(LBRC + word + RBRC)
    
    simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + name
    simpleString2 =  resid + cond + name + Optional(cond) + Optional(segid)
    simpleString3 =  resid + cond + Optional(segid) + Optional(cond) + name
    simpleString4 =  name  + cond + Optional(segid) + Optional(cond) + resid
    simpleString5 =  Optional(segid) + Optional(cond) + name + cond + resid
    simpleString6 =  name + cond + resid + Optional(cond) + Optional(segid)
    
    simpleString = (simpleString1 ^ simpleString2 ^ simpleString3 ^ simpleString4 ^ simpleString5 ^ simpleString6)
    
    display = LBRK + simpleString + RBRK
    string_ = Optional(display) + simpleString
    
    sexp = Forward()
    sexpList = Group(LPAR + ZeroOrMore(sexp) + RPAR)
    sexp << ( string_ | sexpList )
    #optor =  sor + sexp.setResultsName("selQ1") + sexp.setResultsName("selQ2")
    
    pr = assi + Optional(trash) + sexp.setResultsName("sel1") + sexp.setResultsName("sel2") + sexp.setResultsName("sel3") + sexp.setResultsName("sel4")+ numf #+ ZeroOrMore(optor)
    
 
    sexpr = pr.searchString(xxx)
    pprint.pprint(sexpr.asList())
    
    def remove_item(xml):
        #remove xml entry of nasted braket
        join_char=''
        for i in xml.splitlines():
            if not ("<ITEM>" in i or "</ITEM>" in i):
                #print i
                join_char += i + "\n"
        return join_char
    aco_o = []  
    xml_aco = etree.fromstring(remove_item(sexpr.asXML("aco")))
    sele = xml_aco.findall("selection")
    print sele
    for i in sele:
        resid1 = i.xpath("sel1/resid")[0].text.strip()
        name1 = i.xpath("sel1/name")[0].text.strip()
        try:
            segid1 = i.xpath("sel1/segid")[0].text.strip()
        except:
            segid1 = ""
    
        resid2 = i.xpath("sel2/resid")[0].text.strip()
        name2 = i.xpath("sel2/name")[0].text.strip()
        try:
            segid2 = i.xpath("sel2/segid")[0].text.strip()
        except:
            segid2 = ""
        
        resid3 = i.xpath("sel3/resid")[0].text.strip()
        name3 = i.xpath("sel3/name")[0].text.strip()
        try:
            segid3 = i.xpath("sel3/segid")[0].text.strip()
        except:
            segid3 = ""
        
        resid4 = i.xpath("sel4/resid")[0].text.strip()
        name4 = i.xpath("sel4/name")[0].text.strip()
        try:
            segid4 = i.xpath("sel4/segid")[0].text.strip()
        except:
            segid4 = ""
            
        #numf = Group(num.setResultsName("c") + num.setResultsName("ang") + num.setResultsName("d_ang") + num.setResultsName("exp")).setResultsName("angle")
        c = i.xpath("angle/c")[0].text.strip()
        ang = i.xpath("angle/ang")[0].text.strip()
        d_ang = i.xpath("angle/d_ang")[0].text.strip()
        exp = i.xpath("angle/exp")[0].text.strip()
        
        aco_o.append("assign ( resid  %s and name %s ) ( resid  %s and name %s ) ( resid  %s and name %s ) ( resid  %s and name %s )  %s  %s  %s  %s \n" %(diz["%s_%s" %(resid1,segid1)], name1, diz["%s_%s" %(resid2,segid2)], name2,
                                                                                                                                                                  diz["%s_%s" %(resid3,segid3)], name3, diz["%s_%s" %(resid4,segid4)], name4, c, ang, d_ang, exp ))
    print etree.tostring(xml_aco, pretty_print=True)   
  
    return aco_o    

def check_rdc_xplor(rdc_in, diz):
        
     #remove alla betwenn {data}
    file_r = []
    for i in rdc_in:
        file_r.append(i.split('!')[0].replace("\n", ""))
    xxx1 = ''.join(i + " " for i in file_r)
    
    xxx = re.sub(r'\{.*?\}', '',xxx1)
    print xxx
    
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
    seidn = Group('"' + Regex(r" *[a-z A-Z 0-9]") + '"')
    seid = seidvoid | seidn | Regex(r" *[a-z A-Z 0-9]")
    #seid =  ZeroOrMore(Word(alphanums+'"*#+% ') )
    
    segid = Suppress(Regex(r"[sS][eE][gG][iI]*[a-z A-Z]")) + seid.setResultsName("segid")
    trash = Suppress(LBRC + word + RBRC)
    
    #simpleString1T =  Optional(segid) + Optional(cond) + resid + cond + Optional(name) + Optional(cond)
    #simpleString2T = OneOrMore(name + Optional(cond) )
    #
    #simpleStringT = simpleString1T | simpleString2T
    #
    #displayT = LBRK + simpleStringT + RBRK
    #string_T = Optional(displayT) + simpleStringT
    #
    #sexpT = Forward()
    #sexpListT = Group(LPAR + ZeroOrMore(sexpT) + RPAR)
    #sexpT << ( string_T | sexpListT )
    
    simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + name
    simpleString2 =  resid + cond + name + Optional(cond) + Optional(segid)
    simpleString3 =  resid + cond + Optional(segid) + Optional(cond) + name
    simpleString4 =  name  + cond + Optional(segid) + Optional(cond) + resid
    simpleString5 =  Optional(segid) + Optional(cond) + name + cond + resid
    simpleString6 =  name + cond + resid + Optional(cond) + Optional(segid)
    
    #simpleString = simpleString1 | simpleString2 | simpleString3 | simpleString3 | simpleString5 |simpleString6
    simpleString = (simpleString1 ^ simpleString2 ^ simpleString3 ^ simpleString4 ^ simpleString5 ^ simpleString6)
    
    display = LBRK + simpleString + RBRK
    string_ = Optional(display) + simpleString
    
    sexp = Forward()
    sexpList = Group(LPAR + ZeroOrMore(sexp) + RPAR)
    sexp << ( string_ | sexpList )
    #optor =  sor + sexp.setResultsName("selQ1") + sexp.setResultsName("selQ2")
    
    pr = assi + Optional(trash) + sexp.setResultsName("sel1") + sexp.setResultsName("sel2") + sexp.setResultsName("sel3") + sexp.setResultsName("sel4") + sexp.setResultsName("sel5") + sexp.setResultsName("sel6") + numf #+ ZeroOrMore(optor)
    
    #pr = assi + Optional(trash) + sexp.setResultsName("sel1") + numf
    
    sexpr = pr.searchString(xxx)
    pprint.pprint(sexpr.asList())
    
    def remove_item(xml):
        #remove xml entry of nasted braket
        join_char=''
        for i in xml.splitlines():
            if not ("<ITEM>" in i or "</ITEM>" in i):
                #print i
                join_char += i + "\n"
        return join_char
    rdc_o = []  
    xml_rdc = etree.fromstring(remove_item(sexpr.asXML("rdc")))
    sele = xml_rdc.findall("selection")
    print sele
    for i in sele:
        resid1 = i.xpath("sel1/resid")[0].text.strip()
        name1 = i.xpath("sel1/name")[0].text.strip()
        try:
            segid1 = i.xpath("sel1/segid")[0].text.strip()
        except:
            segid1 = ""
    
        resid2 = i.xpath("sel2/resid")[0].text.strip()
        name2 = i.xpath("sel2/name")[0].text.strip()
        try:
            segid2 = i.xpath("sel2/segid")[0].text.strip()
        except:
            segid2 = ""
        
        resid3 = i.xpath("sel3/resid")[0].text.strip()
        name3 = i.xpath("sel3/name")[0].text.strip()
        try:
            segid3 = i.xpath("sel3/segid")[0].text.strip()
        except:
            segid3 = ""
        
        resid4 = i.xpath("sel4/resid")[0].text.strip()
        name4 = i.xpath("sel4/name")[0].text.strip()
        try:
            segid4 = i.xpath("sel4/segid")[0].text.strip()
        except:
            segid4 = ""
            
        resid5 = i.xpath("sel5/resid")[0].text.strip()
        name5 = i.xpath("sel5/name")[0].text.strip()
        try:
            segid5 = i.xpath("sel5/segid")[0].text.strip()
        except:
            segid5 = ""
            
        resid6 = i.xpath("sel6/resid")[0].text.strip()
        name6 = i.xpath("sel6/name")[0].text.strip()
        try:
            segid6 = i.xpath("sel6/segid")[0].text.strip()
        except:
            segid6 = ""
            
        #numf = Group(num.setResultsName("c") + num.setResultsName("ang") + num.setResultsName("d_ang") + num.setResultsName("exp")).setResultsName("angle")
        val_rdc = i.xpath("values/val_rdc")[0].text.strip()
        tol = i.xpath("values/tol")[0].text.strip()
        
        
        rdc_o.append("assign ( resid  %s and name %s ) \n ( resid  %s and name %s ) \n ( resid  %s and name %s ) \n ( resid  %s and name %s ) \n ( resid  %s and name %s ) \n ( resid  %s and name %s ) %s  %s   \n" %(resid1, name1, resid2, name2,
                                                                                                                                                                  resid3, name3, resid4, name4,  diz["%s_%s" %(resid5,segid5)], name5,diz["%s_%s" %(resid6,segid6)], name6, val_rdc, tol ))
    print etree.tostring(xml_rdc, pretty_print=True)   
  
    return rdc_o    

def check_pcs_xplor(pcs_in, diz):
        
     #remove alla betwenn {data}
    file_r = []
    for i in pcs_in:
        file_r.append(i.split('!')[0].replace("\n", ""))
    xxx1 = ''.join(i + " " for i in file_r)
    
    xxx = re.sub(r'\{.*?\}', '',xxx1)
    print xxx
    
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
    seidn = Group('"' + Regex(r" *[a-z A-Z 0-9]") + '"')
    seid = seidvoid | seidn | Regex(r" *[a-z A-Z 0-9]")
    #seid =  ZeroOrMore(Word(alphanums+'"*#+% ') )
    
    segid = Suppress(Regex(r"[sS][eE][gG][iI]*[a-z A-Z]")) + seid.setResultsName("segid")
    trash = Suppress(LBRC + word + RBRC)
    
    #simpleString1T =  Optional(segid) + Optional(cond) + resid + cond + Optional(name) + Optional(cond)
    #simpleString2T = OneOrMore(name + Optional(cond) )
    #
    #simpleStringT = simpleString1T | simpleString2T
    #
    #displayT = LBRK + simpleStringT + RBRK
    #string_T = Optional(displayT) + simpleStringT
    #
    #sexpT = Forward()
    #sexpListT = Group(LPAR + ZeroOrMore(sexpT) + RPAR)
    #sexpT << ( string_T | sexpListT )
    
    simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + name
    simpleString2 =  resid + cond + name + Optional(cond) + Optional(segid)
    simpleString3 =  resid + cond + Optional(segid) + Optional(cond) + name
    simpleString4 =  name  + cond + Optional(segid) + Optional(cond) + resid
    simpleString5 =  Optional(segid) + Optional(cond) + name + cond + resid
    simpleString6 =  name + cond + resid + Optional(cond) + Optional(segid)
    
    #simpleString = simpleString1 | simpleString2 | simpleString3 | simpleString3 | simpleString5 |simpleString6
    simpleString = (simpleString1 ^ simpleString2 ^ simpleString3 ^ simpleString4 ^ simpleString5 ^ simpleString6)
    
    display = LBRK + simpleString + RBRK
    string_ = Optional(display) + simpleString
    
    sexp = Forward()
    sexpList = Group(LPAR + ZeroOrMore(sexp) + RPAR)
    sexp << ( string_ | sexpList )
    #optor =  sor + sexp.setResultsName("selQ1") + sexp.setResultsName("selQ2")
    
    pr = assi + Optional(trash) + sexp.setResultsName("sel1") + sexp.setResultsName("sel2") + sexp.setResultsName("sel3") + sexp.setResultsName("sel4") + sexp.setResultsName("sel5") + numf #+ ZeroOrMore(optor)
    
    #pr = assi + Optional(trash) + sexp.setResultsName("sel1") + numf
 
    sexpr = pr.searchString(xxx)
    pprint.pprint(sexpr.asList())
    
    def remove_item(xml):
        #remove xml entry of nasted braket
        join_char=''
        for i in xml.splitlines():
            if not ("<ITEM>" in i or "</ITEM>" in i):
                #print i
                join_char += i + "\n"
        return join_char
    pcs_o = []  
    xml_pcs = etree.fromstring(remove_item(sexpr.asXML("pcs")))
    sele = xml_pcs.findall("selection")
    print sele
    for i in sele:
        resid1 = i.xpath("sel1/resid")[0].text.strip()
        name1 = i.xpath("sel1/name")[0].text.strip()
        try:
            segid1 = i.xpath("sel1/segid")[0].text.strip()
        except:
            segid1 = ""
    
        resid2 = i.xpath("sel2/resid")[0].text.strip()
        name2 = i.xpath("sel2/name")[0].text.strip()
        try:
            segid2 = i.xpath("sel2/segid")[0].text.strip()
        except:
            segid2 = ""
        
        resid3 = i.xpath("sel3/resid")[0].text.strip()
        name3 = i.xpath("sel3/name")[0].text.strip()
        try:
            segid3 = i.xpath("sel3/segid")[0].text.strip()
        except:
            segid3 = ""
        
        resid4 = i.xpath("sel4/resid")[0].text.strip()
        name4 = i.xpath("sel4/name")[0].text.strip()
        try:
            segid4 = i.xpath("sel4/segid")[0].text.strip()
        except:
            segid4 = ""
            
        resid5 = i.xpath("sel5/resid")[0].text.strip()
        name5 = i.xpath("sel5/name")[0].text.strip()
        try:
            segid5 = i.xpath("sel5/segid")[0].text.strip()
        except:
            segid5 = ""
            
        resid6 = i.xpath("sel6/resid")[0].text.strip()
        name6 = i.xpath("sel6/name")[0].text.strip()
        try:
            segid6 = i.xpath("sel6/segid")[0].text.strip()
        except:
            segid6 = ""
            
        #numf = Group(num.setResultsName("c") + num.setResultsName("ang") + num.setResultsName("d_ang") + num.setResultsName("exp")).setResultsName("angle")
        val_pcs = i.xpath("values/val_pcs")[0].text.strip()
        tol = i.xpath("values/tol")[0].text.strip()
        
        
        pcs_o.append("assign ( resid  %s and name %s ) \n ( resid  %s and name %s ) \n ( resid  %s and name %s ) \n ( resid  %s and name %s ) \n  ( resid  %s and name %s ) %s  %s   \n" %(resid1, name1, resid2, name2,
                                                                                                                                                                  resid3, name3, resid4, name4,  diz["%s_%s" %(resid5,segid5)], name5, val_pcs, tol ))
    print etree.tostring(xml_pcs, pretty_print=True)   
  
    return pcs_o    


def read_pdb_xplor(file_pdb, xml):
    
    def findxml( xml, tag):
        res = []
        for a in xml.getiterator():
            if a.tag == tag:
               res.append(a)
        return res
    
    print "######### info.xml ############"
    print etree.tostring(xml, pretty_print=True)
    print "###############################"
    psfI = findxml(xml, "psf")
    pos = {}
    for i in psfI:
        print "Position"
        print i.get("position")
        if i.get("position"):
            pos[int(i.get("position"))] = {"min" : i.get("min"), "chainid" :i.get("chainid"), "max" : i.get("max")}
            
    pdb_diz = {}
    try:
        pdb = open(file_pdb, "r").readlines()
    except:
        return False
    onlyA = []
    for i in pdb:
        if i.startswith("ATOM") or i.startswith("TER"):
            onlyA.append(i)
    resnum = 0
    renumPDB = []
    renu = iter_res(onlyA)
    for a in range(1, len(pos)+1):
        #print "############################"
        #print a
        #print pos[a]["min"], pos[a]["max"], pos[a]["chainid"]
        #print "############################"
        for b in range(int(pos[a]["min"]), int(pos[a]["max"]) + 1):
            resnum = resnum + 1
            aa =  renu.get_res(str(b), pos[a]["chainid"])
            #print "Cerco", str(b), pos[a]["chainid"]
            if len(aa) == 0:
                print str(b), pos[a]["chainid"], "non trovato"
            else:
                for r in aa:    
                    renumPDB.append("%s%4d%s\n" %(r[:22],resnum,r[26:54]))
                pdb_diz["%s_%s" %(str(b),pos[a]["chainid"].strip())] = str(resnum)
        renumPDB.append("TER\n")
        
    return renumPDB, pdb_diz

def replace_str(fin, fout, sin, sout):
    print "####################"
    print fin
    print fout
    print sin
    print sout
    print "####################"
    ff = open(fin)
    data = ff.read()
    ff.close()
    print data
    #data.replace(sin, sout);
    o = open(fout,"w")
    o.write( re.sub(str(sin), str(sout), data) )
    o.close()

def print_err(var, inte):
    print "######" + inte + "########"
    print var
    print "#########################"
    
def check_file(file, wd):
    filec=os.path.join(wd,file)
    if os.path.isfile(filec):
        return True
    else:
        err="%s: file %s doesn't exist\n\n" % (sys.argv[0], filec)
        sys.stderr.write(err)
        sys.exit()
    
class JobsProcessing(BaseSecurity):
    
    def __init__(self):
        BaseSecurity.__init__(self)
        os.environ['TOPPAR'] = "/prog/xplor-nih-2.29/toppar"
       
    def exec_cmd(self, cmd, work_dir):
        prev = os.getcwd()
        os.chdir(work_dir)
        #ret = call( cmd, shell = True)
        cmdEnv = self._getExternalCmdEnvironment()
        ret = shellCall( self._secCmdTimeout, cmd, env = cmdEnv )
        #ret = os.system(cmd)
        print "#####RET[VALUE]###########"
        print ret['Value']
        print "##########################"
        os.chdir(prev)
        return ret['Value']
        
class xplor_analysis:
    '''
    xplor analysis 
    '''
    def findxml(self, xml, tag):
       res = []
       for a in xml.getiterator():
           if a.tag == tag:
              res.append(a)
       return res
    
    def fit_fanta_rdc(self, struct_name):
        
        def remove_item(xml):
            #remove xml entry of nasted braket
            join_char=''
            for i in xml.splitlines():
                if not ("<ITEM>" in i or "</ITEM>" in i):
                    #print i
                    join_char += i + "\n"
            return join_char
        
        def get_data_rdc(rdc_in):
                
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
            
            #simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + Optional(name) + Optional(cond)
            #simpleString2 = OneOrMore(name + Optional(cond) )
            #
            #simpleString = simpleString1 | simpleString2
            simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + name
            simpleString2 =  resid + cond + name + Optional(cond) + Optional(segid)
            simpleString3 =  resid + cond + Optional(segid) + Optional(cond) + name
            simpleString4 =  name  + cond + Optional(segid) + Optional(cond) + resid
            simpleString5 =  Optional(segid) + Optional(cond) + name + cond + resid
            simpleString6 =  name + cond + resid + Optional(cond) + Optional(segid)
            
            #simpleString = simpleString1 | simpleString2 | simpleString3 | simpleString3 | simpleString5 |simpleString6
            simpleString = (simpleString1 ^ simpleString2 ^ simpleString3 ^ simpleString4 ^ simpleString5 ^ simpleString6)
            
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
            
                     
            xml_rdc = etree.fromstring(remove_item(sexpr.asXML("rdc")))
            
            print remove_item(sexpr.asXML("pcs"))
            return xml_rdc
          
        tree = etree.parse(open(os.path.join(self.tmp_analy_dir, "xplor.xml")))
        
        map_res =  {}
        #pdb_file = open(os.path.join(self.tmp_analy_dir, struct_name), "r").readlines()
        #for num in pdb_file:
        #    if num.startswith("ATOM"):
        #        map_res[int(num[22:26])] = num[17:20]
        
        fanta_in = []
        metal_num  = "XXXXXXX"
        metal_name = "XXXXXXX"
        for node in tree.findall('./rdc'):
            xml_rdc = get_data_rdc(os.path.join(self.tmp_analy_dir, os.path.basename(node.attrib.get('path'))))
            metal_num = node.attrib.get('res_num')
            for met in tree.findall('./metal'):
                if met.attrib.get('res_num') == metal_num:
                    metal_name = met.attrib.get("atom_name")
            
            for elt in xml_rdc.getiterator():
                if elt.tag == "selection":
                    for elt1 in elt.getiterator():       
                        if elt1.tag == "sel1":
                            for elt2 in elt1.getiterator():
                                if elt2.tag == "resid":
                                    res1 = int(elt2.text)
                                if elt2.tag == "name":
                                    atm1 = elt2.text
                        if elt1.tag == "sel2":
                            for elt2 in elt1.getiterator():
                                if elt2.tag == "resid":
                                    res2 = int(elt2.text)
                                if elt2.tag == "name":
                                    atm2 = elt2.text  
                        #if elt1.tag == "resid":
                        #    metal_num = elt1.text
                        if elt1.tag == "val_rdc":
                            rdc_val = float(elt1.text)
                        if elt1.tag == "tol":
                            tol = float(elt1.text)
                                  
    
     #  read(line,'(i3,1x,a3,1x,i3,1x,a3,f9.3,4x,i2,f6.2,f10.3,f4.0)')
     #*           numres1(i),namat1(i),numres2(i),namat2(i),obs(i),
     #*           mlprot(i),tolprot(i),wprot(i),field(i)

                    fanta_in.append("%3s %-3s %3s %-3s%9.3f    %2d%6.2f%10.3f%4.0f\n" %(res1, atm1, res2, atm2, rdc_val,1 , tol, 1.0, 700 ))
                    #print "%3s %3s %3s %3s%9.3f    %2d%6.2f%10.3f%4.0f" %(res1, atm1, res2, atm2, rdc_val,1 , tol, 1.0, 700 )
                    
            open(os.path.join(self.tmp_analy_dir, "xc1fantardc"), "w").writelines(fanta_in)
            open(os.path.join(self.tmp_analy_dir, "xc1fantapcs"), "w").writelines("")
            save_pdb = []
            save_pdb_tmp = ""
            print metal_num, metal_name
            save_matal = True
            for p in open(os.path.join(self.tmp_analy_dir, struct_name), "r").readlines():
                if p.startswith("ATOM"):
                    #print  p[22:26].strip(),  p[22:26].strip()
                    if metal_num == p[22:26].strip() and metal_name == p[12:16].strip():
                        print "TROVATO"
                        save_pdb_tmp = "%s%s%4s%s" %(p[0:12], "MEX  MEX  ",metal_num,p[26:])
                        save_metal = False
                    elif p[17:20] != "ANI":
                        #save_pdb.append(p)
                        save_pdb.append("%s%-4s%s" %(p[0:12], p[12:16].strip(), p[16:]))
                    if save_matal:
                        save_pdb_tmp = "ATOM   9999 MEX  MEX   900       4.168   4.025  -3.639  1.00  0.00"
                    
                       
            save_pdb.append(save_pdb_tmp) 
            open(os.path.join(self.tmp_analy_dir, "xc1fantavv.pdb"), "w").writelines(save_pdb)      
  
            loc = os.getcwd()
            os.chdir(self.tmp_analy_dir)
            shutil.copyfile(os.path.join(config['app_conf']['prog_dir'], "fantallnew", "fantallnew"),
                            os.path.join(self.tmp_analy_dir, "fantallnew") )
            os.chmod(os.path.join(self.tmp_analy_dir, "fantallnew"), 0774)
            cmd = "./fantallnew  %s %s " % ("1.0", "300")
            print "Work Directory and command"
            print self.tmp_analy_dir
            print cmd
            out_leap = os.popen(cmd).read()
            open(os.path.join(self.analy_dir,"RDC_%s_%s" %( os.path.basename(node.attrib.get('path')).split(".")[0], struct_name.split(".")[0] )),"w").write(out_leap)
            
            os.chdir(loc)
            print out_leap

            
    def fit_fanta_pcs(self, struct_name):
        
        def remove_item(xml):
            #remove xml entry of nasted braket
            join_char=''
            for i in xml.splitlines():
                if not ("<ITEM>" in i or "</ITEM>" in i):
                    #print i
                    join_char += i + "\n"
            return join_char
        
        def get_data_pcs(pcs_in):
                
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
            
            #simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + Optional(name) + Optional(cond)
            #simpleString2 = OneOrMore(name + Optional(cond) )
            #
            #simpleString = simpleString1 | simpleString2
            simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + name
            simpleString2 =  resid + cond + name + Optional(cond) + Optional(segid)
            simpleString3 =  resid + cond + Optional(segid) + Optional(cond) + name
            simpleString4 =  name  + cond + Optional(segid) + Optional(cond) + resid
            simpleString5 =  Optional(segid) + Optional(cond) + name + cond + resid
            simpleString6 =  name + cond + resid + Optional(cond) + Optional(segid)
            
            #simpleString = simpleString1 | simpleString2 | simpleString3 | simpleString3 | simpleString5 |simpleString6
            simpleString = (simpleString1 ^ simpleString2 ^ simpleString3 ^ simpleString4 ^ simpleString5 ^ simpleString6)
            
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
            
            #print remove_item(sexpr.asXML("pcs"))
            
            xml_pcs = etree.fromstring(remove_item(sexpr.asXML("pcs")))
            return xml_pcs
          
        tree = etree.parse(open(os.path.join(self.tmp_analy_dir, "xplor.xml")))
        
        map_res =  {}
        pdb_file = open(os.path.join(self.tmp_analy_dir, struct_name), "r").readlines()
        for num in pdb_file:
            if num.startswith("ATOM"):
                map_res[int(num[22:26])] = num[17:20]
        
        fanta_in = []         
        for node in tree.findall('./pcs'):
            xml_pcs = get_data_pcs(os.path.join(self.tmp_analy_dir, os.path.basename(node.attrib.get('path'))))
            metal_num = node.attrib.get('res_num')
            for met in tree.findall('./metal'):
                if met.attrib.get('res_num') == metal_num:
                    metal_name = met.attrib.get("atom_name")
            
            for elt in xml_pcs.getiterator():
                if elt.tag == "selection":
                    for elt1 in elt.getiterator():       
                        if elt1.tag == "sel1":
                            for elt2 in elt1.getiterator():
                                if elt2.tag == "resid":
                                    res1 = int(elt2.text)
                                if elt2.tag == "name":
                                    atm1 = elt2.text
                        #if elt1.tag == "resid":
                        #    metal_num = elt1.text
                        if elt1.tag == "val_pcs":
                            pcs_val = float(elt1.text)
                        if elt1.tag == "tol":
                            tol = float(elt1.text)
                                  
     #          read(line,'(i4,1x,a3,2x,a3,1x,f9.3,4x,i2,f6.2,f10.3)')
     #*           numres(i),namres(i),namat(i),obs(i),
     #*           mlprot(i),tolprot(i),wprot(i)
     #          read(line,'(i4,1x,a3,2x,a3,1x,f9.3,4x,i2,f6.2,f10.3)')
     #*           numres(i),namres(i),namat(i),obs(i),
     #*           mlprot(i),tolprot(i),wprot(i)

                    fanta_in.append("%4d %3s  %-3s %9.3f    %2d%6.2f%10.3f\n" %(res1, map_res[res1], atm1, pcs_val,1 , tol, 1.0 ))
                    #print "%4d %3s  %-3s %9.3f    %2d%6.2f%10.3f" %(res1, map_res[res1], atm1, pcs_val,1 , tol, 1.0 )
                    
            open(os.path.join(self.tmp_analy_dir, "xc1fantapcs"), "w").writelines(fanta_in)
            open(os.path.join(self.tmp_analy_dir, "xc1fantardc"), "w").writelines("")
            save_pdb = []
            save_pdb_tmp = ""
            print metal_num, metal_name
            for p in open(os.path.join(self.tmp_analy_dir, struct_name), "r").readlines():
                if p.startswith("ATOM"):
                    #print  p[22:26].strip(),  p[22:26].strip()
                    if metal_num == p[22:26].strip() and metal_name == p[12:16].strip():
                        print "TROVATO"
                        save_pdb_tmp = "%s%s%4s%s" %(p[0:12], "MEX  MEX  ",metal_num,p[26:])
                    elif p[17:20] != "ANI":
                        #save_pdb.append(p)
                        save_pdb.append("%s%-4s%s" %(p[0:12], p[12:16].strip(), p[16:]))
            save_pdb.append(save_pdb_tmp)
            open(os.path.join(self.tmp_analy_dir, "xc1fantavv.pdb"), "w").writelines(save_pdb)      
  
            loc = os.getcwd()
            os.chdir(self.tmp_analy_dir)
            shutil.copyfile(os.path.join(config['app_conf']['prog_dir'], "fantallnew", "fantallnew"),
                            os.path.join(self.tmp_analy_dir, "fantallnew") )
            os.chmod(os.path.join(self.tmp_analy_dir, "fantallnew"), 0774)
            cmd = "./fantallnew  %s %s " % ("1.0", "300")
            print "Work Directory and command"
            print self.tmp_analy_dir
            print cmd
            out_leap = os.popen(cmd).read()
            open(os.path.join(self.analy_dir,"PCS_%s_%s" %( os.path.basename(node.attrib.get('path')).split(".")[0], struct_name.split(".")[0] )),"w").write(out_leap)
            
            os.chdir(loc)
            #print out_leap
        
    def plot_res(self, xml_file, dir_out):
        
        print "#########PLOT RES############"
        tree = etree.parse(open(xml_file))
        str_viols  =  {}
        for node in tree.findall('./NOE_pdb'):
            fil  = node.attrib.get('file')
            if fil:
                nr_str_viols = 0
                for classnoe in node.findall(".//CLASS"):
                    class_name = classnoe.find("class_name")
                    if class_name is not None:
                        if class_name.text is not "METT":
                            for noe_viol in classnoe.findall("./NOE_violation"):
                                values = noe_viol.find("values")
                                delta = values.find("delta")
                                deltaf = float(delta.text)
                                if abs(deltaf) > 0.1:
                                    nr_str_viols = nr_str_viols + 1
                str_viols[fil] = nr_str_viols
        
        sortpdb = ValueSortedDict(str_viols).items()
        print sortpdb
        #if sortpdb[-1][1] == 0:
        #    max_num_viol = 1
        #else:
        max_num_viol = sortpdb[-1][1]
            
        matr_noe = np.zeros((len(sortpdb),max_num_viol))
        print matr_noe
        
        viol_enum = {}
        viol_num = 0
        stru_num = 0
        for stru in  sortpdb:
            print stru
            
            for node in tree.findall('./DIH_pdb'):
                fil  = node.attrib.get('file')
                if fil == stru[0]:
                    print fil
                    #for classnoe in node.findall(".//CLASS"):
                    #    class_name = classnoe.find("class_name")
                    #    if class_name is not None:
                    #        print class_name.text
                    #        if class_name.text is not "METT":
                    for dih_viol in node.findall(".//dih_violation"):
                        if dih_viol.find("dih_delta"):
                            values = dih_viol.find("dih_val")
                            delta = values.find("dih_delta")
                            deltaf = float(delta.text)
                            if abs(deltaf) > 0.5:
                                sele1 = dih_viol.find("atom_i")
                                sele2 = dih_viol.find("atom_j")
                                sele3 = dih_viol.find("atom_k")
                                sele4 = dih_viol.find("atom_l")
                                atoms1 = sele1.find("atomname")
                                atoms2 = sele2.find("atomname")
                                atoms3 = sele3.find("atomname")
                                atoms4 = sele4.find("atomname")
                                
                                print "###################VIOLATION " + delta.text
                                sele1 = "#S1 "
                                sele2 = "#S2 "
                                for atm in atoms1:
                                    #print "atom1"
                                    resid = atm.find("resid")
                                    resna = atm.find("resname")
                                    atmna = atm.find("atomname")
                                    sele1 = sele1 + atmna.text + " " + resid.text + " " + resna.text + " "
                                for atm in atoms2:
                                    #print "atom2"
                                    resid = atm.find("resid")
                                    resna = atm.find("resname")
                                    atmna = atm.find("atomname")
                                    sele2 = sele2 + atmna.text + " " + resid.text + " " +resna.text + " "
                                key_sele = sele1 + sele2
                                if key_sele not in viol_enum.keys():
                                    if len(viol_enum) > 0:
                                        viol_num = max(viol_enum.values()) + 1
                                    viol_enum[sele1 + sele2] = viol_num
                                else:
                                    viol_num = viol_enum[key_sele]
                                if viol_num > (matr_noe.shape[1] - 1):
                                    print "####inserisco colonna aggiuntiva", viol_num, max_num_viol
                                    matr_noe = np.insert(matr_noe, matr_noe.shape[1], 0, axis=1)
                                    print matr_noe
                                    print "####"
                                matr_noe[stru_num, viol_num] = delta.text
                                print stru_num, viol_num, delta.text
                                print matr_noe
            
            for node in tree.findall('./NOE_pdb'):
                fil  = node.attrib.get('file')
                if fil == stru[0]:
                    print fil
                    for classnoe in node.findall(".//CLASS"):
                        class_name = classnoe.find("class_name")
                        if class_name is not None:
                            print class_name.text
                            if class_name.text is not "METT":
                                for noe_viol in classnoe.findall("./NOE_violation"):
                                    values = noe_viol.find("values")
                                    delta = values.find("delta")
                                    deltaf = float(delta.text)
                                    if abs(deltaf) > 0.08:
                                        sele1 = noe_viol.find("sele1")
                                        sele2 = noe_viol.find("sele2")
                                        atoms1 = sele1.findall("./atom")
                                        atoms2 = sele2.findall("./atom")
                                        print "###################VIOLATION " + delta.text
                                        sele1 = "#S1 "
                                        sele2 = "#S2 "
                                        for atm in atoms1:
                                            #print "atom1"
                                            resid = atm.find("resid")
                                            resna = atm.find("resname")
                                            atmna = atm.find("atomname")
                                            sele1 = sele1 + atmna.text + " " + resid.text + " " + resna.text + " "
                                        for atm in atoms2:
                                            #print "atom2"
                                            resid = atm.find("resid")
                                            resna = atm.find("resname")
                                            atmna = atm.find("atomname")
                                            sele2 = sele2 + atmna.text + " " + resid.text + " " +resna.text + " "
                                        key_sele = sele1 + sele2
                                        if key_sele not in viol_enum.keys():
                                            if len(viol_enum) > 0:
                                                viol_num = max(viol_enum.values()) + 1
                                            viol_enum[sele1 + sele2] = viol_num
                                        else:
                                            viol_num = viol_enum[key_sele]
                                        if viol_num > (matr_noe.shape[1] - 1):
                                            print "####inserisco colonna aggiuntiva", viol_num, max_num_viol
                                            matr_noe = np.insert(matr_noe, matr_noe.shape[1], 0, axis=1)
                                            print matr_noe
                                            print "####"
                                        matr_noe[stru_num, viol_num] = delta.text
                                        print stru_num, viol_num, delta.text
                                        print matr_noe
                                        
                    print viol_enum
                    stru_num = stru_num + 1
        
        data = abs( np.transpose(matr_noe))
        
        dx, dy = 0.05, 0.05
        if len(data) >  0:
            #x = arange(-3.0, 3.0001, dx)
            #y = arange(-3.0, 3.0001, dy)
            #X,Y = meshgrid(x, y)
            lx= len(data[0])            # Work out matrix dimensions
            ly= len(data[:,0])
            x = np.arange(0,lx,1)    # Set up a mesh of positions
            y = np.arange(0,ly,1)
            #print 
            X, Y = np.meshgrid(x, y)
            Z = data
            pcolor(X, Y, Z, cmap=cm.Reds, vmax=abs(Z).max(), vmin=0, edgecolors='k',)
            colorbar()
            print "shape", matr_noe.shape[0], matr_noe.shape[1]
            axis([0,matr_noe.shape[0]-1,0,matr_noe.shape[1]-1])
            savefig(os.path.join(dir_out, "NOE.png"))
            clf()
            
        
    def sort_dict(self, dictionary, field):
        tmp_list = []
        for key, value in dictionary.items():
            tmp_list.append([key, value])
            tmp_list.sort(key=lambda x:x[field])
        return tmp_list

    
    def best_struct(self, wd, frac):
        d={}
        frac=float(frac)
        w=os.path.join(wd,'sa*.pdb')
        save_pdb_model = []
        save_pdb_amber_model = []
        
        for pdb in glob.glob(w):
            cmd="/bin/grep 'REMARK energie overall' %s" % pdb
            o=commands.getoutput(cmd)
            print pdb,o
            no=o[26:].strip()
            print no
            d[pdb]=float(no)
    
        ds=self.sort_dict(d, 1)
        if frac==0:
            frac=0.1
        goods=int((len(ds)*frac))
        todel=ds[goods:]
        tokeep=ds[:goods]
        print tokeep
        for i in range(len(todel)):
            #print todel[i][0]
            os.unlink(todel[i][0])
    
        newlist=[]
        for i in range(len(tokeep)):
            f=os.path.basename(tokeep[i][0])
            p=os.path.dirname(tokeep[i][0])
            nf='orig%s' % f
            nfn=os.path.join(p, nf)
            os.rename(tokeep[i][0], nfn)
            #take only the first 20   
            newlist.append(nfn)
                
        xml_info = etree.parse(os.path.join(self.work_dir,"output", "output_1", "info.xml"))
        diz_amber = []
        
        for i in range(len(newlist)):
            f=os.path.basename(newlist[i])
            p=os.path.dirname(newlist[i])
            nf='ana%s.pdb' % str(i+1)
            #print nf, f
            nfn=os.path.join(p, nf)
            os.rename(newlist[i], nfn)
            self.best_struc_list.append(nf)
            save_pdb_model.append("MODEL %d\n" %(i+1))
            num = 0
            for p in open(os.path.join(self.tmp_analy_dir, nf), "r").readlines():
                if p.startswith("ATOM")and p[17:20] != "ANI":
                    if int(p[22:26]) - num > 1:
                        save_pdb_model.append("TER\n")
                    num = int(p[22:26])
                    save_pdb_model.append(p)
            save_pdb_model.append("END\n")
            save_pdb_model.append("ENDMDL\n")
            pdb_num = 0
            
            #convert pdb in amber sequential number (olny psf now)
            save_pdb_amber_model = save_pdb_amber_model + read_pdb_xplor(os.path.join(self.tmp_analy_dir, nf), xml_info)[0]
            if len(diz_amber) == 0:
                print "lancio read_pdb_xplor"
                diz_amber = read_pdb_xplor(os.path.join(self.tmp_analy_dir, nf), xml_info)[1]
                print "####DIZ####"
                print diz_amber
                print "###########"
    
            save_pdb_amber_model.append("END\n")
            save_pdb_amber_model.append("ENDMDL\n")
        
        noe_rest = self.findxml(xml_info, "noe")
        if len(noe_rest) > 0:
            for i in noe_rest:
                #print "####NOE_parsing####"
                #print os.path.basename(i.get("path"))
                #print check_noe_xplor(open(os.path.join(self.work_dir,"output", "output_1", os.path.basename(i.get("path"))), "r").readlines(), diz_amber)
                #print "###########"
                #print i.get("path")
                #print i.get("path").split(".")[:-1]
                #print i.get("path").split(".")[-1]
                #
                fin = os.path.basename(i.get("path"))
                print "####NOE_parsing PATH####"
                print os.path.join(self.analy_dir, fin.split("." + fin.split(".")[-1])[0] + "_amb." + fin.split(".")[-1])
                open(os.path.join(self.analy_dir, fin.split("." + fin.split(".")[-1])[0] + "_amb." + fin.split(".")[-1]), "w").writelines( check_noe_xplor(open(os.path.join(self.work_dir,"output", "output_1", os.path.basename(fin)), "r").readlines(), diz_amber))
                
        aco_rest = self.findxml(xml_info, "cdih")
        if len(aco_rest) > 0:
            for i in aco_rest:
                fin = os.path.basename(i.get("path"))
                print "####ACO_parsing PATH####"
                print os.path.join(self.analy_dir, fin.split("." + fin.split(".")[-1])[0] + "_amb." + fin.split(".")[-1])
                open(os.path.join(self.analy_dir, fin.split("." + fin.split(".")[-1])[0] + "_amb." + fin.split(".")[-1]), "w").writelines( check_noe_xplor(open(os.path.join(self.work_dir,"output", "output_1", os.path.basename(fin)), "r").readlines(), diz_amber))
                               

        pcs_rest = self.findxml(xml_info, "pcs")
        if len(pcs_rest) > 0:
            for i in pcs_rest:
                fin = os.path.basename(i.get("path"))
                print "####PCS_parsing PATH####"
                print os.path.join(self.analy_dir, fin.split("." + fin.split(".")[-1])[0] + "_amb." + fin.split(".")[-1])
                open(os.path.join(self.analy_dir, fin.split("." + fin.split(".")[-1])[0] + "_amb." + fin.split(".")[-1]), "w").writelines( check_noe_xplor(open(os.path.join(self.work_dir,"output", "output_1", os.path.basename(fin)), "r").readlines(), diz_amber))
                
        rdc_rest = self.findxml(xml_info, "rdc")
        if len(rdc_rest) > 0:
            for i in rdc_rest:
                fin = os.path.basename(i.get("path"))
                print "####RDC_parsing PATH####"
                print os.path.join(self.analy_dir, fin.split("." + fin.split(".")[-1])[0] + "_amb." + fin.split(".")[-1])
                open(os.path.join(self.analy_dir, fin.split("." + fin.split(".")[-1])[0] + "_amb." + fin.split(".")[-1]), "w").writelines( check_noe_xplor(open(os.path.join(self.work_dir,"output", "output_1", os.path.basename(fin)), "r").readlines(), diz_amber))
                
        
        open(os.path.join(self.analy_dir, "BESTMODELS.pdb"), "w").writelines(save_pdb_model)
        #remove ANI Atoms
        save_pdb_amber_model_no_ani = []
        for p in save_pdb_amber_model:
            if p[17:20] != "ANI":
                save_pdb_amber_model_no_ani.append(p)
        open(os.path.join(self.analy_dir, "ambermodels.pdb"), "w").writelines(save_pdb_amber_model_no_ani)
        
        return len(tokeep)


    def extractall(self, tf, path="."):
        for tarinfo in tf:
            if tarinfo.isdir():
                # Extract directories with a safe mode.
                tarinfo = copy.copy(tarinfo)
                tarinfo.mode = 0700
            tf.extract(tarinfo, path)
            
    def get_NOE(self, noe):
        save = False
        solonoe = []
        for i in noe:
            if "NOE_VIOL_END" in i:
                save = False
            if save:
                solonoe.append(i)
            if "NOE_VIOL_INI" in i and "X-PLOR>" not in i:
                save = True
        return solonoe
    
    def get_DIH(self, dih):
        save = False
        solodih = []
        for i in dih:
            if "DIH_VIOL_END" in i:
                save = False
            if save:
                solodih.append(i)
            if "DIH_VIOL_INI" in i and "X-PLOR>" not in i:
                save = True
        return solodih
   
    def get_PCS(self, pcs):
        save = False
        solopcs = []
        for i in pcs:
            if "PCS_VIOL_END" in i:
                save = False
            if save:
                solopcs.append(i)
            if "PCS_VIOL_INI" in i and "X-PLOR>" not in i:
                save = True
        return solopcs
    
    def get_RDC(self, rdc):
        save = False
        solordc = []
        for i in rdc:
            if "RDC_VIOL_END" in i:
                save = False
            if save:
                solordc.append(i)
            if "RDC_VIOL_INI" in i and "X-PLOR>" not in i:
                save = True
        return solordc
    
    def get_PCS_tens(self, pcs, fina):
        save = False
        solopcs = []
        tensor = {}
        root_pcs = etree.Element("tensor_pcs")
        for i in pcs:
            if "PCS_TENSOR_END" in i:
                save = False
            if save:
                solopcs.append(i)
            if "PCS_TENSOR_INI" in i and "X-PLOR>" not in i:
                save = True
        te ={}
        for i in range(len(fina)):
            findcls = "frun %d" %(i+1)
            for a in solopcs:
                if findcls in a:
                    print "PCS trovato"
                    save = True
                    te["class"] = "%d" %(i+1)
                    te["file"] = fina[i]
                if save and a.startswith("A1"):
                    te["A1"] = str(float(a.split()[2].replace(",","")))
                    print a
                if save and a.startswith("A2"):
                    print a
                    te["A2"] = str(float(a.split()[2].replace(",","")))
                    print te
                    save = False
                    etree.SubElement(root_pcs, "tensor_values", attrib = te)
                    te ={}       
        return root_pcs
    
    def get_RDC_tens(self, rdc, fina):
        save = False
        solordc = []
        tensor = {}
        root_rdc = etree.Element("tensor_rdc")
        for i in rdc:
            if "PCS_TENSOR_END" in i:
                save = False
            if save:
                solordc.append(i)
            if "PCS_TENSOR_INI" in i and "X-PLOR>" not in i:
                save = True
        te ={}
        for i in range(len(fina)):
            findcls = "frun %d" %(i+1)
            for a in solordc:
                if findcls in a:
                    print "RDC trovato"
                    save = True
                    te["class"] = "%d" %(i+1)
                    te["file"] = fina[i]
                if save and a.startswith("A1"):
                    te["A1"] = str(float(a.split()[2].replace(",","")))
                    print a
                if save and a.startswith("A2"):
                    print a
                    te["A2"] = str(float(a.split()[2].replace(",","")))
                    print te
                    save = False
                    etree.SubElement(root_rdc, "tensor_values", attrib = te)
                    te ={}       
        return root_rdc
    
    def dih_parsing(self, dih):
        ini_n = Suppress(Literal("========================================"))
        segid = Word(alphas) 
        resid = Word(nums,min=1,max=4) 
        resnam = Word(alphanums,min=1,max=4)
        atmnam = Word(alphanums,min=1,max=4)
        dihedral = Literal("Dihedral=")
        dihedral_val = Word(printables)
        energy = Literal("Energy=")
        energy_val = Word(printables)
        c = Literal("C=")
        c_val = Word(printables)
        equil = Literal("Equil=")
        equil_val = Word(printables)
        delta = Literal("Delta=")
        delta_val = Word(printables)
        rangex = Literal("Range=")
        rangex_val = Word(printables)
        exponent = Literal("Exponent=")
        exponent_val =  Word(printables)
        ai = Group(ZeroOrMore(segid).setResultsName("segid") + resid.setResultsName("resid") + resnam.setResultsName("resname") + atmnam.setResultsName("atomname")).setResultsName("atom_i")
        aj = Group(ZeroOrMore(segid).setResultsName("segid") + resid.setResultsName("resid") + resnam.setResultsName("resname") + atmnam.setResultsName("atomname")).setResultsName("atom_j")
        ak = Group(ZeroOrMore(segid).setResultsName("segid") + resid.setResultsName("resid") + resnam.setResultsName("resname") + atmnam.setResultsName("atomname")).setResultsName("atom_k")
        al = Group(ZeroOrMore(segid).setResultsName("segid") + resid.setResultsName("resid") + resnam.setResultsName("resname") + atmnam.setResultsName("atomname")).setResultsName("atom_l")
        string = Group(ini_n + ai + aj + ak + al + Suppress(dihedral) + dihedral_val.setResultsName("dih_val") + Suppress(energy) + energy_val.setResultsName("dih_ene") + Suppress(c) + c_val.setResultsName("dih_c") + Suppress(equil) + equil_val.setResultsName("dih_equil") + Suppress(delta) + delta_val.setResultsName("dih_delta") + Suppress(rangex) + rangex_val.setResultsName("dih_range") + Suppress(exponent) + exponent_val.setResultsName("dih_exp")).setResultsName("dih_vilolation")
        sexpr = string.searchString(dih)
    
        xml_viol = etree.fromstring(sexpr.asXML("DIH_violations"))
        return xml_viol

    def pcs_parsing(self, pcs):
        #inserire le CLASSI
        ini_n = Suppress(Literal("=============================================================="))
        m_atom = Literal("Set-M-atoms")
        n_atom = Literal("Set-N-atoms")
        segid = Word(alphas) 
        resid = Word(nums,min=1,max=4) 
        resnam = Word(alphanums,min=1,max=4)
        atmnam = Word(alphanums,min=1,max=4)
        calc = Literal("Calc:")
        calc_val = Word(printables)
        obs = Literal("Obs:")
        obs_val = Word(printables)
        error = Literal("Error:")
        error_val = Word(printables)
        delta = Literal("Delta:")
        delta_val = Word(printables)
        
        ai = Group(ZeroOrMore(segid).setResultsName("segid") + resid.setResultsName("resid") + resnam.setResultsName("resname") + atmnam.setResultsName("atomname")).setResultsName("atom_i")
        aj = Group(ZeroOrMore(segid).setResultsName("segid") + resid.setResultsName("resid") + resnam.setResultsName("resname") + atmnam.setResultsName("atomname")).setResultsName("atom_j")
       
        string = Group(ini_n + Suppress(m_atom) + ai + Suppress(n_atom) + aj + Suppress(calc) + calc_val.setResultsName("pcs_cal") + Suppress(obs) + obs_val.setResultsName("pcs_obs") + Suppress(error) + error_val.setResultsName("pcs_error") + Suppress(delta) + delta_val.setResultsName("pcs_delta") ).setResultsName("pcs_vilolation")
        sexpr = string.searchString(pcs)

        xml_viol = etree.fromstring(sexpr.asXML("pcs_violations"))
        return xml_viol
    
    def rdc_parsing(self, rdc):
        #inserire le CLASSI
        ini_n = Suppress(Literal("=============================================================="))
        m_atom = Literal("Set-M-atoms")
        n_atom = Literal("Set-N-atoms")
        segid = Word(alphas) 
        resid = Word(nums,min=1,max=4) 
        resnam = Word(alphanums,min=1,max=4)
        atmnam = Word(alphanums,min=1,max=4)
        calc = Literal("Calc:")
        calc_val = Word(printables)
        obs = Literal("Obs:")
        obs_val = Word(printables)
        error = Literal("Error:")
        error_val = Word(printables)
        delta = Literal("Delta:")
        delta_val = Word(printables)
        
        ai = Group(ZeroOrMore(segid).setResultsName("segid") + resid.setResultsName("resid") + resnam.setResultsName("resname") + atmnam.setResultsName("atomname")).setResultsName("atom_i")
        aj = Group(ZeroOrMore(segid).setResultsName("segid") + resid.setResultsName("resid") + resnam.setResultsName("resname") + atmnam.setResultsName("atomname")).setResultsName("atom_j")
       
        string = Group(ini_n + Suppress(m_atom) + ai + Suppress(n_atom) + aj + Suppress(calc) + calc_val.setResultsName("rdc_cal") + Suppress(obs) + obs_val.setResultsName("rdc_obs") + Suppress(error) + error_val.setResultsName("rdc_error") + Suppress(delta) + delta_val.setResultsName("rdc_delta") ).setResultsName("rdc_vilolation")
        sexpr = string.searchString(rdc)

        xml_viol = etree.fromstring(sexpr.asXML("rdc_violations"))
        return xml_viol
    
    def noe_parsing(self, xxx):
        class1 = Suppress(Literal("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"))
        class2_1 = Suppress(Literal("+++++++++++++++++++++++++++++++ CLASS"))
        class2_2 = Word(printables, exact=4).setResultsName("class_name")
        class2_3 = Suppress(Literal("+++++++++++++++++++++++++++++++++++"))
        class2 = class2_1 + class2_2 + class2_3
        class3 = Suppress(Literal("for this class: ") + Word(printables + " ") + Word(printables + " ") + Word(printables + " "))
        
        ini_n = Suppress(Regex(r"========== spectrum     1 restraint[ \t]*[0-9]+[ \t]*=========="))
        i_atom = Suppress(Literal("set-i-atoms"))
        segid = Word(alphas) 
        resid = Word(nums,min=1,max=4) 
        resnam = Word(alphanums,min=1,max=4)
        atmnam = Word(alphanums,min=1,max=4)
        j_atom = Suppress(Literal("set-j-atoms"))
        
        sele1 = Group(ZeroOrMore(segid).setResultsName("segid") + resid.setResultsName("resid") + resnam.setResultsName("resname") + atmnam.setResultsName("atomname")).setResultsName("atom")
        sele2 = Group(ZeroOrMore(segid).setResultsName("segid") + resid.setResultsName("resid") + resnam.setResultsName("resname") + atmnam.setResultsName("atomname")).setResultsName("atom")
        
        Rave = Literal("R<average>=")
        Rave_val = Word(printables)
        NOE = Literal("NOE=")
        NOE_val = Word(printables + " ", exact=20)
        Delta = Literal("Delta=")
        Delta_val = Word(printables)
        ENoe = Literal("E(NOE)=")
        ENoe_val = Word(printables)
        
        valres = Suppress(Rave) + Rave_val.setResultsName("Raverage") + Suppress(NOE) + NOE_val.setResultsName("NOE") + Suppress(Delta) + Delta_val.setResultsName("delta") + Suppress(ENoe) + ENoe_val.setResultsName("energy")
        
        cl_ini = class1 + class2 + class3
        string1 = Group(ini_n + Suppress(i_atom) +  Group(OneOrMore(sele1)).setResultsName("sele1") + Suppress(j_atom) + Group(OneOrMore(sele2)).setResultsName("sele2") + Group(valres).setResultsName("values")).setResultsName("NOE_violation")
        string2 = Group(cl_ini + OneOrMore(string1)).setResultsName("CLASS")

        sexpr = string2.searchString(xxx)
    
        xml_viol = etree.fromstring(sexpr.asXML("NOE_violations"))
        return xml_viol
        
    def __init__(self, work_dir):
        template = config['app_conf']['xplor_templ']
        self.XPLOR_HOME = "/prog/xplor-nih-2.29"
        self.work_dir = work_dir
        self.analy_dir = os.path.join(work_dir, "analysis")
        self.tmp_analy_dir = os.path.join(self.analy_dir, ".tmp")
        self.best_struc_list = []
        if not os.path.exists(self.analy_dir):
            os.makedirs(self.analy_dir)
        else:
            shutil.rmtree(self.analy_dir)
            os.makedirs(self.analy_dir)
            
        if not os.path.exists(self.tmp_analy_dir):
            os.makedirs(self.tmp_analy_dir)
        else:
            shutil.rmtree(self.tmp_analy_dir)
            os.makedirs(self.tmp_analy_dir)
        findl = []
        path = os.path.join(self.work_dir,"output")
        print_err(path, "FIND PATH")
        for root, dirs, names in os.walk(path):
           for name in names:
              if len(re.findall(r'sa1_[0-9]+.pdb', name) ) > 0:
                 print os.path.join(root, name)                 
                 findl.append(os.path.join(root, name))
        npd = 0
        print_err(findl, "FINDL")
        
        for i in findl:
           npd = npd + 1
           shutil.copy2(i, os.path.join(self.tmp_analy_dir, "sa%d.pdb"%npd))
        
        
        print "####BEST_STRUCT##########"
        numstruct = self.best_struct(self.tmp_analy_dir, 0.5)
        print "####BEST_STRUCT_END##########"
        #extract all file of the input in tmp directory

        tar = tarfile.open(os.path.join(self.work_dir,"input","input_1","in.tgz"), "r:gz")
        self.extractall(tar, self.tmp_analy_dir)
        
        print os.path.join(template, "analysis.inp"), os.path.join(self.tmp_analy_dir, "analysis.inp")
        
        replace_str(os.path.join(template, "analysis.inp"), os.path.join(self.tmp_analy_dir, "analysis.inp"), "Num_struct", numstruct )
        ana_par_in = open(os.path.join(self.tmp_analy_dir, "xplorPM.inp"))
        #print ana_par_in
        par_top = []
        read = False
        for ia in ana_par_in:
            if "BEGIN_COPY_ANALYSIS" in ia:
                read = True
                #print type(ia)
                #print type(par_top)
                par_top.append(ia)
            if read:
                par_top.append(ia)
            if "END_COPY_ANALYSIS" in ia:
                read = False
        print_err(par_top, "PAR_TOP")
        
        join_par = "".join("%s" % i for i in par_top)
        #print "############PARTOP##############"
        #print join_par
        #print "############PARTOP END##############"
        print_err(join_par,"JOIN_PAR")
        replace_str(os.path.join(self.tmp_analy_dir, "analysis.inp"), os.path.join(self.tmp_analy_dir, "analysis.inp"), "!TOP_PAR", join_par)
        
        pcs_class = []
        check = False
        for t in join_par.split("\n"):    
            if t.startswith("xpcs"):
                check = True
            if check:
                if "end" in t.split("!")[0]:
                    check = False
                if t.startswith("@"):
                    pcs_class.append(t.replace("@", ""))
        
        pcs_t = []            
        if len(pcs_class) > 0:
            pcs_t.append("xpcs \n")
            n_pcs = 0
            for cl in pcs_class:
                pcs_t.append("frun %d \n" %(n_pcs + 1))
            pcs_t.append("end \n")
        pcstensor_anal = "".join("%s" % i for i in pcs_t)
        
        rdc_class = []
        check = False
        for t in join_par.split("\n"):    
            if t.startswith("xrdc"):
                check = True
            if check:
                if "end" in t.split("!")[0]:
                    check = False
                if t.startswith("@"):
                    rdc_class.append(t.replace("@", ""))
        
        rdc_t = []           
        if len(rdc_class) > 0:
            rdc_t.append("xrdc \n")
            n_rdc = 0
            for cl in rdc_class:
                rdc_t.append("frun %d \n" %(n_rdc + 1))
            rdc_t.append("end \n")
        rdctensor_anal = "".join("%s" % i for i in rdc_t)
        
        replace_str(os.path.join(self.tmp_analy_dir, "analysis.inp"), os.path.join(self.tmp_analy_dir, "analysis.inp"), "!PCS_TENSOR", pcstensor_anal)
        replace_str(os.path.join(self.tmp_analy_dir, "analysis.inp"), os.path.join(self.tmp_analy_dir, "analysis.inp"), "!RDC_TENSOR", rdctensor_anal)
        os.environ['TOPPAR'] = os.path.join('%s'%self.XPLOR_HOME, "toppar")
        os.environ['PATH'] += os.pathsep + self.XPLOR_HOME  
        exe_path = os.path.join(self.XPLOR_HOME, "bin", "xplor")
        cmd = "cd %s ; export PATH=$PATH:/bin; %s < analysis.inp > out_analysis" % (self.tmp_analy_dir, exe_path)
        print cmd
        jP = JobsProcessing()
        jP.exec_cmd(cmd,self.work_dir)
        out_anal = open(os.path.join(self.tmp_analy_dir, "out_analysis"),"r").readlines()
        result_anal = {}
        save = False
        viol_anal = []
        root = etree.Element("analysis")
        for i in out_anal:
            if "VIOLATIONS_INI" in i and "X-PLOR>" not in i:
                #print i
                struct_name = i.split()[2]
                save = True
            if save:
                viol_anal.append(i)
            if "VIOLATIONS_END" in i:
                te = {}
                te["file"] = struct_name
                #RDC
                rdc_anal =  self.get_RDC(viol_anal)
                if len(rdc_anal) > 3:
                    self.fit_fanta_rdc(struct_name)
                    rdc_xml = etree.SubElement(root, "RDC_pdb", attrib = te)
                    print "####### RDC ANALYSIS INI####"
                    print "PDB -> " + struct_name
                    #print "".join("%s" % ia for ia in dih_anal)
                    print "####### RDC ANALYSIS END####"
                    rdc_xml.append(self.get_RDC_tens(viol_anal, rdc_class))
                    rdc_xml.append(self.rdc_parsing("".join("%s" % ia for ia in rdc_anal )))
                    
                save = False
                #PCS
                pcs_anal =  self.get_PCS(viol_anal)
                if len(pcs_anal) > 3:
                    self.fit_fanta_pcs(struct_name)
                    pcs_xml = etree.SubElement(root, "PCS_pdb", attrib = te)
                    print "####### PCS ANALYSIS INI####"
                    print "PDB -> " + struct_name
                    #print "".join("%s" % ia for ia in dih_anal)
                    print "####### PCS ANALYSIS END####"
                    pcs_xml.append(self.get_PCS_tens(viol_anal, pcs_class))
                    pcs_xml.append(self.pcs_parsing("".join("%s" % ia for ia in pcs_anal )))
                    
                save = False
                #DIH
                dih_anal =  self.get_DIH(viol_anal)
                if len(dih_anal) > 3:
                    dih_xml = etree.SubElement(root, "DIH_pdb", attrib = te)
                    print "####### DIH ANALYSIS INI####"
                    print "PDB -> " + struct_name
                    #print "".join("%s" % ia for ia in dih_anal)
                    print "####### DIH ANALYSIS END####"
                    dih_xml.append(self.dih_parsing("".join("%s" % ia for ia in dih_anal )))
                    
                save = False
                #NOE
                noe_anal = self.get_NOE(viol_anal)
                #print "#################NOE#################"
                #print noe_anal
                if len(noe_anal) > 3:
                    noe_xml = etree.SubElement(root, "NOE_pdb", attrib = te)
                    print "####### NOE ANALYSIS INI####"
                    print "PDB -> " + struct_name
                    #print "".join("%s" % ia for ia in noe_anal)
                    print "####### NOE ANALYSIS END####"
                    noe_xml.append(self.noe_parsing("".join("%s" % ia for ia in noe_anal )))
                save = False
                viol_anal = []
                

        xml_file_w = open(os.path.join(work_dir, "analysis", "analysis.xml"), 'w')
        xml_file_w.write(etree.tostring(root, pretty_print=True))
        xml_file_w.close()
        self.plot_res(os.path.join(work_dir, "analysis", "analysis.xml"), os.path.join(work_dir, "analysis"))
        
class iter_res:
    def __init__(self, pdb):
        self.pdb_save = pdb[:]
        self.pdb = pdb[:]
        self.count = 0
    def __iter__(self):
        return self
    def next(self):    
        retres = []
        #print len(self.pdb)
        if len(self.pdb) == 0:
            raise StopIteration()           
        pdb_c = self.pdb[:]
        for i in range(len(self.pdb)):
            #print i, len(self.pdb), self.count
            #print self.pdb[i]
            if self.pdb[i].startswith("ATOM"):
                if self.count == 0:
                    self.count = int(self.pdb[i][22:26].strip())
                if int(self.pdb[i][22:26].strip()) != self.count:
                    self.count = int(self.pdb[i][22:26].strip())
                    self.pdb = pdb_c[:]   
                    return retres
                if int(self.pdb[i][22:26].strip()) == self.count:
                    retres.append(self.pdb[i])
                    pdb_c.pop(0)
                    if len(pdb_c) == 0:
                        self.pdb = pdb_c[:]   
                        return retres           
            elif self.pdb[i].startswith("TER") :
                pdb_c.pop(0)
                self.pdb = pdb_c[:]
                if len(retres) > 0:
                    return retres
                else:
                    raise StopIteration()
            elif self.pdb[i].startswith("END"):
                pdb_c.pop(0)
                self.pdb = pdb_c[:]
                if len(retres) > 0:
                    return retres
                else:
                    raise StopIteration()
                
            else:
                pdb_c.pop(0)
            
    def get_res(self, resnu, segid):
        retres = []
        for i in self.pdb_save:
            if i.startswith("ATOM") and i[22:26].strip() == resnu.strip() and i[72:76].strip() == segid.strip() :
                retres.append(i)
        return retres
