import logging
import shutil
import os, sys, subprocess
import re
import tarfile
import random
from datetime import datetime
from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from webenmr.model import Projects,Calculations, Jobs, CalculationTipology, Users
from webenmr.lib.base import *
from webenmr.lib.Subprocess import shellCall
from webenmr.model.meta import Session
from webenmr.lib.base import BaseController, render
from webenmr.lib.BaseSecurity import BaseSecurity
from webenmr.lib import Certificates


log = logging.getLogger(__name__)


class JobsProcessing(BaseSecurity):
    
    def __init__(self):
        BaseSecurity.__init__(self)
        if session['PORTAL'] == 'amps-nmr':
            attribute = "/enmr.eu/amber"
        elif session['PORTAL'] == 'xplor-nih':
            attribute = "/enmr.eu/xplornih"
        else:
            attribute = ""
        ret = Certificates.proxy_initialize(attribute)
        #ret = Certificates.proxy_initialize()
        print "######VOMSPROXY INI #############"
        if ret['OK']:
            #print "VOMS_PROXY ", session['voms_proxy']
            #print ret['Value']
            print "OK"
        else:
            print 'voms-proxy-init problem: %s' % ret['Message']
        print "######VOMSPROXY END #############"
        
        os.environ['X509_USER_PROXY'] = session['voms_proxy_file']
        os.environ['X509_USER_CERT'] = session['voms_proxy_file']
        os.environ['X509_USER_KEY'] = session['voms_proxy_file']
       
    # def submit(self, wdir, jdl):
    #     '''Submit a job to the GRID
    #     
    #     input:
    #     wdir = working directory of the job
    #     jdl = jdl file
    #     
    #     return the result of the submission'''
    #     
    #     cmd = 'echo $X509_USER_CERT;cd %s;/opt/glite/bin/glite-wms-job-submit -a %s' % (wdir, jdl)
    #     return self.exec_cmd(cmd)
    def submit(self, wdir, jdl):
        '''Submit a job to the GRID

        input:
        wdir = working directory of the job
        jdl = jdl file

        return the result of the submission'''
        certx = session['voms_proxy_file']
        cmd = 'ssh webenmr@192.168.0.10 "cat %s > %s1 ; chmod 600 %s1; export X509_USER_PROXY=%s1 ;cd %s ;/usr/bin/glite-wms-job-submit -a %s"' %(certx, certx, certx, certx ,wdir, jdl)
        print cmd
        
        prova = 0
        while prova == 0:
            status, output, error =self.exec_cmd(cmd)
            #child = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell= True,env=sep)
            #result_out = child.communicate()[0]
            print "PPPPPPPPPPPPPPPPPPPPPPPPPPP"
            print output
            print "------- error-------------"
            print error
            print "PPPPPPPPPPPPPPPPPPPPPPPPPPP"
            if ("SSL_connect error" in error) or ("SSL_connect error" in output):
                prova = 0
            else:
                prova =1

        
        return status, output, error
        #return self.exec_cmd(cmd)
        
    # def status(self, guid):
    #     '''Check the job status
    #     
    #     input:
    #     guid = the job identifier
    #     
    #     return the status of the job'''
    #     
    #     cmd = '/usr/bin/python /opt/glite/bin/glite-wms-job-status %s' % guid
    #     return self.exec_cmd(cmd)
    def status(self, guid):
        '''Check the job status

        input:
        guid = the job identifier

        return the status of the job'''
        certx = session['voms_proxy_file']

        #cmd = 'set;/usr/bin/glite-wms-job-status -c /opt/glite/etc/enmr.eu/glite_wms.conf %s' % str(guid)
        cmd = 'ssh webenmr@192.168.0.10 "cat %s > %s1 ; chmod 600 %s1; export X509_USER_PROXY=%s1 ;glite-wms-job-status %s"' %(certx, certx, certx, certx, str(guid))
        #cmd='voms-proxy-info'
        #cmd = 'grid-cert-diagnostics -p'
        print "***** jobs.py exec_cmd  INI ******"
        print cmd
        print "***** jobs.py exec_cmd  END ******"
        print "CMD1"
        #cmd1=['/usr/bin/glite-wms-job-status','-c','/opt/glite/etc/enmr.eu/glite_wms.conf']

        #cmd1.append(str(guid))

        print "CMD1"
       
        prova = 0
        while prova == 0:
            status, output, error =self.exec_cmd(cmd)
            #child = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell= True,env=sep)
            #result_out = child.communicate()[0]
            print "PPPPPPPPPPPPPPPPPPPPPPPPPPP"
            print output
            print "------- error-------------"
            print error
            print "PPPPPPPPPPPPPPPPPPPPPPPPPPP"
            if ("GSSAPI" in error) or ("GSSAPI" in output):
                prova = 0
            else:
                prova =1

        
        return status, output, error
        
    # def kill(self, guid):
    #     
    #     cmd = '/opt/glite/bin/glite-wms-job-cancel --noint %s' % guid
    #     return self.exec_cmd(cmd)
    def kill(self, guid):
        certx = session['voms_proxy_file']

        cmd = 'ssh webenmr@192.168.0.10 "cat %s > %s1 ; chmod 600 %s1; export X509_USER_PROXY=%s1 ;/usr/bin/glite-wms-job-cancel --noint %s"' %(certx, certx, certx, certx, guid)
        prova = 0
        while prova == 0:
            status, output, error =self.exec_cmd(cmd)
            #child = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell= True,env=sep)
            #result_out = child.communicate()[0]
            print "PPPPPPPPPPPPPPPPPPPPPPPPPPP"
            print output
            print "------- error-------------"
            print error
            print "PPPPPPPPPPPPPPPPPPPPPPPPPPP"
            if ("GSS" in error) or ("GSS" in output):
                prova = 0
            else:
                prova =1
        return status, output, error
        
    # def retrieve(self, guid, outdir):
    #     cmd = '/opt/glite/bin/glite-wms-job-output --dir %s --nosubdir --noint %s' % (outdir, guid)
    #     print #########################"
    #     print "Coamando di retrive"
    #     print cmd
    #     print "########################"
    #     return self.exec_cmd(cmd)
    
    def retrieve(self, guid, outdir):
        certx = session['voms_proxy_file']
        cmd = """ssh webenmr@192.168.0.10 << EOF
umask 002
cat %s > %s1
chmod 600 %s1
export X509_USER_PROXY=%s1
/usr/bin/glite-wms-job-output --dir %s --nosubdir --noint %s
cd %s
chown -R webenmr.apache *
chmod -R 660 *
EOF
""" % (certx, certx, certx, certx, outdir, guid,outdir)
        print #########################"
        print "Coamando di retrive"
        print cmd
        print "########################"
        prova = 0
        while prova == 0:
            status, output, error =self.exec_cmd(cmd)

            print "PPPPPPPPPPPP RETRIVE  PPPPPPPPPPPPPPP"
            print output
            print "---------Error----------------"
            print type(error)
            print error
            print "PPPPPPPPPPPPPPPPPPPPPPPPPPP"
            if "GSS" in error:
                prova = 0
            else:
                prova =1

        return status, output, error
    
    def exec_cmd(self, cmd):
        cmdEnv = self._getExternalCmdEnvironment()
        result = shellCall( self._secCmdTimeout, cmd, env = cmdEnv )
        return result['Value']

class RanchController(BaseController):
    
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
    
    
    def index(self):
        # Return a rendered template
        #return render('/ranch.mako')
        # or, return a string
        return 'Hello World'

    def saveFile(self, fname, where, name=None):
        if name:
            namef = name
        else:
            namef = fname.filename.split('\\')[0]
        #f = fname.filename.split('\\')
        rfname = os.path.join(where, namef)
        permanent_file = open(rfname, 'wb')
        shutil.copyfileobj(fname.file, permanent_file)
        fname.file.close()
        permanent_file.close()
        
    def ranch_job_submit(self, proj_id, calc_name, jdl):
        '''Submit a job in GRID'''
        project = Session.query(Projects).get(int(proj_id))
        calc_type = Session.query(CalculationTipology).filter(CalculationTipology.tipology == 'ranch').first()
        # New database entry creation
        new_calc = Calculations()
        new_calc.name = calc_name
        new_calc.project = project
        new_calc.calc_type = calc_type
        new_calc.creation_date = datetime.now()
        new_calc.jobs_to_submit = 1
        Session.add(new_calc)
        Session.commit()
        
        w_dir = os.path.join(config['app_conf']['working_dir'],
                        project.owner.home,
                        project.name,
                        session['PORTAL'],
                        calc_name)
           
            
        jP = JobsProcessing()
        #jdl = 'ranch_pre.jdl'
            
        wdir = os.path.join(w_dir, 'input', 'input_1')
                
        status, output, error = jP.submit(os.path.dirname(jdl), os.path.basename(jdl))
                
        if output:
            output = '%s' % output.strip()
                
        print 'status ', status
        print 'output ', output
        print 'error ', error
                
        if error:
            msg = 'Unable to submit job, some network errors occurred. Please, try to re-submit later. '
            h.flash.set_message(msg, 'error') 
            h.redirect('/users/index')
        try:    
            match = re.search('.*(https:\/\/\S+:9000\/[0-9A-Za-z_\.\-]+)', output)
            j = Jobs()
            j.calculation = new_calc
            j.guid = u'%s' % match.group(1)
            j.start_date = datetime.now()
            j.dir_name = wdir
        except AttributeError:
            j.guid = u'No guid'
            j.status = u'A'
            j.log = u'%s' % error
            msg = 'Job aborted'
            
        if match:
            j.status = u'S'
            msg = 'Job(s) successfully started'
            h.flash.set_message(msg, 'success')
            #h.redirect('/jobs/job_list/%s' % id)
        else:
            j.guid = u'No guid'
            j.status = u'A'
            j.log = u'%s' % error
            msg = 'Job aborted [ELSE]'
            h.flash.set_message(msg, 'error')
            
        Session.add(j)
        Session.commit()
        
        #h.redirect('/jobs/show/all')
    
    def check_ava(self):
        proj = request.POST.get("proj_id", "")
        calc = request.POST.get("calc_name", "")
        if proj and calc:
            p = Session.query(Projects).filter(and_(Projects.id==proj, Projects.owner_id==session['REMOTE_USER'], Projects.removed == False)).all()
            c = Session.query(Calculations).filter(and_(Calculations.name==calc, Calculations.project_id==p[0].id, Calculations.removed == False, Calculations.calc_type_id == 5)).all()
            if c:
                return 'already in use!' 
                
            else:
                return 'Ok'
        return ''
        
    def submitRanch(self):
        calcname = request.POST.get('ranch-calcname')
        prj_id = request.POST.get('prj_id')
        project = Session.query(Projects).get(int(prj_id))
        base_path = os.path.join(config['app_conf']['maxocc_data'], session.get('DIR_CACHE'), calcname)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        else:
            shutil.rmtree(base_path)
            os.makedirs(base_path)
        #RANCH INPUT
        ranchseq = request.POST.get('ranchseq')
        self.saveFile(ranchseq, base_path)
        ranchnumdomain = request.POST.get('ranchnumdomain')
        ranchpdb = request.POST.getall('ranchpdb')
        ranchtotstruct = request.POST.get('ranchtotstruct')
        ranchrefstruct = request.POST.get('ranchrefstruct')
        ranchtypelinkers = request.POST.get('ranchtypelinkers')
        ranchorder = request.POST.get('ranchorder')
        ranchmaxs = request.POST.get('ranchmaxs')
        ranchnumpoints = request.POST.get('ranchnumpoints')
        
        #creation of run.sh and in.tgz
        #tar = tarfile.open(os.path.join(base_path,"in.tgz"),"w:gz")
        #tar.add(os.path.join(base_path, ranchseq.filename.split('\\')[0]), arcname=ranchseq.filename.split('\\')[0])
        runsh = open(os.path.join(base_path, 'run.sh'), 'w')
        runsh.write("/opt/exp_soft/enmr/CIRMMP/ranch/ranch << EOF\n")
        runsh.write(ranchseq.filename.split('\\')[0]+"\n")
        runsh.write(ranchnumdomain+"\n")
        for i in ranchpdb:
            self.saveFile(i, base_path)
            #tar.add(os.path.join(base_path, i.filename.split('\\')[0]), arcname=i.filename.split('\\')[0])
            runsh.write(i.filename.split('\\')[0]+"\n")
        runsh.write(ranchtotstruct+"\n")
        runsh.write(ranchrefstruct+"\n")
        runsh.write(ranchtypelinkers+"\n")
        runsh.write(ranchorder+"\n")
        runsh.write(ranchmaxs+"\n")
        runsh.write(ranchnumpoints+"\n")
        runsh.write("EOF\n")
        for i in ranchpdb:
            runsh.write("mv "+i.filename.split('\\')[0]+" "+i.filename.split('\\')[0]+"1"+"\n")
        runsh.close()
        
        #CALPARA INPUT
        calcrdc = request.POST.get('calcrdc')
        self.saveFile(calcrdc, base_path, "input.rdc")
        calcpcs = request.POST.get('calcpcs')
        self.saveFile(calcpcs, base_path, "input.pcs")
        calctensor = request.POST.get('calctensor')
        self.saveFile(calctensor, base_path)
        calcfield = request.POST.get('calcfield')
        calctemp = request.POST.get('calctemp')
        
        if request.POST.get("pre", "") == 'yes':
            prefile = request.POST.get('prefile')
            self.saveFile(prefile, base_path, "input.pre")
            pre_x = request.POST.get('pre-x')
            pre_y = request.POST.get('pre-y')
            pre_z = request.POST.get('pre-z')
            inputfilepre = open(os.path.join(base_path, 'inputpre'), 'w')
            inputfilepre.write("input.pre\n")
            inputfilepre.write("%s %s %s" %(pre_x, pre_y, pre_z)) 
            inputfilepre.close()
        #creation of input file
        inputfile = open(os.path.join(base_path, 'input'), 'w')
        inputfile.write("input.pcs\n")
        inputfile.write("input.rdc\n")
        inputfile.write(calctensor.filename.split('\\')[0]+"\n")
        inputfile.write(calcfield+"  "+calctemp+"\n")
        inputfile.close()
        
        #tar.add(os.path.join(base_path, calctensor.filename.split('\\')[0]), arcname=calctensor.filename.split('\\')[0])
        
        
        #tar.close()
        
        loc_dir = os.getcwd()
        os.chdir(base_path)
        template = config['app_conf']['maxocc_templ']
        shutil.copy(os.path.join(template, "calcalllast"),"calcallnew")
        shutil.copy(os.path.join(template, "calcallpre-basic.py"),"calcallpre-basic.py")
        print "FACCIO TAR"
        listdir = os.listdir(base_path)
        tar = tarfile.open("in.tgz", "w:gz")
        for name in listdir:
            tar.add(name)
        tar.close()
        #subprocess.Popen('cd %s;/bin/tar cvfz in.tgz ./* '%base_path, shell=True).wait()
        #jP = JobsProcessing()
        #cmd = 'cd %s;/bin/tar cvfz in.tgz ./* '%base_path
        #print cmd
        #jP.exec_cmd(cmd)
        #os.system("/bin/pwd;/bin/ls -lh;/bin/tar cvfz in.tgz ./* ")
        print "HO FATTO IL TAR"
        run_pre = """#!/bin/bash

tar xvfz in.tgz

#run ranch
/bin/sh ./run.sh

ls

mkdir structures
find ./ -name \*.pdb -maxdepth 1 -exec mv {} ./structures/ \;
for a in `ls *.pdb1`
do
name=`echo $a |cut -d. -f1 `
mv $a $name.pdb
done


mkdir curveint
find ./ -name \*.int -maxdepth 1 -exec mv {} ./curveint/ \;
mkdir str_info
find ./ -name \*.inf -maxdepth 1 -exec mv {} ./str_info/ \;

chmod 777 ./calcallnew

mkdir curvepcs

mkdir curverdc

mkdir curvepre

for a in `ls structures`

do

i=structures/$a 

echo $i

#echo $1

#name=`echo $i | cut -d. -f1`

#echo $name

cp ./$i structure.pdb


./calcallnew

#name=`echo $i | cut -d. -f1 | cut -d"/" -f2`; out=${name}.pdb

name=`echo $i |cut -d. -f1 | cut -d"/" -f2`

echo $name

out=${name}.pcs

echo $out

cat fort.66| awk '{print $4,$7}' > ./curvepcs/$out

out=${name}.rdc

echo $out

cat fort.67| awk '{print $4,$7}' > ./curverdc/$out

if [ -e inputpre ]
then
python calcallpre-basic.py structure.pdb
out=${name}.pre
echo $out
mv fort.68 ./curvepre/$out
fi

rm fort.66

rm fort.67


rm structure.pdb

rm out

rm out1

rm out2

done
tar cvfz structures.tgz ./structures
tar cvfz str_info.tgz ./str_info
if [ -e inputpre ]
then
tar cvfz curves.tgz ./curvepcs ./curverdc ./curveint ./curvepre
else
tar cvfz curves.tgz ./curvepcs ./curverdc ./curveint
fi
tar cvfz pro.tgz ./curves.tgz  ./structures.tgz str_info.tgz
#tar cvfz pro.tgz ./curvepcs  ./curverdc ./curveint
#tar cvfz pro.tgz *
"""
        open(os.path.join(base_path, 'run_pre.sh'), 'w').writelines(run_pre)
        ranch_jdl = """Executable = "run_pre.sh";
StdOutput  = "std.out";
StdError   = "std.err";
InputSandbox = {"%s/run_pre.sh","%s/in.tgz"};
OutputSandbox = {"std.out","std.err","pro.tgz"};
Requirements = ( other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-verylong" );
""" %(base_path,base_path)
        open(os.path.join(base_path, 'run_pre.jdl'), 'w').writelines(ranch_jdl)
        os.chdir(loc_dir)
        
        #CREO LA DIR DEL PROGETTO E CALCOLO NELLA HOME DELL'UTENTE
        w_dir = os.path.join(config['app_conf']['working_dir'],
                        project.owner.home,
                        project.name,
                        session['PORTAL'],
                        calcname)
        os.makedirs(w_dir)
        
        #CREO DIR DI INPUT E AGGIUNGO I FILE
        os.makedirs(os.path.join(w_dir, "input", "input_1"))
        shutil.copy(os.path.join(base_path, 'in.tgz'), os.path.join(w_dir, "input", "input_1"))
        
        
        
        self.ranch_job_submit(prj_id, calcname, os.path.join(base_path, 'run_pre.jdl'))
        return 'ok'
        #h.redirect('/jobs/show/all')
