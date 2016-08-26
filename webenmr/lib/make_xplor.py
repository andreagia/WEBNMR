import sys, re
import os, shutil
from string import Template
from lxml import etree
from pyparsing import *
from pylons import config
from subprocess import call
from webenmr.lib.Subprocess import shellCall
from webenmr.lib.BaseSecurity import BaseSecurity
import operator

def search_residue(stri, nres):
    f = False
    for i in stri:
            if re.search(r'^\s*resi\w*\s+%s\s*' %nres, i,flags = re.IGNORECASE):
                f = True
    return f

def check_pdb_X(stri):
    res = {}
    test = {}
    bad_r_num = True
    bad_r_name = True
    bad_r_chain = True
    for i in stri:
        if len(i) > 53:
            if i[0:4] == "ATOM":
                r_name = i[17:20]
                r_chain = i[21]
                r_num = i[22:26]
                test[r_name] = "name"
                test[r_chain] = "name"
                test[r_num] = "name"
    if  len(test.keys()) != 3:
        res["error"] = "ERROR: PDB contain more then one residue"
        
    res["name"] = r_name.replace(" ","")
    res["num"] = r_num.replace(" ","")
    res["chain"] = r_chain.replace(" ","")

    return res
                
def dual_patch(stri):
    one = False
    two = False
    trov = False
    for i in stri:
        if re.search(r'\s+1\w+', i,flags = re.IGNORECASE):
            one = True
        if re.search(r'\s+\-\w+', i,flags = re.IGNORECASE):
            one = True
        if re.search(r'\s+2\w+', i,flags = re.IGNORECASE):
            two = True
        if re.search(r'\s+\+\w+', i,flags = re.IGNORECASE):
            two = True   
    return  one and two

def take_patch(inp):
    patch = {}
    npatch = ""
    co_patch = []
    patch_trov = False
    for ip in inp:
        i = ip.split("!")[0]
        
        if re.search(r'^\s*pres\w*\s+\w+\s*', i,flags = re.IGNORECASE):
            npatch=i.split()[1]
            patch_trov = True
            
        if re.search(r'^\s*end\s*', i, flags = re.IGNORECASE) and patch_trov:
            patch_trov = False
            co_patch.append(i)
            patch[npatch] = co_patch
            npatch = ""
            co_patch = []
            
        if patch_trov:
            co_patch.append(i)
            
    return patch


class File(file):
    def head(self, lines_2find=1):
        self.seek(0)                            #Rewind file
        return [self.next() for x in xrange(lines_2find)]


def check_file(file, wd):
    filec=os.path.join(wd,file)
    if os.path.isfile(filec):
        return True
    else:
        err="%s: file %s doesn't exist\n\n" % (sys.argv[0], filec)
        sys.stderr.write(err)
        sys.exit()


class SCDelimiterTemplate(Template):
    delimiter='#%'

class PMDelimiterTemplate(Template):
    delimiter='!##'
    
    
class JobsProcessing(BaseSecurity):
    
    def __init__(self):
        BaseSecurity.__init__(self)
        os.environ['TOPPAR'] = "/prog/xplor-nih-2.29/toppar"
       
    def exec_cmd(self, cmd, wd):
        prev = os.getcwd()
        os.chdir(wd)
        #ret = call( cmd, shell = True)
        cmdEnv = self._getExternalCmdEnvironment()
        ret = shellCall( self._secCmdTimeout, cmd, env = cmdEnv )
        #ret = os.system(cmd)
        print "#####RET[VALUE]###########"
        print "COMMAND: " + cmd
        print ret['Value']
        print "##########################"
        os.chdir(prev)
        return ret['Value']

class info_xplor(object):
    
    def __init__(self, wd, xmlPC):
        self.xmlPC = xmlPC
        self.number_psf = 0
        self.info_psf = {}
        self.info_pdb = {}
        self.number_pdb = 0
        self.wd = wd
        self.his_prot = []
        self.sulf_bridge = []
        self.xml_psf = etree.Element("psfInfo")
        self.xml_pdb = etree.Element("pdbInfo")
    
    def findxml(self, xml, tag):
        res = []
        for a in xml.getiterator():
            if a.tag == tag:
               res.append(a)
        return res
    
    def findxml5(self, xml, tag, attri, strs, getattri ):
        print tag, attri, strs, getattri
        print etree.tostring(xml, pretty_print=True)
        for a in xml.getiterator():
            if a.tag == tag:
                if strs in a.get(attri): 
                    res = a.get(getattri) 
        return res
    
    def add_psf(self, filein, seqfile, metal = False):
        read = False
        num = []
        chain =[]
        for i in open(os.path.join(self.wd, filein.strip("@")), "r").readlines():
            if "!NATOM" in i:
                read = True
            if "!NBOND" in i:
                read = False
            if read and len(i.split()) > 5:
                num.append(int(i[14:18]))
                chain.append(i[9:13])
        if len(chain) > 1:
            print "############### PSF ERROR INI ####################"
            print filein.strip("@") + " contein more than one chain"
            print "############### PSF ERROR END ####################"
        if not metal:
            pos = self.findxml5(self.xmlPC, "sequence", "path", seqfile, "pos" )
        else:
            ##inserire pos anche nei metalli presi dal paramagnetico
            ##pos = "100"
            #ordino i metalli e i tensori per numero di residuo
            pos = num[-1]
        num.sort()
        self.number_psf += 1
        self.info_psf[self.number_psf] = { "min" : num[0] , "max" : num[-1] , "chainid" : chain[0], "filein" : filein.strip("@"), "pos" : int(pos), "seqfile" : seqfile }
        
    def add_pdb(self, filein):
        num = []
        chain =[]
        for i in open(os.path.join(self.wd, filein), "r").readlines():
            if i.startswith("ATOM"):
                num.append(int(i[22:26]))
            if len(i) >= 76:
                if len(i[72:76].strip()) > 0:
                    print "STRINGA "
                    print i[72:76]
                    chain.append(i[72:76].strip())
        if len(chain) > 1:
            print "############### PSF function PDB ERROR INI ####################"
            print filein + " contein more than one chain "
            print chain
            print "############### PSF function PDB ERROR END ####################"
        if len(num) > 1:
            print "############### PSF function PDB ERROR INI ####################"
            print filein + " contein more than one residues"
            print "############### PSF function PDB ERROR END ####################"
        pos = self.findxml5(self.xmlPC, "cofactor", "pdb_path", filein, "pos" )
        num.sort()
        if len(chain) == 0:
            chain = ["    "]
        self.number_pdb += 1
        self.info_pdb[self.number_pdb] = { "min" : num[0] , "max" : num[-1] , "chainid" : chain[0], "filein" : filein, "pos" : int(pos) }
        
    def add_his_prot(self, his):
        self.his_prot.append(his)
    
    def add_sul_bridg(self, sulf):
        self.sulf_bridge.append(sulf)
    
    def sort_struct_psf(self):
        diz_min = {}
        diz_min_psf = {}
        diz_min_pdb = {}
        print self.info_psf
        num = 0
        for i in self.info_psf.keys():
            diz_min_psf[i] = self.info_psf[i]["pos"]
        sorted_diz_psf = sorted(diz_min_psf.iteritems(), key  = operator.itemgetter(1))
        print "####diz_min_psf INI######"
        print diz_min_psf
        print "####diz_min_psf END######"
        print "####sorted_diz_psf INI######"
        print sorted_diz_psf
        print "####sorted_diz_psf END######"
        prot_psf = ""
        pos_incr = 0
        for i in sorted_diz_psf:
            pos_incr = pos_incr + 1
            prot_psf = prot_psf + "@%s" % self.info_psf[i[0]]["filein"].split(".")[0] + ".psf" + "\n"
            self.info_psf[i[0]]["position"] = pos_incr
            print i
            print self.info_psf[i[0]]
            dicstring = dict((k, str(v)) for (k, v) in self.info_psf[i[0]].items())
            etree.SubElement(self.xml_psf, "psf", dicstring)
        print "####seq psf INI######"
        print prot_psf
        print "####seq psf END######"
        return sorted_diz_psf , prot_psf
        
    def sort_struct_pdb(self):
        diz_min = {}
        diz_min_pdb = {}
        prot_pdb = []
        for i in self.info_pdb.keys():
            diz_min_pdb[i] = self.info_pdb[i]["min"]
        sorted_diz_pdb = sorted(diz_min_pdb.iteritems(), key = operator.itemgetter(1))
        for i in sorted_diz_pdb:
            prot_pdb.append( self.info_pdb[i[0]]["filein"])
            self.info_pdb[i[0]]["position"] = i[0]
            dicstring = dict((k, str(v)) for (k, v) in self.info_pdb[i[0]].items())
            etree.SubElement(self.xml_pdb, "pdb", dicstring)
        return sorted_diz_pdb, prot_pdb
    
    def create_xml(self, xml_xplor):
        xml_info = etree.Element("info")
        xml_info.append(xml_xplor)
        xml_info.append(self.xml_pdb)
        xml_info.append(self.xml_psf)
        xmlout = etree.tostring(xml_info, pretty_print=True)
        xmlfout = open(os.path.join(self.wd, "info.xml"),"w")
        xmlfout.writelines(xmlout)
        xmlfout.close()
        
    
    
class PrepareCalculation:
    '''
    Class to prepare xplor input file
    
    methods:
            prepare_xplor_pm for paramagnetic calculations
            prepare_xplor_sc for structure calculations
    '''

#class xplor_tools:
#    '''
#    Gestione input di xplor
#    '''
    
    def __init__(self, doc, template, wd):
        self.xml = doc
        self.XPLOR_HOME = "/prog/xplor-nih-2.29"
        self.metal_par = []
        self.metal_psf = []
        self.tensor_pdb =[]
        self.wd = wd
        self.tab_res_num = {}
        self.res_metal_list = []
        self.metal_tensor_restr = []
        self.doc = doc
        self.wd = wd
        self.template = template
        self.infox = info_xplor(wd, doc)
        

        
    def findxml(self, xml, tag):
        res = []
        for a in xml.getiterator():
            if a.tag == tag:
               res.append(a)
        return res
    
    
    def create_seq(self):
        fst_seq = {"A" : "ALA", "C" : "CYS", "D" : "ASP", "E" : "GLU", "F" : "PHE", "G" : "GLY", "H": "HIS" , "I" : "ILE", "K" : "LYS",
                   "M" : "MET", "N" : "ASN", "P" : "PRO", "R" : "ARG", "S" : "SER", "T" : "THR", "V" : "VAL", "W" : "TRP", "Q" : "GLN",
                   "L" : "LEU", "Y" : "TYR" }
        print "#######XML XPLOR#############"
        print etree.tostring(self.xml)
        print "#############################"
        num_seq = 0
        prot_psf = ""
        prot_par = ""
        
        nstdtopv = []
        nstdparv = []
        etree
        for nonstdres in self.findxml(self.xml, "nonstdresidues"):
            nstdparv += nstdparv + open(nonstdres.get("parameter_path"),"r").readlines()
            nstdtopv += nstdtopv + open(nonstdres.get("topology_path"),"r").readlines()
            
        print "######NSTD PARA AND TOPO ############"
        print nstdtopv
        print nstdparv
        nstdtopf = os.path.join(self.wd, "nonstandardres.top")
        open(nstdtopf,"w").writelines(nstdtopv)
        nstdparf = os.path.join(self.wd, "nonstandardres.par")
        open(nstdparf,"w").writelines(nstdparv)
        
        if len(self.findxml(self.xml, "nonstdresidues")) > 0:
            prot_par = prot_par + "@nonstandardres.par\n" 
        
        for i in self.metal_psf:
            prot_psf = prot_psf + "%s\n" %i
            self.infox.add_psf(i, "metal%s" %i, True)
        
        for i in self.metal_par:
            prot_par = prot_par + "%s\n" %i
        
        chain_diz = {}
        if self.findxml(self.xml, 'noe'):
            for i in self.findxml(self.xml, 'noe'):
                tmp_chain_read = open(i.get("path"),"r").readlines()
                for k in tmp_chain_read:
                    if  len(re.findall(r'[sS][eE][gG][iI][a-z A-Z]?\s+"...."', k)) > 0:
                        for ki in re.findall(r'[sS][eE][gG][iI][a-z A-Z]?\s+"...."', k):
                            chain_diz[ki.split('"')[1].strip()] = ki.split('"')[1]
        print "####CHAIN_DIZ#####"
        print "IMPORTANT -> The chain name are checked only on NOE restraints "
        print chain_diz
        print "##################"
        
            
        for seq in self.findxml(self.xml, "sequence"):
            num_seq = num_seq + 1
            filex = seq.get("path")
            check_seq_file = open(filex,"r").read()
            if len(re.findall(r'([a-z A-Z][a-z A-Z][a-z A-Z])\s+[0-9]+', check_seq_file)) > 0:
                open(filex,"w").writelines("\n".join(re.findall(r'([a-z A-Z][a-z A-Z][a-z A-Z])\s+[0-9]+', check_seq_file)))
            elif len(re.findall(r'([a-z A-Z][a-z A-Z][a-z A-Z])\s+', check_seq_file)) > 0:
                open(filex,"w").writelines("\n".join(re.findall(r'([a-z A-Z][a-z A-Z][a-z A-Z])\s+', check_seq_file)))
            else:
                #try seq
                num_fsta = 0
                tmp_check_seq_file = []
                for i in check_seq_file:
                    if i[0] == ">":
                        num_fsta += 1
                    #take only the first sequence
                    if num_fsta <= 1 and i[0] != ";":
                        for a in i:
                            if a in fst_seq.keys():
                                tmp_check_seq_file.append(fst_seq[a]+"\n")
                open(filex,"w").writelines(tmp_check_seq_file.append)
                        
            print filex
            if not os.path.isfile(os.path.join(self.wd, "seq%d.seq" % num_seq)):
                shutil.copy2(filex,os.path.join(self.wd, "seq%d.seq" % num_seq))
            filex = "seq%d.seq" % num_seq
            num_fi_res = seq.get("numfres")
            chain_name = seq.get("chain")
            if chain_name.strip() in chain_diz.keys():
                chain_name_p = chain_diz[chain_name.strip()]
            else:
                chain_name_p = chain_name
            #os.environ['X509_USER_PROXY'] = "/tmp/x509up_uJP"
            print '"%s"' % chain_name_p
            exe_path = os.path.join(self.XPLOR_HOME, "bin", "seq2psf")
            while len(chain_name_p) < 4:
                chain_name_p += " "
            chain_name_p = chain_name_p.replace(" ",":")
            
            # seq2psf  modificato in modo da prendere un segname di questo tipo "  A " 
            cmd = 'export PATH=$PATH:/bin:/usr/bin:/usr/local/bin ; cd %s ; %s -protein -startresid %s -segname "%s" %s ' % (self.wd, exe_path, num_fi_res, chain_name_p, filex)
            print cmd
            jP = JobsProcessing()
            jP.exec_cmd(cmd, self.wd)
            print os.listdir(self.wd)
            #prot_psf = prot_psf + "@%s" % filex.split(".")[0] + ".psf" + "\n"
            self.infox.add_psf(filex.split(".")[0] + ".psf", os.path.basename(seq.get("path")) )
        
        if os.path.isfile("protein_in_web.psf"):
            os.remove("protein_in_web.psf")
        os.environ['TOPPAR'] = os.path.join('%s'%self.XPLOR_HOME, "toppar")
        os.environ['PATH'] += os.pathsep + self.XPLOR_HOME
        patch_his = ""
        patch_s = ""
        
        #aggiungere il controllo della patch della istidina per questa segid
        if self.findxml(self.xml, 'histidine'):
            for i in self.findxml(self.xml, 'histidine'):
                chain_id = ""
                print "SEGID da WEB ", i.get("segid"), len(i.get("segid"))
                if i.get("segid") in chain_name_p or len(i.get("segid")) == 0:
                    if len(i.get("segid")) == 0:
                        chain_id = "    "
                    elif i.get("segid") in chain_diz.keys():
                        chain_id = chain_diz[i.get("segid")]
                    else:
                        chain_id = i.get("segid")
                        while len(chain_id) < 4:
                            chain_id += " "
                            
                    print "#### HIS PATCH #######"
                    print i.get("type"), i.get("resnum")
                    print "#### HIS PATCH END #######"
                    self.infox.add_his_prot({"type":i.get("type"), "resnum": i.get("resnum"), "chain": chain_id })
                    patch_his+='patch %s reference=nil=(segid "%s" and residue %s) end\n' %  (
                                i.get("type"),
                                chain_id,
                                i.get("resnum"))
        
        print "INFO_PSF INI"
        axy , prot_psf = self.infox.sort_struct_psf()
        print axy
        print "INFO_PSF END"
        
        inp_templ = """
remarks  file  nmr/generate_template.inp
remarks  Generates a "template" coordinate set.  This produces
remarks  an arbitrary extended conformation with ideal geometry.
remarks  Author: Axel T. Brunger

set seed=233321 end
{====>} 
structure

%s

end                         {*Read structure file.*}


parameter  
{====>}
   @TOPPAR:protein.par                                 {*Read parameters.*}
   @par_axis_3.pro
   %s
end

                                  
topology
     mass H 1.008

     presidue HIEP ! change protonation of HIE -> HIP
     add atom HD1 type=H charge= 0.40 end
     add bond ND1 HD1
     add angle HD1 ND1 CE1
     add angle HD1 ND1 CG
     add improper ND1 CE1 CG  HD1
     end {HISE}

     presidue HIED ! change protonation of HIE -> HID
     add atom HD1 type=H charge= 0.40 end
     delete atom HE2 end
     add bond ND1 HD1
     add angle HD1 ND1 CE1
     add angle HD1 ND1 CG
     add improper ND1 CE1 CG  HD1
     end {HISE}

end

{====>}
                {*If protein contains S-S bridges, appropriately modify and*}
                {*then uncomment the following lines.                      *}
                
%s
!patch ndis reference=1=( residue 5  ) reference=2=( residue 55 ) end

vector ident (x) ( all )
vector do (x=x/10.) ( all )
vector do (y=random(0.5) ) ( all )
vector do (z=random(0.5) ) ( all )

vector do (fbeta=50) (all)                 {*Friction coefficient, in 1/ps.*}
vector do (mass=100) (all)                         {*Heavy masses, in amus.*}

parameter 
   nbonds
      cutnb=5.5 rcon=20. nbxmod=-2 repel=0.9  wmin=0.1 tolerance=1.
      rexp=2 irexp=2 inhibit=0.25
   end       
end 

flags exclude * include bond angle vdw end

minimize powell nstep=500  nprint=100 end

flags include impr end

minimize powell nstep=500 nprint=100 end

dynamics  verlet
   nstep=500  timestep=0.001 iasvel=maxwell  firsttemp= 300.  
   tcoupling = true  tbath = 300.   nprint=500  iprfrq=0  
end

parameter 
   nbonds
      rcon=2. nbxmod=-3 repel=0.75
   end
end

minimize powell nstep=1000 nprint=250 end 

dynamics  verlet
   nstep=500  timestep=0.005 iasvel=maxwell  firsttemp= 300.  
   tcoupling = true  tbath = 300.   nprint=1000  iprfrq=0  
end

flags exclude vdw elec end
vector do (mass=1.) ( name h* ) 
hbuild selection=( name h* ) phistep=360 end
flags include vdw elec end

minimize powell nstep=200 nprint=100 end
                                                       {*Write coordinates.*}
remarks produced by nmr/generate_template.inp
write coordinates output=protein.pdb end
write structure output=protein.psf end

stop
        """ % (prot_psf, prot_par, patch_his)
        
        inp_file_name = os.path.join(self.wd, "crea_struttura.inp")
        inp_o = open(inp_file_name, "w")
        inp_o.writelines(inp_templ)
        inp_o.close()
        exe_path = os.path.join(self.XPLOR_HOME, "bin", "xplor")
        cmd = "export PATH=$PATH:/bin:/usr/bin:/usr/local/bin ; cd %s ; %s < crea_struttura.inp > out" % (self.wd, exe_path)
        print cmd
        jP = JobsProcessing()
        jP.exec_cmd(cmd,self.wd)
        
        #self.metal_psf.append(protein_in_web.psf)

    def check_para_xplor(self, tens_in, rest):   
        LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR = map(Suppress, "()[]{}|")
        bytes = Word(printables)
        assi = Suppress(Regex(r"[aA][sS][sS][iI][a-z A-Z]*[a-z A-Z]*")).setResultsName("selection")
        num = Word(nums+"."+"-")
        numf = Group( num.setResultsName("val_tens") + num.setResultsName("tol") ).setResultsName("values")
        word = Word(alphanums+'"*#+%')
        sand = Regex(r"[aA][nN][dD]")
        sor =  Regex(r"[oO][rR]")
        cond = Suppress(sand | sor)
        name = Suppress(Regex(r"[nN][aA][mM][eE]")) + Word(alphanums+'"*#+%').setResultsName("name")
        resid = Suppress(Regex(r"[rR][eE][sS][iI][a-z A-Z]*")) + Word(nums).setResultsName("resid")
        seidvoid = Literal('"    "')
        seidw = Word( alphas, max=1 )
        seidn = Group('"' + seidw + '"')
        seid = seidvoid | seidn | seidw
        segid = Suppress(Regex(r"[sS][eE][gG][iI]*[a-z A-Z]") + seid).setResultsName("segid")
        trash = Suppress(LBRC + word + RBRC)
        sel1 = segid | resid | name
        sel2 = segid | resid | name
        sel3 = segid | resid | name
        simpleString1 = sel1 + cond + sel2 +  Optional(cond) + Optional(sel3)
        #simpleString1 =  Optional(segid) + Optional(cond) + resid + cond + Optional(name) + Optional(cond)
        #simpleString2 = OneOrMore(name + Optional(cond) )
        
        #simpleString = simpleString1 | simpleString2
        simpleString = simpleString1 
        
        display = LBRK + simpleString + RBRK
        string_ = Optional(display) + simpleString
        
        sexp = Forward()
        sexpList = Group(LPAR + ZeroOrMore(sexp) + RPAR)
        sexp << ( string_ | sexpList )
        
        if rest == "pcs":
            print "PCS"
            pr = assi + Optional(trash) + sexp.setResultsName("selorig") + sexp + sexp + sexp + sexp.setResultsName("sel1") + numf
        if rest == "rdc":
            print "RDC"
            pr = assi + Optional(trash) + sexp.setResultsName("selorig") + sexp + sexp + sexp + sexp + sexp.setResultsName("sel1") + numf
        
        file = File(tens_in,"r")
        print file
        file_r = []
        for i in file.head(20):
            file_r.append(i.split('!')[0])
        #file_r = file.readlines()
        xxx = ''.join(i for i in file_r)
        
        #print xxx
        print "INI"
        sexpr = pr.searchString(xxx)
        #pprint.pprint(sexpr.asList())
        print "FINE"
        def remove_item(xml):
            #remove xml entry of nasted braket
            join_char=''
            for i in xml.splitlines():
                if not ("<ITEM>" in i or "</ITEM>" in i):
                    #print i
                    join_char += i + "\n"
            return join_char
        
        print remove_item(sexpr.asXML("tens"))
        
        xml_tens = etree.fromstring(remove_item(sexpr.asXML("tens")))
        num_tens = []
        for i in self.findxml(xml_tens, "selorig"):
            for a in self.findxml(i, "resid"):
                num_tens.append(a.text)
       
        return "%s" %list(set(num_tens))[0]
    
    def create_metall(self):
        num_met = 0
        list_res_tens = {}
        pdb_tensor = """ATOM      1  X   ANI  %4s      89.637   6.049   7.058  1.00  3.06
ATOM      2  Y   ANI  %4s      85.838   4.216   6.602  1.00  4.37
ATOM      3  Z   ANI  %4s      89.007   2.095   8.462  1.00  4.35
ATOM      4  OO  ANI  %4s      88.647   3.496   5.834  1.00  4.04
END
"""
        psf_tensor = """PSF

       4 !NTITLE
 REMARKS FILENAME="axis.psf"
 REMARKS   para_anis.pro
 REMARKS molecule for anisotropy
 REMARKS DATE:15-Jun-97  05:13:52       created by user: nico

       4 !NATOM
       1     %4s  ANI  X    XXX    0.000000E+00   10.0000           0
       2     %4s  ANI  Y    YYY    0.000000E+00   10.0000           0
       3     %4s  ANI  Z    ZZZ    0.000000E+00   10.0000           0
       4     %4s  ANI  OO   OOO    0.000000E+00   10.0000           0

       3 !NBOND: bonds
       4       1       4       2       4       3

       3 !NTHETA: angles
       1       4       2       1       4       3       2       4       3

       0 !NPHI: dihedrals


       0 !NIMPHI: impropers


       0 !NDON: donors


       0 !NACC: acceptors


       0 !NNB

       0       0       0       0

       1       0 !NGRP
       0       0       0
"""


        if not os.path.isfile(os.path.join(self.wd, "par_axis_3.pro")):
                shutil.copy2(os.path.join(config['app_conf']['xplor_templ'],"par_axis_3.pro"), os.path.join(self.wd, "par_axis_3.pro"))
                
        for pcs in self.findxml(self.xml, "pcs"):
            print self.check_para_xplor( pcs.get("path"), "pcs")
            list_res_tens[pcs.get("path")] = self.check_para_xplor( pcs.get("path"), "pcs")
        for rdc in self.findxml(self.xml, "rdc"):
            list_res_tens[rdc.get("path")] = self.check_para_xplor( rdc.get("path"), "rdc")
        print "##############LIST_RES_TENS"
        print list_res_tens
        print "###################"
        #search "type" in "metal" attribute
        #if type = metal -> create metal paramter
        #if type = cofactor -> skip creation of metal parameter
        #if RDC diamagnetics
        print "#########XML###################"
        print etree.tostring(self.xml, pretty_print=True)
        print "###############################"
        if self.findxml(self.xml, 'rdc'):
                for rdc in self.findxml(self.xml, "rdc"):
                    if rdc.get("path") in list_res_tens.keys() and rdc.get("res_num") == "none":
                        num_res_tens = []
                        if list_res_tens[rdc.get("path")] not in num_res_tens:
                            rdc_num = list_res_tens[rdc.get("path")]
                            num_res_tens.append(rdc_num)
                            psf_wri = psf_tensor %(rdc_num, rdc_num, rdc_num, rdc_num)
                            psf_o = open(os.path.join(self.wd,"tens_%s.psf" % rdc_num), "w")
                            psf_o.writelines(psf_wri)
                            psf_o.close()
                            if "@%s.psf" % "tens_%s" % rdc_num not in self.metal_psf:
                                self.metal_psf.append("@%s.psf" % "tens_%s" % rdc_num )

        for metal in self.findxml(self.xml, "metal"):
            num_met = num_met + 1
            if metal.get("type") == "cofactor":
                name_met = "XMC" + str(num_met)
                res_name = metal.get("res_name")
                atom_name = metal.get("atom_name")
                res_num = metal.get("res_num")
                self.tab_res_num[res_num] = res_name
                #nonbonded CA2     0.1     2.15        0.1      2.15
                if self.findxml(metal, "restraint"):
                    rest_to_wr = []
                    for restr in self.findxml(metal, "restraint"):
                        restr_res_num = restr.get("resnum")
                        restr_atm_name = restr.get("atom_name")
                        restrt_dist = restr.get("distance")
                        rest_to_wr.append("assign (resid  %s and name %s  ) (resid %s and name %s   )  %s 0.0 0.0 \n" % (restr_res_num, restr_atm_name, res_num, atom_name, restrt_dist )  )   
                    rest_file_name = os.path.join(self.wd, "rest%s.upl" %name_met)
                    rest_file = open(rest_file_name, "w")
                    rest_file.writelines(rest_to_wr)
                    rest_file.close()
                    self.res_metal_list.append("@rest%s.upl"%name_met)

                num_res_tens = []
                print list_res_tens
                if self.findxml(self.xml, 'rdc'):
                    for rdc in self.findxml(self.xml, "rdc"):
                        if rdc.get("path") in list_res_tens.keys():
                            if list_res_tens[rdc.get("path")] not in num_res_tens:
                                rdc_num = list_res_tens[rdc.get("path")]
                                num_res_tens.append(rdc_num)
                                
                                #pdb_wri = pdb_tensor % (pcs_num, pcs_num, pcs_num, pcs_num)
                                #pdb_o = open(os.path.join(self.work_dir,"tens_%s.pdb" % pcs_num), "w")
                                #pdb_o.writelines(pdb_wri)
                                #pdb_o.close()
                                if "tens_%s.pdb" % pcs_num not in self.tensor_pdb:
                                    self.tensor_pdb.append("tens_%s.pdb" % pcs_num)
                                psf_wri = psf_tensor %(rdc_num, rdc_num, rdc_num, rdc_num)
                                psf_o = open(os.path.join(self.wd,"tens_%s.psf" % rdc_num), "w")
                                psf_o.writelines(psf_wri)
                                psf_o.close()
                                if "@%s.psf" % "tens_%s" % rdc_num not in self.metal_psf:
                                    self.metal_psf.append("@%s.psf" % "tens_%s" % rdc_num )
                                    self.metal_tensor_restr.append("assign (resid %s and name %s  ) (resid %s and name OO  )   0.01  0.01  0.00 \n"% (res_num, atom_name, rdc_num ))
                    
                if self.findxml(self.xml, 'pcs'):
                    for pcs in self.findxml(self.xml, "pcs"):
                        if pcs.get("res_num") == res_num :
                            if list_res_tens[pcs.get("path")] not in num_res_tens:
                                pcs_num = list_res_tens[pcs.get("path")]
                                num_res_tens.append(pcs_num)
                                
                                #pdb_wri = pdb_tensor % (pcs_num, pcs_num, pcs_num, pcs_num)
                                #pdb_o = open(os.path.join(self.work_dir,"tens_%s.pdb" % pcs_num), "w")
                                #pdb_o.writelines(pdb_wri)
                                #pdb_o.close()
                                if "tens_%s.pdb" % pcs_num not in self.tensor_pdb:
                                    self.tensor_pdb.append("tens_%s.pdb" % pcs_num)
                                psf_wri = psf_tensor %(pcs_num, pcs_num, pcs_num, pcs_num)
                                psf_o = open(os.path.join(self.wd,"tens_%s.psf" % pcs_num), "w")
                                psf_o.writelines(psf_wri)
                                psf_o.close()
                                if "@%s.psf" % "tens_%s" % pcs_num not in self.metal_psf:
                                    self.metal_psf.append("@%s.psf" % "tens_%s" % pcs_num )
                                    self.metal_tensor_restr.append("assign (resid %s and name %s  ) (resid %s and name OO  )   0.01  0.01  0.00 \n"% (res_num, atom_name, pcs_num ))
                                  
                                    
            if metal.get("type") == "metal":
                name_met = "XM" + str(num_met)
                epsilon = metal.get("epsilon")
                element = metal.get("element")
                res_name = metal.get("res_name")
                aaa=  metal.get("charge")
                charge = float(metal.get("charge"))
                atom_name = metal.get("atom_name")
                rvdw = metal.get("rvdw")
                res_num = metal.get("res_num")
                self.tab_res_num[res_num] = res_name
                segid_met = "    "
                #nonbonded CA2     0.1     2.15        0.1      2.15
                self.metal_par.append("nonbonded %s     %s     %s        %s      %s"%(name_met, epsilon, rvdw,epsilon, rvdw) )
                psf_file_name = os.path.join(self.wd, "%s.psf"%name_met)
                mass = 40.000
                # da psfio.f -> READ(UNIT,'(I8,1X,4A,1X,4A,1X,4A,1X,4A,1X,4A,1X,2G14.6,I8)',ERR=17,END=16)
                psf = """
PSF

       3 !NTITLE
 REMARKS FILENAME="/mnt/disco1/lavoro/TEST_STRUTTURE/amber_REM/PM_xplor_amber/p"
 REMARKS  TOPH19.pep -MACRO for protein sequence
 REMARKS DATE:21-Apr-09  18:21:13       created by user: andrea

       1 !NATOM
       1 %4s %-4s %-4s %-4s %-4s %14.6f%14.6f       0

       0 !NBOND: bonds


       0 !NTHETA: angles


       0 !NPHI: dihedrals


       0 !NIMPHI: impropers


       0 !NDON: donors


       0 !NACC: acceptors


       0 !NNB

       0

       1       0 !NGRP
       0       0       0
    """ % (segid_met, res_num, res_name, atom_name, name_met, charge, mass)
                psf_o = open(psf_file_name, "w")
                psf_o.writelines(psf)
                psf_o.close()
                self.metal_psf.append("@%s.psf" % name_met)
                if self.findxml(metal, "restraint"):
                    rest_to_wr = []
                    for restr in self.findxml(metal, "restraint"):
                        restr_res_num = restr.get("resnum")
                        restr_atm_name = restr.get("atom_name")
                        restrt_dist = restr.get("distance")
                        rest_to_wr.append("assign (resid  %s and name %s  ) (resid %s and name %s   )  %s 0.0 0.0 \n" % (restr_res_num, restr_atm_name, res_num, atom_name, restrt_dist )  )   
                    rest_file_name = os.path.join(self.wd, "rest%s.upl"%name_met)
                    rest_file = open(rest_file_name, "w")
                    rest_file.writelines(rest_to_wr)
                    rest_file.close()
                    self.res_metal_list.append("@rest%s.upl"%name_met)
                    
                num_res_tens = []
                print list_res_tens
                if self.findxml(self.xml, 'rdc'):
                    for rdc in self.findxml(self.xml, "rdc"):
                        if rdc.get("path") in list_res_tens.keys():
                            if list_res_tens[rdc.get("path")] not in num_res_tens:
                                rdc_num = list_res_tens[rdc.get("path")]
                                num_res_tens.append(rdc_num)
                                psf_wri = psf_tensor %(rdc_num, rdc_num, rdc_num, rdc_num)
                                psf_o = open(os.path.join(self.wd,"tens_%s.psf" % rdc_num), "w")
                                psf_o.writelines(psf_wri)
                                psf_o.close()
                                
                                # aggiunger i segid
                                if "@%s.psf" % "tens_%s" % rdc_num not in self.metal_psf:
                                    self.metal_psf.append("@%s.psf" % "tens_%s" % rdc_num )
                                    self.metal_tensor_restr.append("assign (resid %s and name %s  ) (resid %s and name OO  )   0.01  0.01  0.00 \n"% (res_num, atom_name, rdc_num ))
                    
                if self.findxml(self.xml, 'pcs'):
                    for pcs in self.findxml(self.xml, "pcs"):
                        if pcs.get("res_num") == res_num :
                            if list_res_tens[pcs.get("path")] not in num_res_tens:
                                pcs_num = list_res_tens[pcs.get("path")]
                                num_res_tens.append(pcs_num)
                                psf_wri = psf_tensor %(pcs_num, pcs_num, pcs_num, pcs_num)
                                psf_o = open(os.path.join(self.wd,"tens_%s.psf" % pcs_num), "w")
                                psf_o.writelines(psf_wri)
                                psf_o.close()
                                
                                #aggiungere i segid
                                if "@%s.psf" % "tens_%s" % pcs_num not in self.metal_psf:
                                    self.metal_psf.append("@%s.psf" % "tens_%s" % pcs_num )
                                    self.metal_tensor_restr.append("assign (resid %s and name %s  ) (resid %s and name OO  )   0.01  0.01  0.00 \n"% (res_num, name_met, pcs_num ))
                                  
#class PrepareCalculation:
#    '''
#    Class to prepare xplor input file
#    
#    methods:
#            prepare_xplor_pm for paramagnetic calculations
#            prepare_xplor_sc for structure calculations
#    '''
         
        
    def prepare_xplor_pm(self):
        '''
        Prepare xplor input file for paramagnetic calculations
        
        input parameters:
            new: is an xml_parser.dict_accessor to access to the XML objects
            template: is the template file containing the xplor calculation directives
            wd: is the working directory
        return parameters:
            p: the complete fill template 
        '''
        def findxml(xml, tag):
            res = []
            for a in xml.getiterator():
                if a.tag == tag:
                   res.append(a)
            return res
            
        # CHECK defines the input file existance check
        # For testing you can set it to False, in production you have to set to True
        CHECK = False           
        
        t = open(self.template).read()
        p = PMDelimiterTemplate(t)
        
        # Initialize template substitution variables
        seed=init_t=high_step=cool_step=parameter=structure=topology=coordinates=patch=''
        noe_i=dih=flags=xpcs_i=xrdc_i=num_stru_main=num_stru_loop=timestep=''
        xpcs_frun=xrdc_frun=xpcs_fmed=xrdc_fmed=''
        
        #inp = xplor_tools(doc, wd)
        
        self.create_metall()
        self.create_seq()
        print self.metal_psf
        print self.metal_par
        print self.res_metal_list
        print self.tab_res_num
        print self.metal_tensor_restr
        
        print self.metal_psf
        
        #sys.exit()
        
        init_t="evaluate ($init_t = %s)\n" % "1000"
        timestep="evaluate ($timestep = %s)\n" % "0.003"
        flags="flags exclude * include bonds angle dihe impr vdw noe "
        
        if findxml(self.doc, 'pcs') and findxml(self.doc, 'rdc'):
            flags += "xpcs xrdc "
        elif findxml(self.doc, 'pcs'):
            flags += "xpcs "
        elif findxml(self.doc, 'rdc'):
            flags += "xrdc "
        if findxml(self.doc, 'dih'):
            flags += "cdih "
        
        flags += " end \n"
        
        #num_struct = findxml(doc, "output")[0].get("nro_struct")
        
        num_stru_main="evaluate ($end_count = %s)\n" % "10"
        
        num_stru_loop="evaluate ($loop_count = %s)\n" % "1"
        
        high_step="evaluate ($high_steps = %s)\n"%"10000"
        cool_step="evaluate ($cool_steps = %s)\n"%"20000"
    
        parameter="parameter \n"
        parameter+="@TOPPAR:protein.par\n"
        #parameter+="@parallhdg5.3.pro\n"
        
        if len(findxml(self.doc, "nonstdresidues")) > 0:
            parameter += "@nonstandardres.par\n"
        
        #TOPOLOGIES
        if findxml(self.doc, 'cofactor'):
            for cofactor in findxml(self.doc, "cofactor"):
                parameter += "@" + os.path.basename(cofactor.get("par_path")) + "\n"
                #if os.path.isfile(os.path.join(wd,os.path.basename(cofactor.get("par_path")))):
                #    os.remove(os.path.join(wd, os.path.basename(cofactor.get("par_path"))))
                #shutil.copyfile(cofactor.get("par_path"), os.path.join(wd,os.path.basename(cofactor.get("par_path"))))
                
        for i in self.metal_par:
            parameter += "%s\n" %i
       
        if findxml(self.doc, 'pcs') or findxml(self.doc, 'rdc'):
            parameter +=  "@par_axis_3.pro \n"
        parameter += "end\n"
        
        # STRUCTURES
        structure += "structure \n"
        #topology+="@TOPPAR:topallhdg.pro\n"
        #for i in inp.metal_psf:
        #    structure += i + "\n" 
        structure += "@protein.psf\n"
        structure += "end \n"
        
        
        topology += "topology \n"
        if findxml(self.doc, 'cofactor'):
            for cofactor in findxml(self.doc, "cofactor"):
                topology += "@" + os.path.basename(cofactor.get("topology_path")) + "\n"
                #if os.path.isfile(os.path.join(wd,os.path.basename(cofactor.get("topology_path")))):
                #    os.remove(os.path.join(wd, os.path.basename(cofactor.get("topology_path"))))
                #shutil.copyfile(cofactor.get("topology_path"), os.path.join(wd,os.path.basename(cofactor.get("topology_path"))))
        topology += "end \n"
        
        
        #buils segment for new cofactor
        coordinates += "coordinates @protein.pdb\n"
        if findxml(self.doc, 'cofactor'):
            for cofactor in findxml(self.doc, "cofactor"):

                self.infox.add_pdb(cofactor.get("pdb_path"))
            
            pdb_disz , pdb_pos = self.infox.sort_struct_pdb()
            for pdb_x_in in pdb_pos:
                res  = check_pdb_X( open(pdb_x_in , "r").readlines() )
            
            
                coordinates += """
segment                                                {*Generate protein.*}

name="%-4s"                              {*This name has to match the   *}
                                        {*four characters in columns 73*}
                                        {*through 76 in the coordinate *}
                                        {*file; in XPLOR this name is  *}
                                        {*referred to as SEGId.        *}
chain
!     @TOPPAR:toph19.pep                      {*Read peptide bond file;     *}
 coordinates @%s                    {*interpret coordinate file to*}
end                                       {*obtain the sequence.        *}
end
                """ % (res["chain"], os.path.basename(pdb_x_in)) # ricordarsi di aggiungere la catena

        chain_diz = {}
        if findxml(self.doc, 'noe'):
            for i in findxml(self.doc, 'noe'):
                tmp_chain_read = open(i.get("path"),"r").readlines()
                for k in tmp_chain_read:
                    if  len(re.findall(r'[sS][eE][gG][iI][a-z A-Z]?\s+"...."', k)) > 0:
                        for ki in re.findall(r'[sS][eE][gG][iI][a-z A-Z]?\s+"...."', k):
                            chain_diz[ki.split('"')[1].strip()] = ki.split('"')[1]
        print "####CHAIN_DIZ#####"
        print "IMPORTANT -> The chain name are checked only on NOE restraints "
        print chain_diz
        print "##################"
        
        if findxml(self.doc, 'cofactor'):
            for cofactor in findxml(self.doc, "cofactor"):
                #mettere qui funzione per ordinare
                coordinates += "coordinates " + "@" + os.path.basename(cofactor.get("pdb_path")) + "\n"
       
        coordinates += "end\n"
            
        
        if findxml(self.doc, 'disulfide'):
            for i in findxml(self.doc, 'disulfide'):
                chain_ida = ""
                if len(i.get("segida")) == 0:
                    chain_ida = "    "
                elif i.get("segida") in chain_diz.keys():
                    chain_ida = chain_diz[i.get("segida")]
                else:
                    chain_ida = i.get("segida")
                    while len(chain_ida) < 4:
                        chain_ida += " "
                        
                chain_idb = ""
                if len(i.get("segidb")) == 0:
                    chain_idb = "    "
                elif i.get("segidb") in chain_diz.keys():
                    chain_idb = chain_diz[i.get("segidb")]
                else:
                    chain_idb = i.get("segidb")
                    while len(chain_idb) < 4:
                        chain_idb += " "
                            
                patch+='patch DISU reference=1=(segid "%s" and residue %s) reference=2=(segid "%s" and residue %s) end\n' %  (
                            chain_ida,
                            i.get("resnuma"),
                            chain_idb,
                            i.get("resnumb")
                            )
        
        
        #aggiungere il controllo della patch della istidina per questa segid
        
        
        #if findxml(doc, 'histidine'):
        #    for i in findxml(doc, 'histidine'):
        #        print "#### HIS PATCH #######"
        #        print i.get("type"), i.get("resnum")
        #        print "#### HIS PATCH END #######"
        #        patch+="patch %s reference=nil=(residue %s) end\n" %  (
        #                    i.get("type"),
        #                    i.get("resnum"))
                
        if findxml(self.doc, 'patchcof'):
            for i in findxml(self.doc, 'patchcof'):
                chain_ida = ""
                if len(i.get("chaina")) == 0:
                    chain_ida = "    "
                elif i.get("chaina") in chain_diz.keys():
                    chain_ida = chain_diz[i.get("chaina")]
                else:
                    chain_ida = i.get("chaina")
                    while len(chain_ida) < 4:
                        chain_ida += " "
                        
                chain_idb = ""
                if len(i.get("chainb")) == 0:
                    chain_idb = "    "
                elif i.get("chainb") in chain_diz.keys():
                    chain_idb = chain_diz[i.get("chainb")]
                else:
                    chain_idb = i.get("chainb")
                    while len(chain_idb) < 4:
                        chain_idb += " "
                        
                patch+='patch %s reference=1=(segid "%s" and residue %s) reference=2=(segid "%s" and residue %s) end\n' %  (
                            i.get("type"),
                            chain_ida,
                            i.get("resnuma"),
                            chain_idb,
                            i.get("resnumb")
                            )
        
        noe_i="noe \n"
        noe_i+="nres=30000 \n"
            
        if len(self.metal_tensor_restr) > 0:
            noe_i+="class mett \n"
            noe_i+="scale mett 1000 \n"
            for i in self.metal_tensor_restr:
                noe_i+= i + "\n"
        if len(self.res_metal_list) > 0:
            noe_i+="class metc \n"
            noe_i+="scale metc 100 \n"
            for i in self.res_metal_list:
                noe_i+= i + "\n"
                
        noe_i += "class noe_r\n" 
        noe_i += "scale noe_r 50 \n" 
        if findxml(self.doc, 'noe'):   
            for i in findxml(self.doc, 'noe'):
                noe_i += "@%s\n" %os.path.basename(i.get("path"))
                #if os.path.isfile(os.path.join(wd,os.path.basename(i.get("path")))):
                #    os.remove(os.path.join(wd, os.path.basename(i.get("path"))))
                #shutil.copyfile(i.get("path"), os.path.join(wd,os.path.basename(i.get("path"))))
        noe_i+="end\n"
                
        if  findxml(self.doc, 'dih'):
            dih="restraints dihedral \n"
            for i in findxml(self.doc, 'dih'):
                dih += "@%s\n" %os.path.basename(i.get("path"))
                #if os.path.isfile(os.path.join(wd,os.path.basename(i.get("path")))):
                #    os.remove(os.path.join(wd, os.path.basename(i.get("path"))))
                #shutil.copyfile(i.get("path"), os.path.join(wd,os.path.basename(i.get("path"))))
            
            dih+="end \n"
                
            
        stemp=""
        
        if findxml(self.doc, 'pcs'):
            xpcs_i="xpcs \n"
            xpcs_i+="nres=2000 \n"
            pcs_num_class = 0
            for i in findxml(self.doc, 'pcs'):
                pcs_num_class += 1
                pcs_name_class = "%dpcs" % pcs_num_class
                xpcs_i+="class %s \nforce %s\n coeff %s %s\n" % (
                        pcs_name_class,
                        "1",
                        i.get("rh"),
                        i.get("ax")
                    )
                #if os.path.isfile(os.path.join(wd,os.path.basename(i.get("path")))):
                #    os.remove(os.path.join(wd, os.path.basename(i.get("path"))))
                #shutil.copyfile(i.get("path"), os.path.join(wd,os.path.basename(i.get("path"))))
                xpcs_i+="@%s\n"%os.path.basename(i.get("path"))
                    
            xpcs_i+="end\n"
                        
        stemp=""
        if findxml(self.doc, 'rdc'):
            xrdc_i="xrdc \n"
            xrdc_i+="nres=2000 \n"
            rdc_num_class = 0
            for i in findxml(self.doc, 'rdc'):
                rdc_num_class += 1
                rdc_name_class = "%drdc" % rdc_num_class
                xrdc_i+="class %s \nforce %s\n coeff %s %s\n" % (
                        rdc_name_class,
                        "1",
                        i.get("rh"),
                        i.get("ax")
                    )
                #if os.path.isfile(os.path.join(wd,os.path.basename(i.get("path")))):
                #    os.remove(os.path.join(wd, os.path.basename(i.get("path"))))
                #shutil.copyfile(i.get("path"), os.path.join(wd,os.path.basename(i.get("path"))))
                xrdc_i+="@%s\n"%os.path.basename(i.get("path"))
                    
            xrdc_i+="end\n"
            
        if findxml(self.doc, 'pcs'):
            xpcs_frun="xpcs \n"
            xpcs_frun+="foff \n"
            xpcs_frun+="son \n"
            for i in range(len(findxml(self.doc, 'pcs'))):
                xpcs_frun+='evaluate ($filename="%dpse"+encode($count1)+"_"+encode($count))\n' % (i+1)
                xpcs_frun+="save $filename\n"
                xpcs_frun+="frun %d\n"%(i+1)
                 
            xpcs_frun+="soff\n"
            xpcs_frun+="end\n"
        
        if findxml(self.doc, 'rdc'):
            xrdc_frun="xrdc \n"
            xrdc_frun+="foff \n"
            xrdc_frun+="son \n"
            for i in range(len(findxml(self.doc, 'rdc'))):
                xrdc_frun+='evaluate ($filename="%ddip"+encode($count1)+"_"+encode($count))\n' % (i+1)
                xrdc_frun+="save $filename\n"
                xrdc_frun+="frun %d\n"%(i+1)
                 
            xrdc_frun+="soff\n"
            xrdc_frun+="end\n"
                    
        stemp=""    
        seed='!##seed'
        
        ff = p.substitute(
            seed=seed,
            init_t=init_t,
            high_step=high_step,
            cool_step=cool_step,
            parameter=parameter,
            structure=structure,
            topology=topology,
            coordinates=coordinates,
            patch=patch,
            noe_i=noe_i,
            dih=dih,
            flags=flags,
            xpcs_i=xpcs_i,
            xrdc_i=xrdc_i,
            num_stru_main=num_stru_main,
            num_stru_loop=num_stru_loop,
            timestep=timestep,
            xpcs_frun=xpcs_frun,
            xrdc_frun=xrdc_frun,
            xpcs_fmed=xpcs_fmed,
            xrdc_fmed=xrdc_fmed)
        #print "########FF####"
        #print ff
        #print "#############"
        #save info xml
        self.infox.create_xml(self.doc)
        
        return ff
                   
#def prepare_xplor(new, template, wd, pdbfile):
#    '''
#    Function that call the appropriate Prepare class method based on the type
#    of xplor calculation
#    
#    input parameters:
#        new: is an xml_parser.dict_accessor to access to the XML objects
#        template: is the template file containing the xplor calculation directives
#        wd: is the working directory
#    return parameters:
#        out: the full content of the xplor input file
#    '''
#    p=PrepareCalculation()
#    #types=['pm', 'sc']
#    #if new.calculation.protocol.attrib_.type in types:
#    #    f='p.prepare_xplor_%s' % new.calculation.protocol.attrib_.type
#    #    out=eval("%s(%s, %s, %s)" % (f, new, template, wd))
#    if new.calculation.protocol.attrib_.type=='pm':
#        out=p.prepare_xplor_pm(new, template, wd, pdbfile)
#        if new.calculation.protocol.metal_parameter:
#            if new.calculation.protocol.metal_parameter.attrib_.type=='xml':
#                p.prepare_metal(new, wd)
#        return out
#    elif new.calculation.protocol.attrib_.type=='sc':
#        out=p.prepare_xplor_sc(new, template, wd)
#        if new.calculation.protocol.metal_parameter:
#            if new.calculation.protocol.metal_parameter.attrib_.type=='xml':
#                p.prepare_metal(new, wd)
#        return out
        
def extract_patch_top(xml):
    pt = {}
    pf = {}
    for a in xml.getiterator():
            if a.tag == "filetopatch":
                top_file = a.get("top")
                pdb_file = a.get("pdb")
    top = open(top_file, "r").readlines()
    pdb = open(pdb_file, "r").readlines()
    
    pt = take_patch(top)
    #print pt
    
    for i in pt.keys():
        if dual_patch(pt[i]):
            pf[i] = "2"
        else:
            pf[i] = "1"
    
    res  = check_pdb_X(pdb)
    if res.has_key("error"):
        pf = res["error"]
    else:
        for i in pf.keys():
            pf[i] = pf[i] + "-" + res["name"] + "-" + res["num"] + "-" + res["chain"]
            
    print res["name"]
    if not search_residue(top, res["name"]):
        pf = "Error: topology file doesn't contain PDB Residue"
        
    return pf
    

def make_xplor(wd, template, doc):
    #wd = os.getcwd()
    #xml_input = os.path.join(wd,'pyinput.xml')
    #template = os.path.join(wd,'template_xplor_pm.inp')
    #doc = etree.ElementTree(file=xml_input)
    print os.path.join(wd,"xplorPM.inp")
    print doc
    print dir(doc)
    xmlout = etree.tostring(doc, pretty_print=True)
    xmlfout = open(os.path.join(wd, "xplor.xml"),"w")
    xmlfout.writelines(xmlout)
    xmlfout.close()
    p = PrepareCalculation(doc, template, wd)
    out = p.prepare_xplor_pm()
    print os.path.join(wd,"xplorPM.inp")
    print doc
    print dir(doc)
    xmlout = etree.tostring(doc, pretty_print=True)
    xmlfout = open(os.path.join(wd, "xplor.xml"),"w")
    xmlfout.writelines(xmlout)
    xmlfout.close()
    fout = open(os.path.join(wd, "xplorPM.inp"),"w")
    fout.writelines(out)
    fout.close()
