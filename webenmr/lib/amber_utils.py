from lxml import etree
from pylons import config, session
import os
from numpy import matrix
from numpy import linalg
from numpy import linalg as LA
import tarfile
import StringIO
import re

ff_type = ["amber", "iupac", "cns", "dyana", "pdbf1", "uniov31"]
amber_C = set(["H1","H2","H3","O","OXT"])
amber_N = set(["O","OXT","HN]"])
amber_O = set(["H1","H2","H3","O"])


iupac_C = set(["H1","H2","H3","O'","O''","HT","NT"])
iupac_N = set(["O'","O''","HT","NT","H"])
iupac_O = set(["H1","H2","H3","O","HT","NT"])

cns_C   = set(["HT1","HT2","HT3","OT1","OT2"])
cns_N   = set(["OT1","OT2","HN]"])
cns_O   = set(["HT1","HT2","HT3","O"])

dyana_C = set(["H1","H2","H3","O","OXT"])
dyana_N = set(["O","OXT","HN]"])
dyana_O = set(["H1","H2","H3","O"])

pdbf1_C   = set(["H1","H2","H3","O","OXT"])
pdbf1_N   = set(["O","OXT","H]"])
pdbf1_O   = set(["H1","H2","H3","O"])

uniov31_C = set(["H1","H2","H3","O'","O''","HT","NT"])
uniov31_N = set(["O'","O''","HT","NT","H"])
uniov31_O = set(["H1","H2","H3","O","HT","NT"])

def check_v(inv):   
    try:
        if not inv[0]:
            return False
        else:
            return True
    except:
        return False 
       
def set2str(pp):
    out= ""
    for i in pp:
        out += "%-5s" % i
    return out

def list2txt(pp):
    out= ""
    for i in pp:
        out += i + "\n"
    return out

def create_map(ffin, ffout, tpdbx):
    map_pdb = {}
    for elt in tpdbx.getiterator():
        if elt.tag == "residue":
            resni = elt.get("%s_name" %ffin)
            resno = elt.get("%s_name" %ffout)
            for ty in elt:
                if ty.tag == "atom":
                    atmi = ty.get("%s_name" %ffin )
                    atmo = ty.get("%s_name" %ffout )
                    map_pdb["%s:%s" %(resni, atmi)] = "%s:%s" %(resno, atmo)

    return map_pdb
    
def conv_name(rna, pana, map_pdb):
    
    se = "%s:%s" % (rna, pana)
    if se in map_pdb:
        oana = map_pdb[se].split(":")[1]
    else:
        oana = rna + " not found in any ff"
    return oana


def conv_name_old(ffin, ffout, rna, pana, tpdbx):
    
    if pana[0].isdigit():
        ana = pana[1:] + pana[0]
    else:
        ana = pana
    
    oana = ""
    w_rna = 0
    #for eiu in iupac.getiterator():
    #    if eiu.tag == "residue":
    #        if eiu.get("name") == res1:
    #            iuinfo = eiu
    for elt in tpdbx.getiterator():
        if elt.tag == "residue":
            for ty in ff_type:
                if elt.get("%s_name" %ty ) == rna:
                    w_rna = 1
                    #print "trovato in %s" %ty
                    len_res = 0
                    for elt1 in elt.getiterator():
                        if elt1.tag == "atom":                            
                            if ty == ffin:
                                if elt1.get("%s_name" %ty) == ana:
                                    oana = elt1.get("%s_name" %ffout)
    if w_rna == 0 and oana == "":
        return rna + " not found in any ff"
    else:
        return oana

def check_res(resp, res1, nco, tpdbx):
    print " ******************************************"
    print "          ESEGUO CHECK_RES                 "
    print " ******************************************"
    
    atm_loos = {"amber" : 0, "iupac" : 0,"cns" : 0, "dyana" : 0 , "pdbf1" : 0 , "uniov31" : 0}
    
    atmte_a = []
    atmte_i = []
    atmte_c = []
    atmte_d = []
    atmte_p1 = []
    atmte_u = []
    
    res = []
    for i in resp:
    #    if i[0].isdigit():
    #        res.append(i[1:]+i[0])
    #    else:
            res.append(i)
            
    #for eiu in iupac.getiterator():
    #    if eiu.tag == "residue":
    #        if eiu.get("name") == res1:
    #            iuinfo = eiu
            
    for elt in tpdbx.getiterator():
        if elt.tag == "residue":
            for ty in ff_type:
                if elt.get("%s_name" %ty ) == res1:
                    #print "trovato in %s" %ty
                    len_res = 0
                    for elt1 in elt.getiterator():
                        if elt1.tag == "atom":
                            
                            if ty == "amber":
                                if elt1.get("%s_name" %ty) != "None":
                                    atmte_a.append(elt1.get("%s_name" %ty))
                                    
                            if ty == "iupac":
                                if elt1.get("%s_name" %ty) != "None":
                                    atmte_i.append(elt1.get("%s_name" %ty))                                
                                
                            if ty == "cns":
                                if elt1.get("%s_name" %ty) != "None":
                                    atmte_c.append(elt1.get("%s_name" %ty))                               
                                        
                            if ty == "dyana":
                                if elt1.get("%s_name" %ty) != "None":
                                    atmte_d.append(elt1.get("%s_name" %ty))
                                    
                            if ty == "pdbf1":
                                if elt1.get("%s_name" %ty) != "None":
                                    atmte_p1.append(elt1.get("%s_name" %ty))
                                    
                            if ty == "uniov31":
                                if elt1.get("%s_name" %ty) != "None":
                                    atmte_u.append(elt1.get("%s_name" %ty))
                                    
                            len_res += 1
    
    satmte_a = set(atmte_a)                      
    satmte_i = set(atmte_i)
    satmte_c = set(atmte_c)
    satmte_d = set(atmte_d)
    satmte_p1 = set(atmte_p1)
    satmte_u = set(atmte_u)
    
    if nco == "N":
        satmte_a = satmte_a.difference(amber_N)
        satmte_i = satmte_i.difference(iupac_N)
        satmte_c = satmte_c.difference(cns_N)
        satmte_d = satmte_d.difference(dyana_N)
        satmte_p1 = satmte_p1.difference(pdbf1_N)
        satmte_u = satmte_u.difference(uniov31_N)
        satmte_d.add("O")
    if nco == "C":
        satmte_a = satmte_a.difference(amber_C)
        satmte_i = satmte_i.difference(iupac_C)
        satmte_c = satmte_c.difference(cns_C)
        satmte_d = satmte_d.difference(dyana_C)
        satmte_p1 = satmte_p1.difference(pdbf1_C)
        satmte_u = satmte_u.difference(uniov31_C)
        satmte_d.add("O")
    if nco == "O":
        satmte_a = satmte_a.difference(amber_O)
        satmte_i = satmte_i.difference(iupac_O)
        satmte_c = satmte_c.difference(cns_O)
        satmte_d = satmte_d.difference(dyana_O)
        satmte_p1 = satmte_p1.difference(pdbf1_O)
        satmte_u = satmte_u.difference(uniov31_O)
        satmte_d.add("O")
        
    #print set(res)
    #print res
    #print str(len(res)) + " " + str(len(satmte_i))
    #print satmte_i
    #print len(satmte_i)
    #print set(res).issubset(satmte_i)
    #print satmte_c
    #print set(res).issubset(satmte_c)
    #print satmte_d
    #print set(res).issubset(satmte_d)
    #print len_res
    
    set_ff = {}
    set_ff["amber"] = len(set(res).difference(satmte_a))
    set_ff["iupac"] = len(set(res).difference(satmte_i))
    set_ff["cns"] = len(set(res).difference(satmte_c))
    set_ff["dyana"] = len(set(res).difference(satmte_d))
    set_ff["pdbf1"] = len(set(res).difference(satmte_p1))
    set_ff["uniov31"] = len(set(res).difference(satmte_u))
    
    te = {}
    te["resname"] = res1
    te["type"] = nco
    te["NMAtom"] = str(len(satmte_i) - len(res) )
    
    root = etree.Element("status", te)
    te={}
    te['force_filed'] = "amber"
    if len(set(res).difference(satmte_a)) > 0:
        etree.SubElement(root, "Atom_not_found",te).text  = set2str(set(res).difference(satmte_a))
        atm_loos["amber"] += len(set2str(set(res).difference(satmte_a)).split())
    te={}
    te['force_filed'] = "iupac"
    if len(set(res).difference(satmte_i)) > 0:
        etree.SubElement(root, "Atom_not_found",te).text  = set2str(set(res).difference(satmte_i))
        atm_loos["iupac"] += len(set2str(set(res).difference(satmte_i)).split())
    te={}
    te['force_filed'] = "cns"
    if len(set(res).difference(satmte_c)) > 0:
        etree.SubElement(root, "Atom_not_found",te).text = set2str(set(res).difference(satmte_c))
        atm_loos["cns"] += len(set2str(set(res).difference(satmte_c)).split())
    te={}
    te['force_filed'] = "dyana"
    if len(set(res).difference(satmte_d)) > 0:
        etree.SubElement(root, "Atom_not_found",te).text = set2str(set(res).difference(satmte_d))
        atm_loos["dyana"] += len(set2str(set(res).difference(satmte_d)).split())
    te={}
    te['force_filed'] = "pdbf1"
    if len(set(res).difference(satmte_p1)) > 0:
        etree.SubElement(root, "Atom_not_found",te).text = set2str(set(res).difference(satmte_p1))
        atm_loos["pdbf1"] += len(set2str(set(res).difference(satmte_p1)).split())
    
    te={}
    te['force_filed'] = "uniov31"
    if len(set(res).difference(satmte_u)) > 0:
        etree.SubElement(root, "Atom_not_found",te).text = set2str(set(res).difference(satmte_u))
        atm_loos["uniov31"] += len(set2str(set(res).difference(satmte_u)).split())
        
    print set2str(satmte_i )
    print set2str(satmte_c )
    print set2str(satmte_d )
    print set2str(satmte_p1 )
    print set2str(satmte_u )
    
        
    print etree.tostring(root, pretty_print=True)
    
    #return sorted([(value,key) for (key,value) in set_ff.items()])[0][1]
    return atm_loos

class model2tar:
    
    def __init__(self, fileobj):
        self.seq = fileobj.readlines(  )
        self.line_num = 0    # current index into self.seq (line number)
        self.para_num = 0    # current index into self (paragraph number)


    def __getitem__(self, index):   
        separator=re.compile("MODEL|MODEL \d")
        if index != self.para_num:
            raise TypeError, "Only sequential access supported"
        self.para_num += 1
        while 1:
            line = self.seq[self.line_num]
            self.line_num += 1
            if not separator.match(line): break
        result = [line]
        while 1:
            try:
                line = self.seq[self.line_num]
            except IndexError:
                break
            self.line_num += 1
            if  separator.match(line): break
            if  line.startswith("TER"):
                line = "TER\n"
            result.append(line)
        return ''.join(result)

def extract_model2tar(filename, numpars=100):
    pp = model2tar(open(filename))
    if os.path.exists(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "multijobs.tgz")):
        os.remove(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "multijobs.tgz"))
    tar = tarfile.open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "multijobs.tgz"),"w:gz")
    npdb = 0
    
    for p in pp:
        print "Par#%d, line# %d:" % (
            pp.para_num, pp.line_num)
        if pp.para_num>numpars: break
        check_atom = 0
        
        for i in p.split("\n"):
            if i.startswith("ATOM"):
                check_atom += 1
        
        if check_atom > 1:
            npdb = npdb + 1
            tarinfo = tarfile.TarInfo('pdb_%d.pdb'%npdb)
            tarinfo.size = len(p)
            tar.addfile(tarinfo, StringIO.StringIO(p))
            
    tar.close()
    print os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "multijobs.tgz")
    return npdb

def check_pdb(f_pdb):
    in_pdb = open(f_pdb, 'r').readlines()
    if os.path.exists(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "multijobs.tgz")):
        os.remove(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "multijobs.tgz"))
    num_model = 0
    for i in in_pdb:
        if i.startswith("MODEL"):
                num_model += 1
    if num_model > 1:
        num_model_pdb = extract_model2tar(f_pdb)
    else:
        num_model_pdb = 1
    #response.headers['content-type'] = 'text/xml; charset=utf-8'
    tpdbx = etree.parse(os.path.join(config['app_conf']['amber_data'],"atomnames.xml"))
    #iupac = etree.parse(os.path.join(config['app_conf']['amber_data'],"atomnames.xml"))
    warning = []
    info = []
    info.append("Number of model found in pdb: %d" %num_model_pdb)
    model = 0
    rnconf = 100000
    res = []
    error = []
    end = 0
    rn = ""
    ter = 1
    c_ff = []
    
    model_switch = True
    
    model_find = False
    # check and change name on HIS depending on the protonations following amber ff rules
    # HD1 -> HID | HE2 -> HIE | HD1,HE2 -> HIP
    prim_res = 0
    list_repl = {}
    model_f = 0
    first_res = True
    rnu_old = 1000000
    ter_contr = 0
    ter_old = 0
    for i in in_pdb:
        
        if  'TER ' in i[0:6]:
                ter_contr += 1
                
        if 'MODEL' in i[0:6]:
            model_f = model_f + 1
            
        if 'ATOM' in i[0:6] and model_f <= 1 :
                si = i.split()
                try:
                    anu = int(i[6:11])
                except:
                    #error.append("line %s have some format problem")
                    anu = 1
                ana = i[12:17].replace(" ","")
                rna = i[17:21].replace(" ","")
                try:
                    rnu = int(i[22:26])
                except:
                    #error.append("line %s have some format problem")
                    rnu = 1
                if rnu > rnu_old:
                    first_res = False
                    
                if first_res:
                    if ana == "H" or ana == "H1" or ana == "H2" or ana == "H3" or ana == "1H" or ana == "2H" or ana == "3H" or ana == "HT1" or ana == "HT2" or ana == "HT3":
                        in_pdb.remove(i)
                rnu_old = rnu
                
                if rna == "HIS" and ana == "HD1":
                    if i[17:26] in list_repl:
                        list_repl[i[17:26]]=i[17:26].replace("HIS", "HIP")
                    else:
                        list_repl[i[17:26]]=i[17:26].replace("HIS", "HID")
                        
                if rna == "HIS" and ana == "HE2":
                    if i[17:26] in list_repl:
                        list_repl[i[17:26]]=i[17:26].replace("HIS", "HIP")
                    else:
                        list_repl[i[17:26]]=i[17:26].replace("HIS", "HIE")
                        
        if ter_contr != ter_old:
            first_res = True
        ter_old = ter_contr
            
    print list_repl
    ch_pdb = in_pdb
    in_pdb = []
    for i in ch_pdb:
        if i[17:26] in list_repl:
            in_pdb.append(i.replace(i[17:26], list_repl[i[17:26]]))
        else:
            in_pdb.append(i)
    
    open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "out_HIS_coverted.pdb"),"w").writelines(in_pdb)
    tot_atm_loos = {"amber" : 0, "iupac" : 0,"cns" : 0, "dyana" : 0 , "pdbf1" : 0 , "uniov31" : 0}
    for i in in_pdb:
        if len(i) > 0:
            
            if 'MODEL' in i[0:6] and not model_find:
                model_find = True
            elif 'MODEL' in i[0:6] and model_find:
                model_switch = False
                
            if 'HETATM' in i[0:6] and model_switch:
                warning.append("%s are not included in standard amber ff please use ligand session" %i[0:15] )
                    
            if  'TER ' in i[0:6] and model_switch:
                ter = 1
                print i[:-1]
            
            if 'END' in i[0:6] and model_switch:
                end = 1
                #try:
                #    nco = 'O'
                #    c_ff.append(self.check_res(res, res1, nco))
                #except:
                #    error.append("END encontered previus than ATOM defined ")
            rep_err = 0        
            if 'ATOM' in i[0:6] and model_switch:
                #print i[:-1]+ "----"
                si = i.split()
                try:
                    anu = int(i[6:11])
                except:
                    anu = 1
                    rep_err = 1
                    
                ana = i[12:17].replace(" ","")
                rna = i[17:21].replace(" ","")
                ci = i[21]
                
                try:
                    rnu = int(i[22:26])
                except:
                    rnu = 1
                    rep_err = 1
                    
                try:    
                    xf = float(i[30:39])
                except:
                    xf = 1
                    err_app =1
                    
                try:
                    yf = float(i[39:46])
                except:
                    yf = 1
                    err_app = 1
                    
                try:
                    zf = float(i[46:54])
                except:
                    zf = 1
                    err_app = 1
                
                if rep_err == 1:
                    error.append("line %s have some format problems" %i)
                
                if "+" in rna or "-" in rna:
                    rna=rna.replace("-","")
                    rna=rna.replace("+","")
                    warning.append("- or + removed from residue %i %s \n" %(rnu,rna))
                    
                if rnu == rnconf:
                    res1 = rna
                    res.append(ana)
                    nco = "C"
                    
                if rnconf == 100000:
                    res.append(ana)
                    rnconf = rnu
                    res1 = rna
                
                if ter == 1:
                    nco = "N"
                if ter == 0:
                    nco = "C"
                    
                if rnu != rnconf:
                    #c_ff.append(check_res(res, res1, nco, tpdbx))
                    print "#### ATOMs in RESIDUE READED ########"
                    print res
                    add_atm = check_res(res, res1, nco, tpdbx)
                    print "##### ADD ATOM LOOS TO FF LIST ####### "
                    print add_atm
                    for ff in add_atm.keys():
                        tot_atm_loos[ff] += add_atm[ff]
                        
                    print "##### TOTAL ADD ATOM LOOS TO FF LIST ####### "    
                    print tot_atm_loos
                    ter = 0
                    rnconf = rnu
                    res = []
                    res1 = rna
                    res.append(ana)
                    
                    
                #if len(ana) == 1:
                #    print "%-6s%5i  %s   %3s %1s%4i    %8.3f%8.3f%8.3f" %("ATOM", anu, ana, rna, ci, rnu, xf, yf, zf)
                #if len(ana) == 2:
                #    print "%-6s%5i  %s  %3s %1s%4i    %8.3f%8.3f%8.3f" %("ATOM", anu, ana, rna, ci, rnu, xf, yf, zf)
                #if len(ana) == 3:
                #    print "%-6s%5i %4s %3s %1s%4i    %8.3f%8.3f%8.3f" %("ATOM", anu, ana, rna, ci, rnu, xf, yf, zf)
                #if len(ana) == 4:
                #    print "%-6s%5i %4s %3s %1s%4i    %8.3f%8.3f%8.3f" %("ATOM", anu, ana, rna, ci, rnu, xf, yf, zf)
    
    #in_pdb.close()
    
    #in_pdb = open(f_pdb, 'r')
    #print "C_FF"
    #print c_ff
    #si = 0
    #ffx = []
    #for i in c_ff: 
    #    if si == 0:
    #        ffx.append(i)
    #    else:
    #        if ffx.count(i) == 0:
    #            ffx.append(i)
    #    si += 1
    #print "FFX "
    #print ffx
    #
    #teff = {}
    #for i in ffx:
    #    teff[i] = c_ff.count(i)
    
    #print teff
    #if len(teff) > 0:
        #ffin = sorted([(value,key) for (key,value) in teff.items()], reverse=True)[0][1]
    ffin = sorted([(value,key) for (key,value) in tot_atm_loos.items()], reverse=False)[0][1]
    #else:
    #    ffin="cns"
    print "Force Field selected "
    print ffin
    ffout = "amber"  
    pdb_out = []
    pdb_ref = []
    warning_res = []
    
    model_switch = True
    model_find = False
    
    map_pdb = create_map(ffin, ffout, tpdbx)
    for i in map_pdb:
        print i
    
    print "***************************************************"
    print "           CONV PDB"
    print model
    print f_pdb
    print "***************************************************"
    
    model = 0
    res_skip = ["LL","PL","LP"]
    w_removed = 0
    print_war_lp = 0
    i= 0
    while i < len(in_pdb):
        remove = 0
        if in_pdb[i][17:21].replace(" ","") in res_skip:
            if i+1 <= len(in_pdb):
                if in_pdb[i+1][17:21].replace(" ","") not in res_skip:
                    in_pdb.insert(i+1,"TER\n")
                    #in_pdb.pop(i)
                    
        if in_pdb[i][17:21].replace(" ","") in res_skip:
            if print_war_lp == 0:
                warning.append("LP or LL or PL residues CYANA/DYANA removed")
            print_war_lp = 1
            in_pdb.remove(in_pdb[i])
            remove = 1
            w_removed = 1
            
        if remove == 0:
            i = i + 1
            
    if w_removed == 1:
        warning.append("Some LP and LL dummy atoms were removed consider that in NMR restraints assignment")
        
    for i in in_pdb:
        if len(i) > 0 and model == 0:
            
            if 'MODEL' in i[0:6] and not model_find:
                model_find = True
                
            elif 'MODEL' in i[0:6] and model_find:
                #warning.append("More then one model found in PDB program will use only the first")
                model_switch = False
                
            if 'HETATM' in i[0:6] and model_switch:
                warning.append("%s are not included in standard amber ff please use ligand session" %i[0:15] )
                    
            if  'TER' in i[0:6] and model_switch:
                ter =1
                pdb_out.append(i[:-1])
                print i[:-1]
            
            if 'END' in i[0:6] and model_switch:
                end = 1
                
            #list of residues to skip
            
            if 'ATOM' in i[0:6] and model_switch:
                #print i[:-1]+ "----"
                si = i.split()
                try:
                    anu = int(i[6:11])
                except:
                    anu = 1
                ana = i[12:17].replace(" ","")
                rna = i[17:21].replace(" ","")
                ci = i[21]
                try:
                    rnu = int(i[22:26])
                except:
                    rnu = 1
                try:
                    xf = float(i[30:39])
                except:
                    xf = 1
                try:
                    yf = float(i[39:46])
                except:
                    yf = 1
                try:
                    zf = float(i[46:54])
                except:
                    zf = 1
                
                if "+" in rna or "-" in rna:
                    rna = rna.replace("-","")
                    rna = rna.replace("+","")
                    warning.append("- or + removed from residue %i %s \n" %(rnu,rna))
                
                #Patch CYANA HG1 THR -> 1HG THR
                if rna == "THR" and ana == "HG1" and ffin == "amber":
                    ana = "1HG"
                    
                oana = conv_name(rna, ana, map_pdb)
                
                if oana == "":
                    warning.append("res %s atom %s not coverted from ff %s to ff %s" %(rna, ana, ffin, ffout))
                elif oana[0] == "1" or oana[0] == "2" or oana[0] == "3" :
                    aa = "%-6s%5i %-4s %3s %1s%4i    %8.3f%8.3f%8.3f" %("ATOM", anu, oana, rna, ci, rnu, xf, yf, zf)
                    print aa
                    pdb_out.append(aa)
                    pdb_ref.append("%6s%6s%6s \n" %(rna, ana, oana))
                elif len(oana) > 5:
                    print"OANA"
                    print"Atom not found"
                    print oana
                    print i
                    warning_res.append(oana+" "+i)
                    pdb_out.append(i.replace("\n",""))
                    pdb_ref.append("%6s%6s%6s \n" %(rna, ana, ana))
                elif len(oana) == 1:
                    aa = "%-6s%5i  %s   %3s %1s%4i    %8.3f%8.3f%8.3f" %("ATOM", anu, oana, rna, ci, rnu, xf, yf, zf)
                    print aa
                    pdb_out.append(aa)
                    pdb_ref.append("%6s%6s%6s \n" %(rna, ana, oana))
                elif len(oana) == 2:
                    aa = "%-6s%5i  %s  %3s %1s%4i    %8.3f%8.3f%8.3f" %("ATOM", anu, oana, rna, ci, rnu, xf, yf, zf)
                    print aa
                    pdb_out.append(aa)
                    pdb_ref.append("%6s%6s%6s \n" %(rna, ana, oana))
                elif len(oana) == 3:
                    aa = "%-6s%5i %4s %3s %1s%4i    %8.3f%8.3f%8.3f" %("ATOM", anu, oana, rna, ci, rnu, xf, yf, zf)
                    print aa
                    pdb_out.append(aa)
                    pdb_ref.append("%6s%6s%6s \n" %(rna, ana, oana))
                elif len(oana) == 4:
                    aa = "%-6s%5i %4s %3s %1s%4i    %8.3f%8.3f%8.3f" %("ATOM", anu, oana, rna, ci, rnu, xf, yf, zf)
                    print aa
                    pdb_out.append(aa)
                    pdb_ref.append("%6s%6s%6s \n" %(rna, ana, oana))
                    
                else:
                    warning.append("res %s atom %s not coverted from ff %s to ff %s" %(rna, ana, ffin, ffout))
                    
    if end == 0 :
        error.append("Please put END stantment in the end of pdb")
    warning_char = ""
    for iu in warning:
        warning_char += "%s \n" %iu
    error_char = ""
    for iu in error:
        error_char += "%s \n" %iu
    info_char = ""
    for iu in info:
        info_char += "%s \n" %iu
       
    #print  warning_char
    te={}
    te["BaseName"] = os.path.basename( f_pdb )
    root_st = etree.Element("Status")
    root_wn =  etree.SubElement(root_st, "File" , te )
    etree.SubElement(root_st, "PDB" ).text = list2txt(pdb_out)
    
    
    ## creo PDB.ref
    pdb_che = os.path.join( os.path.dirname(f_pdb), os.path.basename(f_pdb).split(".")[0] + "_c.pdb")
    #pdb_ref_n = os.path.join( os.path.dirname(f_pdb), os.path.basename(f_pdb).split(".")[0] + "_c.ref")
    pdb_ref_n = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "pdb.ref")
    
    pdb_ref_n_f = open(pdb_ref_n, 'w')
    #remove all duplicate
    set ={}
    pdb_ref_n_f.writelines([set.setdefault(e,e) for e in pdb_ref if e not in set])
    pdb_ref_n_f.close()       
    
    pdb_che_f = open(pdb_che, 'w')
    pdb_out_e = []
    for ik in pdb_out:
        pdb_out_e.append(ik+"\n")
        
    pdb_che_f.writelines(pdb_out_e)
    pdb_che_f.close()
    ####
    
    if len(warning_res) > 0:
        for jk in warning_res:
            jk_a = {}
            jk_a['Residue'] = jk.split()[0]
            etree.SubElement(root_wn, "Warning_res", jk_a ).text = jk
    if len(warning) > 0:
        etree.SubElement(root_wn, "Warning_PDB").text = warning_char
    if len(error) > 0:
        etree.SubElement(root_wn, "Error_PDB").text = error_char
    if len(info) > 0:
        etree.SubElement(root_wn, "Info_PDB").text = info_char
    
    print warning
    return etree.tostring(root_st, pretty_print=True, xml_declaration=True, encoding="utf-8")

#def find_metal1():
#    lista = []
#    listaa = {}
#    pdb_out = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "out_leap.pdb")
#    filel = open(pdb_out,"r").readlines()
#
#    for i in filel:
#        if len(i.split()) >= 8 and i.startswith("ATOM"):
#            rnu = int(i[22:26])
#            panu = int(i[6:11])
#            pana = i[12:17].replace(" ","")
#            prna = i[17:21].replace(" ","")
#            prnu = int(i[22:26])                
#            lista.append("%s %s" %( prna, prnu))
#            listaa["%s %s" %( prna, prnu)] = pana
#    root = etree.Element("sel_metal")   
#    for a in lista:
#        if lista.count(a) == 1 :
#            print "pino"
#            etree.SubElement(root, "sel").text  = "%s %s " % (listaa[a], a)
#    etree.SubElement(root, "sel").text  = "No Par. Cent."
#    print etree.tostring(root, pretty_print=True)
#
#    return etree.tostring(root, pretty_print=True)           
 
def validate_pdbFile(rfname):
    #file_name = request.POST.get('protein_file')
    #if 'pdbFile' in request.params:
    #    file = request.params['pdbFile']
    
    #f = file_name.filename.split('\\')
    
    #rfname = os.path.join(config['app_conf']['amber_data'], f[len(f)-1])
    #rfname = os.path.join(config['app_conf']['amber_data'], "generate_protein.pdb")
    #permanent_file = open(rfname, 'wb')
    #shutil.copyfileobj(file_name.file, permanent_file)
    #file_name.file.close()
    #permanent_file.close()
    
    #some controls to validate file
    #xml_r = self.check_pdb(rfname)
    
    #res = Response()
    #res.charset = 'utf8'
    #if file == 'e1.txt':
    #    res.body = 'warning'
    #    res.status = 201
    #elif file == 'e2.txt':
    #    res.body = 'error'
    #    res.status = 201
    #else:
    #    res.status = 204
        
    #response.headers['content-type'] = 'text/xml; charset=utf-8'
    #response.status = 201
    #xml_r = "<?xml version=\"1.0\" standalone=\"yes\"?>"
    #xml_r = xml_r + "<warror><file><basename>generate_protein.pdb</basename><warnings><ATOM>H</ATOM><ELECTRON>112249</ELECTRON></warnings></file></warror>"
    return xml_r

def extractEnvVar(var):
    allVars = request.environ['webob._parsed_post_vars']
    
    listReqKeys = allVars[0].keys();
    
    list_matched = []
    for it in (item for item in listReqKeys if var in item):
         list_matched.append(it)
    print list_matched
    
    return list_matched
    
def take_out_rdc(out_leap, protocoll, root, f_rdc):
    if protocoll == "calc":
        te = {}
        #root = etree.Element("fanta_rdc")
        rdc_fo = []
        rdc_gnu = []
        trf = 0
        for i in out_leap.splitlines():
            if len(i) > 0:
           
                if "qfactor" in i:
                    trf = 0
                if trf == 1:
                    rdc_fo.append(i)
                    rdc_gnu.append(i+'\n')
                    
                if "RDC_out" in i:
                    trf =1
                if " chi:" in i:
                    te["a1val"] = i.split()[1]
                    te["a2val"] = i.split()[2]
                    te["a3val"] = i.split()[3]
                    exx = float(i.split()[1])
                    eyy = float(i.split()[2])
                    ezz = float(i.split()[3])
                    etree.SubElement(root, "RDC_eig" , te)
                    te = {}
                if "Dchi:" in i:
                    te["dchiax"] = i.split()[1]
                    dchiax = i.split()[1]
                    te["dchirh"] = i.split()[2]
                    dchirh = i.split()[2]
                    etree.SubElement(root, "aniso" , te)
                    te = {}
                    
                if "Dchim3:" in i:
                    te["dchiax"] = i.split()[1]
                    te["dchirh"] = i.split()[2]
                    etree.SubElement(root, "anisom" , te)
                    te = {}
                    
                if "qfactor" in i:
                    te["qfactor_val"] = i.split()[2]
                    te["num"] = i.split()[4]
                    te["den"] = i.split()[6]
                    etree.SubElement(root, "qfactor" , te)
                    te = {}                    
        return root, rdc_fo, rdc_gnu, dchiax, dchirh
    if protocoll == "fit":
        te = {}
        #root = etree.Element("fanta_rdc")
        rdc_fo = []
        rdc_gnu = []
        trf = 0
        for i in out_leap.splitlines():
            if len(i) > 0:
           
                if "qfactor" in i:
                    trf = 0
                    
                if trf == 1:
                    rdc_fo.append(i)
                    rdc_gnu.append(i+'\n')
                    
                if "RDC_out" in i:
                    trf =1
                    
                if " chi:" in i:
                    te["a1val"] = i.split()[1]
                    te["a2val"] = i.split()[2]
                    te["a3val"] = i.split()[3]
                    exx = float(i.split()[1])
                    eyy = float(i.split()[2])
                    ezz = float(i.split()[3])
                    etree.SubElement(root, "RDC_eig" , te)
                    te = {}
                    
                if "Dchi:" in i:
                    te["dchiax"] = i.split()[1]
                    dchiax = i.split()[1]
                    te["dchirh"] = i.split()[2]
                    dchirh = i.split()[2]
                    etree.SubElement(root, "aniso" , te)
                    te = {}
                    
                if "Dchim3:" in i:
                    te["dchiax"] = i.split()[1]
                    te["dchirh"] = i.split()[2]
                    etree.SubElement(root, "anisom" , te)
                    te = {}
                    
                if "qfactor" in i:
                    te["qfactor_val"] = i.split()[2]
                    te["num"] = i.split()[4]
                    te["den"] = i.split()[6]
                    etree.SubElement(root, "qfactor" , te)
                    te = {}
                    
                if "omega" in i:
                    te["phi"] = i.split()[1]
                    te["theta"] = i.split()[3]
                    te["omega"] = i.split()[5]
                    etree.SubElement(root, "euler" , te)
                    te = {}
                    
                if "matrix" in i:
                    te["vxx"] = i.split()[1]
                    te["vxy"] = i.split()[2]
                    te["vxz"] = i.split()[3]
                    
                    te["vyx"] = i.split()[4]
                    te["vyy"] = i.split()[5]
                    te["vyz"] = i.split()[6]
                    
                    te["vzx"] = i.split()[7]
                    te["vzy"] = i.split()[8]
                    te["vzz"] = i.split()[9]
                    
                    vxx = float(i.split()[1])
                    vxy = float(i.split()[2])
                    vxz = float(i.split()[3])
                    
                    vyx = float(i.split()[4])
                    vyy = float(i.split()[5])
                    vyz = float(i.split()[6])
                    
                    vzx = float(i.split()[7])
                    vzy = float(i.split()[8])
                    vzz = float(i.split()[9])
                    
                    etree.SubElement(root, "matrix" , te)
                    te = {}
        
        matrA = matrix( [[exx,0.0,0.0],[0.0,eyy,0.0],[0.0,0.0,ezz]])
        matrD = matrix( [[vxx,vxy,vxz],[vyx,vyy,vyz],[vzx,vzy,vzz]])
        
        print 'MATRIX'
        print 'matrD, matrA'
        print matrD
        print matrA
        print 'matrB = matrD*matrA*matrD.T'
        matrB = matrD*matrA*matrD.T
        print matrB
        [w, v] = LA.eig(matrB)
        print '------------------'
        print w
        print "------------------"
        print v
        
        te = {}
        te['c11'] = str(matrB.tolist()[0][0])
        te['c12'] = str(matrB.tolist()[0][1])
        te['c13'] = str(matrB.tolist()[0][2])
        te['c22'] = str(matrB.tolist()[1][1])
        te['c23'] = str(matrB.tolist()[1][2])
        etree.SubElement(root, "matrix_rdc" , te)
        te = {}
        xml_file = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), f_rdc+".xml")
        xml_final = etree.parse(xml_file)
        xml_final.getroot().append(etree.fromstring(etree.tostring(root)))
        xml_final.write(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), f_rdc+"_final.xml"))
        print "***************"
        print etree.tostring(root, pretty_print=True)
        return root, rdc_fo, rdc_gnu, dchiax, dchirh
        
def take_out_pcs(out_leap, protocoll, root, f_pcs):
    if protocoll == "calc":
        te = {}
        #root = etree.Element("fanta_pcs")
        pcs_fo = []
        pcs_gnu = []
        trf = 0
        for i in out_leap.splitlines():
            if len(i) > 0:
           
                if "qfactor pcs" in i:
                    trf = 0
                if trf == 1:
                    pcs_fo.append(i)
                    pcs_gnu.append(i+'\n')
                    
                if "PCS_out" in i:
                    trf =1
                if " chi:" in i:
                    te["a1val"] = i.split()[1]
                    te["a2val"] = i.split()[2]
                    te["a3val"] = i.split()[3]
                    etree.SubElement(root, "RDC_eig" , te)
                    te = {}
                if "Dchi:" in i:
                    te["dchiax"] = i.split()[1]
                    dchiax = i.split()[1]
                    te["dchirh"] = i.split()[2]
                    dchirh = i.split()[2]
                    etree.SubElement(root, "aniso" , te)
                    te = {}
                    
                if "Dchim3:" in i:
                    te["dchiax"] = i.split()[1]
                    te["dchirh"] = i.split()[2]
                    etree.SubElement(root, "anisom" , te)
                    te = {}
                    
                if "qfactor pcs=" in i:
                    te["qfactor_val"] = i.split()[2]
                    te["num"] = i.split()[4]
                    te["den"] = i.split()[6]
                    etree.SubElement(root, "qfactor" , te)
                    te = {}             
        return root, pcs_fo, pcs_gnu, dchiax, dchirh
    
    if protocoll == "fit":
        te = {}
        #root = etree.Element("fanta_pcs")
        pcs_fo = []
        pcs_gnu = []
        trf = 0
        for i in out_leap.splitlines():
            if len(i) > 0:
           
                if "RDC_out" in i:
                    trf = 0
                if trf == 1:
                    pcs_fo.append(i)
                    pcs_gnu.append(i+'\n')
                    
                if "PCS_out" in i:
                    trf =1
                if " chi:" in i:
                    te["a1val"] = i.split()[1]
                    te["a2val"] = i.split()[2]
                    te["a3val"] = i.split()[3]
                    etree.SubElement(root, "RDC_eig" , te)
                    te = {}
                if "Dchi:" in i:
                    te["dchiax"] = i.split()[1]
                    dchiax = i.split()[1]
                    te["dchirh"] = i.split()[2]
                    dchirh = i.split()[2]
                    etree.SubElement(root, "aniso" , te)
                    te = {}
                    
                if "Dchim3:" in i:
                    te["dchiax"] = i.split()[1]
                    te["dchirh"] = i.split()[2]
                    etree.SubElement(root, "anisom" , te)
                    te = {}
                    
                if "qfactor" in i:
                    te["qfactor_val"] = i.split()[2]
                    te["num"] = i.split()[4]
                    te["den"] = i.split()[6]
                    etree.SubElement(root, "qfactor" , te)
                    te = {}
                    
                if "omega" in i:
                    te["phi"] = i.split()[1]
                    te["theta"] = i.split()[3]
                    te["omega"] = i.split()[5]
                    etree.SubElement(root, "euler" , te)
                    te = {}
                    
        xml_file = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), f_pcs + ".xml")
        xml_final = etree.parse(xml_file)
        xml_final.getroot().append(etree.fromstring(etree.tostring(root)))
        xml_final.write(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), f_pcs+"_final.xml"))
        print etree.tostring(root, pretty_print=True)
        return root, pcs_fo, pcs_gnu, dchiax, dchirh
           

def nfi(ntx, irest, ntrx):
    res = 'ntx=%s, ' % ntx
    if irest > 0:
        res = '%sirest=%s, ' % (res, irest)
    res = '%sntrx=%s,\n' % (res, ntrx)
    
    return res

def nfo(ntxo, ntpr, ntave, ntwr, iwrap, ntwx, ntwv, ntwe, ioutfm, ntwprt, idecomp):
    res = 'ntxo=%s, ntpr=%s, ' % (ntxo, ntpr)
    if ntave > 0:
        res = '%sntave=%s, ' % (res, ntave)
    res = '%sntwr=%s, ' % (res, ntwr)
    if iwrap > 0:
        res = '%siwrap=%s, ' % (res, iwrap)
    if ntwx > 0:
        res = '%sntwx=%s, ' % (res, ntwx)
    if ntwv > 0:
        res = '%sntwx=%s, ' % (res, ntwv)
    if ntwe > 0:
        res = '%sntwx=%s, ' % (res, ntwe)
    res = '%sioutfm=%s, ntwprt=%s, ' % (res, ioutfm, ntwprt)
    if idecomp > 0:
        res = '%sidecomp=%s,\n' % (res, idecomp)
    
    return res

def fra(ibelly, ntr, restraint_wt, restraintmask, bellymask):
    res = ""
    if ibelly > 0:
        res = '%sibelly=%s, ' % (res, ibelly)
    if ntr > 0:
        res = '%sntr=%s, ' % (res, ntr)
        
    res = '%srestraint_wt=%s, restraintmask=%s, bellymask=%s,\n' % (res,
                                                                    restraint_wt,
                                                                    restraintmask,
                                                                    bellymask)
    
    return res

def em(maxcyc, ncyc, ntmin, dxo, drms):
    res = 'maxcyc=%s, ncyc=%s, ntmin=%s, dxo=%s, drms=%s,\n' % (maxcyc,
                                                                ncyc,
                                                                ntmin,
                                                                dxo,
                                                                drms)

    return res

def md(nstlim, nscm, t, dt, nrespa):
    res = 'nstlim=%s, nscm=%s, t=%s, dt=%s, nrespa=%s,\n' % (nstlim,
                                                             nscm,
                                                             t,
                                                             dt,
                                                             nrespa)
    
    return res

def sgld(isgld, tsgavg, tempsg, sgft, isgsta, isgend):
    res = ""
    if isgld > 0:
        res = '%sisgld=%s, tsgavg=%s, tempsg=%s, sgft=%s, isgsta=%s, isgend=%s,\n' % (res,
                                                                                      isgld,  
                                                                                      tsgavg,
                                                                                      tempsg,
                                                                                      sgft,
                                                                                      isgsta,
                                                                                      isgend)
    return res

def tr(ntt, temp0, temp0les, tempi, ig, tautp, gamma_ln, vrand, vlimit):
    res = 'ntt=%s, temp0=%s, temp0les=%s, tempi=%s, ig=%s, tautp=%s, \
gamma_ln=%s, vrand=%s, vlimit=%s,\n' % (ntt,
                                        temp0,
                                        temp0les,
                                        tempi,
                                        ig,
                                        tautp,
                                        gamma_ln,
                                        vrand,
                                        vlimit)
   
    return res

def pr(ntp, pres0, comp, taup):
    res = 'ntp=%s, pres0=%s, comp=%s, taup=%s,\n' % (ntp,
                                                     pres0,
                                                     comp,
                                                     taup)
    
    return res

def sblc(ntc, tol, jfastw, watnam, owtnm, hwtnm1, hwtnm2, noshakemask):
    res = ""
    if ntc > 0:
        res = '%s,ntc=%s, tol=%s, jfastw=%s, watnam=%s, owtnm=%s, \
hwtnm1=%s, hwtnm2=%s, noshakemask=%s,\n' % (res,
                                            ntc,
                                            tol,
                                            jfastw,
                                            watnam,
                                            owtnm,
                                            hwtnm1,
                                            hwtnm2,
                                            noshakemask)
    
    return res

def wc(ivcap, fcap):
    res = ""
    if ivcap < 2:
        res = "%sivcap=%s, fcap=%s,\n" % (res, ivcap, fcap)
    return res

def nmrro(iscale, noeskp, ipnlty, mxsub, scalm, pencut, tausw):
    res = 'iscale=%s, noeskp=%s, ipnlty=%s, mxsub=%s, scalm=%s, \
pencut=%s, tausw=%s,\n' % (iscale,
                            noeskp,
                            ipnlty,
                            mxsub,
                            scalm,
                            pencut,
                            tausw)
    
    return res

def pfp(ntf, dielc, scnb, nsnb, ifqnt, ievb, ntb, cut, scee, ipol, igb, iamoeba):
    res = 'ntf=%s, dielc=%s, scnb=%s, nsnb=%s, ifqnt=%s, ievb=%s \
ntb=%s, cut=%s, scee=%s, ipol=%s, igb=%s, iamoeba=%s,\n' % (ntf,
                                                            dielc,
                                                            scnb,
                                                            nsnb,
                                                            ifqnt,
                                                            ievb,
                                                            ntb,
                                                            cut,
                                                            scee,
                                                            ipol,
                                                            igb,
                                                            iamoeba)
  
    return res

def ipscni(ips):
    res = ""
    if ips > 0:
        res = "%sips=%s,\n" % (res, ips)
    return res

def pme(nbtell, netfrc, vdwmeth, eedmeth, eedtbdns, column_fft):
    res = "&ewald\n"
    res = "%snbtell=%s, netfrc=%s, vdwmeth=%s, eedmeth=%s, \
eedtbdns=%s, column_fft=%s,\n" % (res,
                                nbtell,
                                netfrc,
                                vdwmeth,
                                eedmeth,
                                eedtbdns,
                                column_fft)
    
    return res

def epo(frameon, chngmask):
    res = 'frameon=%s, chngmask=%s,\n' % (frameon, chngmask)
    
    return res

def pp(indmeth, diptol, maxiter, dipmass, diptau, irstdip, scaldip):
    res = "indmeth=%s, diptol=%s, maxiter=%s, dipmass=%s, diptau=%s, \
irstdip=%s, scaldip=%s,\n" % (indmeth,
                              diptol,
                              maxiter,
                              dipmass,
                              diptau,
                              irstdip,
                              scaldip)
    
    return res

def wci(tp, istep1, istep2, value1, value2, iinc, imult):
    res = "&wt\n"
    res = "%sTYPE='%s', istep1=%s, istep2=%s, value1=%s, value2=%s, iinc=%s \
imult=%s,\n &wt TYPE=END" % (res,
                             tp,
                             istep1,
                             istep2,
                             value1,
                             value2,
                             iinc,
                             imult)
    return res

def gdi(do_debugf, atomn, nranatm, ranseed, neglgdel, chkvir, dumpfrc, rmsfrc,
        zerochg, zerovdw, zerodip, do_dir, do_rec, do_adj, do_self, do_bond,
        do_cbond, do_angle, do_ephi, doxconst, do_cap):
    res = ""
    if do_debugf > 0:
        res = '%s&debug\n' % res
        res = "%satomn=%s, nranatm=%s, ranseed=%s, neglgdel=%s, chkvir=%s, \
dumpfrc=%s, rmsfrc=%s, zerochg=%s, zerovdw=%s, zerodip=%s, do_dir=%s, \
do_rec=%s, do_adj=%s, do_self=%s, do_bond=%s, do_cbond=%s, do_angle=%s, \
do_ephi=%s, doxconst=%s, do_cap=%s,\n" % (res,
                                          atomn,
                                          nranatm,
                                          ranseed,
                                          neglgdel,
                                          chkvir,
                                          dumpfrc,
                                          rmsfrc,
                                          zerochg,
                                          zerovdw,
                                          zerodip,
                                          do_dir,
                                          do_rec,
                                          do_adj,
                                          do_self,
                                          do_bond,
                                          do_cbond,
                                          do_angle,
                                          do_ephi,
                                          doxconst,
                                          do_cap)
        
    return res
