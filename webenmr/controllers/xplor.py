from lxml import etree
import logging
import random
import os
import shutil
import types, cgi
from pylons import config
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from webenmr.model import Projects, Calculations, Jobs, CalculationTipology, Users
from webenmr.model.meta import Session
from webenmr.lib.base import *
from webenmr.lib.base import BaseController, render
from webenmr.lib.xplor_analysis import *
from webenmr.lib.make_xplor import *
from webenmr.lib.JobManagementSystem import *

log = logging.getLogger(__name__)

class XplorController(BaseController):

    def __before__(self):
        c.page_base = u'Xplor-NIH'
        c.page_title = u'Xplor-NIH'
        
        random.seed()
        if session.get('DIR_CACHE', None) is None:
            session['DIR_CACHE'] = os.path.join(config['app_conf']['xplor_data'], str(random.randint(100000000, 999999999)))
            session.save()
        elif 'xplor_data' not in session.get('DIR_CACHE'):
            session['DIR_CACHE'] = os.path.join(config['app_conf']['xplor_data'], str(random.randint(100000000, 999999999)))
            session.save()
        if not os.path.isdir(session.get('DIR_CACHE')):
            os.makedirs(session.get('DIR_CACHE'))
    
    
    def index(self):
        return render('/calculations/xplor_calc.mako')

    def helpinfo(self):
        field = request.POST.get('field')
        info = open(os.path.join(config['app_conf']['properties'], "xplor-info.properties"))
        l = 'pipppo'
        for line in info:
            if line.startswith(field):
                l = line.split('=')[1]
                break
        return l
    
    def isCalcExist(self):
        owner = Session.query(Users).get(session['REMOTE_USER'])
        proj = request.POST.get('proj')
        calc = request.POST.get('calc')
        print proj, calc
        cname = Session.query(Calculations).filter(and_(Calculations.name==calc, Calculations.removed == False, Calculations.project_id==int(proj))).first()
        if cname:
            return "no"
        else:
            return "ok"
        
    def removefile(self):
        f = request.POST.get("file")
        
    def uploadfile(self):
        filepath = os.path.join(config['app_conf']['xplor_data'], session['DIR_CACHE'])
        field = request.POST.get("namefield")
        f = request.POST.get(field)
        self.saveFile(f, filepath)
        
    def saveFile(self, fname, where, name=None):
        if name:
            namef = name
        else:
            namef = fname.filename.split('\\')[0]
        namef.replace(" ", "_")
        #f = fname.filename.split('\\')
        rfname = os.path.join(where, namef)
        permanent_file = open(rfname, 'wb')
        shutil.copyfileobj(fname.file, permanent_file)
        fname.file.close()
        permanent_file.close()
        return rfname
    
    def submitXplor(self):
        basepath = os.path.join(config['app_conf']['xplor_data'], session['DIR_CACHE'])
        root_st = etree.Element("xplor-calculation")
        
        xplor_prj_id = request.POST.get("xplor-prj_id")
        proj = Session.query(Projects).filter(and_(Projects.owner_id == session['REMOTE_USER'], Projects.removed == False, Projects.id == int(xplor_prj_id))).first()
        proj_name = proj.name
        te = {}
        te["name"] = proj_name
        etree.SubElement(root_st, "project", te)
        
        xplor_namecalc = request.POST.get("xplor-namecalc")
        te = {}
        te["name"] = xplor_namecalc
        etree.SubElement(root_st, "calculation", te)
        
        xplor_seqfile = request.POST.getall("xplor-seqfile")
        xplor_residuenum = request.POST.getall("xplor-residuenum")
        xplor_chainname = request.POST.getall("xplor-chainname")
        xplor_posseq = request.POST.getall("xplor-posseq")
        te={}
        idx = 0
        for it in xplor_seqfile:
            te["path"] =  self.saveFile(it, basepath)
            te["numfres"] = xplor_residuenum[idx]
            te["chain"] = xplor_chainname[idx]
            te["pos"] = xplor_posseq[idx]
            idx += 1
            etree.SubElement(root_st, "sequence" , te )
        
        if request.POST.get("nonstdres") == 'yes':
            xplor_nonstdres_top = request.POST.getall("xplor-nonstdrestop")
            xplor_nonstdres_par = request.POST.getall("xplor-nonstdrespar")
            if len(xplor_nonstdres_top) >= 1:
                te = {}
                for i,e in enumerate(xplor_nonstdres_top):
                    te["parameter_path"] = self.saveFile(xplor_nonstdres_par[i], basepath)
                    te["topology_path"] = self.saveFile(e, basepath)
                    etree.SubElement(root_st, "nonstdresidues", te)
        
        
        if request.POST.get("parcenter") == 'yes':
            xplor_m_atomname = request.POST.getall("m_atom_name")
            xplor_m_element = request.POST.getall("m_element")
            xplor_m_res_name = request.POST.getall("m_res_name")
            xplor_m_res_num = request.POST.getall("m_res_num")
            xplor_m_charge = request.POST.getall("m_charge")
            xplor_m_rvdw = request.POST.getall("m_rvdw")
            xplor_m_eps = request.POST.getall("m_eps")
            xplor_m_bind_res_str = request.POST.getall("m_bind_res")
            print xplor_m_bind_res_str
            met_res_diz = {}
            for br in xplor_m_bind_res_str:
                br_list = br.split(":::")
                met_res_diz[br_list[0]] = br_list[1]
            te = {}
            idx = 0
            for it in xplor_m_atomname:
                if xplor_m_element[idx] != 'n/a':
                    te["type"] = "metal"
                else:
                    te["type"] = "cofactor"
                te["atom_name"] = it
                te["element"] = xplor_m_element[idx]
                te["res_name"] = xplor_m_res_name[idx]
                te["res_num"] = xplor_m_res_num[idx]
                te["charge"] = xplor_m_charge[idx]
                te["rvdw"] = xplor_m_rvdw[idx]
                te["epsilon"] = xplor_m_eps[idx]
                met_el = etree.SubElement(root_st, "metal", te)
                if met_res_diz.has_key(xplor_m_res_num[idx]):
                    te2 = {}
                    xplor_m_bind_res_list = met_res_diz.get(xplor_m_res_num[idx]).split(',')
                    for multi in xplor_m_bind_res_list:
                        multi_splitted = multi.split()
                        te2["resnum"] = multi_splitted[0].strip()
                        te2["atom_name"] = multi_splitted[1].strip()
                        if len(multi_splitted) == 4:
                            te2["segid"] = multi_splitted[2].strip()
                        else:
                            te2["segid"] = ""
                        te2["distance"] = multi_splitted[2].strip()
                        etree.SubElement(met_el, "restraint", te2)
                idx += 1
                
        if request.POST.get("cof") == 'yes': 
            xplor_cofpdb = request.POST.getall("xplor-cofpdb")
            xplor_coftop = request.POST.getall("xplor-coftop")
            xplor_cofpar = request.POST.getall("xplor-cofpar")
            xplor_poscof = request.POST.getall("xplor-poscof")
            
            if 'hpatch-name' in request.params:
                patchname = request.POST.getall("hpatch-name")
                patchres1 = request.POST.getall("hpatch-res1")
                patchres1chain = request.POST.getall("hpatch-res1chain")
                patchres2 = request.POST.getall("hpatch-res2")
                patchres2chain = request.POST.getall("hpatch-res2chain")
                if len(patchres1chain) == 0:
                    patchres1chain = ['']*len(patchname)
                    patchres2chain = ['']*len(patchname)
                for i,pn in enumerate(patchname):
                    #print i,pn
                    #print patchres1[i]
                    #print patchres2[i]
                    te = {}
                    te["type"] = pn
                    te["resnuma"] = patchres1[i].split(',')[0].strip()
                    if len(patchres1[i].split(',')) > 1:
                        te["chaina"] = patchres1chain[i]
                    else:
                        te["chaina"] = "    "
                    te["resnumb"] = patchres2[i].split(',')[0].strip()
                    if len(patchres2[i].split(',')) > 1:
                        te["chainb"] = patchres2chain[i]
                    else:
                        te["chainb"] = "    "
                    
                    etree.SubElement(root_st, "patchcof", te)
            te = {}
            idx = 0
            for it in xplor_cofpdb:
                te["pdb_path"] = self.saveFile(it, basepath)
                te["topology_path"] = self.saveFile(xplor_coftop[idx], basepath)
                te["par_path"] = self.saveFile(xplor_cofpar[idx], basepath)
                te["pos"] = xplor_poscof[idx]
                etree.SubElement(root_st, "cofactor", te)
                idx += 1
                
        if request.POST.get("dis") == 'yes': 
            #xplor_disatoma = request.POST.getall("xplor-disatoma")
            xplor_disresnamea = request.POST.getall("xplor-disresnuma")
            xplor_dischaina = request.POST.getall("chain-selector-disa")
            xplor_dischainb = request.POST.getall("chain-selector-disb")
            xplor_disresnameb = request.POST.getall("xplor-disresnumb")
            if len(xplor_dischaina) == 0:
                xplor_dischaina = ['']*len(xplor_disresnamea)
                xplor_dischainb = ['']*len(xplor_disresnamea)
            te = {}
            idx = 0
            for it in xplor_disresnamea:
                #te["atoma"] = it 
                te["resnuma"] = it
                te["segida"] = xplor_dischaina[idx]
                te["resnumb"] = xplor_disresnameb[idx]
                te["segidb"] = xplor_dischainb[idx]
                etree.SubElement(root_st, "disulfide", te)
                idx += 1
                
        if request.POST.get("phis") == 'yes': 
            xplor_phisresnum = request.POST.getall("xplor-phisresnum")
            xplor_phischain = request.POST.getall("chain-selector-phis")
            xplor_phistype = request.POST.getall("xplor-phistype")
            
            if len(xplor_phischain) == 0:
                xplor_phischain = ['']*len(xplor_phisresnum)
            te = {}
            idx = 0
            for it in xplor_phisresnum:
                te["resnum"] = it
                te["segid"] = xplor_phischain[idx]
                te["type"] = xplor_phistype[idx]
                etree.SubElement(root_st, "histidine", te)
                idx += 1
                
        xplor_noefile = request.POST.getall("xplor-noefile")
        if len(xplor_noefile) > 1 or (len(xplor_noefile) == 1 and xplor_noefile[0] != ''):
            te = {}
            for it in xplor_noefile:
                te["path"] = self.saveFile(it, basepath)
                etree.SubElement(root_st, "noe", te)

        xplor_dihfile = request.POST.getall("xplor-dihfile")
        if len(xplor_dihfile) > 1 or (len(xplor_dihfile) == 1 and xplor_dihfile[0] != ''):
            te = {}
            for it in xplor_dihfile:
                te["path"] = self.saveFile(it, basepath)
                etree.SubElement(root_st, "dih", te)
            
        xplor_rdc_metal = request.POST.getall("xplor-rdc-metal")
        xplor_rdc_ax = request.POST.getall("xplor-rdctnsax")
        xplor_rdc_rh = request.POST.getall("xplor-rdctnsrh")
        xplor_rdc_file = request.POST.getall("xplor-rdcfile")
        te = {}
        idx = 0;
        if len(xplor_rdc_file) > 1 or (len(xplor_rdc_file) == 1 and xplor_rdc_file[0] != ''):
            for it in xplor_rdc_file:
                te["res_num"] = xplor_rdc_metal[idx]
                te["path"] = self.saveFile(it, basepath)
                te["ax"] = xplor_rdc_ax[idx]
                te["rh"] = xplor_rdc_rh[idx]
                etree.SubElement(root_st, "rdc", te)
                idx += 1 
        
        xplor_pcs_metal = request.POST.getall("xplor-pcs-metal")    
        xplor_pcs_ax = request.POST.getall("xplor-pcstnsax")
        xplor_pcs_rh = request.POST.getall("xplor-pcstnsrh")
        xplor_pcs_file = request.POST.getall("xplor-pcsfile")
        te = {}
        idx = 0;
        if len(xplor_pcs_file) > 1 or (len(xplor_pcs_file) == 1 and xplor_pcs_file[0] != ''):
            for it in xplor_pcs_file:
                te["res_num"] = xplor_pcs_metal[idx]
                te["path"] = self.saveFile(it, basepath)
                te["ax"] = xplor_pcs_ax[idx]
                te["rh"] = xplor_pcs_rh[idx]
                etree.SubElement(root_st, "pcs", te)
                idx += 1 
            
        xplor_nrostruct = request.POST.get("xplor-nrostruct")
        te = {}
        te["nro_struct"] = xplor_nrostruct
        etree.SubElement(root_st, "output", te)
        
        print etree.tostring(root_st, pretty_print=True)

        make_xplor(basepath, os.path.join(config['app_conf']['xplor_templ'], "template_xplor_pm.inp"), root_st)
        
        jms = JobManagementSystem(basepath, root_st, session['PORTAL'])
        ret = jms.setupJobs(xplor_nrostruct)
        
        if ret:
            h.redirect('/jobs/show/all')
        h.redirect('/jobs/show/all')
        
    def selectPatch(self):
        basepath = os.path.join(config['app_conf']['xplor_data'], session['DIR_CACHE'])
        root_st = etree.Element("xplor-patch")
        te = {}
        numpos = int(request.POST.get("pos")) - 1
        pdbfile = request.POST.getall("xplor-cofpdb")
        te["pdb"] = self.saveFile(pdbfile[numpos], basepath)

        topfile = request.POST.getall("xplor-coftop")
        te["top"] = self.saveFile(topfile[numpos], basepath)
        etree.SubElement(root_st, "filetopatch", te)
        
        patch_info = extract_patch_top(root_st)
        ret = ''
        if isinstance(patch_info, types.DictType ):
            for k in patch_info.keys():
                info_list = patch_info[k].split("-")
                ret += k+','+','.join(info_list)
                ret = ret[:-1] + '::'
        else:
            ret = patch_info
        return ret
    