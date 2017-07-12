import logging
import tarfile
import os
import time
import shutil
import re
from datetime import datetime
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config, app_globals
from lxml import etree
import random
from webenmr.lib import files
from webenmr.lib.base import *
from webenmr.lib import return_values
from webenmr.lib.return_values import S_OK, S_ERROR
from webenmr.model import Projects, Users, CalculationTipology, Calculations, Jobs

log = logging.getLogger(__name__)
os.umask(0002)


class CalculationsController(BaseController):
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
        c.page_title = u'Calculations'
        #
        
    def xplor(self):
        # Return a rendered template
        #return render('/calculations.mako')
        # or, return a string
        c.projects = Session.query(Projects).filter(Projects.owner.has(id=session['REMOTE_USER']))
        c.calc_type = Session.query(CalculationTipology).all()
        return render('/calculations/index.mako')
       
    @check_access('Fill Amber') 
    def amber(self, id=None):
        #c.tipology = 'amber'
        c.tipology = session['PORTAL']
        if id:
            c.prj_id = id            
        else:
            # Create a project automatically
            ret = self.project_self_creation(c.tipology)
            if ret['OK']:
                c.prj_id = ret['Value']                
            else:
                h.flash.set_message(ret['Value'], 'error')
                h.redirect('/users/index')
                
        #c.calc_name = 'self_calculation_%s' % str(time.time()).split('.')[0]
        random.seed()
        if session.get('DIR_CACHE', None) is None:
            session['DIR_CACHE'] = os.path.join(config['app_conf']['amber_data'], str(random.randint(100000000, 999999999)))
            session.save()
        elif 'amber_data' not in session.get('DIR_CACHE'):
            session['DIR_CACHE'] = os.path.join(config['app_conf']['amber_data'], str(random.randint(100000000, 999999999)))
            session.save()
        
        if not os.path.isdir(session.get('DIR_CACHE')):
            os.makedirs(session.get('DIR_CACHE'))
        else:
            shutil.rmtree(session.get('DIR_CACHE'))
            os.makedirs(session.get('DIR_CACHE'))
        # Return a rendered template
        c.dir = session.get('DIR_CACHE')
        c.template_dir = config['app_conf']['template_dir']
        return render('/calculations/provaTabs.mako')
        #return render('/calculations/amber.mako')   
    
    
    def newcalc(self, id=None):
        c.tipology = session['PORTAL']
        if session['PORTAL'] == 'amps-nmr':
            tip = 'amber'
        else:
            tip = session['PORTAL']
        if id:
            c.prj_id = id            
        else:
            # Create a project automatically
            ret = self.project_self_creation(tip)
            print ret
            if ret['OK']:
                c.prj_id = ret['Value']
                print "progetto id: %d" %c.prj_id
            else:
                h.flash.set_message(ret['Value'], 'error')
                h.redirect('/users/index')
        if session['PORTAL'] == 'amps-nmr':
            data = 'amber_data'
        elif session['PORTAL'] == 'maxocc':
            data = 'maxocc_data'
        elif session['PORTAL'] == 'xplor-nih':
            data = 'xplor_data'
        #c.calc_name = 'self_calculation_%s' % str(time.time()).split('.')[0]
        random.seed()
        if session.get('DIR_CACHE', None) is None:
            session['DIR_CACHE'] = os.path.join(config['app_conf'][data], str(random.randint(100000000, 999999999)))
            session.save()
        elif data not in session.get('DIR_CACHE'):
            session['DIR_CACHE'] = os.path.join(config['app_conf'][data], str(random.randint(100000000, 999999999)))
            session.save()
        elif data in session.get('DIR_CACHE') and data == 'maxocc_data':
            session['DIR_CACHE'] = os.path.join(config['app_conf'][data], str(random.randint(100000000, 999999999)))
            session.save()
            
        if not os.path.isdir(session.get('DIR_CACHE')):
            os.makedirs(session.get('DIR_CACHE'))
        else:
            shutil.rmtree(session.get('DIR_CACHE'))
            os.makedirs(session.get('DIR_CACHE'))
        # Return a rendered template
        c.dir = session.get('DIR_CACHE')
        c.template_dir = config['app_conf']['template_dir']
        if session['PORTAL'] == 'amps-nmr':
            return render('/calculations/provaTabs.mako')
        elif session['PORTAL'] == 'maxocc':
            return render('/calculations/ranch.mako')
        elif session['PORTAL'] == 'xplor-nih':
            return render('/calculations/xplor_calc.mako')
    
    def maxocc(self, id=None):
        return render('/calculations/maxocc.mako')
    
    def project_self_creation(self, tipology):
        '''Create a project and a calculation without user intervention
        
        project name: new_project_[seconds since 1/1/1970]
        
        '''
        owner = Session.query(Users).get(session['REMOTE_USER'])
        project = u'new_project_%s' % str(time.time()).split('.')[0]
        
        # Create the directory structure on the filesystem
        pdir = os.path.join(config['app_conf']['working_dir'], owner.home)
        if os.path.isdir(pdir):
            pdir = os.path.join(pdir, project, tipology)
        try:
            os.makedirs(pdir)
            # Project creation
            p = Projects()
            p.name = project
            p.creation_date = datetime.now()
            p.owner = owner
            Session.add(p)
            Session.commit()
            return S_OK(p.id)
        except IOError, (errno, strerror):
            return S_ERROR( "I/O Error: %s %s" % (pname, strerror))
    
    
    def calculation_list(self, id=None):
        if id:
            c.project = Session.query(Projects).get(int(id))
            if c.project:
                return render('/calculations/calculation_list.mako')
                
            
    def calculation_download(self, idproj, namecalc):
        project = Session.query(Projects).get(int(idproj))
        tfilename = '%s_%s.tgz' % (project.name, namecalc)
        tfile = os.path.join(
                config['app_conf']['temp_dir'],
                tfilename)
        permanent_file = open(tfile, 'rb')
        data = permanent_file.read()
        permanent_file.close()

        response.content_type = guess_type(tfile)[0] or 'text/plain'
        response.headers['Content-Lenght'] = len(data)
        response.headers['Pragma'] = 'public'
        response.headers['Cache-Control'] = 'max-age=0'
        response.headers['Content-Disposition'] = 'attachment; filename="%s"'%(tfilename)
        return data
    
    def calculation_compress(self, idproj, namecalc):
        c = Session.query(Calculations).filter(and_(Calculations.name==namecalc, Calculations.project_id==idproj)).all()
        project = Session.query(Projects).get(int(idproj))
        owner = Session.query(Users).get(session['REMOTE_USER'])
        tfilename = '%s_%s.tgz' % (project.name, namecalc)
        tfile = os.path.join(
                config['app_conf']['temp_dir'],
                tfilename)

        to_add = os.path.join(
            config['app_conf']['working_dir'],
            owner.home,
            project.name,
            'amber/'+c[0].name
        )
        
        t = tarfile.open(tfile, 'w:gz')
        t.add(to_add, arcname=c[0].name, recursive=True)
        t.close()
    
    def restart(self):
        random.seed()
        if session.get('DIR_CACHE', None) is None:
            session['DIR_CACHE'] = os.path.join(config['app_conf']['amber_data'], str(random.randint(100000000, 999999999)))
            session.save()
            
        if not os.path.isdir(session.get('DIR_CACHE')):
            os.makedirs(session.get('DIR_CACHE'))
        else:
            shutil.rmtree(session.get('DIR_CACHE'))
            os.makedirs(session.get('DIR_CACHE'))
        
        return render('/calculations/restart.mako')
        
    def read_file(self):
        owner = Session.query(Users).get(session['REMOTE_USER'])
        path = request.POST.get("path")
        p = path.replace("Projects/", "")
        pfile = os.path.join(config['app_conf']['working_dir'], owner.home, p)
        if not os.path.exists(pfile):
            pfile = pfile.replace("amber", "amps-nmr")
        d = open(pfile, 'r')
        return d.readlines()

    def save_protocol(self):
        owner = Session.query(Users).get(session['REMOTE_USER'])
        filename = request.POST.get("filename")
        data_content = request.POST.get("data_content")
        descr_content = request.POST.get("descr_content")
        
        #controllo se ha gia una cartella personal
        if not os.path.exists(os.path.join(config['app_conf']['working_dir'], owner.home, "personal")):
            os.mkdir(os.path.join(config['app_conf']['working_dir'], owner.home, "personal"))
        i = 0
        flist = filename.split('.')
        fname = filename + '-1.step'
        if os.path.exists(os.path.join(config['app_conf']['working_dir'], owner.home, "personal", fname)):
            flist = fname.split('.')
            fname = flist[0].replace("-1", "(1)-1.") + flist[1];
            i = 1
            while os.path.exists(os.path.join(config['app_conf']['working_dir'], owner.home, "personal", fname)):
                i_s = str(i)
                iplus_s = str(i+1)
                fname = fname.replace("("+i_s+")", "("+iplus_s+")")
                i = i + 1
            filename = fname
        else:
            filename = filename + '-1.step'
        tfile = os.path.join(config['app_conf']['working_dir'], owner.home, "personal", filename)
        t = open(tfile, 'w')
        t.write(data_content)
        t.close()
        
        if descr_content != '':
            descrname = fname.replace("-1.step", ".dscr")
        dfile = os.path.join(config['app_conf']['working_dir'], owner.home, "personal", descrname)
        d = open(dfile, 'w')
        d.write(descr_content)
        d.close()
        
    def get_protList(self):
        owner = Session.query(Users).get(session['REMOTE_USER'])
        group = request.POST.get('group')
        if group == 'preset':
            dirpath = os.path.join(config['app_conf']['template_dir'], "restart")
        else:
            dirpath = os.path.join(config['app_conf']['working_dir'], owner.home, "personal")
        klist = sorted(os.listdir(dirpath))
        p = '-[1].step$'
        f = re.compile(p)
        t = [ i[:-7] for i in klist if f.search(i)]
        return ",".join(t)
    
    def isMultistep(self):
        group = request.POST.get('group')
        prot = request.POST.get('protocol')
        if group == 'preset':
            dirpath = os.path.join(config['app_conf']['template_dir'], "restart")
        else:
            owner = Session.query(Users).get(session['REMOTE_USER'])
            step = request.POST.get('step')
            dirpath = os.path.join(config['app_conf']['working_dir'], owner.home, "personal")
        dirlist = os.listdir(dirpath)
        p = '%s-[0-9].step$' % prot
        f = re.compile(p)
        t = [ i for i in range(len(dirlist)) if f.search(dirlist[i])]
        return str(len(t))
    
    def get_protContent(self):
        group = request.POST.get('group')
        prot = request.POST.get('protocol')
        step = request.POST.get('step')
        if group == 'preset':
            filepath = os.path.join(config['app_conf']['template_dir'], "restart", prot+'-'+step+".step")
            if step == 'dscr':
                filepath = os.path.join(config['app_conf']['template_dir'], "restart", prot+'.'+step)
        else:
            owner = Session.query(Users).get(session['REMOTE_USER'])
            
            if step == 'dscr':
                filepath = os.path.join(config['app_conf']['working_dir'], owner.home, "personal", prot+'.'+step)
            else:
                filepath = os.path.join(config['app_conf']['working_dir'], owner.home, "personal", prot+'-'+step+".step")
        dfile = open(filepath,"r")
        return dfile.readlines()
        
    def __select_job(self, j, jstat):
        #  'R': 'Running',
        #  'S': 'Scheduled',
        #  'F': 'Finished',
        #  'C': 'Cancelled',
        #  'A': 'Aborted',
        #  'L': 'Cleared',
        #  'E': 'Finished/Retrieved'
        _STATUS = ['R', 'S', 'F', 'C', 'A', 'L', 'E']
        
        owner = Session.query(Users).get(session['REMOTE_USER'])
        j_ret = []
        if jstat in _STATUS:
            for item in j:
                if item.status == jstat:
                    if jstat == 'E':
                        if item.dir_name != None:
                            p_list = item.dir_name.split("/")
                            p_tmp = p_list[-1].replace("input_", "output_")
                            p_tmp_dir = p_list[-2].replace("input", "output")
                            pout = '/'.join(p_list[:-2])
                            pout = pout + '/' + p_tmp_dir + '/' + p_tmp
                            pout = pout.replace("NMA", "proj2L0A")
                            pout = pout.replace("Demo","Refinement")
                            if os.path.exists(os.path.join(config['app_conf']['working_dir'], owner.home, pout, "prmtop")):
                                s = 'sander'
                                p = '%s[0-9].crd$' % s
                                f = re.compile(p)
                                outlist = os.listdir(pout)
                                t = [ i for i in outlist if f.search(i)]
                                if t:
                                    j_ret.append(item)
                    else:
                        j_ret.append(item)
                    
        return j_ret
        
    def get_jobList(self):
        owner = Session.query(Users).get(session['REMOTE_USER'])
        proj = request.POST.get('proj')
        calc = request.POST.get('calc')
        project = Session.query(Projects).filter(and_(Projects.name==proj, Projects.owner_id==session['REMOTE_USER'], Projects.removed == False)).all()
        c = Session.query(Calculations).filter(and_(Calculations.name==calc, Calculations.project_id==project[0].id, Calculations.removed == False)).all()
        if c:
            job = Session.query(Jobs).filter(and_(Jobs.calculation_id == c[0].id, Calculations.removed == False)).all()
            if job:
                jobs = self.__select_job(job, 'E')
                if jobs:
                    if jobs[0].dir_name != None:
                        print jobs[0].dir_name
                        bname = os.path.basename(jobs[0].dir_name)
                        str = bname.replace("input", "output")
                        for j in jobs[1:]:
                            bname = os.path.basename(j.dir_name)
                            outdir = bname.replace("input", "output")
                            str = str +',%s' %outdir
                        return str
                    else:
                        str = jobs[0].guid
                        for j in jobs[1:]:
                            str = str +',%s' %j.guid
                        return str
        return ''
    
    def check_calc_name(self):
        proj = request.POST.get("proj_name")
        calc = request.POST.get("calc_name")
        p = Session.query(Projects).filter(and_(Projects.name==proj, Projects.owner_id==session['REMOTE_USER'], Projects.removed == False)).all()
        c = Session.query(Calculations).filter(and_(Calculations.name==calc, Calculations.project_id==p[0].id, Calculations.removed == False)).all()
        if c:
            return 'already used!' 
            
        else:
            return 'Ok'
        
    def restart_submit(self):
        
        restart = etree.Element("restart")
        #dircache = etree.SubElement(restart, "dircache")
        #dircache.text = session.get('DIR_CACHE')
        project = etree.SubElement(restart, "project")
        calculation = etree.SubElement(restart, "calculation")
        job = etree.SubElement(restart, "job")
        input = etree.SubElement(restart, "input")
        topology = etree.SubElement(input, "topology")
        coordinates = etree.SubElement(input, "coordinates")
        newcalculation  = etree.SubElement(restart, "newcalculation")
        newcalculation.text = request.POST.get('name-restart')

        session["usegpu"] = True
        session["useclo"] = False
        session.save()

        owner = Session.query(Users).get(session['REMOTE_USER'])
        proj = request.POST.get('proj_list')
        project.text = proj
        calc = request.POST.get('calc_list')
        calculation.text = calc
        j = request.POST.get('job_list')
        job.text = j
        top = request.POST.get('top_input')
        coord = request.POST.get('coord_input')
        if top != '' and coord != '':
            top_name = self.__uploadFile(top)
            topology.text = top_name
            coord_name = self.__uploadFile(coord)
            coordinates.text = coord_name
            noe_dih = request.POST.get('noe_dih')
            rdc_ = request.POST.get('rdc')
            pcs_ = request.POST.get('pcs')
            if noe_input != '':
                noe = etree.SubElement(input, "noe")
                noe_name = self.__uploadFile(noe_input, "allNOE_allDIH.in")
                noe.text = noe_name
            if rdc_input != '':
                rdc = etree.SubElement(input, "rdc")
                rdc_name = self.__uploadFile(rdc_, 'allRDC.in')
                rdc.text = rdc_name
            if pcs_input != '':
                pcs = etree.SubElement(input, "pcs")
                pcs_name = self.__uploadFile(pcs_, 'PCS.in')
                pcs.text = pcs_name
        else:
            #devo prendermi i file dalla cartella di output di un calcolo
            #ma prima devo controllare se si tratta di un calcolo vecchio o nuovo
            if j.startswith('https://'):
                jabs = j.replace('https://', '')
                jdirname = 'root_%s' %jabs.split("/")[1]
            else:
                jdirname = j
            filepath = os.path.join(config['app_conf']['working_dir'], owner.home, proj, 'amber', calc, 'output', jdirname)
            prmtopfp = os.path.join(filepath, "prmtop")
            if (os.path.exists(prmtopfp)):
                topology.text = prmtopfp
            s = 'sander'
            p = '%s[0-9].crd$' % s
            f = re.compile(p)
            sanderlist = os.listdir(filepath)
            t = [ i for i in sanderlist if f.search(i)]
            t_sorted = sorted(t)
            prmcrdfp = os.path.join(filepath, t_sorted[-1])
            if (os.path.exists(prmcrdfp)):
                coordinates.text = prmcrdfp
            
            
            noefp = os.path.join(filepath, "allNOE_allDIH.in")
            if (os.path.exists(noefp)):
                noe = etree.SubElement(input, "noe")
                noe.text = noefp
            rdcfp =  os.path.join(filepath, "allRDC.in")
            if (os.path.exists(rdcfp)):
                rdc = etree.SubElement(input, "rdc")
                rdc.text = rdcfp
            pcsfp =  os.path.join(filepath, "PCS.in")
            if (os.path.exists(pcsfp)):
                pcs = etree.SubElement(input, "pcs")
                pcs.text = pcsfp
        
        s = 'chk_step'
        p = '%s[1-9]$' % s
        f = re.compile(p)
        params = (request.params).keys()
        t = [ i.split("_")[1] for i in params if f.search(i)]
        #sander.text = str(len(t))
        if not len(t):
            sander = request.POST.get("sander")
            fname = 'sander0.in'
            rfname = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), fname)
            s = etree.SubElement(input, "sander")
            s.text = rfname
            ofile = open(rfname, 'w')
            ofile.writelines(sander + "\n")
            ofile.close()
        else:
            for j in range(len(t)):
                sander = request.POST.get(t[j])
                fname = 'sander%d.in' %j
                rfname = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), fname)
                s = etree.SubElement(input, "sander")
                s.text = rfname
                ofile = open(rfname, 'w')
                ofile.writelines(sander + "\n")
                ofile.close()
        print etree.tostring(restart, pretty_print=True)
        self.job_prepare_restart(restart)
        
    def job_prepare_restart(self,xmlin):
        
        '''Prepare a job for submission 
        steps:
        a) check for the calculation existance
        b) directory creation
        c) database new calculation entry creation
        d) put data into new directory
        e) start job
        '''
        #grid_req = """( other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-long" || other.GlueCEUniqueID == "ce01.dur.scotgrid.ac.uk:2119/jobmanager-lcgpbs-q6h" );"""
        #grid_req = """( other.GlueCEUniqueID == "ce-enmr.chem.uu.nl:2119/jobmanager-lcgpbs-long" || other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:2119/jobmanager-lcgpbs-long" );"""
        #grid_req = """other.GlueCEPolicyMaxCPUTime > 2000 && (other.GlueCEInfoHostName == "deimos.htc.biggrid.nl" || other.GlueCEInfoHostName == "trekker.nikhef.nl" ||  other.GlueCEInfoHostName == "pbs-enmr.cerm.unifi.it" || other.GlueCEInfoHostName == "gazon.nikhef.nl" || other.GlueCEInfoHostName == "ce-enmr.chemie.uni-frankfurt.de" || other.GlueCEInfoHostName == "ce-enmr.chem.uu.nl" );"""
        #grid_req = """other.GlueCEPolicyMaxCPUTime > 2000 && (other.GlueCEInfoHostName == "deimos.htc.biggrid.nl" || other.GlueCEInfoHostName == "trekker.nikhef.nl"  || other.GlueCEInfoHostName == "gazon.nikhef.nl" || other.GlueCEInfoHostName == "ce-enmr.chemie.uni-frankfurt.de" || other.GlueCEInfoHostName == "ce-enmr.chem.uu.nl" );"""
        
        #prj_id = request.POST.get('prj_id')
        sander = []
        rdc_file = ""
        pcs_file = ""
        noe_dih_file = ""
        
        for elt in xmlin.getiterator():
            if elt.tag == "project":
                project = elt.text

            if elt.tag == "newcalculation":
                calc_name = elt.text
                
            if elt.tag == "sander":
                sander.append(elt.text)
                
            if elt.tag == "coordinates":
                coordinates_file = elt.text
                
            if elt.tag == "topology":
                topology_file = elt.text
            
            if elt.tag == "rdc":
                rdc_file = elt.text                
                
            if elt.tag == "pcs":
                pcs_file = elt.text

            if elt.tag == "noe_dih":
                noe_dih_file = elt.text
        
        
        prj_id = Session.query(Projects).filter(and_(Projects.name==project, Projects.owner_id==session['REMOTE_USER'], Projects.removed == False)).all()[0].id
        tipology = "amps-nmr"
        
        numStep = len(sander)
        #numStep = request.POST.get('step')
        
        print "step %s" %numStep
        list_input_sander = list()
        for i in sander:
            list_input_sander.append(os.path.basename(i))
        print "###############List of Amber restart .in files###############"
        print list_input_sander
        print "numStep"
        print numStep
        print "#####################################################"
        
        calc_name = calc_name.replace(' ', '_')
        owner = Session.query(Users).get(session['REMOTE_USER'])
        project = Session.query(Projects).get(int(prj_id))
        calc_type = Session.query(CalculationTipology).filter(CalculationTipology.tipology == tipology).first()
        
        #cname = Session.query(Calculations).filter(and_(Calculations.name==calc_name, Calculations.project_id==int(prj_id))).first()
        #
        ## Check the existance of the calculation
        #if cname:
        #    h.flash.set_message('Calculation name already exists', 'Error')
        #    h.redirect('/calculations/%s' % tipology)
        
        # Directory creation
       
        num_m = 1
        pdir = os.path.join(config['app_conf']['working_dir'], owner.home, project.name, "amber", calc_name, "input", 'input_1')
        
        
        
        print pdir
        try:
            os.makedirs(pdir)
        except IOError, (errno, strerror):
            h.flash.set_message('An error occurred during calculation creation.', 'Error')
            h.redirect('/calculations/%s' % tipology)
        #move
        shutil.copy(coordinates_file, os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"prmcrd"))
        shutil.copy(topology_file, os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"prmtop"))
        if len(noe_dih_file) > 0:
            shutil.copy(noe_dih_file, os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in"))
        if len(rdc_file) > 0:
            shutil.copy(rdc_file, os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allRDC.in"))
        if len(pcs_file) > 0:
            shutil.copy(pcs_file, os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"PCS.in"))

        #     jdl = """
        # Executable = "run_amber.sh";
        # StdOutput = "std.out";
        # StdError = "std.err";
        # VirtualOrganisation="enmr.eu";
        # InputSandbox = {"%s/in.tgz","%s/run_amber.sh"};
        # OutputSandbox = {"std.out", "std.err","pro.tgz"};
        # Requirements = %s
        # """ % (pdir, pdir, app_globals.grid_req)
        #
        # abs_fullpath = os.path.join(pdir, "amber.jdl")
                
        jdl = """[
executable = "run_amber.sh";
stdOutput = "std.out";
stdError = "std.err";
outputsandboxbasedesturi = "gsiftp://localhost";
inputsandbox = {"%s/in.tgz","%s/run_amber.sh"};
outputsandbox = {"std.out", "std.err","pro.tgz"};
]
""" %(pdir, pdir)

        abs_fullpath = os.path.join(pdir, "amber.jdl")
        open(abs_fullpath,"w").write(jdl)

        run_amber = """
#!/bin/bash
export CUDA_HOME=/usr/local/cuda-5.5
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64
export AMBERHOME=/nfs_export/gpucluster/NMR_GPU/bin/amber14GPU_NOE/
PATH=/usr/lib64/openmpi/bin:${CUDA_HOME}/bin:${PATH}
export PATH
#cd /nfs_export/gpucluster/GPU_Validation_Test
#How many GPUs in node

echo $AMBERHOME
nvidia-smi

DIRAE=$AMBERHOME/bin/


tar xvfz in.tgz


#AMBER_COMMAND

#$DIRAE/pmemd.cuda -O -i sander.in -o sander.out -p prmtop -c prmcrd -r prm_out.crd
#$DIRAE/ambpdb -p prmtop < prm_out.crd > amber_final.pdb

tar cvfz pro.tgz ./* --exclude in.tgz --exclude run_amber.sh --exclude gettensor.pl

"""




#         run_amber = """
# #!/bin/bash
# /bin/uname -a | /bin/grep 'x86_64' > /dev/null && ARCH='64' || ARCH='32'
#
# AMBERHOME=$VO_ENMR_EU_SW_DIR/CIRMMP/amber/11/$ARCH
#
# DIRAE=$AMBERHOME/exe/
#
# tar xvfz in.tgz
#
#
# #AMBER_COMMAND
#
#
# #$DIRAE/sander -O -i sander.in -o sander.out -p prmtop -c prmcrd -r prm_out.crd
# #$DIRAE/ambpdb -p prmtop < prm_out.crd > amber_final.pdb
#
# tar cvfz pro.tgz ./*
#
# """
        abs_fullpath = os.path.join(pdir, "run_amber.sh")
        run_amber_post = []
        for a in run_amber.split("\n"):
            run_amber_post.append(a + "\n")
            if "#AMBER_COMMAND" in a:
                ct = 0
                for i in list_input_sander:
                    ct = ct + 1
                    if ct == 1:
                        run_amber_post.append("$DIRAE/pmemd.cuda -O -i %s -o %s -p prmtop -c prmcrd -r %s -ref prmcrd -x prod.crd \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-1) + ".crd"  ))
                        run_amber_post.append("$DIRAE/ambpdb -p prmtop < %s > %s \n" %(i[:-4] + str(ct-1) + ".crd", "amber_final" + str(ct-1) + ".pdb"))
                    else:
                        run_amber_post.append("$DIRAE/pmemd.cuda -O -i %s -o %s -p prmtop -c %s -r %s -ref  %s \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-2) + ".crd", i[:-4] + str(ct-1) + ".crd",i[:-4] + str(ct-2) + ".crd" ))
                        run_amber_post.append("$DIRAE/ambpdb -p prmtop < %s > %s \n" %(i[:-4] + str(ct-1) + ".crd", "amber_final" + str(ct-1) + ".pdb"))
                    
                    
        open(abs_fullpath,"w").writelines(run_amber_post)
      
        tar = tarfile.open(os.path.join(pdir,"in.tgz"),"w:gz")
        tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"prmcrd"), arcname="prmcrd")
        tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"prmtop"), arcname="prmtop")
        if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in")):
            tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in"),arcname="allNOE_allDIH.in")
        if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"PCS.in")):
            tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"PCS.in"),arcname="PCS.in")
        if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allRDC.in")):
            tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allRDC.in"),arcname="allRDC.in")
        for i in list_input_sander:
            tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), i), arcname=i)
        tar.close()
        
        # New database entry creation
        new_calc = Calculations()
        new_calc.name = calc_name
        new_calc.project = project
        new_calc.calc_type = calc_type
        new_calc.creation_date = datetime.now()
        new_calc.jobs_to_submit = num_m
        Session.add(new_calc)
        Session.commit()
        
        
        # Submit job
        id = '%s_%s_0' % (new_calc.id, prj_id)
        h.redirect('/jobs/job_submit/%s' % id)

            
    def __uploadFile(self, file_name, newname=None):
        if newname == None:
            f = file_name.filename.split('\\')
            rfname = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), f[len(f)-1])
        else:
            rfname = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), newname)
        
        permanent_file = open(rfname, 'wb')
        shutil.copyfileobj(file_name.file, permanent_file)
        file_name.file.close()
        permanent_file.close()
        return rfname
