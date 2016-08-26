from lxml import etree
import os
import sys
import string
import shutil
import random
import logging
import re
import commands
import tarfile
from datetime import *
from webenmr.model import Projects, Users
from webenmr.model import Calculations, Jobs, CalculationTipology

from webenmr.lib.base import *
from webenmr.lib import files

import webenmr.lib.cnvrdc_xml2fanta as convrdcxml2fanta
import webenmr.lib.cnvpcs_xml2fanta as convpcsxml2fanta
#import amber_md.lib.convpcs
#import amber_md.lib.convrdc

from pylons import config
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from mako.template import Template
from webenmr.lib.base import BaseController, render
from webenmr.lib.amber_utils import *
from webenmr.lib.amber_checks import *
from mimetypes import guess_type
from pyparsing import *
import pprint
import math

log = logging.getLogger(__name__)


class StructureuploadController(BaseController):
      
    def __before__(self):
        """
        This __before__ method calls the parent method, and then sets up the
        tabs on the page.
        """
        #BaseController.__before__(self)
        
        c.page_base = u'Calculations'
        #if 'REMOTE_USER' in session:
        #    c.current_user = Session.query(Users).get(session['REMOTE_USER'])
        #    c.main_menu = Session.query(Menu).filter(and_(Menu.parent_id==None, Menu.sibling_id==None)).order_by(Menu.weight.asc()).all()
        c.page_title = u''
        #
    def sander(self):
        return render('sander.mako')
    
    def checkXA(self):
        check = request.POST.get('path').replace("Projects/", "")
        owner = Session.query(Users).get(session['REMOTE_USER'])
        if os.path.exists(os.path.join(config['app_conf']['working_dir'], owner.home, check, "analysis", ".XA", "XA.xml" )) and os.path.exists(os.path.join(config['app_conf']['working_dir'], owner.home, check, "analysis", ".XA", "ambermodels.pdb" )):
            return "0"
        else:
            return "1"
        
    def extractall(self, tf, path="."):
        for tarinfo in tf:
            if tarinfo.isdir():
                # Extract directories with a safe mode.
                tarinfo = copy.copy(tarinfo)
                tarinfo.mode = 0700
            tf.extract(tarinfo, path)
            
    def submitStructureXA(self):
        
        def findxml3XA(xml, tag, attri):
            #print tag, attri, strs, getattri
            #print etree.tostring(xml, pretty_print=True)
            res = []
            for i in xml.getiterator():
                if i.tag == "XA":
                    for a in i.getiterator():
                        if a.tag == tag:
                            res.append(a.get(attri))
            #remove None values
            return [x for x in res if x is not None]
        
        template = config['app_conf']['xplor_templ']
        XA_home = request.POST.get('path')
        #new_project_1373642575/xplor-nih/klo
        project_name = XA_home.split("/")[0]
        calc_name = XA_home.split("/")[2]
        owner = Session.query(Users).get(session['REMOTE_USER'])
        xml_XA = etree.parse(os.path.join(config['app_conf']['working_dir'], owner.home, XA_home, "analysis", ".XA", "XA.xml" ))            
        print "##### XA.xml #########"
        print etree.tostring(xml_XA, pretty_print=True)
        #insert pdbfile
        pdb_file = findxml3XA(xml_XA, "pdb", "file" )[0]
        print "#######DIR_CACHE #########"
        print session.get('DIR_CACHE')
        if session.get('DIR_CACHE', None) is None:
            session['DIR_CACHE'] = os.path.join(config['app_conf']['amber_data'], str(random.randint(100000000, 999999999)))
            session.save()
        #elif 'amber_data' not in session.get('DIR_CACHE'):
        #    session['DIR_CACHE'] = os.path.join(config['app_conf']['amber_data'], str(random.randint(100000000, 999999999)))
        #    session.save()   
        if not os.path.isdir(session.get('DIR_CACHE')):
            os.makedirs(session.get('DIR_CACHE'))
        else:
            shutil.rmtree(session.get('DIR_CACHE'))
            os.makedirs(session.get('DIR_CACHE'))
        print "#######DIR_CACHE #########"
        print session.get('DIR_CACHE')
        xml_r = check_pdb(pdb_file)
        #multijobs
        root_st = etree.Element("structure")
        print xml_r
        te={}
        te["filename"] = os.path.join(os.path.dirname(pdb_file), os.path.basename(pdb_file).split('.')[0] + '_c.pdb')
        print pdb_file
        print te
        etree.SubElement(root_st, "protein" , te )
       
        
        amino_top_files = findxml3XA(xml_XA, "amberpar", "lib" )
        print amino_top_files
        #for it in amino_names:
        #    item = request.POST.get(it)
        #    amino_top_files.append(item);
        #if self.check_v(amino_top_files):
        #    self.saveFiles(amino_top_files)
        amino_par_files = findxml3XA(xml_XA, "amberpar", "par" )
        #if self.check_v(amino_par_files):
        #    self.saveFiles(amino_par_files)
        
        amino_atmtype_files = findxml3XA(xml_XA, "amberpar", "type" )

        if check_v(amino_top_files):
            #per ogni residuo, sua topologia e parametri creo nodo per il doc XML
            for j in range(len(amino_top_files)):
                res_top = amino_top_files[j]

                res_par = amino_par_files[j]
                
                res_atmtype = amino_atmtype_files[j]
               
                te = {}
                te["top_filename"] = res_top
                te["par_filename"] = res_par
                te["atm_filename"] = res_atmtype
                etree.SubElement(root_st, "no_std_ligand" , te )
                
        
        file_leap = "leaprc.ff99SB"
        te = {}
        te["value"] = file_leap
        etree.SubElement(root_st, "ff" , te )
        #remove solvent if PCS restraints are present
        pcs_files = findxml3XA(xml_XA, "pcs", "file" )
        if not check_v(pcs_files):
            te={}
            te["solvent"] = "TIP3PBOX"
            te["geo"] = "box"
            te["distance"] = "10.0"
            etree.SubElement(root_st, "solv", te)
        
        new_xml = self.run_tleap_1(root_st)
        
        #SUBMITCOSTRIANT
        noe_dih = []
        #creo elemento di root per doc XML
        root_stC = etree.Element("constraint")
        
        noe_files = findxml3XA(xml_XA, "noe", "file" )
        print "####NOE FILES#######"
        print noe_files 
        if check_v(noe_files):
            #self.saveFiles(noe_files)
            for nf_idx in range(len(noe_files)):
                self.check_constraintXA("noe", noe_files[nf_idx])
                te = {}
                te["filename"] = noe_files[nf_idx]
                te["number"] = "1"
                te["type"] = "xplor"
               
                te["nocorr"] = "False"
                etree.SubElement(root_stC, "noe" , te )
                noe_dih.append(noe_files[nf_idx] + "_noe_RST")
        
        dihedral_files = findxml3XA(xml_XA, "aco", "file" )
        print "####ACO FILES#######"
        if check_v(dihedral_files):
            #self.saveFiles(dihedral_file)
            for df_idx in range(len(dihedral_files)):
                self.check_constraintXA("dihedral", dihedral_files[df_idx])
                te = {}
                te["filename"] = dihedral_files[df_idx]
                te["number"] = "1"
                te["type"] = "xplor"
                etree.SubElement(root_stC, "dihedral" , te )
                noe_dih.append(dihedral_files[df_idx] + "_dih_RST")
        
        rdc_files = findxml3XA(xml_XA, "rdc", "file" )
        
        if check_v(rdc_files):
            #rdc_number = findxml3XA(xml_XA, "rdc", "res_num" )
            #rdc_cyXp = request.POST.getall('rdc_cyanaXplor_c')
            #rdc_fit = request.POST.getall('rdc_fit_t')
            #rx_rdc = request.POST.getall('rdc_rx')
            #ax_rdc = request.POST.getall('rdc_ax')
            #alpha_rdc = request.POST.getall('rdc_alpha')
            #beta_rdc = request.POST.getall('rdc_beta')
            #gamma_rdc = request.POST.getall('rdc_gamma')
            for rf_idx in range(len(rdc_files)):
                te = {}
        
                te["filename"] = rdc_files[rf_idx]
                te["number"] = "1"
                te["type"] = "xplor"
                #te["rx"] = rx_rdc[i]
                #te["ax"] = ax_rdc[i]
                #te["alpha"] = alpha_rdc[i]
                #te["beta"] = beta_rdc[i]
                #te["gamma"] = gamma_rdc[i]
        
                #te["filename"] = rdc_files[i]
                #te["number"] = rdc_number[i]
                #te["type"] = dihedral_cyXp[i]
                #te["rx"] = rx_rdc[i]
                #te["ax"] = ax_rdc[i]
                #te["alpha"] = alpha_rdc[i]
                #te["beta"] = beta_rdc[i]
                #te["gamma"] = gamma_rdc[i]
        
                etree.SubElement(root_stC, "rdc" , te )
                
        pcs_files = findxml3XA(xml_XA, "pcs", "file" )
        pcs_metal = findxml3XA(xml_XA, "pcs", "res_num" )
        print "XA.xml OUT"
        etree.tostring(xml_XA)
  #if elt.tag == "metal":
  #              metal = elt.text
  #          if elt.tag == "euler":
  #              theta = elt.get("theta")
  #              phi = elt.get("phi")
  #              omega = elt.get("omega")
  #          if elt.tag == "aniso":
  #              a1 = elt.get("dchiax")
  #              a2 = elt.get("dchirh")
                
        if check_v(pcs_files):
        #    pcs_number = request.POST.getall('pcs_number_n')
        #    pcs_cyXp = request.POST.getall('pcs_cyanaXplor_c')
        #    pcs_fit = request.POST.getall('pcs_fit_t')
        #    #rx_pcs = request.POST.getall('pcs_rx')
        #    #ax_pcs = request.POST.getall('pcs_ax')
        #    #alpha_pcs = request.POST.getall('pcs_alpha')
        #    #beta_pcs = request.POST.getall('pcs_beta')
        #    #gamma_pcs = request.POST.getall('pcs_gamma')
            for pf_idx in range(len(pcs_files)):
                te = {}
                te["theta"] = "0"
                te["phi"] = "0"
                te["omega"] = "0"
                te["dchiax"] = "0"
                te["dchirh"] = "0"
                te["metal"] = pcs_metal[pf_idx]
                te["filename"] = pcs_files[pf_idx]
                te["number"] = "1"
                te["type"] = "xplor"
        #
                etree.SubElement(root_stC, "pcs" , te )
        
        #QUI METODO DI ANDREA SU root_stC
        
        #seguono alcune chiamate di debugging
        pdb_out = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "out_leap.pdb")
        pdb_ref_n = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "pdb.ref")
        
        print "ROOT_STc"
        print etree.tostring(root_stC)

        if check_v(rdc_files):
            convrdcxml2fanta.convert_fin(root_stC, pdb_out, pdb_ref_n)
        if check_v(pcs_files):
            convpcsxml2fanta.convert_fin(root_stC, pdb_out, pdb_ref_n)
        #unisco tutti i NOE e i diedri
        if len(noe_dih) > 0:
            if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in")):
                os.remove(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in"))
            fout = open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in"),'a')
            for ff in noe_dih:
                lines = open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), ff)).readlines()
                fout.writelines(lines)
            fout.close() 
                
        print "############## INI submitConstraint XA #################"
        print etree.tostring(root_stC, pretty_print=True)
        print "############## END submitConstraint XA #################"
        #return etree.tostring(root_stC, pretty_print=True)
        
        #copia protocollo usato
        if check_v(pcs_files) and check_v(rdc_files):
            tar = tarfile.open(os.path.join(template, "protPCSRDC.tgz"), "r:gz")
            self.extractall(tar, os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
            #print os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'))
            
        elif check_v(pcs_files):
            tar = tarfile.open(os.path.join(template, "protPCS.tgz"), "r:gz")
            self.extractall(tar, os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
        elif check_v(rdc_files):
            tar = tarfile.open(os.path.join(template, "protRDC.tgz"), "r:gz")
            self.extractall(tar, os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
        elif len(noe_dih) > 0:
            tar = tarfile.open(os.path.join(template, "protNOE.tgz"), "r:gz")
            self.extractall(tar, os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
        
        if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"XA.xml")):
            os.remove(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"XA.xml"))    
        else:
            shutil.copyfile(os.path.join(config['app_conf']['working_dir'], owner.home, XA_home, "analysis", ".XA", "XA.xml" ), os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"XA.xml")
                            )
        return "0"
        return new_xml
    
        
    
    def submitStructure(self):
        #creo elemento di root per doc XML
        root_st = etree.Element("structure")
        
        protein_files = request.POST.getall('protein_name')
        
        #per tutte i filename delle proteine creo un nodo per il doc XML
        for prot_name in protein_files:
            prot_name_c = prot_name.split('.')[0] + '_c.pdb'
            te={}
            te["filename"] = prot_name_c
            root_prot =  etree.SubElement(root_st, "protein" , te )
            
        if 'pcs-rdc_fitting' in request.params:
            dest = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'))
            files_top = [ 'metal1.lib', 'metal2.lib', 'metal3.lib', 'metal4.lib', 'metal5.lib', 'metal6.lib']
            te = {}
            for i in files_top:
                source = os.path.join(config['app_conf']['amber_data'], i)
                shutil.copy(source, dest)
                te["top_filename"] = i
                
            source = os.path.join(config['app_conf']['amber_data'], 'metal_amber.par')
            shutil.copy(source, dest) 
            te["par_filename"] = 'metal_amber.par'
            te["atm_filename"] = ""
            root_res =  etree.SubElement(root_st, "no_std_ligand" , te )
            
            #statistics about use of AnisoFIT
            statfile = open(os.path.join(config['app_conf']['statistics'], 'anisofit.stat'), 'a')
            d = datetime.now()
            str = '%s %s %s\n' %(d.day, d.month, d.year)
            statfile.write(str)
            statfile.close()
                     
        if 'residue1' in request.params:
            residue1_list = request.POST.getall('residue1')
            atom1_list = request.POST.getall('atom1')
            residue2_list = request.POST.getall('residue2')
            atom2_list = request.POST.getall('atom2')
            for idx in range(len(residue1_list)):
                te = {}
                te["residue1"] = residue1_list[idx]
                te["atom1"] = atom1_list[idx]
                te["residue2"] = residue2_list[idx]
                te["atom2"] = atom2_list[idx]
                etree.SubElement(root_st, "bond", te)
            
        if 'solvent' in request.params:
            te={}
            te["solvent"] = request.POST.get("solvent")
            te["geo"] = request.POST.get("geometry")
            if request.POST.get("geometry") == 'scap':
                te["resid"] = request.POST.get("resid")
            te["distance"] = request.POST.get("distance")
            etree.SubElement(root_st, "solv", te)
        
        if 'ion' in request.params:
            ions = request.POST.getall("ion")
            nums = request.POST.getall("number")
            for i, e in enumerate(ions):
                te={}
                te["type"] = e
                te["number"] = nums[i]
                etree.SubElement(root_st, "ions", te)
        
        if 'born' in request.params:   
            te={}
            te["type"] = request.POST.get("born")
            etree.SubElement(root_st, "born", te)
                
        #leggo dalla request legandi con topologia e parametri e li salvo su disco
        ligand_files = request.POST.getall('ligand_name')
        #if self.check_v(ligand_files):
        #    self.saveFiles(ligand_files)
        ligand_top_files = request.POST.getall('ligand_top_name')
        #if self.check_v(ligand_top_files):
        #    self.saveFiles(ligand_top_files)
        ligand_par_files = request.POST.getall('ligand_par_name')
        #if self.check_v(ligand_par_files):
        #    self.saveFiles(ligand_par_files)
        
        if check_v(ligand_files):
            #per ogni legante, topologia e parametri creo un nodo per il doc XML
            for i in range(len(ligand_files)):
                ligand_name = ligand_files[i]
                te = {}
                te["filename"] = ligand_name
                te["top_filename"] = ligand_top_files[i]
                if len(ligand_par_files) > 0:
                    te["par_filename"] = ligand_par_files[i]
                else:
                    te["par_filename"] = ""
                    
                root_lig =  etree.SubElement(root_st, "ligand" , te )
            
        #leggo dalla request i residui non standard e li salvo sul disco
        #amino_labels = request.POST.getall('res_label')
        #amino_names = self.extractEnvVar("amino_top")
        #amino_top_files = []
        amino_top_files = request.POST.getall('amino_top_name')
        #for it in amino_names:
        #    item = request.POST.get(it)
        #    amino_top_files.append(item);
        #if self.check_v(amino_top_files):
        #    self.saveFiles(amino_top_files)
        amino_par_files = request.POST.getall('amino_par_name')
        #if self.check_v(amino_par_files):
        #    self.saveFiles(amino_par_files)
        
        amino_atmtype_files = request.POST.getall('amino_atmtype_name')

        if check_v(amino_top_files):
            #per ogni residuo, sua topologia e parametri creo nodo per il doc XML
            for j in range(len(amino_top_files)):
                res_top = amino_top_files[j]

                if check_v(amino_par_files):
                    res_par = amino_par_files.pop(0)
                else:
                    res_par = ""
                if check_v(amino_atmtype_files):
                    res_atmtype = amino_atmtype_files.pop(0)
                else:
                    res_atmtype = ""
                te = {}
                te["top_filename"] = res_top
                te["par_filename"] = res_par
                te["atm_filename"] = res_atmtype
                root_res =  etree.SubElement(root_st, "no_std_ligand" , te )
        
        #leggo dalla request il force field e creo nodo per il doc XML
        file_leap_temp = request.POST.get('forcefield').split('R')[1]
        file_leap = "leaprc.ff"+file_leap_temp
        te = {}
        te["value"] = file_leap
        root_ff = etree.SubElement(root_st, "ff" , te )
        
        if 'antechamber' in request.params:
            antechamber = request.POST.get('antechamber')
            te = {}
            te["include"] = antechamber
            root_ante = etree.SubElement(root_st, "antechamber", te)
        
        #new_xml = etree.tostring(root_st, pretty_print=True)
        new_xml = self.run_tleap_1(root_st)

        return new_xml

    
    def submitConstraint(self):
        noe_dih = []
        #creo elemento di root per doc XML
        root_st = etree.Element("constraint")
        
        noe_files = request.POST.getall('noe_file_f')
        if check_v(noe_files):
            #self.saveFiles(noe_files)
            noe_number = request.POST.getall('noe_number_n')
            noe_cyXp = request.POST.getall('noe_cyanaXplor_c')
            if 'noe_noe_nocorr_r' in request.params:
                noe_nocorr = request.POST.getall('noe_noe_nocorr_r')
                print noe_nocorr
            for nf_idx in range(len(noe_files)):
                te = {}
                te["filename"] = noe_files[nf_idx]
                te["number"] = noe_number[nf_idx]
                te["type"] = noe_cyXp[nf_idx]
                if 'noe_nocorr' in request.params:
                    te["nocorr"] = noe_nocorr[nf_idx]
                else:
                    te["nocorr"] = "False"
                etree.SubElement(root_st, "noe" , te )
                noe_dih.append(noe_files[nf_idx] + "_noe_RST")
        
        dihedral_files = request.POST.getall('dih_file_f')

        if check_v(dihedral_files):
            #self.saveFiles(dihedral_file)
            dihedral_number = request.POST.getall('dih_number_n')
            dihedral_cyXp = request.POST.getall('dih_cyanaXplor_c')
            for df_idx in range(len(dihedral_files)):
                te = {}
                te["filename"] = dihedral_files[df_idx]
                te["number"] = dihedral_number[df_idx]
                te["type"] = dihedral_cyXp[df_idx]
                etree.SubElement(root_st, "dihedral" , te )
                noe_dih.append(dihedral_files[df_idx] + "_dih_RST")
        
        rdc_files = request.POST.getall('rdc_file_f')
        
        if check_v(rdc_files):
            rdc_number = request.POST.getall('rdc_number_n')
            rdc_cyXp = request.POST.getall('rdc_cyanaXplor_c')
            rdc_fit = request.POST.getall('rdc_fit_t')
            #rx_rdc = request.POST.getall('rdc_rx')
            #ax_rdc = request.POST.getall('rdc_ax')
            #alpha_rdc = request.POST.getall('rdc_alpha')
            #beta_rdc = request.POST.getall('rdc_beta')
            #gamma_rdc = request.POST.getall('rdc_gamma')
            for rf_idx in range(len(rdc_files)):
                te = {}

                te["filename"] = rdc_files[rf_idx]
                te["number"] = rdc_number[rf_idx]
                te["type"] = rdc_cyXp[rf_idx]
                #te["rx"] = rx_rdc[i]
                #te["ax"] = ax_rdc[i]
                #te["alpha"] = alpha_rdc[i]
                #te["beta"] = beta_rdc[i]
                #te["gamma"] = gamma_rdc[i]

                #te["filename"] = rdc_files[i]
                #te["number"] = rdc_number[i]
                #te["type"] = dihedral_cyXp[i]
                #te["rx"] = rx_rdc[i]
                #te["ax"] = ax_rdc[i]
                #te["alpha"] = alpha_rdc[i]
                #te["beta"] = beta_rdc[i]
                #te["gamma"] = gamma_rdc[i]

                etree.SubElement(root_st, "rdc" , te )
                
        pcs_files = request.POST.getall('pcs_file_f')
        
        if check_v(pcs_files):
            pcs_number = request.POST.getall('pcs_number_n')
            pcs_cyXp = request.POST.getall('pcs_cyanaXplor_c')
            pcs_fit = request.POST.getall('pcs_fit_t')
            #rx_pcs = request.POST.getall('pcs_rx')
            #ax_pcs = request.POST.getall('pcs_ax')
            #alpha_pcs = request.POST.getall('pcs_alpha')
            #beta_pcs = request.POST.getall('pcs_beta')
            #gamma_pcs = request.POST.getall('pcs_gamma')
            for pf_idx in range(len(pcs_files)):
                te = {}

                te["filename"] = pcs_files[pf_idx]
                te["number"] = pcs_number[pf_idx]
                te["type"] = pcs_cyXp[pf_idx]
 
                etree.SubElement(root_st, "pcs" , te )
        
        #QUI METODO DI ANDREA SU root_st
        
        #seguono alcune chiamate di debugging
        pdb_out = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "out_leap.pdb")
        pdb_ref_n = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "pdb.ref")
        

        if check_v(rdc_files):
            convrdcxml2fanta.convert_fin(root_st, pdb_out, pdb_ref_n)
        if check_v(pcs_files):
            convpcsxml2fanta.convert_fin(root_st, pdb_out, pdb_ref_n)
        #unisco tutti i NOE e i diedri
        if len(noe_dih) >0:
            if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in")):
                os.remove(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in"))
            fout = open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in"),'a')
            for ff in noe_dih:
                lines = open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), ff)).readlines()
                fout.writelines(lines)
            fout.close() 
                
        print "############## INI submitConstraint #################"
        print etree.tostring(root_st, pretty_print=True)
        print "############## END submitConstraint #################"
        return etree.tostring(root_st, pretty_print=True)


    #def submitJob(self):
        
        #if 'multiJobFile' in request.params:
        #    multyJobsFile = request.POST.get('multiJobFile')
        #    f = multyJobsFile.filename.split('\\')
        #    rfname = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f[len(f)-1])
        #    permanent_file = open(rfname, 'wb')
        #    shutil.copyfileobj(multyJobsFile.file, permanent_file)
        #    multyJobsFile.file.close()
        #    permanent_file.close()
        
        
    
    def saveFiles(self, files):
        for fname in files:
            if fname != "":
                f = fname.filename.split('\\')
                rfname = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f[len(f)-1])
                permanent_file = open(rfname, 'wb')
                shutil.copyfileobj(fname.file, permanent_file)
                fname.file.close()
                permanent_file.close()
        
    
    def justUploaded(self):
        file_name = request.GET.get('file_name')
        rfname = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), file_name)
        if os.path.exists(rfname):
            return "0"
        else:
            return "1"

    
    def check_input_pdb(self):
        #leggo variabile contenente nome file field da controllare
        check_file = request.POST.get('submit_check');
        
        #risalgo all'attributo name del file field
        name = check_file.split('_')[0] + "_file"
        nr = check_file.split('_')[2]
        
        #leggo il path del file da uplodare e lo copio nella cartella relativa alla sessione in corso
        file_name = request.POST.getall(name);
        if len(file_name) > 1:
            idx = int(nr) - 1
        else:
            idx = 0
        f = file_name[idx].filename.split('\\')
        rfname = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f[len(f)-1])
        permanent_file = open(rfname, 'wb')
        shutil.copyfileobj(file_name[idx].file, permanent_file)
        file_name[idx].file.close()
        permanent_file.close()
        
        #eseguo la conversione del file di input e restituisco un file XML contententi (eventuali) warning ed errori
        xml_r = check_pdb(rfname)
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        response.body = xml_r
        #return xml_r
    
    def check_constraintXA(self, field, filename):
         #creo elemento di root per doc XML
        root_st = etree.Element("constraint")
        #leggo variabile contenente nome file field da controllare
        # filed: noe dihedral noe 
        te = {}
        
        if field != 'dihedral':
            str_n = field[0:3] + '_number'
        else:
            str_n = field + '_number'
        te["number"] = "1"
        if field == "noe":
            te['nocorr'] = 'False'
            te['lol'] = 'False'
       
        #str_f = field + '_file'
        #file_name = request.POST.get(str_f)
        #f = file_name.filename.split('\\')
        #rfname = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f[len(f)-1])
        #permanent_file = open(rfname, 'wb')
        #shutil.copyfileobj(file_name.file, permanent_file)
        #file_name.file.close()
        #permanent_file.close()
        te["filename"] = filename
        
        if field != 'dihedral':
            str_t = field[0:3] + '_cyanaXplor'
        else:
            str_t = field + '_cyanaXplor'
        te["type"] = "xplor"
        print "########## TE ###############"
        print te
        print "#############################"
        entry_dict  = {"type": "type", "number": "1"}
        f = filename.split('\\')
        output = self.add_tag_xml("run_amber.xml", "constraint", field[0:3], f[len(f)-1], entry_dict)
        if output == 'True':
            print 'some OOOOrrors'
        #if field == 'rdc' or field == 'pcs':
        #    str_p = field + '_select'
        #    fit_param = request.POST.get(str_p)
        #    te["fit"] = fit_param
        if field != 'dihedral':
            etree.SubElement(root_st, field[0:3] , te )
        else:
            etree.SubElement(root_st, field , te )
        
        
        cyanaXplor = "xplor"
        if field[0:3] == 'noe' and cyanaXplor == 'xplor':
            body = check_noe_xplor(root_st)
        
            
        if field == 'dihedral' and cyanaXplor == 'xplor':
            body = check_dih_xplor(root_st)
        

        if field == 'rdc' and cyanaXplor == 'xplor':
            body = check_rdc_xplor(root_st)
            

        if field == 'pcs' and cyanaXplor == 'xplor':
            body = check_pcs_xplor(root_st)            
        
            
    def check_constraint(self):
         #creo elemento di root per doc XML
        root_st = etree.Element("constraint")
        #leggo variabile contenente nome file field da controllare
        field = request.POST.get('field')

        te = {}
        
        if field != 'dihedral':
            str_n = field[0:3] + '_number'
        else:
            str_n = field + '_number'
        number = request.POST.get(str_n)
        te["number"] = number
        if field == "noe":
            if 'noe_nocorr_r' in request.params:
                nocorrlist = request.POST.getall('noe_nocorr_r')
                te['nocorr'] = nocorrlist[len(nocorrlist)-1]
            else:
                te['nocorr'] = 'False'
            te['lol'] = 'False'
        elif field == "noeLol":
            if 'noeLol_nocorr_r' in request.params:
                nocorrlist = request.POST.getall('noeLol_nocorr_r')
                te['nocorr'] = nocorrlist[len(nocorrlist)-1]
            elif 'noeLol_nocorr_r' in request.params:
                nocorrlist = request.POST.getall('noeLol_nocorr_r')
                te['nocorr'] = nocorrlist[len(nocorrlist)-1]
            else:
                te['nocorr'] = 'False'
            te['lol'] = 'True'
        str_f = field + '_file'
        file_name = request.POST.get(str_f)
        f = file_name.filename.split('\\')
        rfname = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), f[len(f)-1])
        permanent_file = open(rfname, 'wb')
        shutil.copyfileobj(file_name.file, permanent_file)
        file_name.file.close()
        permanent_file.close()
        te["filename"] = file_name.filename
        
        if field != 'dihedral':
            str_t = field[0:3] + '_cyanaXplor'
        else:
            str_t = field + '_cyanaXplor'
        cyanaXplor = request.POST.get(str_t)
        te["type"] = cyanaXplor
        print "########## TE ###############"
        print te
        print "#############################"
        entry_dict  = {"type": cyanaXplor, "number": number}
        output = self.add_tag_xml("run_amber.xml", "constraint", field[0:3], f[len(f)-1], entry_dict)
        if output == 'True':
            print 'some OOOOrrors'
        #if field == 'rdc' or field == 'pcs':
        #    str_p = field + '_select'
        #    fit_param = request.POST.get(str_p)
        #    te["fit"] = fit_param
        if field != 'dihedral':
            etree.SubElement(root_st, field[0:3] , te )
        else:
            etree.SubElement(root_st, field , te )
        
        #ANDREA chiama il tuo metodo per il check e come input usa root_st
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        #response.body = etree.tostring(root_st, pretty_print=True)
        
        if field[0:3] == 'noe' and cyanaXplor == 'xplor':
            response.body = check_noe_xplor(root_st)
        if field[0:3] == 'noe' and cyanaXplor == 'dyana':
            cyana = False
            response.body = check_noe_d_cyana(root_st, cyana)
        if field[0:3] == 'noe' and cyanaXplor == 'cyana':
            cyana = True
            response.body = check_noe_d_cyana(root_st, cyana)
            
        if field == 'dihedral' and cyanaXplor == 'xplor':
            response.body = check_dih_xplor(root_st)
        if field == 'dihedral' and cyanaXplor == 'dyana':
            cyana = False
            response.body = check_dih_d_cyana(root_st, cyana)
        if field == 'dihedral' and cyanaXplor == 'cyana':
            cyana = True
            response.body = check_dih_d_cyana(root_st, cyana)

        if field == 'rdc' and cyanaXplor == 'xplor':
            response.body = check_rdc_xplor(root_st)            
        if field == 'rdc' and cyanaXplor == 'dyana':
            cyana = False
            response.body = check_rdc_d_cyana(root_st, cyana)
        if field == 'rdc' and cyanaXplor == 'cyana':
            cyana = True
            response.body = check_rdc_d_cyana(root_st, cyana)

        if field == 'pcs' and cyanaXplor == 'xplor':
            response.body = check_pcs_xplor(root_st)            
        if field == 'pcs' and cyanaXplor == 'dyana':
            cyana = False
            response.body = check_pcs_d_cyana(root_st, cyana)
        if field == 'pcs' and cyanaXplor == 'cyana':
            cyana = True
            response.body = check_pcs_d_cyana(root_st, cyana)           

        
    def fit_pcs(self, protocol = "", xml_in = "",metal = "", ini_num = "", temperature = "", b = "", tolerance = ""):
        print "FIT_PCS"
        if len(xml_in) == 0:
            xml_in = request.POST.get("pcs_xml")
            metal = request.POST.get("metal")
            ini_num = request.POST.get("number")
            protocol = request.POST.get("protocol")
            temperature = request.POST.get("temperature")
            b = request.POST.get("b")
            tolerance = request.POST.get("tolerance")
          #xml_file = xml_in.split('.')[0]+'.xml'
        
        if "withpcsrdc" in request.params and len(protocol) > 0:
            with_r = request.POST.get("withpcsrdc")
            weight = request.POST.get("weight")
            self.fit_rdc("" , with_r, metal, ini_num, temperature, tolerance)
        else:
            with_r = ""
            weight = "1.0"
        #print protocol 
        
        def fit_multi():
            if metal == "No Par. Cent.":
                for iu in range(len(pdb_onm)):
                    if len(pdb_onm[iu]) > 5:
                        pdb_o.append(pdb_onm[iu])
                        if iu == lupdb-1 :
                            nuatm = int(pdb_onm[iu].split()[1])
                            nures = int(pdb_onm[iu].split()[4])
                            pdb_o.append("ATOM   %4d MEX  MEX  %4d       0.000   0.000   0.000\n" %(nuatm + 1, nures + 1))
                            if protocol == "calc":
                                pdb_o.append("ATOM   %4d  AX  CHX  %4d       %8.3f   %8.3f   %8.3f\n" %(nuatm + 2, nures + 2, float(x[0]), float(x[1]), float(x[2])))
                                pdb_o.append("ATOM   %4d  AY  CHY  %4d       %8.3f   %8.3f   %8.3f\n" %(nuatm + 3, nures + 3, float(y[0]), float(y[1]), float(y[2])))
                                pdb_o.append("ATOM   %4d  AZ  CHZ  %4d       %8.3f   %8.3f   %8.3f\n" %(nuatm + 4, nures + 4), float(z[0]), float(z[1]), float(z[2]))
            else:
                stop_w_pdb = 0
                for iu in pdb_c:
                    if len(iu) > 5:
                        if metal.split()[0].strip() in iu[12:16].strip() and metal.split()[1].strip() in iu[17:20].strip() and metal.split()[2].strip() in iu[22:26].strip():
                            tmp_iu1 = iu[0:12] + "MEX " + iu[17:]
                            pdb_o.append(iu.replace(iu,tmp_iu1))
                            #pdb_o.append(iu.replace(iu.split()[2],"MEX"))
                            if protocol == "calc":
                                nuatm = int(iu.split()[1])
                                nures = int(iu.split()[4])
                                pdb_o.append("ATOM   %4d  AX  CHX  %4d       %8.3f   %8.3f   %8.3f\n" %(nuatm + 2, nures + 2, float(x[0]), float(x[1]), float(x[2])))
                                pdb_o.append("ATOM   %4d  AY  CHY  %4d       %8.3f   %8.3f   %8.3f\n" %(nuatm + 3, nures + 3, float(y[0]), float(y[1]), float(y[2])))
                                pdb_o.append("ATOM   %4d  AZ  CHZ  %4d       %8.3f   %8.3f   %8.3f\n" %(nuatm + 4, nures + 4, float(z[0]), float(z[1]), float(z[2])))
                                stop_w_pdb = 1
                        elif not "MEX" in iu and stop_w_pdb == 0:
                            pdb_o.append(iu)
                    
            pdb_fanta = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "xc1fantavv.pdb")
            pdb_o_f = open(pdb_fanta,"w")
            pdb_o_f.writelines(pdb_o)
            pdb_o_f.close()
            
            rdc_fanta = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "xc1fantardc" )
            if os.path.exists(rdc_fanta):
                os.remove(rdc_fanta)
                if len(with_r) > 0:
                    shutil.copyfile(os.path.join(config['app_conf']['amber_data'],
                                                 session.get('DIR_CACHE'),with_r + "rdc_in" ), rdc_fanta)
                else:
                    file_tmp = open(rdc_fanta, 'w')
                    file_tmp.write(" ")
                    file_tmp.close()
            else:
                print "creo rdc_fanta"
                file_tmp = open(rdc_fanta, 'w')
                file_tmp.write(" ")
                file_tmp.close()
    
                
            pcs_fanta = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "xc1fantapcs")
            pcs_o_f = open(pcs_fanta,"w")
            pcs_o_f.writelines(rst)
            pcs_o_f.close()
            
            shutil.copyfile(pcs_fanta,os.path.join(config['app_conf']['amber_data'],
                                                   session.get('DIR_CACHE'), xml_in + "pcs_in"))
            print metal
            print pcs_fanta
            
            w_dir = os.path.join(config['app_conf']['prog_dir'], "fantallnew")
            
            
            if protocol == "fit": 
                loc = os.getcwd()
                os.chdir(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
                shutil.copyfile(os.path.join(config['app_conf']['prog_dir'], "fantallnew", "fantallnew"),
                                os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "fantallnew") )
                os.chmod(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "fantallnew"), 0774)
                cmd = "./fantallnew  %s %s " % (weight, temperature)
                
                print cmd
                out_leap=os.popen(cmd).read()
                open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"pcsoutfanta"),"w").write(out_leap)
                os.chdir(loc)
                
                print out_leap
                
                root_pcs = etree.SubElement(root, "fanta_pcs")
                etree.SubElement(root_pcs, "metal").text = metal
                root_pcs, pcs_fo, pcs_gnu, dchiax, dchirh= take_out_pcs(out_leap, "fit", root_pcs, xml_in)
                
                if len(with_r) > 0:
                    root_rdc = etree.SubElement(root, "fanta_rdc" )
                    root_rdc, rdc_fo, rdc_gnu, dchiax, dchirh = take_out_rdc(out_leap, "fit", root_rdc, with_r)
                    
                    rdc_fons = []
                    af = ""
                    for i in rdc_fo:
                        a = i.split()
                        for ai in a:
                            if len(ai) > 0:
                                if len(ai) > 7:
                                    ai = "%6.4f" %float(ai)
                                af += ai + ";"
                        rdc_fons.append(af)
                        af = ""
                    #shutil.copyfile(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "fort.99"), os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), xml_in + "_fanta.pdb") )
                    
                    etree.SubElement(root_rdc, "rdc_out" ).text = list2txt(rdc_fons)
                    
    
                pcs_fons = []
                af = ""
                for i in pcs_fo:
                    a = i.split()
                    for ai in a:
                        if len(ai) > 0:
                            if len(ai) > 7:
                                ai = "%6.4f" %float(ai)
                            af += ai + ";"
                    pcs_fons.append(af)
                    af = ""
                shutil.copyfile(os.path.join(config['app_conf']['amber_data'],
                                             session.get('DIR_CACHE'), "fort.99"),
                                os.path.join(config['app_conf']['amber_data'],
                                             session.get('DIR_CACHE'), xml_in + "_fanta.pdb") )
                
                etree.SubElement(root_pcs, "pcs_out" ).text = list2txt(pcs_fons)
                
                graph =  xml_in + "_fanta.png"
                gnudata = "data_in_pcs"
                print "GNUPLOT"
                loc = os.getcwd()
                os.chdir(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
                gnudataf = open(gnudata, "w")
                gnudataf.writelines(pcs_gnu)
                gnudataf.close()
        
                gp = os.popen( '/usr/bin/gnuplot', 'w' )
                gp.write( "set output '%s'; set terminal png; \n" % graph )
                gp.write( 'set title "PCS plot %s Dchi= %s %s" \n' %(xml_in, dchiax, dchirh) )
                gp.write( 'set xlabel "PCS calculated" \n' )
                gp.write( 'set ylabel "PCS observed" \n' )
                gp.write( 'unset key \n' )
                #gp.write( 'plot "%s" using 1:2 smooth unique with points , "" using 1:2:3 smooth unique with yerrorbars \n' % gnudata)
                gp.write( 'plot "%s" using 1:2:3 smooth unique with yerrorbars \n' % gnudata)
                gp.write( "exit\n" )
                gp.close()
        
                png_out = os.path.join(config['app_conf']['png_image'], str(random.randint(100000000, 999999999))+'.png')
                shutil.copyfile(graph, png_out)
                os.chdir(loc)
                print "END GNUPLOT"
                
                etree.SubElement(root_pcs, "pcs_graph" ).text = os.path.split(png_out)[1]
                etree.SubElement(root_pcs, "pcs_pdb" ).text = xml_in + "_fanta.pdb"
                
                if len(with_r) > 0:
                    
                    graph =  xml_in + "_fanta.png"
                    gnudata = "data_in_rdc"
                    print "GNUPLOT"
                    loc = os.getcwd()
                    os.chdir(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
                    gnudataf = open(gnudata, "w")
                    gnudataf.writelines(rdc_gnu)
                    gnudataf.close()
            
                    gp = os.popen( '/usr/bin/gnuplot', 'w' )
                    gp.write( "set output '%s'; set terminal png; \n" % graph )
                    gp.write( 'set title "RDC plot %s Dchi= %s %s" \n' %(xml_in, dchiax, dchirh) )
                    gp.write( 'set xlabel "RDC calculated" \n' )
                    gp.write( 'set ylabel "RDC observed" \n' )
                    gp.write( 'unset key \n' )
                    #gp.write( 'plot "%s" using 1:2 smooth unique with points , "" using 1:2:3 smooth unique with yerrorbars \n' % gnudata)
                    gp.write( 'plot "%s" using 1:2:3 smooth unique with yerrorbars \n' % gnudata)
                    gp.write( "exit\n" )
                    gp.close()
            
                    png_out = os.path.join(config['app_conf']['png_image'], str(random.randint(100000000, 999999999))+'.png')
                    shutil.copyfile(graph, png_out)
                    os.chdir(loc)
                    print "END GNUPLOT RDC"
                    etree.SubElement(root_rdc, "rdc_graph" ).text = os.path.split(png_out)[1]
                    #etree.SubElement(root_pcs, "rdc_pdb" ).text = xml_in + "_fanta.pdb"
               
                print etree.tostring(root, pretty_print=True)
                shutil.copyfile(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "fort.99"),
                            os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), xml_in + "_pcsfanta.pdb") )
                loc = os.getcwd()
                os.chdir(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
                os.system("/bin/tar cvf pcsoutfanta.tar pcsoutfanta %s" %  (xml_in + "_pcsfanta.pdb")) 
                os.chdir(loc)
        
        
        xmlpcs = etree.parse(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), xml_in + ".xml"))  
        pdb_out = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "out_leap.pdb")
        pdb_ref_n = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb.ref")
             
        print pdb_out
        print pdb_ref_n
        print "XML_PCS"
        print etree.tostring(xmlpcs, pretty_print=True)
        
        #ini_num = 0
        [ resu_vx, rst ]= convpcsxml2fanta.convert(xmlpcs, ini_num, pdb_out, pdb_ref_n, tolerance, b)        
        
        pdb_o = []
        pdb_onm = []
        pdb_c = open(pdb_out,"r").readlines()
        
        for iu in pdb_c:
            if iu.startswith("ATOM"):
                pdb_onm.append(iu)
        lupdb = len(pdb_onm)
        root = etree.Element("fanta")
        fit_multi()
        #response.headers['content-type'] = 'text/xml; charset=utf-8'
        
        #response.body = etree.tostring(root, pretty_print=True)
        print metal
        print "PROTOCOL "
        print protocol
        return etree.tostring(root, pretty_print=True)
    
    def find_metal1(self):
        # Call real function from metal_utils
        #result = find_metal1()
        #return result
        lista = []
        listaa = {}
        pdb_out = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "out_leap.pdb")
        filel = open(pdb_out,"r").readlines()
    
        for i in filel:
            if len(i.split()) >= 8 and i.startswith("ATOM"):
                rnu = int(i[22:26])
                panu = int(i[6:11])
                pana = i[12:17].replace(" ","")
                prna = i[17:21].replace(" ","")
                prnu = int(i[22:26])                
                lista.append("%s %s" %( prna, prnu))
                listaa["%s %s" %( prna, prnu)] = pana
        root = etree.Element("sel_metal")   
        for a in lista:
            if lista.count(a) == 1 :
                print "pino"
                etree.SubElement(root, "sel").text  = "%s %s " % (listaa[a], a)
        etree.SubElement(root, "sel").text  = "No Par. Cent."
        print etree.tostring(root, pretty_print=True)
    
        return etree.tostring(root, pretty_print=True)       
    
    def fit_rdc(self, protocol = "", xml_in = "",metal = "", ini_num = "", temperature = "", b = "", tolerance = ""):
        find_metal = False
        if len(xml_in) == 0:
            xml_in = request.POST.get("rdc_xml")
            #xml_file = xml_in.split('.')[0]+'.xml'
            temperature = request.POST.get("temperature")
            b = request.POST.get("b")
            tolerance = request.POST.get("tolerance")
            metal = request.POST.get("metal")
            protocol = request.POST.get("protocol")
            ini_num = request.POST.get("number")
        
        if "withpcsrdc" in request.params and len(protocol) > 0 :
            with_r = request.POST.get("withpcsrdc")
            weight = request.POST.get("weight")
            self.fit_pcs("" , with_r, metal, ini_num, temperature, tolerance)
        else:
            with_r = ""
            weight = "1.0"
            
        xmlrdc = etree.parse(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), xml_in+".xml"))
        pdb_out = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "out_leap.pdb")
        pdb_ref_n = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb.ref")
        
        if protocol == "calc":
            x = []
            y = []
            z = []
            nx = math.sqrt(float(request.POST.get("x1"))**2 + float(request.POST.get("x2"))**2 +
                                                                float(request.POST.get("x3"))**2)
            x.append(float(request.POST.get("x1"))/nx)
            x.append(float(request.POST.get("x2"))/nx)
            x.append(float(request.POST.get("x3"))/nx)
            ny = math.sqrt(float(request.POST.get("y1"))**2 + float(request.POST.get("y2"))**2 +
                                                                float(request.POST.get("y3"))**2)
            y.append(float(request.POST.get("y1"))/ny)
            y.append(float(request.POST.get("y2"))/ny)
            y.append(float(request.POST.get("y3"))/ny)
            nz = math.sqrt(float(request.POST.get("z1"))**2 + float(request.POST.get("z2"))**2 +
                                                                float(request.POST.get("z3"))**2)
            z.append(float(request.POST.get("z1"))/nz)
            z.append(float(request.POST.get("z2"))/nz)
            z.append(float(request.POST.get("z3"))/nz)
            
            #aggiungere controllo se il set e' ortogonale
            ax_tensor = request.POST.get("ax")
            rh_tensor = request.POST.get("rh")
            #tolerance = ""
            
        print pdb_out
        print pdb_ref_n
        print "XML_RDC"
        print etree.tostring(xmlrdc, pretty_print=True)
        
        
        [ resu_vx, rst ]= convrdcxml2fanta.convert(xmlrdc, ini_num, pdb_out, pdb_ref_n, tolerance, b)        
        
        pdb_o = []
        pdb_onm = []
        pdb_c = open(pdb_out,"r").readlines()
        
        for iu in pdb_c:
            if iu.startswith("ATOM"):
                pdb_onm.append(iu)
        lupdb = len(pdb_onm)
        
        if metal == "No Par. Cent.":
            for iu in range(len(pdb_onm)):
                if len(pdb_onm[iu]) > 5:
                    pdb_o.append(pdb_onm[iu])
                    if iu == lupdb-1 :
                        nuatm = int(pdb_onm[iu].split()[1])
                        nures = int(pdb_onm[iu].split()[4])
                        pdb_o.append("ATOM   %4d MEX  MEX  %4d       0.000   0.000   0.000\n" %(nuatm + 1, nures + 1))
                        find_metal = True
                        if protocol == "calc":
                            pdb_o.append("ATOM   %4d  AX  CHX  %4d       %8.3f   %8.3f   %8.3f\n" %(nuatm + 2, nures + 2, float(x[0]), float(x[1]), float(x[2])))
                            pdb_o.append("ATOM   %4d  AY  CHY  %4d       %8.3f   %8.3f   %8.3f\n" %(nuatm + 3, nures + 3, float(y[0]), float(y[1]), float(y[2])))
                            pdb_o.append("ATOM   %4d  AZ  CHZ  %4d       %8.3f   %8.3f   %8.3f\n" %(nuatm + 4, nures + 4), float(z[0]), float(z[1]), float(z[2]))
        else:
            stop_w_pdb = 0
            for iu in pdb_c:
                if len(iu) > 5:
                    if metal.split()[0] == iu.split()[2] and metal.split()[1] == iu.split()[3] and metal.split()[2] == iu.split()[4]:
                        tmp_iu1 = iu[0:12] + "MEX " + iu[17:]
                        pdb_o.append(iu.replace(iu,tmp_iu1))
                        find_metal = True
                        if protocol == "calc":
                            nuatm = int(iu.split()[1])
                            nures = int(iu.split()[4])
                            pdb_o.append("ATOM   %4d  AX  CHX  %4d       %8.3f   %8.3f   %8.3f\n" %(nuatm + 2, nures + 2, float(x[0]), float(x[1]), float(x[2])))
                            pdb_o.append("ATOM   %4d  AY  CHY  %4d       %8.3f   %8.3f   %8.3f\n" %(nuatm + 3, nures + 3, float(y[0]), float(y[1]), float(y[2])))
                            pdb_o.append("ATOM   %4d  AZ  CHZ  %4d       %8.3f   %8.3f   %8.3f\n" %(nuatm + 4, nures + 4, float(z[0]), float(z[1]), float(z[2])))
                            stop_w_pdb = 1
                    elif not "MEX" in iu and stop_w_pdb == 0:
                        pdb_o.append(iu)
                    
        pdb_fanta = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "xc1fantavv.pdb")
        pdb_o_f = open(pdb_fanta,"w")
        pdb_o_f.writelines(pdb_o)
        pdb_o_f.close()
        
        pcs_fanta = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "xc1fantapcs" )
        if os.path.exists(pcs_fanta):
            os.remove(pcs_fanta)
            print "LEN " + with_r
            if len(with_r) > 0:
                shutil.copyfile(os.path.join(config['app_conf']['amber_data'],
                                             session.get('DIR_CACHE'),with_r + "pcs_in" ), pcs_fanta)
            else:
                file_tmp = open(pcs_fanta, 'w')
                file_tmp.write(" ")
                file_tmp.close() 
        else:
            file_tmp = open(pcs_fanta, 'w')
            file_tmp.write(" ")
            file_tmp.close()

            
        rdc_fanta = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "xc1fantardc")
        rdc_o_f = open(rdc_fanta,"w")
        rdc_o_f.writelines(rst)
        rdc_o_f.close()
        shutil.copyfile(rdc_fanta,os.path.join(config['app_conf']['amber_data'],
                                               session.get('DIR_CACHE'), xml_in + "rdc_in"))
        print metal
        print rdc_fanta
        
        w_dir = os.path.join(config['app_conf']['prog_dir'], "fantallnew")
        
        #if protocol == "calc":
        #    loc = os.getcwd()
        #    os.chdir(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
        #    shutil.copyfile(os.path.join(config['app_conf']['prog_dir'], "fantallnew", "calcpcsrdc"),
        #                    os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "calcpcsrdc") )
        #    os.chmod(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "calcpcsrdc"), 0774)
        #    cmd = "./calcpcsrdc  %s %s %s %s " % ("1.0", temperature, ax_tensor, rh_tensor )
        #    
        #    print cmd
        #    out_leap=os.popen(cmd).read()
        #    os.chdir(loc)
        #    
        #    print out_leap           
        #    root, rdc_fo, rdc_gnu, dchiax, dchirh= take_out_rdc(out_leap, "calc", "")
        #
        #    rdc_fons = []
        #    af = ""
        #    for i in rdc_fo:
        #        a = i.split()
        #        for ai in a:
        #            if len(ai) > 0:
        #                if len(ai) > 7:
        #                    ai = "%6.4f" %float(ai)
        #                af += ai + ";"
        #        rdc_fons.append(af)
        #        af = ""
        #    shutil.copyfile(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "fort.99"),
        #                    os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), xml_in + "_fanta.pdb") )
        #    
        #    etree.SubElement(root, "rdc_out" ).text = list2txt(rdc_fons)
        #    
        #    print "METAL"
        #    print metal
        #    
        #    graph =  xml_in + "_fanta.png"
        #    gnudata = "data_in_rdc"
        #    print "GNUPLOT"
        #    loc = os.getcwd()
        #    os.chdir(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
        #    gnudataf = open(gnudata, "w")
        #    gnudataf.writelines(rdc_gnu)
        #    gnudataf.close()
        #
        #    gp = os.popen( '/usr/bin/gnuplot', 'w' )
        #    gp.write( "set output '%s'; set terminal png; \n" % graph )
        #    gp.write( 'set title "RDC plot %s Dchi= %s %s" \n' %(xml_in, dchiax, dchirh) )
        #    gp.write( 'set xlabel "RDC calculated" \n' )
        #    gp.write( 'set ylabel "RDC observed" \n' )
        #    gp.write( 'unset key \n' )
        #    #gp.write( 'plot "%s" using 1:2 smooth unique with points , "" using 1:2:3 smooth unique with yerrorbars \n' % gnudata)
        #    gp.write( 'plot "%s" using 1:2:3 smooth unique with yerrorbars \n' % gnudata)
        #    gp.write( "exit\n" )
        #    gp.close()
        #
        #    png_out = os.path.join(config['app_conf']['png_image'], str(random.randint(100000000, 999999999))+'.png')
        #    shutil.copyfile(graph, png_out)
        #    os.chdir(loc)
        #    print "END GNUPLOT"
        #    
        #    etree.SubElement(root, "rdc_graph" ).text = os.path.split(png_out)[1]
        #    etree.SubElement(root, "rdc_pdb" ).text = xml_in + "_fanta.pdb"
        #    print etree.tostring(root, pretty_print=True)
        #run fantalnew
        root = etree.Element("fanta")
        if not find_metal:
            etree.SubElement(root, "error").text = "Metal not find in selection"
            
        if protocol == "fit" and find_metal: 
            loc = os.getcwd()
            os.chdir(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
            shutil.copyfile(os.path.join(config['app_conf']['prog_dir'], "fantallnew", "fantallnew"),
                            os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "fantallnew") )
            os.chmod(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "fantallnew"), 0774)
            cmd = "./fantallnew  %s %s " % (weight, temperature)
            print "Work Directory and command"
            print os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'))
            print cmd
            out_leap = os.popen(cmd).read()
            open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"rdcoutfanta"),"w").write(out_leap)
            
            os.chdir(loc)
            print out_leap
            
            
            root_rdc = etree.SubElement(root, "fanta_rdc")
            root_rdc, rdc_fo, rdc_gnu, dchiax, dchirh = take_out_rdc(out_leap, "fit", root_rdc, xml_in)
            
            if len(with_r) > 0:
                root_pcs = etree.SubElement(root, "fanta_pcs" )
                etree.SubElement(root_pcs, "metal").text = metal
                root_pcs, pcs_fo, pcs_gnu, dchiax, dchirh = take_out_pcs(out_leap, "fit", root_pcs, with_r)
                pcs_fons = []
                af = ""
                for i in pcs_fo:
                    a = i.split()
                    for ai in a:
                        if len(ai) > 0:
                            if len(ai) > 7:
                                ai = "%6.4f" %float(ai)
                            af += ai + ";"
                    pcs_fons.append(af)
                    af = ""
                #shutil.copyfile(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "fort.99"), os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), xml_in + "_fanta.pdb") )
                
                etree.SubElement(root_pcs, "pcs_out" ).text = list2txt(pcs_fons)
            
            rdc_fons = []
            af = ""
            for i in rdc_fo:
                a = i.split()
                for ai in a:
                    if len(ai) > 0:
                        if len(ai) > 7:
                            ai = "%6.4f" %float(ai)
                        af += ai + ";"
                rdc_fons.append(af)
                af = ""
            shutil.copyfile(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "fort.99"),
                            os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), xml_in + "_rdcfanta.pdb") )
            loc = os.getcwd()
            os.chdir(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
            os.system("/bin/tar cvf rdcoutfanta.tar rdcoutfanta %s" %  (xml_in + "_rdcfanta.pdb")) 
            os.chdir(loc)
                      
            etree.SubElement(root_rdc, "rdc_out" ).text = list2txt(rdc_fons)
                       
            if len(with_r) > 0 and find_metal:
                
                graph =  xml_in + "_fanta.png"
                gnudata = "data_in_pcs"
                print "GNUPLOT"
                loc = os.getcwd()
                os.chdir(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
                gnudataf = open(gnudata, "w")
                gnudataf.writelines(pcs_gnu)
                gnudataf.close()
        
                gp = os.popen( '/usr/bin/gnuplot', 'w' )
                gp.write( "set output '%s'; set terminal png; \n" % graph )
                gp.write( 'set title "PCS plot %s Dchi= %s %s" \n' %(xml_in, dchiax, dchirh) )
                gp.write( 'set xlabel "PCS calculated" \n' )
                gp.write( 'set ylabel "PCS observed" \n' )
                gp.write( 'unset key \n' )
                #gp.write( 'plot "%s" using 1:2 smooth unique with points , "" using 1:2:3 smooth unique with yerrorbars \n' % gnudata)
                gp.write( 'plot "%s" using 1:2:3 smooth unique with yerrorbars \n' % gnudata)
                gp.write( "exit\n" )
                gp.close()
        
                png_out = os.path.join(config['app_conf']['png_image'], str(random.randint(100000000, 999999999))+'.png')
                shutil.copyfile(graph, png_out)
                os.chdir(loc)
                etree.SubElement(root_pcs, "pcs_graph" ).text = os.path.split(png_out)[1]
                print "END GNUPLOT RDC"
                
            
            graph =  xml_in + "_fanta.png"
            gnudata = "data_in_rdc"
            print "GNUPLOT"
            loc = os.getcwd()
            os.chdir(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE')))
            gnudataf = open(gnudata, "w")
            gnudataf.writelines(rdc_gnu)
            gnudataf.close()
    
            gp = os.popen( '/usr/bin/gnuplot', 'w' )
            gp.write( "set output '%s'; set terminal png; \n" % graph )
            gp.write( 'set title "RDC plot %s Dchi= %s %s" \n' %(xml_in, dchiax, dchirh) )
            gp.write( 'set xlabel "RDC calculated" \n' )
            gp.write( 'set ylabel "RDC observed" \n' )
            gp.write( 'unset key \n' )
            #gp.write( 'plot "%s" using 1:2 smooth unique with points , "" using 1:2:3 smooth unique with yerrorbars \n' % gnudata)
            gp.write( 'plot "%s" using 1:2:3 smooth unique with yerrorbars \n' % gnudata)
            gp.write( "exit\n" )
            gp.close()
    
            png_out = os.path.join(config['app_conf']['png_image'], str(random.randint(100000000, 999999999))+'.png')
            shutil.copyfile(graph, png_out)
            os.chdir(loc)
            print "END GNUPLOT"
            
            etree.SubElement(root_rdc, "rdc_graph" ).text = os.path.split(png_out)[1]
            etree.SubElement(root_rdc, "rdc_pdb" ).text = xml_in + "_fanta.pdb"
            print etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8")
        
        #response.headers['content-type'] = 'text/xml; charset=utf-8'
        #response.body = etree.tostring(root, pretty_print=True)
        print metal
        print "PROTOCOL "
        print protocol
        return etree.tostring(root, pretty_print=True)        
        

    def run_tleap_1(self, xmlin):
        print "######## XMLIN da run_tlep_1 ##########"
        print etree.tostring(xmlin, pretty_print=True)
        print "#######################"
        protein = []
        ligand = []
        no_std_ligand = []
        ligand_top = []
        ligand_par = []
        top_lib = []
        top_prep = []
        bond = []
        solv = ""
        ions = ""
        two = False
        born = ""
        anteff = ""
        temp_am = """
#ForceField
source ${ff}

#Antechamber ff
% if len(anteff)>0:
source leaprc.gaff
% endif

#Atomtype
% if len(atm_type)>0:
% for atmy in atm_type:
${atmy}
% endfor
% endif

#Load all parameters
% if len(par)>0:
% for ik in par:
loadamberparams  ${ik}
% endfor
% endif
    
#Load all topology lib format
% if len(top_lib)>0:
% for ik in top_lib:
loadOff  ${ik}
% endfor
% endif
    
#Load all topology prep format
% if len(top_prep)>0:
% for ik in top_prep:
loadAmberPrep  ${ik}
% endfor
% endif
    
#Define logfile
logFile  ${log}
    
#Laod PDB
sys = loadPdb ${pdb}

#Define bond 
% if len(bond)>0:
% for ik in bond:
bond ${ik}
% endfor
% endif

#pdb no solvent
savepdb sys ${pdb_out}

#Define solvatation
% if len(solv)>0:
${solv}
% endif

#Define ions
% if len(ions)>0:
${ions}
% endif

saveamberparm sys ${prmtop} ${prmcrd}
savepdb sys ${pdb_solvent}
quit
    
        """
        atm_type = []
        mytemp = Template(temp_am)
        dir_w =  os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'))
        for elt in xmlin.getiterator():
            if elt.tag == "protein":
                protein.append(elt.get('filename'))
            
            
            
            if elt.tag == "ligand":
                ligand.append(elt.get('filename'))
                ligand_top.append(elt.get("top_filename"))
                if elt.get("par_filename") != "":
                    ligand_par.append(elt.get("par_filename"))
                    
            if elt.tag == "no_std_ligand":
                #no_std_ligand.append(elt.get('filename'))
                ligand_top.append(elt.get("top_filename"))
                if elt.get("par_filename") != "":
                    ligand_par.append(elt.get("par_filename"))
                #addAtomTypes
                if elt.get("atm_filename") != "":
                    atm_type = open(os.path.join(dir_w, elt.get("atm_filename")), "r").readlines()
                    print atm_type
                else:
                    atm_type = []
            
            
            if elt.tag == "bond":
                bond.append("sys.%s.%s sys.%s.%s" %(elt.get('residue1'),elt.get('atom1'),elt.get('residue2'),elt.get('atom2')))
                
            if elt.tag == "solv":
                if elt.get('geo') == "box":
                    geo = "solvateBox"
                    solv = "%s sys %s %s" %(geo, elt.get('solvent'), elt.get('distance'))
                elif elt.get('geo') == "oct":
                    geo = "solvateOct"
                    solv = "%s sys %s %s" %(geo, elt.get('solvent'), elt.get('distance'))
                elif elt.get('geo') == "boxDC":
                    geo = "solvateDontClip"
                    solv = "%s sys %s %s" %(geo, elt.get('solvent'), elt.get('distance'))
                elif elt.get('geo') == "scap":
                    geo = "solvateCap"
                    solv = "%s sys %s sys.%s %s" %(geo, elt.get('solvent'), elt.get('resid'), elt.get('distance'))
                elif elt.get('geo') == "sshell":
                    geo = "solvateShell"
                    solv = "%s sys %s %s" %(geo, elt.get('solvent'), elt.get('distance'))
                    
            #da togliere#        
            #solv = "solvatecap sys TIP3PBOX sys.10  30.0"
                
            if elt.tag == "ions" and not two:
                if ions:
                    ions += " %s %s" %(elt.get('type'), elt.get('number'))
                    two = True
                else:
                    ions = "addIons sys %s %s" %(elt.get('type'), elt.get('number'))
                #type puo essere Cl- Na+ K+ Li+ MG2
            
            if elt.tag == "born":   
                born = "set PBradii = %s " %(elt.get('type'))
                # type puo essere mbondi mbondi2 amber6 bondi
            
            if elt.tag == "ff":
                ff = elt.get('value')
                
            if elt.tag == "antechamber":
                anteff = elt.get('include')
                
        par = []
        for ik in ligand_par:
            par.append(os.path.join(dir_w, ik))
                
        for ik in ligand_top:
            ext = os.path.basename(ik).split(".")[1]
            if ext == "lib":
                top_lib.append(os.path.join(dir_w, ik))
            if ext == "in" or ext == "prepi" or ext == "prep":
                top_prep.append(os.path.join(dir_w, ik))
                
                    
        prot_tot = []
        
        pdb_out = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "out_leap.pdb")
        pdb_solvent = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "pdb_solvent.pdb")
        for ap in protein:
            apw = os.path.join(dir_w, ap)
            fit = open(apw, 'r')
            tf = fit.readlines()
            prot_tot.extend(tf)
            if  not 'TER' in tf[len(tf)-1] :
                prot_tot.append('TER')
            fit.close()
        for ap in no_std_ligand:
            apw = os.path.join(dir_w, ap)
            fit = open(apw, 'r')
            tf = fit.readlines()
            prot_tot.extend(tf)
            if  not 'TER' in tf[len(tf)-1] :
                prot_tot.append('TER')
            fit.close()
            
        pdbo = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "amber_in.pdb")
            
        log = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "log.out")
        prmtop = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "prmtop")
        prmcrd = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "prmcrd")
        if os.path.exists(pdbo):
            os.remove(pdbo)
        if os.path.exists(log):
            os.remove(log)
        if os.path.exists(pdb_out):
            os.remove(pdb_out)
        if os.path.exists(prmtop):
            os.remove(prmtop)
        if os.path.exists(prmcrd):
            os.remove(prmcrd)
        
        fito = open(pdbo, 'w')
        no_ter_prot_tot = []
        for kk in prot_tot:
            if kk[0:3] == "TER":
                no_ter_prot_tot.append("TER\n")
            else:
                no_ter_prot_tot.append(kk)
        fito.writelines(no_ter_prot_tot)
        fito.close()

        print pdbo
        
        command = mytemp.render(ff=ff ,anteff=anteff ,par=par, top_lib=top_lib ,top_prep=top_prep,
                                pdb=pdbo, log=log, pdb_out=pdb_out, prmtop=prmtop, prmcrd=prmcrd, bond=bond, solv=solv, ions=ions, born=born, pdb_solvent=pdb_solvent, atm_type=atm_type)
        
        os.environ["AMBER_HOME"] = "/prog/amber10"
        amber_h_exe = "/prog/amber10/exe/"
        leap_in = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "leap.in")
        if os.path.exists(leap_in):
            os.remove(leap_in)
        com_leap_f = open(leap_in,'w')
        com_leap_f.writelines(command)
        com_leap_f.close()
        
        cmd = "%s/tleap -f %s "%(amber_h_exe, leap_in)
        out_leap_s=os.popen(cmd).read()
        out_leap1 = []
        #da riverdere
        fatal = []
        warning = []
        for i in out_leap_s.splitlines():
            if i.startswith("FATAL:"):
                fatal.append(i)
            if i.startswith("WARNING:"):
                warning.append(i) 
            if dir_w in i:
                i.replace(dir_w, "")
                out_leap1.append(i)
            else:
                out_leap1.append(i)
        out_leap = list2txt(out_leap1)
        out_fatal = list2txt(fatal)
        out_warning = list2txt(warning)
        
        leap_xml = etree.Element("leap")
        if len(fatal) > 0:
            etree.SubElement(leap_xml, "fatal").text = out_fatal
        etree.SubElement(leap_xml, "warning").text = out_warning
        etree.SubElement(leap_xml, "out").text = out_leap
        
        if os.path.exists(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "prmcrd")):
            if os.path.getsize(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "prmcrd")) == 0:
                etree.SubElement(leap_xml, "Error").text="File AMBER coordinates bad size "
        else:
            etree.SubElement(leap_xml, "Error").text="File AMBER coordinates not created"
            
        if os.path.exists(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "prmtop")):
            if os.path.getsize(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "prmtop")) == 0:
                etree.SubElement(leap_xml, "Error").text="File AMBER topology bad size "
        else:
            etree.SubElement(leap_xml, "Error").text="File AMBER topology not created"
            
        if not os.path.exists(pdb_out):
            etree.SubElement(leap_xml, "Error").text="Amber PDB not created"
        else:
            sp = {}
            pdb_i = open(pdb_out, 'r').readlines()
            sp_st = "1"
            c_ter = 1
            for il in range(len(pdb_i)):
                if "TER" in pdb_i[il]:
                    sp_st = sp_st + "-" + pdb_i[il-1][22:26].replace(" ","")
                    sp["chain_n"] = "%d" %c_ter
                    sp["chain_range"] = sp_st
                    etree.SubElement(leap_xml, "chain", sp)
                    sp = {}
                    try:
                        if "ATOM" in pdb_i[il+1]:
                            sp_st = pdb_i[il+1][22:26].replace(" ","")
                            c_ter += 1
                    except:
                        sp = {}
                    
        leap_xml_out = etree.tostring(leap_xml, pretty_print=True, xml_declaration=True, encoding="utf-8")
        leap_xml_tree = etree.ElementTree(leap_xml)
        leap_xml_tree.write(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "tleap.xml"))
        return leap_xml_out

    def download(self):
        requested_filename = request.GET.get('requested_filename', "")
        if requested_filename:
            filename = os.path.join(
                config['app_conf']['amber_data'],session.get('DIR_CACHE'),
                requested_filename.replace(os.sep, '_')
            )
            if not os.path.exists(filename):
                return 'No such file'
            permanent_file = open(filename, 'rb')
            data = permanent_file.read()
            permanent_file.close()
            response.content_type = guess_type(filename)[0] or 'text/plain'
            response.headers['Content-Disposition'] = 'attachment; filename="%s"'%(requested_filename)
            return data
        else:
            return 'No such file'

    def get_sanderConfig(self):
        filename = os.path.join(
            config['app_conf']['amber_data'],'sander_config.xml')
        if not os.path.exists(filename):
            return 'No such file'
        permanent_file = open(filename, 'rb')
        data = permanent_file.read()
        permanent_file.close()
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        response.body = data

    def prova(self):
        rfname = os.path.join(config['app_conf']['amber_data'], "generate_protein.pdb")
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        xml_r = check_pdb(rfname)
        return xml_r
    
    
    
    def jmol_file(self):
        file_name = request.GET.get('file_name')
        rfname = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), file_name)
        permanent_file = open(rfname, 'r')
        return permanent_file
    
    def upload(self):
        field = request.POST.get('field')
        file_name = request.POST.get(field)
        #file_name = request.POST.get('chain_file')
        f = file_name.filename.split('\\')
        print f
        rfname = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), f[len(f)-1])
        permanent_file = open(rfname, 'wb')
        shutil.copyfileobj(file_name.file, permanent_file)
        file_name.file.close()
        permanent_file.close()
        
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        if field == 'chain_file': 
            xml_r = check_pdb(rfname)
            response.body = xml_r
        else:
            response.body = "<OK>ok</OK>"
        
    
    def uploadMultiJobs(self):
        file_name = request.POST.get('multijob')
        f = file_name.filename.split('\\')
        ext = ''.join(f[0][-4:])
        rfname = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "multijobs"+ext)
        permanent_file = open(rfname, 'wb')
        shutil.copyfileobj(file_name.file, permanent_file)
        file_name.file.close()
        permanent_file.close()
        
    
    def removeUploadedFile(self):
        
        file_name = request.GET.get('file_name')
        
        rfname = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), file_name)
        if os.path.exists(rfname):
            os.remove(rfname)
        
        file_c = file_name.split('.')[0] + '_c.pdb'
        rfname_c = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), file_c)
        if os.path.exists(rfname_c):
            os.remove(rfname_c)
        
    #def img_loader(self):
    #    file_name = request.POST.get('file_name')
    #    rfname = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), file_name)
    #    
    #    response.headers['content-type'] = 'image/bmp';
    #    response.body = 

    
    def add_tag_xml(self, xmlFile, where, tagName, id, attributes):
        """
        This function open XML file <xmlFile> and append new tag <tagName>
        and your childs <attributes> inside node <where>
        
        input:
            <xmlFile> is a string of relative path of xml file to open
            <where> is location about insert <tagName> as child
            <tagName> is a string representing name of tag to add
            <id> ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ # FERELLA DOCET
            <attributes> is a dictionary representing childs of tag <tagName>
        
        return:
            True if no error 
            False otherwise
        """
        
        
        
        try:
            #rfile = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), xmlFile)
            #if os.path.exists(rfname):
            #    ofile = open(rfile, 'w')
            #else:
            #    ofile = open(rfile, 'w')
            #    ofile.write('<run><constraint></constraint></run>')
            
            hfile = etree.parse(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), xmlFile))
            root = hfile.getroot()
            print root.tag
            htag = hfile.find(where)
            newTag = etree.Element(tagName)
            newTag.attrib["filename"] = id
            for key  in attributes.keys():
                etree.SubElement(newTag, key).text = attributes[key]
            etree.SubElement(htag, newTag)
            htag.append(newTag)
            hfile.write(xmlFile)
        except:
            return False
        
        return True
    
    def remove_tag_xml(self, xmlFile, tagName, id):
        """
        This function open XML file <xmlFile> search tag <tagName>
        with attribute filename = <id> and remove it
        
        input:
            <xmlFile> is a string of relative path of xml file to open
            <tagName> is a string representing name of tag to update
            <id> is a content of attribute filename (like db primary key)
        
        return:
            True if no error 
            False otherwise
        """
        
        try: 
            rfile = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), xmlFile)
            ofile = open(rfile, 'w')
            hfile = etree.parse(ofile)
            root = hfile.getroot()
            
            tag_item = root.find(tagName)
            if tag_item != 'null':
                root.remove(tag_item)
                return True;
            else:
                return False
        except:
            return False
        
    
    def update_tag_xml(self, xmlFile, tagName, id, attributes):
        """
        This function open XML file <xmlFile> search tag <tagName>
        and add/update your childs with <attributes>
        
        input:
            <xmlFile> is a string of relative path of xml file to open
            <tagName> is a string representing name of tag to update
            <attributes> is a dictionary representing childs of tag <tagName>
        
        return:
            True if no error 
            False otherwise
        """
        try:
            rfile = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), xmlFile)
            
            ofile = open(rfile, 'w')
            hfile = etree.parse(ofile)
            root = hfile.getroot()
            
            tag_item = root.findall(".//"+tagName+"[@filename="+id+"]")[0]
            if tag_item != 'null':
                for key  in attributes.keys():
                    child_item = tag_item.find(key)
                    if child_item == 'null':
                        etree.SubElement(tag_item, key).text = attributes[key]
                    else:
                        new_child_item = etree.Element(key).text = attributes[key]
                        tag_item.replace(child_item, new_child_item)
                return True;
            else:
                return False
        except:
            return False
    
    def submitSander(self):
        print "#### SUBMIT SANDER ######"
        sander_str = request.POST.get('sout')
        #print sander_str
        sander_descr = request.POST.get('description')
        #print sander_descr
        descriptions = sander_descr.split("??")
        sander_str = sander_str[:-8]
        #print "stringona %s" %sander_str
        sander_protocols = sander_str.split('????')
        for prot in range(len(sander_protocols)):
            if sander_protocols[prot].endswith('-'):
                sander_protocols[prot] = sander_protocols[prot][:-4]
        print "calculations %s" %sander_protocols
        len_calc = len(sander_protocols)
        for idx_prtcl in range(len(sander_protocols)):
            sander_sections = sander_protocols[idx_prtcl].split('----')
            print "sander sections %s" %sander_sections
            rfname = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "sander"+str(idx_prtcl)+".in")
            fout = open(rfname, 'w')
            fout.write(descriptions[idx_prtcl]+'\n')
            iswt = False
            for i in range(len(sander_sections)):
                sec = sander_sections[i]
                if sec[len(sec)-1] == '^':
                    sec = sec[:-1]
                content = sec.split('^')
                print "content %s" %content
                if content[0] != 'sander_file':
                    fout.write('&'+content[0]+'\n')
                    if content[0] == 'wt':
                        iswt = True
                else:
                    if not iswt:
                        fout.write("&wt type='END' /\n")
                    fout.write("LISTOUT=POUT\n")
                len_content = len(content[1:])
                j = 0
                issander = False
                
                for flag in content[1:]:
                    j = j + 1
                    if content[0] == 'sander_file':
                        issander = True
                        fout.write(flag+'\n')
                    elif len_content == j:
                        fout.write(flag+'\n')
                    else:
                        fout.write(flag+',\n')
                
                if not issander:
                    if iswt:
                        fout.write(" /\n&wt type='END' /\n")
                    else:
                        fout.write("/\n")
                #else:
                #    fout.write("\n")
            #LISTOUT va aggiunto solo all'ultimo calcolo
            if not issander:
                fout.write("\n")
                
            fout.close()
        return "sander(0-9).in created!"
    

    def load_template(self):
        fname = request.POST.get('filename')
        filename = os.path.join(
            config['app_conf']['amber_data'],fname)
        if not os.path.exists(filename):
            return 'No such file'
        permanent_file = open(filename, 'rb')
        data = permanent_file.read()
        permanent_file.close()
        response.headers['content-type'] = 'text/xml; charset=utf-8'
        response.body = data
    
    def isCalcExist(self):
        owner = Session.query(Users).get(session['REMOTE_USER'])
        proj = request.POST.get('proj')
        calc = request.POST.get('calc')
        print "check if exist %s --%s" %(proj, calc)
        cname = Session.query(Calculations).filter(and_(Calculations.name==calc, Calculations.project_id==int(proj))).first()
        
        print "cname is: ", cname
        if cname:
            return "True"
        else:
            return "False"
    
    def isDirExist(self):
        
        prj_id = request.POST.get('prj_id')
        calc_name = request.POST.get('calc_name')
        tipology = request.POST.get('tipology')
        
        print "project: %s" %prj_id
        print "tipology: %s" %tipology
        print "calculation: %s"   %calc_name
        
        calc_name = calc_name.replace(' ', '_')
        owner = Session.query(Users).get(session['REMOTE_USER'])
        project = Session.query(Projects).get(int(prj_id))
        calc_type = Session.query(CalculationTipology).filter(CalculationTipology.tipology == tipology).first()
        
        cname = Session.query(Calculations).filter(and_(Calculations.name==calc_name, Calculations.project_id==int(prj_id))).first()
        
        print cname
        # Check the existance of the calculation
        if cname:
            return 'True'
        
        return 'False'
    
    def checkprmd(self):
        pathcrd = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "prmcrd")
        pathtop = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "prmtop")
        if os.path.exists(pathcrd) and os.path.exists(pathcrd):
            (filetype, perms, owner, group, sizecrd, mtime) = files.get_fileinfo(pathcrd, 0, );
            (filetype, perms, owner, group, sizetop, mtime) = files.get_fileinfo(pathtop, 0, );
            if sizecrd > 0 and sizetop > 0:
                return 'ok'
            else:
                return 'error'
    
