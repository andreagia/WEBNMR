import logging
import random
import shutil
import copy
import os, subprocess
from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from webenmr.lib.base import *
from mimetypes import guess_type
import fileinput
import os
import sys
import shutil
import random
import tarfile
from lxml import etree
import re
from datetime import datetime
from webenmr.model import Projects, Calculations, Jobs, CalculationTipology, Users
from webenmr.model.meta import Session
from operator import itemgetter, attrgetter
import numpy, string, pickle
#import matplotlib.pyplot as plt

log = logging.getLogger(__name__)
os.umask(0002)

CE_REQ = "as-ce01.euasiagrid.org deimos.htc.biggrid.nl ce-enmr.chemie.uni-frankfurt.de phoebe.htc.biggrid.nl"
#CE_REQ = "gantt.cefet-rj.br grid001.cecalc.ula.ve cream-ce-grid.obspm.fr ce-enmr.chemie.uni-frankfurt.de as-ce01.euasiagrid.org ce01.dur.scotgrid.ac.uk deimos.htc.biggrid.nl"
#XML_STATUS = "/opt/jobcontrol/STATUS.xml"
XML_STATUS = os.path.join(config['app_conf']['maxocc_data'], "STATUS.xml")

def findxml(xml,tag):
    res = []
    for a in xml.getiterator():
        if a.tag == tag:
           res.append(a)
    return res

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
    o = open(fout,"w")
    o.write( re.sub(sin, sout, data) )
    o.close()
#argomenti esterni dizionario con locazione certificato, nome progetto, directory di lavoro


# entra diz['name'] nome progetto


def checkGRID_maxocc():
    black_list = []
    black_list.append("ce01.eela.if.ufrj.br")
    black_list.append("ce02.eela.if.ufrj.br")
    black_list.append("cream-ce-grid.obspm.fr")
    print "##########CE BLACK LIST##############"
    print black_list
    print "######################################"
    dd = "gazon.nikhef.nl"
    ddJ = """( other.GlueCEUniqueID == "gazon.nikhef.nl:8443/cream-pbs-medium" || other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-verylong");"""
    if os.path.exists("/opt/checkGRID/pickle.pck"):
        file_pickle = open("/opt/checkGRID/pickle.pck", "r") # read mode
        job = pickle.load(file_pickle)
    else:
        print "NO JOBS INFORMATIONS "
        return dd
    
    #pprint(job)
    queue_time = 721
    req_cpu = 100
    ce_sub = []

    for check_ce in job.keys():
        if job[check_ce].has_key("status"):
            if job[check_ce]["status"] == "OK":
                if job[check_ce].has_key("VOMaxCPUTime") and job[check_ce].has_key("TotalCPUs"):
                    time = job[check_ce]["VOMaxCPUTime"]
                    TotCPU = job[check_ce]["TotalCPUs"]
                    if time.isdigit() and TotCPU.isdigit():
                        if (int(job[check_ce]["VOMaxCPUTime"]) > queue_time and int(job[check_ce]["VOMaxCPUTime"]) < 9999999999 ) and (int(job[check_ce]["VOMaxCPUTime"]) > req_cpu):
                            ce_sub.append(check_ce)
    print ce_sub
    if len(ce_sub) > 0:
        list_ce = ""
        list_ceJt = "( "
        for i in ce_sub:
            if i.split(":")[0] not in black_list:
                print i.split(":")[0]
                list_ce = list_ce + " " + i.split(":")[0]
                list_ceJt = list_ceJt + ' other.GlueCEUniqueID == "%s" ||' %i
            list_ceJ = list_ceJt[:-2] + ");\n"
    else:
        list_ce = dd
        list_ceJ = ddJ
        
    print "############# CE Selected for MAXOCC JOB ################"
    print list_ce
    print "#############      JDL ##################################"
    print list_ceJ
    print "#########################################################"
    return list_ce, list_ceJ

def crea_input(diz):
    template = config['app_conf']['maxocc_templ']
    wdir = os.path.join(config['app_conf']['maxocc_data'], session.get('DIR_CACHE'), diz['name'])
    loc_dir = os.getcwd()
    os.chdir(wdir)
    XML_IN = wdir
    #building XML
    root = etree.Element("JobControl")
    attr = {}
    #attr["file"] =  "/home/webenmr/WebENMR/data/.cert/x509up_u1"
    attr["file"] =  "/home/webtest/WebENMR/data/.cert/x509up_u1"
    etree.SubElement(root, "Certificate", attrib = attr)
    attr = {}
    attr["name"] =  diz['name']
    project = etree.SubElement(root, "Project", attrib = attr)
    #lista ce
    
    SE_CEres, CEres = checkGRID_maxocc()
    
    etree.SubElement(project, "CERequired").text = SE_CEres
    seinput = etree.SubElement(project, "SEInput")
    
    attr = {}
    attr["time"] =  "90"
    etree.SubElement(seinput, "LifeTime", attrib = attr)
    
    raN = str(random.randint(100000000, 999999999)) + '_'
    #file1 = etree.SubElement(seinput, "Files")
    file2 = etree.SubElement(seinput, "Files")
    attr = {}
    attr["name"] =  "se-enmr.cerm.unifi.it"
    #etree.SubElement(file1, "Destination", attrib = attr)
    etree.SubElement(file2, "Destination", attrib = attr)
    #etree.SubElement(file1, "Replica").text = "FROM_CE tbn18.nikhef.nl"
    etree.SubElement(file2, "Replica").text = "FROM_CE"
    #attr1 = {}
    attr2 = {}
    
    #strMAX = os.path.join(wdir, "struttureMAX.tgz")
    #tar = tarfile.open(strMAX,"w:gz")
    #
    #attr1["local"] = strMAX
    #attr1["remote"] = raN + "strMAX.tgz"
    
    attr2["local"] =  os.path.join(wdir, "curve_input.tgz")
    attr2["remote"] = raN + "cu_in.tgz"
    #etree.SubElement(file1, "Names", attrib = attr1)
    etree.SubElement(file2, "Names", attrib = attr2)
    home = os.path.join(os.getcwd(),"sub_usecase")
    try:
        os.mkdir(home)
    except:
        os.removedirs(home)
        os.mkdir(home)
        print "Directory sub_usecase was removed and recreated"
    for w in diz['weight']:
        for i in diz['numstruct']:
            dir_w = os.path.join(home, "input_w%s_%d" %(w, i))
            os.mkdir(dir_w)
            #shutil.copyfile(os.path.join(template, "maxoccenmr.64"), os.path.join(dir_w, "maxoccenmr.64"))
            print os.getcwd()
            print dir_w
            shutil.copy("./in.tgz", os.path.join(dir_w, "in.tgz"))
            
            attr = {}
            attr["jdl"] = os.path.join(dir_w, "run_a-map_mu.jdl")
            etree.SubElement(project, "Job", attrib = attr)
            
            replace_str(os.path.join(template, "run_a-map_mu.jdl"), os.path.join(dir_w, "run_a-map_mu.jdl"), "CAMBIA", dir_w + "/")
            replace_str(os.path.join(dir_w, "run_a-map_mu.jdl"), os.path.join(dir_w, "run_a-map_mu.jdl"), "SEL_CE", CEres )
                    #successivamente inserire qui la lista dei CE
                    #line=line.replace("CE_da_usare", "lista ce in formato require. jdl")
                    
            replace_str(os.path.join(template, "run_a-map.sh"), os.path.join(dir_w, "run_a-map.sh"), "./maxoccenmr.64" , "./maxoccenmr.64 %s %s " %(i, w))
            #replace_str(os.path.join(dir_w, "run_a-map.sh"), os.path.join(dir_w, "run_a-map.sh"), "STRUM1", raN + "strMAX.tgz")
            replace_str(os.path.join(dir_w, "run_a-map.sh"), os.path.join(dir_w, "run_a-map.sh"), "STRUM2", raN + "cu_in.tgz")
    
    
    filexml = etree.tostring(root, pretty_print=True)
    
    #xml_file = "/opt/jobcontrol/xml_in/maxocc%s%s.xml" %(raN[0:3],diz['name'])
    xml_file = os.path.join(config['app_conf']['maxocc_data'], "xml_in", "maxocc%s%s.xml" %(raN[0:3],diz['name']))
    xml_file_w = open(xml_file, 'w')
    xml_file_w.write(filexml)
    xml_file_w.close()    
    os.chdir(loc_dir)


class MaxoccController(BaseController):
    
    def __before__(self):
        """
        This __before__ method calls the parent method, and then sets up the
        tabs on the page.
        """
        c.page_base = u'MaxOcc'
        c.page_title = u'MaxOcc'
        
        random.seed()
        if session.get('DIR_CACHE', None) is None:
            session['DIR_CACHE'] = os.path.join(config['app_conf']['maxocc_data'], str(random.randint(100000000, 999999999)))
            session.save()
        elif 'maxocc_data' not in session.get('DIR_CACHE'):
            session['DIR_CACHE'] = os.path.join(config['app_conf']['maxocc_data'], str(random.randint(100000000, 999999999)))
            session.save()
        if not os.path.isdir(session.get('DIR_CACHE')):
            os.makedirs(session.get('DIR_CACHE'))
        #else:
        #    shutil.rmtree(session.get('DIR_CACHE'))
        #    os.makedirs(session.get('DIR_CACHE'))
    
    def check_status(self):
        conto = request.POST.get('calcname')
        percentuale = 80.0
        doc = etree.ElementTree(file=XML_STATUS)
        output = []
        num_finiti = 0
        for a in doc.getiterator():
            if a.tag == "jobs":
                if a.get("Project_name") == conto:
                    if a.get("Status") == "E":
                        output.append(a.get("output"))
                    num_finiti = a.get("num_job_project")
        
        if len(output) > (percentuale/100)*float(num_finiti):
            #lanciare l'analisi
            path_proj = ''
            path_proj = path_proj + "/".join(output[0].split("/")[:-2])
            print 'project path: %s' %path_proj
            #cmd_status = os.system("/home/webtest/WebENMR/data/maxocc/templates/ana_script.sh")
            #subprocess.Popen('cd %s; /home/webtest/WebENMR/data/maxocc/templates/ana_script.sh' %(path_proj, os.path.basename(ranch_pcs.filename)), shell=True).wait()
            #subprocess.Popen('cd %s; /home/webtest/WebENMR/data/maxocc/templates/num2.sh' %(path_proj, os.path.basename(ranch_pcs.filename)), shell=True).wait()
            #copiare i risultati
            return "True"
        else:
            return "False"
    
    def download(self, conto):
        doc = etree.ElementTree(file=XML_STATUS)
        output = []
        for a in doc.getiterator():
            if a.tag == "jobs":
                if a.get("Project_name") == conto:
                    if a.get("Status") == "E":
                        output.append(a.get("output"))
        filename = output
        if len(output):
            permanent_file = open(filename, 'rb')
            data = permanent_file.read()
            permanent_file.close()
            response.content_type = guess_type(filename)[0] or 'text/plain'
            response.headers['Content-Disposition'] = 'attachment; filename="%s"'%(requested_filename)
            return data
        
    def download_examples(self):
        what = request.GET.get("type")
        if what:
            permanent_file = open(os.path.join(config['app_conf']['maxocc_templ'], 'examples', what), 'rb')
            data = permanent_file.read()
            permanent_file.close()
            response.content_type = guess_type(what)[0] or 'text/plain'
            response.headers['Content-Disposition'] = 'attachment; filename="%s"'%(what)
            return data
        else:
            print os.path.join(config['app_conf']['maxocc_templ'], 'examples', what)
            
    
    # python 2.4's tarfile doesn't have extractall.
    def extractall(self, tf, path="."):
        for tarinfo in tf:
            if tarinfo.isdir():
                # Extract directories with a safe mode.
                tarinfo = copy.copy(tarinfo)
                tarinfo.mode = 0700
            tf.extract(tarinfo, path)
        
    def getDataJob(self):
        diz = {}
        calcname = request.POST.get('maxocc-calcname')
        prj_id = request.POST.get('prj_id')
        diz['name'] = calcname
        
        base_path = os.path.join(config['app_conf']['maxocc_data'], session.get('DIR_CACHE'), calcname)
        try:
            os.makedirs(base_path)
        except:
            shutil.rmtree(base_path)
            os.makedirs(base_path)
            print "rimosso calcolo esistente %s" %base_path
            

        print "MAXOCC directory lavoro " + base_path
        numstruct = request.POST.get('numstruct')
        #creo lista di strutture da prendere
        listnumstruct = numstruct.split(",")
        finalstructs = []
        for i in listnumstruct:
            i = i.replace(" ", "")
            listi = i.split("-")
            if len(listi) > 1:
                for j in range(int(listi[0]),int(listi[1])+1):
                    finalstructs.append(j)
            else:
                listi = listi[0].replace(" ", "")
                finalstructs.append(int(listi))
        diz['numstruct'] = finalstructs
        weightconf = request.POST.get('weightconf')
        w = weightconf.replace(" ", "").split(',')
        w.sort()
        diz['weight'] = w
        str2 = '%d\n%s' % (len(finalstructs), '\n'.join(w))
        self.writeWeight(str2, 'maxocc.wst', base_path)
        
        expavetf = request.POST.get("expavetf","")
        tfstd = request.POST.get("tfstd","")
        
        if expavetf and tfstd:
            artfile = open(os.path.join(base_path, "artificial.mo"), 'w')
            artfile.write(expavetf + ' ' + tfstd)
            
        bias = request.POST.get('thresholds')
        b = bias.replace(" ", "").split(',')
        str2 = '%s' % '\n'.join(b)
        self.writeBias(str2, 'maxocc.tre', base_path)
        
        maxnumstruct = request.POST.get('maxnumstruct')
        numstructstep = request.POST.get('numstructstep')
        numstepaddstruct = request.POST.get('numstepaddstruct')
        initnumens = request.POST.get('initnumens')
        ensremstep = request.POST.get('ensremstep')
        starttemp = request.POST.get('starttemp')
        targetmutrate = request.POST.get('targetmutrate')
        weightmin = request.POST.get('weightmin')
        maxnumcg = request.POST.get('maxnumcg')
        cggradtol = request.POST.get('cggradtol')
        satol = request.POST.get('satol')
        target = request.POST.get('target')
        maxnumiter = request.POST.get('maxnumiter')
        numtempstep = request.POST.get('numtempstep')
        weightSA = request.POST.get('weightSA')
        weightinitreplace = request.POST.get('weightinitreplace')
        weightaddstruct = request.POST.get('weightaddstruct')
        weightheusteepdesc = request.POST.get('weightheusteepdesc')
        iterrestart = request.POST.get('iterrestart')
        
        self.writeInput_maxocc(maxnumstruct, numstructstep, numstepaddstruct, initnumens, ensremstep, starttemp,
           targetmutrate, weightmin, maxnumcg, cggradtol, satol, target, maxnumiter, numtempstep, weightSA,
           weightinitreplace, weightaddstruct, weightheusteepdesc, iterrestart, 'input_maxocc', base_path)

        exp_path = os.path.join(base_path, 'experimental')
        os.makedirs(exp_path)
        
        relweightpcs = request.POST.get('relweightpcs')
        relweightrdc = request.POST.get('relweightrdc')
        relweightpre = request.POST.get('relweightpre')
        relweightsax = request.POST.get('relweightsax')
        multharmonic = request.POST.get('multiharmonic')
        
        relative = '%s %s %s %s %s\n' % (relweightpcs, relweightrdc, relweightpre, relweightsax, multharmonic)
        frel = open(os.path.join(exp_path, 'pesirelativi'), 'w')
        frel.write(relative)
        frel.close()
        inputproj = request.POST.get("proj_list")
        prj = Session.query(Projects).filter(and_(Projects.name == inputproj, Projects.removed == False, Projects.owner_id == session['REMOTE_USER'])).all()
        project = prj[0]
        home = project.owner.home
        inputcalc = request.POST.get("calc_list")
        shutil.copy(os.path.join(config['app_conf']['working_dir'], home, inputproj, "maxocc", inputcalc, "input", "input_1", "in.tgz"), base_path)
        tarintgz = tarfile.open(os.path.join(base_path, "in.tgz"), "r")
        pcsfile = tarintgz.extractfile(tarintgz.getmember("input.pcs")).read()
        pcsfilewrite = open(os.path.join(base_path, "input.pcs"), "w")
        pcsfilewrite.write(pcsfile)
        pcsfilewrite.close()
        
        rdcfile = tarintgz.extractfile(tarintgz.getmember("input.rdc")).read()
        rdcfilewrite = open(os.path.join(base_path, "input.rdc"), "w")
        rdcfilewrite.write(rdcfile)
        rdcfilewrite.close()
        
        #if input.pre are not present create an empty one
        if "input.pre" in tarintgz.getnames():
            prefile = tarintgz.extractfile(tarintgz.getmember("input.pre")).read()
        else:
            prefile = ""
        prefilewrite = open(os.path.join(base_path, "input.pre"), "w")
        prefilewrite.write(prefile)
        prefilewrite.close()
        
        #convert rdc and pcs and store them in ./experimental folder
        cmdpcs = "cd %s; /bin/cat input.pcs | /bin/awk '{print $4, $7}' >./experimental/1.pcs" %base_path
        subprocess.Popen(cmdpcs, shell=True).wait()
        cmdrdc = "cd %s; /bin/cat input.rdc | /bin/awk '{print $4, $7}' >./experimental/1.rdc" %base_path
        subprocess.Popen(cmdrdc, shell=True).wait()
        cmdrdc = "cd %s; /bin/cat input.pre | /bin/awk '{print $4, $7}' >./experimental/1.pre" %base_path
        subprocess.Popen(cmdrdc, shell=True).wait()
        
        #self.extractall(tarintgz, base_path)
        #exp_pcs = request.POST.get('exp-pcs') #ora va preso da un progetto esistente
        #self.saveFile(exp_pcs, exp_path, "1.pcs")
        #prj = Session.query(Projects).filter(and_(Projects.name == inputproj, Projects.removed == False, Projects.owner_id == session['REMOTE_USER'])).all()
        #home = prj[0].owner.home
        
        #shutil.copy(os.path.join(config['app_conf']['working_dir'], home, inputproj, "maxocc", inputcalc, "input.pcs"), os.path.join(exp_path, "1.pcs"))
        #exp_rdc = request.POST.get('exp-rdc') #ora va preso da un progetto esistente
        #self.saveFile(exp_rdc, exp_path, "1.rdc")
        #shutil.copy(os.path.join(config['app_conf']['working_dir'], home, inputproj, "maxocc", inputcalc, "input.rdc"), os.path.join(exp_path, "1.rdc"))
        #awk print '{$4, $7} >1.rdc '
        exp_sax = request.POST.get('exp-saxs')
        self.saveFile(exp_sax, exp_path, "1.saxs")
        exp_sax_blind = request.POST.get("exp-saxs-blind")
        
        #exp_distance = request.POST.get('exp-distance') #va creato con gli script esistenti
        #self.saveFile(exp_distance, exp_path, "distanze") #va creato con gli script esistenti
        #VA LANCIATO LO SCRIPT distcalc
        
        
        #exp_struct = request.POST.get('exp-struct') #va creato con gli script esistenti
        #self.saveFile(exp_struct, exp_path, "strutture")
        shutil.copy(os.path.join(config['app_conf']['working_dir'], home, inputproj, "maxocc", inputcalc, "output", "output_1", "str_info.tgz"), os.path.join(base_path, "str_info.tgz"))
        tarstr_infotgz = tarfile.open(os.path.join(base_path, "str_info.tgz"), "r")
        #str_infofile = tarstr_infotgz.extractfile(tarstr_infotgz.getmember("str_info.tgz")).read()
        #str_infofilewrite = open(os.path.join(base_path, "str_info.tgz"), "w")
        #str_infofilewrite.write(str_infofile)
        #str_infofilewrite.close()
        
        
        #exp_filename = request.POST.get('exp-filename') #va creato con gli script esistenti
        #self.saveFile(exp_filename, exp_path, "nomifiles")
        nomifile = open(os.path.join(base_path, "experimental", "nomifiles"), "w")
        numfinalstructs = str(len(finalstructs))
        structtgzfile = tarfile.open(os.path.join(config['app_conf']['working_dir'], home, inputproj, "maxocc", inputcalc, "output", "output_1", "str_info.tgz"), "r")
        memberlist = structtgzfile.getmembers()
        nomifile.write("%s\n"%(len(memberlist)-1))
        saxsfile = open(os.path.join(base_path, "experimental", "1.saxs"), "r")
        saxsfilelist = saxsfile.readlines()
        saxsfile.close()
        numrows = len(saxsfilelist)-int(exp_sax_blind)
        nomifile.write(" %d "%numrows)
        nomifile.write("%s\n"%exp_sax_blind)
        pcsfile = open(os.path.join(base_path, "experimental", "1.pcs"), "r")
        pcsfilelist = pcsfile.readlines()
        pcsfile.close()
        nomifile.write(" %d\n"%len(pcsfilelist))
        rdcfile = open(os.path.join(base_path, "experimental", "1.rdc"), "r")
        rdcfilelist = rdcfile.readlines()
        rdcfile.close()
        nomifile.write(" %d\n"%len(rdcfilelist))
        totlines_pre = request.POST.get('pre-total', "0")
        force_pre = request.POST.get('pre-const', "0")
        nomifile.write("%s %s\n"%(totlines_pre, force_pre))
        for i in range(1, (len(memberlist))):
            str3 = '0'*(5 - len(str(i)))+"%d.inf" %i
            nomifile.write(str3+"\n")
        nomifile.close()
        self.extractall(tarstr_infotgz, base_path)
        tarstr_infotgz.close()
        shutil.copy(os.path.join(config['app_conf']['maxocc_templ'], "descr_grid"), os.path.join(base_path, "descr_grid"))
        cmd = "cd %s; /bin/chmod 754 descr_grid; ./descr_grid" %base_path
        subprocess.Popen(cmd, shell=True).wait()
        
        
        shutil.copy(os.path.join(config['app_conf']['maxocc_templ'], "distcalcnew"), os.path.join(base_path, "distcalc"))
        #cmd = "cd %s; /bin/chmod 754 distcalc; ./distcalc 7 >./experimental/distanze" %base_path
        #subprocess.Popen(cmd, shell=True).wait()
        
        
        loc_dir = os.getcwd()
        os.chdir(base_path)
        #os.makedirs(os.path.join(base_path,"curveint"))
        #os.makedirs(os.path.join(base_path,"curvepcs"))
        #os.makedirs(os.path.join(base_path,"curverdc"))
        
        #ranch_pcs = request.POST.get('ranch-pcs')
        #self.saveFile(ranch_pcs, base_path, os.path.basename(ranch_pcs.filename))
        #f = ranch_pcs.filename.split('\\')
        ##subprocess.Popen('cd curvepcs; tar xvfz ../%s ; cd ..' %os.path.basename(ranch_pcs.filename), shell=True).wait()
        #tarpcs = tarfile.open(os.path.join(base_path, os.path.basename(ranch_pcs.filename)),"r:gz")
        #tarpcslist = tarpcs.getmembers()
        #print "Untar PCS"
        #for i in tarpcslist:
        #
        #    tarpcs.extract(i, path="./curvepcs")
        ##os.system('cd curvepcs; tar xvfz ../%s ; cd ..' %os.path.basename(ranch_pcs.filename) )
        #
        #ranch_rdc = request.POST.get('ranch-rdc')
        #self.saveFile(ranch_rdc, base_path, os.path.basename(ranch_rdc.filename))
        ##subprocess.Popen('cd curverdc; tar xvfz ../%s ; cd ..' %os.path.basename(ranch_rdc.filename), shell=True).wait()
        #tarrdc = tarfile.open(os.path.join(base_path, os.path.basename(ranch_rdc.filename)),"r:gz")
        #print "Untar RDC"
        #tarrdclist = tarrdc.getmembers()
        #for i in tarrdclist:
        #    tarrdc.extract(i, path="./curverdc")
        ##os.system('cd curverdc; tar xvfz ../%s ; cd ..' %os.path.basename(ranch_rdc.filename) )
        #
        #ranch_int = request.POST.get('ranch-int')
        #self.saveFile(ranch_int, base_path, os.path.basename(ranch_int.filename))
        ##subprocess.Popen('cd curveint; tar xvfz ../%s ; cd ..' %os.path.basename(ranch_int.filename), shell=True).wait()
        #tarint = tarfile.open(os.path.join(base_path, os.path.basename(ranch_int.filename)),"r:gz")
        #print "Untar SAX"
        #tarintlist = tarint.getmembers()
        #for i in tarintlist:
        #    tarint.extract(i, path="./curveint")
        #os.system('cd curveint; tar xvfz ../%s ; cd ..' %os.path.basename(ranch_int.filename) )
        #subprocess.Popen('tar cvfz curve_input.tgz curvepcs curverdc curveint', shell=True).wait()
        print "creo curve_input.tgz"
        shutil.copy(os.path.join(config['app_conf']['working_dir'], home, inputproj, "maxocc", inputcalc, "output", "output_1", "curves.tgz"), os.path.join(base_path, "curve_input.tgz"))
        #tar = tarfile.open(os.path.join(base_path,"curve_input.tgz"),"w:gz")
        #tar.add(os.path.join(base_path,"curvepcs"), arcname="curvepcs")
        #tar.add(os.path.join(base_path,"curverdc"), arcname="curverdc")
        #tar.add(os.path.join(base_path,"curveint"), arcname="curveint")
        #tar.close()
        print "Ho finito di creare curve_input.tgz"
        #os.system('tar cvfz curve_input.tgz curvepcs curverdc curveint')
        shutil.copy(os.path.join(config['app_conf']['maxocc_templ'], "maxoccenmr-new-ind.64"), os.path.join(base_path, "maxoccenmr.64"))
        print "###################INTGZ#########################"
        print os.getcwd()
        #subprocess.Popen('tar cvfz ./in.tgz ./experimental ./input_maxocc ./maxoccenmr.64 ', shell=True).wait()
        #os.system('tar cvfz ./in.tgz ./experimental ./input_maxocc ./maxoccenmr.64')
        tar = tarfile.open(os.path.join(base_path,"in.tgz"),"w:gz")
        tar.add(os.path.join(base_path,"experimental"), arcname="experimental")
        tar.add(os.path.join(base_path,"input_maxocc"), arcname="input_maxocc")
        tar.add(os.path.join(base_path,"maxoccenmr.64"), arcname="maxoccenmr.64")
        #tar.add(os.path.join(base_path,"descr_grid"), arcname="descr_grid")
        tar.add(os.path.join(base_path,"distcalc"), arcname="distcalc")
        tar.close()
        #while not os.path.exists("./in.tgz"):
         #   print "#################PROVO###########################"
          #  subprocess.Popen('/bin/tar cvfz ./in.tgz ./experimental ./input_maxocc ./maxoccenmr.64 ', shell=True).wait()
            
        print "############################################"
        crea_input(diz)
        os.chdir(loc_dir)
        
        
        prj = Session.query(Projects).filter(and_(Projects.name == inputproj, Projects.removed == False, Projects.owner_id == session['REMOTE_USER'])).all()
        project = prj[0]
        calc_type = Session.query(CalculationTipology).filter(CalculationTipology.tipology == session['PORTAL'])
        print project.owner.home
        print project.name
        print calcname
        w_dir = os.path.join(config['app_conf']['working_dir'],
                            project.owner.home,
                            project.name,
                            calc_type[0].tipology,
                            calcname)
        print w_dir
        
        pdir = os.path.join(config['app_conf']['working_dir'], project.owner.home, project.name, calc_type[0].tipology, calcname, "input")
        try:
            os.makedirs(pdir)
        except IOError, (errno, strerror):
            h.flash.set_message('An error occurred during calculation creation.', 'Error')
            h.redirect('/calculations/newcalc')
        shutil.copy(os.path.join(config['app_conf']['maxocc_data'], session.get('DIR_CACHE'), diz['name'], "in.tgz"), pdir)
         # New database entry creation
        new_calc = Calculations()
        new_calc.name = calcname
        
        new_calc.project = project
        new_calc.calc_type = calc_type[0]
        new_calc.creation_date = datetime.now()
        new_calc.jobs_to_submit = 1
        Session.add(new_calc)
        Session.commit()
        
        j = Jobs()
        j.calculation = new_calc
        j.guid = u''
        j.start_date = datetime.now()
        j.dir_name = w_dir
        j.status = u'S'
        j.log = u'Job waiting to be processed'
        msg = 'Job successfully submitted'
        h.flash.set_message(msg, 'success')
        Session.add(j)
        Session.commit()
        #h.redirect('/jobs/show/all')
    
    def saveFile(self, fname, where, name=None):
        if name:
            namef = name
        else:
            namef = fname.filename.split('\\')
        #f = fname.filename.split('\\')
        rfname = os.path.join(where, namef)
        permanent_file = open(rfname, 'wb')
        shutil.copyfileobj(fname.file, permanent_file)
        fname.file.close()
        permanent_file.close()
    
    def helpinfo(self):
        field = request.POST.get('field')
        info = open(os.path.join(config['app_conf']['properties'], "maxocc-info.properties"))
        l = 'pipppo'
        for line in info:
            if line.startswith(field):
                l = line.split('=')[1]
                break
        return l
        
    def writeInput_maxocc(self, maxnumstruct, numstructstep, numstepaddstruct, initnumens, ensremstep, starttemp,
           targetmutrate, weightmin, maxnumcg, cggradtol, satol, target, maxnumiter, numtempstep, weightSA,
           weightinitreplace, weightaddstruct, weightheusteepdesc, iterrestart, name, where):
        
        str = '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n' \
        % (maxnumstruct, numstructstep, numstepaddstruct, initnumens, ensremstep, starttemp,
           targetmutrate, weightmin, maxnumcg, cggradtol, satol, target, maxnumiter, numtempstep, weightSA,
           weightinitreplace, weightaddstruct, weightheusteepdesc, iterrestart)
        inp_file = os.path.join(where, name)
        f = open(inp_file,"w")
        f.write(str)
        f.close()
    
    def writeWeight(self, str, name, where):
        inp_file = os.path.join(where, name)
        f = open(inp_file,"w")
        f.write(str)
        f.close()
        
    def writeBias(self, str, name, where):
        inp_file = os.path.join(where, name)
        f = open(inp_file,"w")
        f.write(str)
        f.close()
        
    def projects_list(self):
        _proj = Session.query(Projects).filter(and_(Projects.owner_id == session['REMOTE_USER'], Projects.removed == False)).order_by(Projects.name).all()
        #proj_list = sorted(_proj, key=attrgetter('name'))
        proj_list = _proj
        if proj_list:
             projs_name = proj_list[0].name
             for item in proj_list[1:]:
                  projs_name = projs_name + ','+item.name
             return projs_name
            
            
    def calculations_list(self):
        proj = request.GET.get("proj")
        prj = Session.query(Projects).filter(and_(Projects.name == proj, Projects.removed == False, Projects.owner_id == session['REMOTE_USER'])).all()
        calcsmaxocc = Session.query(Calculations).filter(and_(Calculations.project_id == prj[0].id, Calculations.removed == False, Calculations.calc_type_id == 5)).order_by(Calculations.name).all()
        if calcsmaxocc:
            l = ''
            #l = calcsmaxocc[0].name
            for i in calcsmaxocc:
                 l += '%s,' % i.name
            l = l[:-1]
            return l
        else:
            l = ''
    
    def ranch_calculations_list(self):
        proj = request.GET.get("proj")
        prj = Session.query(Projects).filter(and_(Projects.name == proj, Projects.removed == False, Projects.owner_id == session['REMOTE_USER'])).all()
        home = prj[0].owner.home
        calcsmaxocc = Session.query(Calculations).filter(and_(Calculations.project_id == prj[0].id, Calculations.removed == False, Calculations.calc_type_id == 6)).order_by(Calculations.name).all()
        if calcsmaxocc:
            l = ''
            for i in calcsmaxocc:
                calc_path = os.path.join(config['app_conf']['working_dir'], home, proj, "maxocc", i.name)
                if os.path.exists(os.path.join(calc_path, "output", "output_1","curves.tgz")):    
                    l += '%s,' % i.name
            l = l[:-1]            
            return l
        else:
            l = ''
    
    def existPRE(self):
        totlines = 0
        proj = request.POST.get("proj")
        calcname = request.POST.get("calc")
        base_path = os.path.join(config['app_conf']['maxocc_data'], session.get('DIR_CACHE'), calcname)
        prj = Session.query(Projects).filter(and_(Projects.name == proj, Projects.removed == False, Projects.owner_id == session['REMOTE_USER'])).all()
        calc = Session.query(Calculations).filter(and_(Calculations.project_id == prj[0].id, Calculations.removed == False, Calculations.calc_type_id == 6, Calculations.name == calcname)).order_by(Calculations.name).all()
        home = prj[0].owner.home
        if calc:
            calc_path = os.path.join(config['app_conf']['working_dir'], home, proj, "maxocc", calc[0].name)
            tarin = tarfile.open(os.path.join(calc_path, "input", "input_1", "in.tgz"), "r:gz")
            if "input.pre" in tarin.getnames():
                tarin.extract("input.pre", base_path)
                tarin.close()
                prefile = open(os.path.join(base_path, "input.pre")).readlines()
                totlines = len(prefile)
            else:
                totlines = 0
        return str(totlines)
    
    def check_ava(self):
        proj = request.POST.get("proj_name", "")
        calc = request.POST.get("calc_name", "")
        if proj and calc:
            p = Session.query(Projects).filter(and_(Projects.name==proj, Projects.owner_id==session['REMOTE_USER'], Projects.removed == False)).all()
            c = Session.query(Calculations).filter(and_(Calculations.name==calc, Calculations.project_id==p[0].id, Calculations.removed == False, Calculations.calc_type_id == 5)).all()
            if c:
                return 'already in use!' 
            else:
                return 'Ok'
        return ''
    
    def merge(self):
        return render('/calculations/maxoccMerge.mako')
        
    def merge_do(self):
        #usa il valore di soglia in argv[1]
        #Usa ini.str = cat */mo-usr.crv |awk '{print $1}' come elenco strutture
        #Usa ini.wei = grep s */mo-usr.crv come elenco di tutti i possibili pesi
        #Usa ini.crv = cat */mo-usr.crv
        projs = request.POST.getall("proj_list")
        calcs = request.POST.getall("calc_list")
        
        projsClenead = []
        for p in projs:
            if p != 'none':
                projsClenead.append(p)
        print projs
        print projsClenead
        print calcs
        
        base_path = os.path.join(config['app_conf']['maxocc_data'], session.get('DIR_CACHE'))
        
        wd_path = os.path.join(base_path, str(random.randint(100000000, 999999999)))
        os.makedirs(wd_path)
        print wd_path
        
        str_f = open(os.path.join(wd_path, "ini.str"), "w")
        wei_f = open(os.path.join(wd_path, "ini.wei"), "w")
        new_crv = open(os.path.join(wd_path, "ini.crv"), "w")
        
        for ip, p in enumerate(projsClenead):
            prj = Session.query(Projects).filter(and_(Projects.name == p, Projects.removed == False, Projects.owner_id == session['REMOTE_USER'])).all()
            project = prj[0]
            crv_path = os.path.join(config['app_conf']['working_dir'],
                            project.owner.home,
                            project.name,
                            "maxocc",
                            calcs[ip], "output", "mo-usr.crv")
            cnt_crv = open(crv_path).readlines()
            
            for l in cnt_crv:
                if "s" not in l:
                    lsplitted = l.split()
                    str_f.write(lsplitted[0]+"\n")
                if "s" in l:
                    wei_f.write(l)
                new_crv.write(l)
        str_f.close()
        wei_f.close()
        new_crv.close()
        
        wei=[]
        stc=[]
        S = []
        S_temp = request.POST.get("threshold")
        s_splitted = S_temp.split(",")
        for i in s_splitted:
            S.append(float(i.strip()))
        
        for line in open(os.path.join(wd_path, "ini.wei")):
            tmp = line.split()
            ent = tmp[1:len(tmp)]
            for i in ent:
        
                if i not in wei:
                    wei.append(float(i))
        for line in open(os.path.join(wd_path, 'ini.str')):
            if int(line) not in stc:
                stc.append(int(line))
        wei.sort()
        stc.sort()
        nstr=len(stc)
        xx = numpy.zeros([nstr + 1,len(wei)],float)
        
        for line in open(os.path.join(wd_path, 'ini.crv')):
            if line.split()[0] == 's/w':
                tmp = line.split()
                ent = tmp[1:len(tmp)]
                tmpw=[]
                for i in ent:
                    tmpw.append(float(i))
            else:
                tmp = line.split()
                idx = int(line.split()[0])
                ent = tmp[1:len(tmp)]
                for i in ent:
                    val = float(i)
                    kk = ent.index(i)
                    ii = wei.index(tmpw[kk])
                    jj = stc.index(idx)
                    if xx[jj][ii] > 0 and val < xx[jj][ii]:
                        xx[jj][ii] = val
                    if xx[jj][ii]==0:
                        xx[jj][ii] = val
        #print xx
        wrncount=0
        file6 = open(os.path.join(wd_path, 'mo-usr.crv'),'w')
        file5 = open(os.path.join(wd_path, 'mo.val'),'w')
        file3 = open(os.path.join(wd_path, 'mo.log'),'w')
        culo4="""
        Please note that the Target Function curves are interpolated and not fitted to obtain the following MO values. You may wish to fit the curves (in file mo-usr.crv) with an exponential growth function.
        """
        file5.write(culo4)       
        file5.write('\n')
        culo5="""
        -------------------------------
        """
        file5.write(culo5)
        file5.write('\n')
        
        #SONO ARRIVATO QUI
        
        for x in range (0,nstr):
            valmap=numpy.ones([len(S)],float)
            f1 = numpy.zeros([len(S)],int)
            for y in range (0,len(wei)):
        #        file4.write(str(xx[x][y]))
        #        file4.write('  ')
                 for k in range (0,len(S)):
        #             print xx[x][y], S[k]
                     if xx[x][y] > S[k]:
        #                 print xx[x][y]
                         if  f1[k] == 0:
                             f1[k] =1
                             if xx[x][y-1]== 0:
                                 valmap[k]=wei[y]
                                 wrnstr='Warning: estimate for %d th treshold in structure %d is biased from missing point ' %(k,x)
                                 file3.write(wrnstr)
                                 file3.write('\n')
                                 wrncount += 1
                             else:
                                 mo=(float(wei[y])+float(wei[y-1]))/2
                                 valmap[k]=mo
        #                         print mo
            file5.write('Str.')       
        #    print x
            file5.write(str(stc[x]))       
            file5.write('  ')
            for z in range (0,len(S)):
                file5.write(str(valmap[k]))
                file5.write('  ')
            file5.write('\n')
        #    file4.write('\n')
        file3.close()
        file6.write('s/w')
        file6.write('  ')
        for x in range (0,len(wei)-1):
        
            file6.write(str(wei[x]))
            file6.write('  ')
        file6.write(str(wei[len(wei)-1]))
        file6.write('\n')
        for y in range (0,nstr):
            file6.write(str(stc[y]))
            file6.write('  ')
            for x in range (0,len(wei)):
                file6.write(str(xx[y][x]))
                file6.write('  ')
            file6.write('\n')
        file6.close()
        file4 = open(os.path.join(wd_path, 'mo.crv'),'w')
        for x in range (0,len(wei)):
            file4.write(str(wei[x]))
            file4.write('  ')
            for y in range (0,nstr):
                file4.write(str(xx[y][x]))
                file4.write('  ')
            file4.write('\n')
        file4.close()
        
        file5.close()
        
        #os.environ['MPLCONFIGDIR'] = config['app_conf']['working_dir']
        os.environ['MPLCONFIGDIR'] = wd_path
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        mox= numpy.zeros([nstr,len(S)],float)
        mof= numpy.zeros([nstr,len(S)],int)
        ktt=0
        for line in (open(os.path.join(wd_path,'mo.val'))):
        
            culo=line.split()
        
            if culo:
                if culo[0].split('.')[0]=='Str':
        #            print len(S)
                    for i in range(0,len(S)):
        #                print i+1, culo[i+1]
                        mox[ktt][i]=(float(culo[i+1]))
                        if mox[ktt][i]==1. :
                            mof [ktt][i]=1
                        #print ktt, i, mox[ktt][i]
                    ktt=ktt+1
        #print mox
        if os.path.exists(os.path.join(wd_path,'histogram.png')):
            print "histo already exists"
            shutil.rmtree(os.path.join(wd_path,'histogram.png'))
        bins=20
        plt.hist(mox,bins,range=(0,1),normed=True,histtype='bar')
        plt.xlabel('Maximum Occurrence')
        plt.ylabel('Normalized structure count')
        plt.ylim(0,bins)
        plt.savefig(os.path.join(wd_path,'histogram'), dpi=600, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None, transparent=False, bbox_inches=None, pad_inches=0.1)
        plt.clf()
        file9 = open(os.path.join(wd_path,'restart.log'),'w')
        for i in range(0,len(S)):
            lststr=[]
            for kxt in range(0,nstr):
                if mof[kxt][i]==1:
                    lststr.append(stc[kxt])
            start=False
            outlst='%s -- ' %str(S[i])
            for index in range(0,len(lststr)):
        #        if lststr[index] == 1906:
        #            print lststr[index]+1 == lststr[index+1], start
                if index == 0:
                    outlst += ('%s' %lststr[index])
                elif index == len(lststr)-1:
                    if start==False:
                        outlst += (',%s' %lststr[index])
                    else:
                        outlst += ('%s' %lststr[index])
                else:
                    if start==False:
                        if lststr[index]+1 == lststr[index+1]:
                            outlst += (',%s-' %lststr[index])
                            start = True
                        else:
                            outlst += (',%s' %lststr[index])
                            start = False
                        continue
                    if start==True:
        #                print index+1,len(lststr)
                        if lststr[index]+1 == lststr[index+1]:
                            continue
                        else:
                            outlst += ('%s' %lststr[index])
                            start = False
            outlst += '\n'
            file9.write(outlst)
        file9.close()


        gp = os.popen( '/usr/bin/gnuplot', 'w' )
        gp.write( "set output '"+wd_path+"/mo.png'; set terminal png; \n" )
        gp.write( 'set xlabel "Weight of considered conformer" \n' )
        gp.write( 'set ylabel "TF" \n' )
        gp.write( 'unset key \n' )
        cmdp='p "'+wd_path+'/mo.crv" u 1:2 w linespoints'
        for i in range (2,nstr):
            kkk=i+1
            cmdp=cmdp+', "'+wd_path+'/mo.crv" u 1:%s w linespoints ' %str(kkk)
        kvt=len(S)
        for i in range (0,kvt):
            cmdp=cmdp+', %s w dots ' %str(S[i])
        gp.write(cmdp + "\n")
        #gp.write( "set output 'mo-det.png'; set terminal png; \n" )
        #gp.write( 'set yrange [%s:%s] \n' %(str(ave-SD10),str(ave+SD10)))
        #gp.write(cmdp + "\n")
        gp.write( "exit\n" )
        gp.close()
        
        #print wrncount
        #print nstr*len(S)
        #mylist = []
        #for x in range(1,11): myfile.write(str(x)),myfile.write('\n')
        #myfile.close()
        
        tar = tarfile.open(os.path.join(wd_path,"mergeOutput.tgz"),"w:gz")
        tar.add(os.path.join(wd_path,"mo.crv"), arcname="mo.crv")
        tar.add(os.path.join(wd_path,"mo.log"), arcname="mo.log")
        tar.add(os.path.join(wd_path,"mo.log"), arcname="mo.log")
        tar.add(os.path.join(wd_path,"mo.png"), arcname="mo.png")
        tar.add(os.path.join(wd_path,"mo-usr.crv"), arcname="mo-usr.crv")
        tar.add(os.path.join(wd_path,"mo.val"), arcname="mo.val")
        tar.add(os.path.join(wd_path,"histogram.png"), arcname="histogram.png")
        tar.add(os.path.join(wd_path,"restart.log"), arcname="restart.log")
        tar.close()
        
        permanent_file = open(os.path.join(wd_path,"mergeOutput.tgz"), 'rb')
        data = permanent_file.read()
        permanent_file.close()

        response.content_type = guess_type(os.path.join(wd_path,"mergeOutput.tgz"))[0] or 'text/plain'
        response.headers['Content-Lenght'] = len(data)
        response.headers['Pragma'] = 'public'
        response.headers['Cache-Control'] = 'max-age=0'
        response.headers['Content-Disposition'] = 'attachment; filename="mergeOutput.tgz"'
        return data
        
