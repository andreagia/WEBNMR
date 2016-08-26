import os, subprocess, shutil, tarfile, fileinput, random, pickle
from pprint import pprint
from distutils.dir_util import copy_tree
from pylons import request, response, session, tmpl_context as c
from lxml import etree
from pylons import config, app_globals
from datetime import datetime
import time
from sqlalchemy.sql import and_
from sqlalchemy.sql import or_
from webenmr.lib.base import *
from webenmr.lib.return_values import S_OK, S_ERROR
from webenmr.lib.Subprocess import shellCall
from webenmr.lib.BaseSecurity import BaseSecurity
from webenmr.model import  Users, Projects, Calculations, CalculationTipology, Jobs
from webenmr.lib import Certificates
import re

class JobManagementSystem(BaseSecurity):
    
    _xplorMinGroup = 10
    
    def __init__(self, wd, xmlcalc, app ):
        BaseSecurity.__init__(self)
        os.environ['X509_USER_PROXY'] = session['voms_proxy_file']
        os.environ['X509_USER_CERT'] = session['voms_proxy_file']
        os.environ['X509_USER_KEY'] = session['voms_proxy_file']
        if session['PORTAL'] == 'amps-nmr':
            attribute = "/enmr.eu/amber"
        elif session['PORTAL'] == 'xplor-nih':
            attribute = "/enmr.eu/xplornih"
        else:
            attribute = ""
        ret = Certificates.proxy_initialize(attribute)
        os.environ['X509_USER_PROXY'] = session['voms_proxy_file']
        os.environ['X509_USER_CERT'] = session['voms_proxy_file']
        os.environ['X509_USER_KEY'] = session['voms_proxy_file']
        print "######VOMSPROXY INI #############"
        if ret['OK']:
            #print "VOMS_PROXY ", session['voms_proxy']
            #print ret['Value']
            print "VOMSPROXY OK"
        else:
            print 'voms-proxy-init problem: %s' % ret['Message']
        print "######VOMSPROXY END #############"
        print "INI ################CERT PROXY############"
        #print session['voms_proxy_file']
        print "END ################CERT PROXY############"
        self.xml = xmlcalc
        self._wd = wd
        self._user = session["REMOTE_USER"]
        self._projName = xmlcalc.find("project").get("name")
        #print self._projName
        self._calcName = xmlcalc.find("calculation").get("name")
        self._app = app
        self._optJDL = """        
Executable = "run.sh";
StdOutput = "std.out";
StdError = "std.err";
VirtualOrganisation="enmr.eu";
InputSandbox = {"%s/in.tgz","%s/run.sh"};
OutputSandbox = {"std.out", "std.err","pro.tgz"};
Requirements = %s
    """
        self._userHome = os.path.join(config['app_conf']['working_dir'],Session.query(Users).get(self._user).home)
    
    def checkGRID(self):
        dd = """( other.GlueCEUniqueID == "deimos.htc.biggrid.nl:2119/jobmanager-pbs-medium" || other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-verylong");"""
        if os.path.exists("/opt/checkGRID/pickle.pck"):
            file_pickle = open("/opt/checkGRID/pickle.pck", "r") # read mode
            job = pickle.load(file_pickle)
        else:
            print "NO JOBS INFORMATIONS "
            return dd
        
        #pprint(job)
        queue_time = 1441
        ce_sub = []

        for check_ce in job.keys():
            if job[check_ce].has_key("status"):
                if job[check_ce]["status"] == "OK":
                    if job[check_ce].has_key("VOMaxCPUTime"):
                        time = job[check_ce]["VOMaxCPUTime"]
                        if time.isdigit():
                            if int(job[check_ce]["VOMaxCPUTime"]) > queue_time and int(job[check_ce]["VOMaxCPUTime"]) < 9999999999 :
                                ce_sub.append(check_ce)
        #print ce_sub
        if len(ce_sub) > 0:
            list_cet = "("
            for i in ce_sub:
                list_cet = list_cet + ' other.GlueCEUniqueID == "%s" ||' %i
                list_ce = list_cet[:-2] + ")"
        else:
            list_ce = dd
        return list_ce
    
    def setupJobs(self, nrojobs):
        jdl_list = self.__fillCalc(nrojobs)
        newcalc = self.buildCalculationDB(nrojobs)
        self.submitOnGrid(newcalc,jdl_list)
        return True
    
    def createExecFile(self):
        print ""
            
    #def createJdlFile(self, path=None, opt=None):
    #    #se vogliamo mettere il file gia nella cartella del calcolo, allora va creato prima il calcolo e poi il jdl
    #    if path:
    #        work_dir = path
    #    else:
    #        work_dir = self._wd
    #    jdlfilehandler = open(os.path.join(work_dir, "run.jdl"), "w")
    #    #aggiorno il dizionario delle opzioni del JDL
    #    if opt:
    #        for knew in opt.keys():
    #            self._optJDL[knew] = opt[knew]
    #    #riempio il file JDL
    #    for k in self._optJDL.keys():
    #        jdlfilehandler.write(k+" = "+ self._optJDL[k])
    
    def buildCalculationDB(self, nrojobs):
        new_calc = Calculations()
        new_calc.name = self._calcName
        new_calc.project = Session.query(Projects).filter(and_(Projects.owner_id == session['REMOTE_USER'], Projects.removed == False, Projects.name == self._projName)).first()
        new_calc.calc_type = Session.query(CalculationTipology).filter(CalculationTipology.tipology == self._app).first()
        new_calc.creation_date = datetime.now()
        new_calc.jobs_to_submit = nrojobs 
        Session.add(new_calc)
        Session.commit()
        return new_calc
    
    def __create_tar(self):
        tar = tarfile.open(os.path.join(m_dir,"in.tgz"),"w:gz")
    
    def __fillCalc(self, nrojobs):
        """
        crea le directories di input e le riempie con i relativi file
        """
        jdl_list = []
        if not os.path.exists(os.path.join(self._userHome, self._projName, session["PORTAL"])):
            os.mkdir(os.path.join(self._userHome, self._projName, session["PORTAL"]))
        os.mkdir(os.path.join(self._userHome, self._projName, session["PORTAL"],self._calcName))
        nroGroup = int(nrojobs)/self._xplorMinGroup
        os.mkdir(os.path.join(self._userHome, self._projName, session['PORTAL'], self._calcName, "input"))
        for i in range(nroGroup):
            dir_n = os.path.join(self._userHome, self._projName, session['PORTAL'], self._calcName, "input", "input_%d" %(i+1))
            os.mkdir(dir_n)
            copy_tree(self._wd, dir_n)
            
            file_seed = open(os.path.join(dir_n, "xplorPM.inp"),"r").readlines()
            file_seed_out = []
            for line in file_seed:
                if "!##seed" in line:
                    line = line.replace("!##seed","set seed = %d end \n" %int(random.random()*10000000) )
                file_seed_out.append(line)
            open(os.path.join(dir_n, "xplorPM.inp"),"w").writelines(file_seed_out)
            
            tar = tarfile.open(os.path.join(dir_n,"in.tgz"),"w:gz")
            for it in os.listdir(dir_n):
                if it != "in.tgz":
                    tar.add(os.path.join(dir_n, it), arcname=it)
            tar.close()
            for it in os.listdir(dir_n):
                if it != "in.tgz":
                    os.unlink(os.path.join(dir_n,it))
            shutil.copy(os.path.join(config['app_conf']['xplor_templ'],"run.sh"),dir_n)
            file = open(os.path.join(dir_n,"run_xplor.jdl"),"w")
            checkgridRet = self.checkGRID()
            checkgridRet = ' other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-short" '
            file.write(self._optJDL %( dir_n, dir_n, checkgridRet))
            file.close()
            jdl_list.append(os.path.join(dir_n,"run_xplor.jdl"))
        return jdl_list
        #bisogna mettere i file di input nelle relative cartelle
        
    def submitOnGrid(self, calc, jdllist):
        if self._app == 'xplor-nih':
            totjobs = len(jdllist)
            for jdl_idx, jdl_path in enumerate(jdllist):
                wdir = os.path.dirname(jdl_path)
                jdl_name = os.path.basename(jdl_path)
                
                serror = True
                count_retry = 0
                print "##### submit JDL ####"
                print wdir, jdl_name
                while serror:
                    time.sleep(count_retry)
                    count_retry = count_retry + 1
                    status, output, error = self.submit(wdir, jdl_name)
                    
                    print 'status ', status
                    print 'output ', output
                    print 'error ', error
                    
                    if output:
                        output = '%s' % output.strip()
                    
                    if len(error) > 0:
                        serror = True
                        print "######ERROR IN SUBMISSION --- RETRY #############"
                        print "NUMBER %d" %count_retry
                        print "##### ######"
                    elif count_retry == 20:
                        serror = True
                        print "#### LIMIT of 20 resumittion #####"
                    else:
                        serror = False
                        print "## OK"
                    
                if error:
                    msg = 'Unable to start job %s' % (jdl_idx+1)
                    h.flash.set_message(msg, 'error')
                    id = "%d_%s_0" %(calc.id, 1)
                    h.redirect('/jobs/job_list/%s' % id)
                try:    
                    match = re.search('.*(https:\/\/\S+:9000\/[0-9A-Za-z_\.\-]+)', output)
                    
                    #calc = Session.query(Calculations).get(int(calc_id))
                    j = Jobs()
                    j.calculation = calc
                    j.guid = u'%s' % match.group(1)
                    j.start_date = datetime.now()
                    j.dir_name = wdir
                except AttributeError:
                    j.guid = u'No guid'
                    j.status = u'A'
                    j.log = u'%s' % error
                    msg = 'Job %s aborted' %(jdl_idx+1)
                    
                if match:
                    j.status = u'S'
                    msg = '%s job(s) successfully started' %(totjobs)
                    h.flash.set_message(msg, 'success')
                    #h.redirect('/jobs/job_list/%s' % id)
                else:
                    j.guid = u'No guid'
                    j.status = u'A'
                    j.log = u'%s' % error
                    msg = 'Job %s aborted' %(jdl_idx+1)
                    h.flash.set_message(msg, 'error')
                        
                Session.add(j)
                Session.commit()
                
            h.redirect('/jobs/show/all')
        else:
            #verranno man mano gestiti sia amber, maxocc e compagnia bella
            print "non si tratta di xplor-nih"
    
    
    def submit(self, wdir, jdl):
        '''Submit a job to the GRID
        
        input:
        wdir = working directory of the job
        jdl = jdl file
        
        return the result of the submission'''
        print "#### USING JobManagmentSytem #####"
        cmd = 'cd %s; echo $X509_USER_PROXY; /opt/glite/bin/glite-wms-job-submit -a %s' % (wdir, jdl)
        return self.exec_cmd(cmd)
        
    def status(self, guid):
        '''Check the job status
        
        input:
        guid = the job identifier
        
        return the status of the job'''
        
        #cmd = '/usr/bin/python /opt/glite/bin/glite-wms-job-status %s' % guid
        cmd = '/opt/glite/bin/glite-wms-job-status %s' % guid
        return self.exec_cmd(cmd)
        
    def kill(self, guid):
        
        cmd = '/opt/glite/bin/glite-wms-job-cancel --noint %s' % guid
        return self.exec_cmd(cmd)
        
    def retrieve(self, guid, outdir):
        cmd = '/opt/glite/bin/glite-wms-job-output --dir %s --nosubdir --noint %s' % (outdir, guid)
        print #########################"
        print "Comando di retrieve"
        print cmd
        print "########################"
        return self.exec_cmd(cmd)
    
    def exec_cmd(self, cmd):
        cmdEnv = self._getExternalCmdEnvironment()
        result = shellCall( self._secCmdTimeout, cmd, env = cmdEnv )
        return result['Value']