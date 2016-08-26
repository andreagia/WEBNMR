#!/usr/bin/env python
import cnvx
from lxml import etree
import string
from pyparsing import *
import os
import pprint
import sys

#def check_noe_xplor(self, xmlin):
    #print etree.tostring(xmlin, pretty_print=True)
    #
    #for elt in xmlin.getiterator():
    #    if elt.tag == "noe":
    #        f_noe = elt.get('filename')
    #        ini_num = elt.get('number')
    #
    #print f_noe
    
noe_in = "/home/andrea/pylons/amber_md/data/amber_data/aug20_1908.upl"
#if os.path.exists(noe_in):
#    os.remove(noe_in)
num = Word(nums+".")

##num = Regex(r"[0-9]+\.[0-9]*")
#resinu = Word(nums)
#resina = Word(alphas+"+"+"-")
##resina = Regex(r"[A-Z0-9][A-Z0-9][A-Z0-9][ +-]")
##resinu = Word(nums)
##resinu = Regex(r"[0-9][0-9]*")
#atmna = Regex(r"[A-Z0-9][A-Z0-9][ A-Z0-9][ A-Z0-9]")
#
## 1 LYS+ HN      1 LYS+ HA      5.60 
##resi1 = Group(resinu + resina + stringEnd).setResultsName("resid1")
#
##pr1 = resi1 + OneOrMore(atmna.setResultsName("atm1") + Group(resinu + resina + atmna).setResultsName("resid2") + num.setResultsName("value"))
##pr = pr1.setResultsName("selection")
#pr = (resinu + resina ) | (atmna + resinu + resina + atmna + num)
##all1 = Group(atmna + resinu + resina + atmna + num)
##pr =   resi1
##pr = all1

#LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR = map(Suppress, "()[]{}|")
#bytes = Word(printables)
#assi = Suppress(Regex(r"[aA][sS][sS][iI][a-z A-Z]*[a-z A-Z]*")).setResultsName("selection")
#num = Word(nums+".")
#numf = Group(num.setResultsName("D") + num.setResultsName("D_minus") + num.setResultsName("D_plus"))
#word = Word(alphanums+'"*#+%')
#sand = Regex(r"[aA][nN][dD]")
#sor =  Regex(r"[oO][rR]")
#cond = Suppress(sand | sor)
#name = Suppress(Regex(r"[nN][aA][mM][eE]")) + Word(alphanums+'"*#+%').setResultsName("name")
#resid = Suppress(Regex(r"[rR][eE][sS][iI][a-z A-Z]*")) + Word(nums).setResultsName("resid")
#
#seidvoid = Literal('"    "')
#seidn = Group('"' + word + '"')
#seid = seidvoid | seidn
##seid =  ZeroOrMore(Word(alphanums+'"*#+% ') )
#
#segid = Suppress(Regex(r"[sS][eE][gG][iI]*[a-z A-Z]") + seid)
#trash = Suppress(LBRC + word + RBRC)
#
#simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + Optional(name) + Optional(cond)
#simpleString2 = OneOrMore(name + Optional(cond) )
#
#simpleString = simpleString1 | simpleString2
#
#display = LBRK + simpleString + RBRK
#string_ = Optional(display) + simpleString
#
#sexp = Forward()
#sexpList = Group(LPAR + ZeroOrMore(sexp) + RPAR)
#sexp << ( string_ | sexpList )
#
#pr = assi + Optional(trash) + sexp.setResultsName("sel1") + sexp.setResultsName("sel2") + numf 

#file = open(noe_in,"r")
#file_r = []
#for i in file:
#    
#    file_r.append(i.split('#')[0])
##file_r = file.readlines()
#xxx = ''.join(i for i in file_r)


xxx = """  1 LYS+
         HN      1 LYS+ HA      5.60 
         HN      1 LYS+ HB2     7.00  
         HN      1 LYS+ HB3     7.00  
         HN      1 LYS+ QG      6.70  
         HN      1 LYS+ QD      7.60  
         HN      2 SER  HN      7.00  
         HA      1 LYS+ HB2     3.20 
         HA      1 LYS+ HB3     4.10 
         HA      1 LYS+ QG      5.60  
         HA      1 LYS+ QD      5.80  
         HB2     1 LYS+ QG      4.90  
         HB2     1 LYS+ QD      4.70  
         HB3     1 LYS+ QG      4.50  
         HB3     1 LYS+ QD      4.40  
         QG      1 LYS+ QD      5.00  
         QD      1 LYS+ QE      7.30  
         QD      2 SER  HN      8.00  
  2 SER
         HN      2 SER  HA      3.50  
         HN      2 SER  HB2     3.20  
         HN      2 SER  HB3     3.70  
         HN      3 PRO  QD      8.00  
         HN      4 GLU- HN      7.00  
         HN      5 GLU- HN      5.20  
         HN      5 GLU- HA      7.00  
         HN      5 GLU- HB2     4.80  
         HN      5 GLU- HB3     4.20  
         HN      5 GLU- HG2     7.00 
         HN      5 GLU- HG3     4.60 
         HN      6 LEU  HN      7.00  
         HA      2 SER  HB2     3.30 
         HA      2 SER  HB3     4.10 
         HA      3 PRO  QD      5.00  
         HA      4 GLU- HN      5.30  
         HB2     4 GLU- HN      6.60 
         HB2     5 GLU- HN      6.80  
""".splitlines()
#print xxx
xxx = open(noe_in,"r").readlines()

root = etree.Element("noe")
for t in xxx:
    if len(t) > 0:
        sd = t.split("#")[0].replace(">","").replace("<","")
        sf = sd.split()
        if len(sf) == 2 and sf[0].isdigit():
            sel = etree.SubElement(root, "selection")
            resnu1 = sf[0]
            resna1 = sf[1]
            
        if len(sf) >= 5 and not sf[0].isdigit():
            if sf[1].isdigit():
                atm1 = sf[0]  
                resnu2 = sf[1]
                resna1 = sf[2]
                atm2 = sf[3]
                
                if atm1[0] == "Q":
                    atm1 = "H"+atm1[1]+"#"
                if atm1[0] == "Q" and atm1[1] == "Q":
                    if resna1 == "LEU":
                        atm1 = "CG"
                    if resna1 == "VAL":
                        atm1 = "CB"
                        
                if atm2[0] == "Q":
                    atm2 = "H"+atm2[1]+"#"
                if atm2[0] == "Q" and atm2[1] == "Q":
                    if resna2 == "LEU":
                        atm2 = "CG"
                    if resna2 == "VAL":
                        atm2 = "CB"
                        
                val = sf[4]
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
        if len(sf) >= 7 and sf[0].isdigit():
            if sf[3].isdigit():
                sel = etree.SubElement(root, "selection")
                resnu1 = sf[0]
                resna1 = sf[1]
                atm1 = sf[0]
                resnu2 = sf[1]
                resna1 = sf[2]
                atm2 = sf[3]
                
                if atm1[0] == Q:
                    atm1 = "H"+atm1[1]+"#"
                if atm1[0] == Q and atm1[1] == Q:
                    if resna1 == "LEU":
                        atm1 = "CG"
                    if resna1 == "VAL":
                        atm1 = "CB"
                        
                if atm2[0] == Q:
                    atm2 = "H"+atm2[1]+"#"
                if atm2[0] == Q and atm2[1] == Q:
                    if resna2 == "LEU":
                        atm2 = "CG"
                    if resna2 == "VAL":
                        atm2 = "CB"
                        
                val = sf[4]
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

print etree.tostring(root, pretty_print=True)

conto = 0
for elt in root.getiterator():
    #print elt.tag
    if elt.tag == "sel1" or elt.tag == "sel2":
        conto += 1
print conto/2
#xml = """<noe>
#  <selection>
#    <sel1>
#      <resid>1</resid>
#      <name>HG2#</name>
#    </sel1>
#    <sel2>
#      <resid>1</resid>
#      <name>HG22</name>
#    </sel2>
#    <D>
#      <D>3.02</D>
#      <D_minus>1.32</D_minus>
#      <D_plus>1.00</D_plus>
#    </D>
#  </selection>

sys.exit()
sexpr = pr.searchString(xxx)
pprint.pprint(sexpr.asList())

print sexpr.asXML("noe")

conto = 0
for elt in etree.fromstring(sexpr.asXML("noe")).getiterator():
    #print elt.tag
    if elt.tag == "resid1" or elt.tag == "resid2":
        conto += 1
print conto
        
        
    
#def remove_item(xml):
#    #remove xml entry of nasted braket
#    join_char=''
#    for i in xml.splitlines():
#        if not ("<ITEM>" in i or "</ITEM>" in i):
#            #print i
#            join_char += i + "\n"
#    return join_char
#
#
#         
#xml_noe = etree.fromstring(remove_item(sexpr.asXML("noe")))
#
#pdb_out = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "out_leap.pdb")
#pdb_ref_n = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "pdb.ref")
#
#
#xml_file = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "xml_noe")
#xml_file_w = open(xml_file, 'w')
#xml_file_w.write(remove_item(sexpr.asXML("noe")))
#xml_file_w.close()
#
#print pdb_out
#print pdb_ref_n
#print etree.tostring(xml_noe, pretty_print=True)
#
#resu_vx = cnvx.convert(xml_noe, ini_num, pdb_out, pdb_ref_n)
##return resu_vx
#return remove_item(sexpr.asXML("noe"))


#xml = """<noe>
#  <selection>
#    <sel1>
#      <resid>1</resid>
#      <name>HG2#</name>
#    </sel1>
#    <sel2>
#      <resid>1</resid>
#      <name>HG22</name>
#    </sel2>
#    <D>
#      <D>3.02</D>
#      <D_minus>1.32</D_minus>
#      <D_plus>1.00</D_plus>
#    </D>
#  </selection>
#  <selection>
#    <sel1>
#      <resid>1</resid>
#      <name>HG2#</name>
#    </sel1>
#    <sel2>
#      <resid>1</resid>
#      <name>HG2#</name>
#    </sel2>
#    <D>
#      <D>3.02</D>
#      <D_minus>1.32</D_minus>
#      <D_plus>1.00</D_plus>
#    </D>
#  </selection>
#  <selection>
#    <sel1>
#      <resid>1</resid>
#      <name>HS</name>
#    </sel1>
#    <sel2>
#      <resid>59</resid>
#      <name>HA</name>
#    </sel2>
#    <D>
#      <D>5.68</D>
#      <D_minus>3.98</D_minus>
#      <D_plus>1.00</D_plus>
#    </D>
#  </selection>
#  <selection>
#    <sel1>
#      <resid>1</resid>
#      <name>HA</name>
#    </sel1>
#    <sel2>
#      <resid>62</resid>
#      <name>HB1</name>
#    </sel2>
#    <D>
#      <D>5.69</D>
#      <D_minus>3.99</D_minus>
#      <D_plus>1.00</D_plus>
#    </D>
#  </selection>
#  <selection>
#    <sel1>
#      <resid>1</resid>
#      <name>HB</name>
#    </sel1>
#    <sel2>
#      <resid>1</resid>
#      <name>HG11</name>
#    </sel2>
#    <D>
#      <D>3.03</D>
#      <D_minus>1.33</D_minus>
#      <D_plus>1.00</D_plus>
#    </D>
#  </selection>
#  <selection>
#    <sel1>
#      <resid>1</resid>
#      <name>HB</name>
#    </sel1>
#    <sel2>
#      <resid>1</resid>
#      <name>HG22</name>
#    </sel2>
#    <D>
#      <D>2.41</D>
#      <D_minus>0.71</D_minus>
#      <D_plus>1.00</D_plus>
#    </D>
#  </selection>
#  <selection>
#    <sel1>
#      <resid>1</resid>
#      <name>HB</name>
#    </sel1>
#    <sel2>
#      <resid>1</resid>
#      <name>HS2</name>
#    </sel2>
#    <D>
#      <D>2.64</D>
#      <D_minus>0.94</D_minus>
#      <D_plus>1.00</D_plus>
#    </D>
#  </selection>
#  <selection>
#    <sel1>
#      <resid>1</resid>
#      <name>HB</name>
#    </sel1>
#    <sel2>
#      <resid>1</resid>
#      <name>HT3</name>
#    </sel2>
#    <D>
#      <D>3.52</D>
#      <D_minus>1.82</D_minus>
#      <D_plus>1.00</D_plus>
#    </D>
#  </selection>
#</noe>
#"""
#
#xml_noe = etree.fromstring(xml)
#pdb_out = "/home/andrea/pylons/amber_md/data/amber_data/841439256/out_leap.pdb"
#pdb_ref_n = '/home/andrea/pylons/amber_md/data/amber_data/841439256/pdb.ref'
#
#resu_vx = cnvx.convert(xml_noe, "1", pdb_out, pdb_ref_n)

