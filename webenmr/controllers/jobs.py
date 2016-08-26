import logging
import os, subprocess, glob
import re
import shutil
import tarfile
from pprint import pprint
import pickle
import zipfile
import md5
import copy
import commands
import simplejson as json
from lxml import etree
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config, app_globals
import pycurl
from dateutil import parser
from datetime import datetime
import time
from sqlalchemy.sql import and_
from sqlalchemy.sql import or_
from webenmr.lib.base import *
from webenmr.lib import return_values
from webenmr.lib.multi_input import multi_input
from webenmr.model import Projects, Users, Jobs
from webenmr.lib.return_values import S_OK, S_ERROR
from webenmr.lib.Subprocess import shellCall
from webenmr.lib.BaseSecurity import BaseSecurity
from webenmr.model import Calculations, Jobs, CalculationTipology, Users
from webenmr.lib import Certificates
from webenmr.lib import ssox
import math

log = logging.getLogger(__name__)
os.umask(0002)

os.environ['PATH'] += os.pathsep


class JobsProcessing(BaseSecurity):

    def __init__(self):
        BaseSecurity.__init__(self)
        if session['PORTAL'] == 'amps-nmr':
            attribute = "/enmr.eu/amber"
        elif session['PORTAL'] == 'xplor-nih':
            attribute = "/enmr.eu/xplornih"
        else:
            attribute = ""
            
        if 'timesession' in session.keys():
            before = session['timesession']
            now = datetime.now()
            hours  = math.floor(((now - before).seconds) / 3600)
            if hours > 1.0:
                print "@@@@@@@ RINNOVO CERTIFICATO @@@@@@@@@@@"
                ret = Certificates.proxy_initialize(attribute)
                #ret = Certificates.proxy_initialize()
                print "######VOMSPROXY INI #############"
                if ret['OK']:
                    #print "VOMS_PROXY ", session['voms_proxy']
                    #print ret['Value']
                    print "OK"
                else:
                    print 'voms-proxy-init problem: %s' % ret['Message']
            print "@@@@@@@  CERTIFICATO BUONO @@@@@@@@@@@"
                
        else:
            print "@@@@@@@ PRIMO ACCESSO CERTIFICATO @@@@@@@@@@@"
            session['timesession'] = datetime.now()
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
        print "X509_USER_KEY ", session['voms_proxy_file']
        print "X509_USER_KEY ", session['voms_proxy_file']
        print "X509_USER_PROXY ", session['voms_proxy_file']


    def submitclo(self, wdir, jdl):

        '''Submit a job to the GRID

        input:
        wdir = working directory of the job
        jdl = jdl file

        return the result of the submission'''

        cmd = """ssh webenmr@192.168.0.30 << EOF
cd %s
sync
curl -i -H "Content-Type: application/json" -X POST -d '{"application":"3","description":"amber test run", "output_files": [ {"name":"pro.tgz"}], "input_files": [ {"name":"run_amber.sh"},{"name":"in.tgz"} ]}' http://localhost:8888/v1.0/tasks?user=brunor
EOF
""" %(wdir)
        print cmd
        status, output, error =self.exec_cmd(cmd)
        match = re.search('.*("id": "[0-9]+")',output)
        idj=match.group(1).split()[1].replace('"',"")
        print output
        print idj
        cmd1 = '''ssh webenmr@192.168.0.30 << EOF
cd %(wdir)s
sync
curl -i -F "file[]=@run_amber.sh" -F "file[]=@in.tgz"  POST http://localhost:8888/v1.0/tasks/%(idj)s/input?user=brunor
EOF
''' %{'wdir':wdir,'idj':idj}
        
        print cmd1
        return self.exec_cmd(cmd1)

    def submitgpu(self, wdir, jdl):
        
        print "SUBMIT GPU "

        '''Submit a job to the GRID

        input:
        wdir = working directory of the job
        jdl = jdl file

        return the result of the submission'''
        certx = session['voms_proxy_file']

        cmd = 'ssh webenmr@192.168.0.10 "cat %s > %s1 ; chmod 600 %s1; export X509_USER_PROXY=%s1 ;cd %s;/usr/bin/glite-ce-job-submit -a -r cegpu.cerm.unifi.it:8443/cream-pbs-batch %s"' %(certx, certx, certx, certx, wdir, jdl)
        print cmd
        return self.exec_cmd(cmd)

    def submit(self, wdir, jdl):
        '''Submit a job to the GRID

        input:
        wdir = working directory of the job
        jdl = jdl file

        return the result of the submission'''
        certx = session['voms_proxy_file']
        cmd = 'ssh webenmr@192.168.0.10 "cat %s > %s1 ; chmod 600 %s1; export X509_USER_PROXY=%s1 ;cd %s ;/usr/bin/glite-wms-job-submit -a %s"' %(certx, certx, certx, certx ,wdir, jdl)
        print cmd
        return self.exec_cmd(cmd)

    def statusclo(self,guidf):
        guid=guidf.split()[1]
        cmd = 'ssh webenmr@192.168.0.30 " sync;curl -i -X GET http://localhost:8888/v1.0/tasks/%s?user=brunor"'%( guid)
        print cmd
        return self.exec_cmd(cmd)

    def statusgpu(self, guid):
        print "CHECK GPU"
        '''Check the job status

        input:
        guid = the job identifier

        return the status of the job'''
        certx = session['voms_proxy_file']

        #cmd = 'set;/usr/bin/glite-wms-job-status -c /opt/glite/etc/enmr.eu/glite_wms.conf %s' % str(guid)
        cmd = 'ssh webenmr@192.168.0.10 "cat %s > %s1 ; chmod 600 %s1; export X509_USER_PROXY=%s1 ;glite-ce-job-status %s"' % (certx, certx, certx, certx,str(guid))
        #cmd='voms-proxy-info'
        #cmd = 'grid-cert-diagnostics -p'
        print "***** jobs.py exec_cmd  INI ******"
        print cmd
        print "***** jobs.py exec_cmd  END ******"
        #print "CMD1"
        #cmd1=['/usr/bin/glite-wms-job-status','-c','/opt/glite/etc/enmr.eu/glite_wms.conf']

        #cmd1.append(str(guid))

        #print "CMD1"
        #sep =  {'SSH_ASKPASS': '/usr/libexec/openssh/gnome-ssh-askpass', 'VO_DTEAM_DEFAULT_SE': 'se-enmr.cerm.unifi.it', 'LCG_LOCATION': '/usr', 'GLOBUS_TCP_PORT_RANGE': '20000,25000', 'LESSOPEN': '|/usr/bin/lesspipe.sh %s', 'LCG_GFAL_INFOSYS': 'bdii-enmr.cerm.unifi.it:2170', 'LOGNAME': 'webenmr', 'USER': 'webenmr', 'INPUTRC': '/etc/inputrc', 'DPNS_HOST': 'se-enmr.cerm.unifi.it', 'PATH': '/usr/kerberos/bin:/bin:/usr/local/bin:/usr/bin:/home/webenmr/bin', 'GLITE_LOCATION_VAR': '/var', 'GLITE_SD_PLUGIN': 'file,bdii', 'LANG': 'en_US.UTF-8', 'TERM': 'xterm', 'SHELL': '/bin/bash', 'GLITE_LOCATION': '/usr', 'GRID_ENV_LOCATION': '/usr/libexec', 'VO_OPS_DEFAULT_SE': 'se-enmr.cerm.unifi.it', 'G_BROKEN_FILENAMES': '1', 'HISTSIZE': '1000', 'X509_USER_PROXY': '/home/webenmr/WebENMR/data/enmr_r1/user_2/.voms_cert', 'MANPATH': '/opt/glite/share/man::', 'VO_ENMR_EU_DEFAULT_SE': 'se-enmr.cerm.unifi.it', 'GLITE_SD_SERVICES_XML': '/opt/glite/etc/services.xml', 'HOME': '/home/webenmr', 'MYPROXY_SERVER': 'myproxy.cnaf.infn.it', 'PYTHONPATH': '/usr/lib64/python2.4/site-packages:/usr/lib64/python:/opt/fpconst/lib/python2.4/site-packages:/opt/ZSI/lib/python2.4/site-packages', 'GT_PROXY_MODE': 'old', 'GLITE_WMS_LOCATION': '/usr', '_': '/usr/bin/ipython', 'PERL5LIB': '/usr/lib64/perl5', 'DPM_HOST': 'se-enmr.cerm.unifi.it', 'VO_INFNGRID_DEFAULT_SE': 'se-enmr.cerm.unifi.it', 'HOSTNAME': 'py-enmr.cerm.unifi.it', 'SHLVL': '1', 'PWD': '/home/webenmr', 'CVS_RSH': 'ssh', 'MAIL': '/var/spool/mail/webenmr', 'LS_COLORS': 'no=00:fi=00:di=00;34:ln=00;36:pi=40;33:so=00;35:bd=40;33;01:cd=40;33;01:or=01;05;37;41:mi=01;05;37;41:ex=00;32:*.cmd=00;32:*.exe=00;32:*.com=00;32:*.btm=00;32:*.bat=00;32:*.sh=00;32:*.csh=00;32:*.tar=00;31:*.tgz=00;31:*.arj=00;31:*.taz=00;31:*.lzh=00;31:*.zip=00;31:*.z=00;31:*.Z=00;31:*.gz=00;31:*.bz2=00;31:*.bz=00;31:*.tz=00;31:*.rpm=00;31:*.cpio=00;31:*.jpg=00;35:*.gif=00;35:*.bmp=00;35:*.xbm=00;35:*.xpm=00;35:*.png=00;35:*.tif=00;35:'}

        #result_out=commands.getstatusoutput(cmd)
        #child = subprocess.Popen( cmd1,close_fds = True,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell= False,env=sep)
        #child = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell= True,env=sep)
        #result_out = child.communicate()[0]
        #result_out=os.popen(cmd).read()

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

        #print result_out
        #return result_out
        return status, output, error

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
        #sep =  {'SSH_ASKPASS': '/usr/libexec/openssh/gnome-ssh-askpass', 'VO_DTEAM_DEFAULT_SE': 'se-enmr.cerm.unifi.it', 'LCG_LOCATION': '/usr', 'GLOBUS_TCP_PORT_RANGE': '20000,25000', 'LESSOPEN': '|/usr/bin/lesspipe.sh %s', 'LCG_GFAL_INFOSYS': 'bdii-enmr.cerm.unifi.it:2170', 'LOGNAME': 'webenmr', 'USER': 'webenmr', 'INPUTRC': '/etc/inputrc', 'DPNS_HOST': 'se-enmr.cerm.unifi.it', 'PATH': '/usr/kerberos/bin:/bin:/usr/local/bin:/usr/bin:/home/webenmr/bin', 'GLITE_LOCATION_VAR': '/var', 'GLITE_SD_PLUGIN': 'file,bdii', 'LANG': 'en_US.UTF-8', 'TERM': 'xterm', 'SHELL': '/bin/bash', 'GLITE_LOCATION': '/usr', 'GRID_ENV_LOCATION': '/usr/libexec', 'VO_OPS_DEFAULT_SE': 'se-enmr.cerm.unifi.it', 'G_BROKEN_FILENAMES': '1', 'HISTSIZE': '1000', 'X509_USER_PROXY': '/home/webenmr/WebENMR/data/enmr_r1/user_2/.voms_cert', 'MANPATH': '/opt/glite/share/man::', 'VO_ENMR_EU_DEFAULT_SE': 'se-enmr.cerm.unifi.it', 'GLITE_SD_SERVICES_XML': '/opt/glite/etc/services.xml', 'HOME': '/home/webenmr', 'MYPROXY_SERVER': 'myproxy.cnaf.infn.it', 'PYTHONPATH': '/usr/lib64/python2.4/site-packages:/usr/lib64/python:/opt/fpconst/lib/python2.4/site-packages:/opt/ZSI/lib/python2.4/site-packages', 'GT_PROXY_MODE': 'old', 'GLITE_WMS_LOCATION': '/usr', '_': '/usr/bin/ipython', 'PERL5LIB': '/usr/lib64/perl5', 'DPM_HOST': 'se-enmr.cerm.unifi.it', 'VO_INFNGRID_DEFAULT_SE': 'se-enmr.cerm.unifi.it', 'HOSTNAME': 'py-enmr.cerm.unifi.it', 'SHLVL': '1', 'PWD': '/home/webenmr', 'CVS_RSH': 'ssh', 'MAIL': '/var/spool/mail/webenmr', 'LS_COLORS': 'no=00:fi=00:di=00;34:ln=00;36:pi=40;33:so=00;35:bd=40;33;01:cd=40;33;01:or=01;05;37;41:mi=01;05;37;41:ex=00;32:*.cmd=00;32:*.exe=00;32:*.com=00;32:*.btm=00;32:*.bat=00;32:*.sh=00;32:*.csh=00;32:*.tar=00;31:*.tgz=00;31:*.arj=00;31:*.taz=00;31:*.lzh=00;31:*.zip=00;31:*.z=00;31:*.Z=00;31:*.gz=00;31:*.bz2=00;31:*.bz=00;31:*.tz=00;31:*.rpm=00;31:*.cpio=00;31:*.jpg=00;35:*.gif=00;35:*.bmp=00;35:*.xbm=00;35:*.xpm=00;35:*.png=00;35:*.tif=00;35:'}

        #result_out=commands.getstatusoutput(cmd)
        #child = subprocess.Popen( cmd1,close_fds = True,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell= False,env=sep)
        #child = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell= True,env=sep)
        #result_out = child.communicate()[0]
        #result_out=os.popen(cmd).read()

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

        #print result_out
        #return result_out
        return status, output, error
        #return self.exec_cmd(cmd)

    def statusv3(self, guid):
        '''Check the job status

        input:
        guid = the job identifier

        return the status of the job'''
        certx = session['voms_proxy_file']

        diz_stat = {}
        cmd = 'ssh webenmr@192.168.0.10 "export X509_USER_PROXY=%s1 ; /usr/bin/glite-wms-job-status -c /opt/glite/etc/enmr.eu/glite_wms.conf --verbosity 3 %s"' %(certx, guid)
        print cmd
        parse = self.exec_cmd(cmd)
        read = False


        for i in parse[1].split("\n"):
            if "- Destination                =" in i:
                cmd ="/usr/bin/lcg-info --vo enmr.eu --list-ce --query 'CE=%s' --attrs 'CFP2000'" % i.split("=")[1]
                print cmd
                parse = self.exec_cmd(cmd)
                for a1 in parse[1].split("\n"):
                    if "CFP2000" in a1:
                        diz_stat["CFP2000"] = a1.split()[2]
                cmd ="/usr/bin/lcg-info --vo enmr.eu --list-ce --query 'CE=%s' --attrs 'CINT2000'" % i.split("=")[1]
                print cmd
                parse = self.exec_cmd(cmd)
                for a1 in parse[1].split("\n"):
                    if "CINT2000" in a1:
                        diz_stat["CINT2000"] = a1.split()[2]
                diz_stat["CE"] = i.split("=")[1]

            if   "- Stateentertimes =" in i:
                read = True
            if read and "Submitted" in i:
                diz_stat["Submitted"] = i.split(":",1)[1]
            if read and "Waiting" in i:
                diz_stat["Waiting"] = i.split(":",1)[1]
            if read and "Ready" in i:
                diz_stat["Ready"] = i.split(":",1)[1]
            if read and "Scheduled" in i:
                diz_stat["Scheduled"] = i.split(":",1)[1]
            if read and "Running" in i:
                diz_stat["Running"] = i.split(":",1)[1]
            if read and "Done" in i:
                diz_stat["Done"] = i.split(":",1)[1]
            if read and "Cleared" in i:
                diz_stat["Cleared"] = i.split(":",1)[1]
            if read and "Done" in i:
                diz_stat["Done"] = i.split(":",1)[1]
            if read and "Aborted" in i:
                diz_stat["Aborted"] = i.split(":",1)[1]
            if read and "Cancelled" in i:
                diz_stat["Cancelled"] = i.split(":",1)[1]
            if read and "Unknown" in i:
                diz_stat["Unknown"] = i.split(":",1)[1]
        return diz_stat

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
        #return self.exec_cmd(cmd)


    def retrieveclo(self, guid, outdir):
            j1 = JobsProcessing()
            cmd = 'ssh webenmr@192.168.0.30 " sync;curl -i -X GET http://localhost:8888/v1.0/tasks/%s?user=brunor"'%( guid)
            print "check cloud job"

            status, output, error =self.exec_cmd(cmd)
            print cmd
            # rimouvo la roba non json
            print output
            s=[]
            conta = 0
            for i in output.split("\n"):
                conta = conta + i.count("{")
                conta = conta - i.count("}")
                if conta >0:
                    s.append(i)
            s.append("}")
            j = "".join(s)
            print j
            jsa = json.loads(j)
            for i in jsa['output_files']:
                if i["name"] == "pro.tgz":
                     fileo = i["url"]
                     print i["url"]
                     
            cmd = """ssh webenmr@192.168.0.30 << EOF
cd %s
wget "http://localhost:8888/v1.0/%s" -O ./pro.tgz
EOF
""" % (outdir,fileo)
            print #########################"
            print "Comando di retrive"
            print cmd
            print "########################"
            
            status, output, error =self.exec_cmd(cmd)
            
    
            return status, output, error

    def retrievegpu(self, guid, outdir):
        j1 = JobsProcessing()
        certx = session['voms_proxy_file']
        cmd = """ssh webenmr@192.168.0.10 << EOF
umask 002
cat %s > %s1
chmod 600 %s1
export X509_USER_PROXY=%s1
/usr/bin/glite-ce-job-output --noint --dir %s %s
cp -r %s/cegpu*/* %s
rm -r %s/cegpu*
cd %s
chown -R webenmr.apache *
chmod -R 660 *
whoami
ls -lh
EOF
""" % (certx, certx, certx, certx,outdir, guid,outdir,outdir,outdir,outdir)
        print #########################"
 #       print "Comando di retrive"
 #       print cmd
        print "########################"
        prova = 0
        while prova == 0:
            status, output, error =self.exec_cmd(cmd)
            print "PPPPPPPPPPPP RETRIVE GPU PPPPPPPPPPPPPPP"
            print cmd
            print output
            print "---------Error----------------"
            print type(error)
            print error
            print "PPPPPPPPPPPPPPPPPPPPPPPPPPP"
            if ("UBERFTP ERROR" in error) or ("UBERFTP ERROR" in output):
                prova = 0

 #               cmd1 = 'rm -rf %s/cegpu.cerm.unifi.it*;ls -lh %s' %(outdir,outdir)
  #              print "Rimuovo la directory ", cmd1
 #               cmd1s,cmd1o,cmd1e = j1.exec_cmd(cmd1)
  #              print cmd1o
            else:
                prova =1

        return status, output, error

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
        #cmdEnv = self._getExternalCmdEnvironment()
        # metto il python path della versione 2.4
        cmdEnv = {'SSH_ASKPASS': '/usr/libexec/openssh/gnome-ssh-askpass', 'VO_DTEAM_DEFAULT_SE': 'se-enmr.cerm.unifi.it', 'LCG_LOCATION': '/usr', 'GLOBUS_TCP_PORT_RANGE': '20000,25000', 'LESSOPEN': '|/usr/bin/lesspipe.sh %s', 'LCG_GFAL_INFOSYS': 'bdii-enmr.cerm.unifi.it:2170', 'LOGNAME': 'webenmr', 'USER': 'webenmr', 'INPUTRC': '/etc/inputrc', 'DPNS_HOST': 'se-enmr.cerm.unifi.it', 'PATH': '/usr/kerberos/bin:/bin:/usr/local/bin:/usr/bin:/home/webenmr/bin', 'GLITE_LOCATION_VAR': '/var', 'GLITE_SD_PLUGIN': 'file,bdii', 'LANG': 'en_US.UTF-8', 'TERM': 'xterm', 'SHELL': '/bin/bash', 'GLITE_LOCATION': '/usr', 'GRID_ENV_LOCATION': '/usr/libexec', 'VO_OPS_DEFAULT_SE': 'se-enmr.cerm.unifi.it', 'G_BROKEN_FILENAMES': '1', 'HISTSIZE': '1000', 'X509_USER_PROXY': '/home/webenmr/WebENMR/data/enmr_r1/user_2/.voms_cert', 'MANPATH': '/opt/glite/share/man::', 'VO_ENMR_EU_DEFAULT_SE': 'se-enmr.cerm.unifi.it', 'GLITE_SD_SERVICES_XML': '/opt/glite/etc/services.xml', 'HOME': '/home/webenmr', 'MYPROXY_SERVER': 'myproxy.cnaf.infn.it', 'PYTHONPATH': '/usr/lib64/python2.4/site-packages:/usr/lib64/python:/opt/fpconst/lib/python2.4/site-packages:/opt/ZSI/lib/python2.4/site-packages', 'GT_PROXY_MODE': 'old', 'GLITE_WMS_LOCATION': '/usr', '_': '/usr/bin/ipython', 'PERL5LIB': '/usr/lib64/perl5', 'DPM_HOST': 'se-enmr.cerm.unifi.it', 'VO_INFNGRID_DEFAULT_SE': 'se-enmr.cerm.unifi.it', 'OLDPWD': '/home/webenmr/WebENMR/webenmr', 'HOSTNAME': 'py-enmr.cerm.unifi.it', 'SHLVL': '1', 'PWD': '/home/webenmr', 'CVS_RSH': 'ssh', 'MAIL': '/var/spool/mail/webenmr', 'LS_COLORS': 'no=00:fi=00:di=00;34:ln=00;36:pi=40;33:so=00;35:bd=40;33;01:cd=40;33;01:or=01;05;37;41:mi=01;05;37;41:ex=00;32:*.cmd=00;32:*.exe=00;32:*.com=00;32:*.btm=00;32:*.bat=00;32:*.sh=00;32:*.csh=00;32:*.tar=00;31:*.tgz=00;31:*.arj=00;31:*.taz=00;31:*.lzh=00;31:*.zip=00;31:*.z=00;31:*.Z=00;31:*.gz=00;31:*.bz2=00;31:*.bz=00;31:*.tz=00;31:*.rpm=00;31:*.cpio=00;31:*.jpg=00;35:*.gif=00;35:*.bmp=00;35:*.xbm=00;35:*.xpm=00;35:*.png=00;35:*.tif=00;35:'}

        #cmdEnv["PYTHONPATH"]="/usr/lib64/python2.4/site-packages:/usr/lib64/python:/opt/fpconst/lib/python2.4/site-packages:/opt/ZSI/lib/python2.4/site-packages"
        #print cmdEnv
        result = shellCall( self._secCmdTimeout, cmd, env = cmdEnv )
        return result['Value']

class JobsController(BaseController):


    def __before__(self):
        """
        This __before__ method calls the parent method, and then sets up the
        tabs on the page.
        """
        #BaseController.__before__(self)

        c.page_base = u'Jobs'
        if 'REMOTE_USER' in session:
            c.current_user = Session.query(Users).get(session['REMOTE_USER'])
            #c.main_menu = Session.query(Menu).filter(and_(Menu.parent_id==None, Menu.sibling_id==None)).order_by(Menu.weight.asc()).all()
        c.page_title = u'Jobs Management'

        c.STATUS = {'R': 'Running',
          'S': 'Scheduled',
          'F': 'Finished',
          'C': 'Cancelled',
          'A': 'Aborted',
          'L': 'Cleared',
          'E': 'Finished/Retrieved'
          }

    def job_remove(self):
        status = request.POST.get('status')
        projects = Session.query(Projects).filter(and_(Projects.owner_id==session['REMOTE_USER'], Projects.removed == False)).all()
        for p in projects:
            for c in p.calculation:
                if c.removed == False:
                    for j in c.job:
                        if j:
                            if j.status == status:
                                job = Session.query(Jobs).get(j.id)
                                job.removed = True
                                Session.add(job)
                                Session.commit()
        #print "ho rimosso tutti i job %s" %status

    #def remove_and_redirect(self):
    #    status = request.POST.get('status')
    #    self.job_remove(status)
    #    h.redirect('/jobs/show/all')


    def job_list(self, id=None):
        '''Show a job list'''
        if id:
            (c.calc_id, c.prj_id, job_id) = id.split('_')
            c.jobs = Session.query(Jobs).filter(and_(Jobs.calculation_id==c.calc_id, Jobs.removed == False)).order_by('start_date').all()
            if c.jobs:
                return render('/jobs/job_list.mako')
            else:
                h.flash.set_message('No jobs for that calculation', 'error')
                h.redirect('/calculations/calculation_list/%d' % int(c.prj_id))

    def job_submit(self, id=None):
        '''Submit a job in GRID'''
        if id:
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
            print "X509_USER_KEY ", session['voms_proxy_file']
            print "X509_USER_KEY ", session['voms_proxy_file']
            print "X509_USER_PROXY ", session['voms_proxy_file']
            (calc_id, prj_id, job_id) = id.split('_')
            project = Session.query(Projects).get(int(prj_id))
            calc = Session.query(Calculations).filter(and_(Calculations.id==int(calc_id), Calculations.project_id==project.id, Calculations.removed == False)).first()
            if calc.calc_type.tipology == 'amps-nmr':
                ty = 'amber'
            else:
                ty = calc.calc_type.tipology
            w_dir = os.path.join(config['app_conf']['working_dir'],
                            project.owner.home,
                            project.name,
                            ty,
                            calc.name)
            print w_dir

            jP = JobsProcessing()
            jdl = 'amber.jdl'

            for jb in range(calc.jobs_to_submit):
                wdir = os.path.join(w_dir, 'input', 'input_%s' % (jb+1))

                serror = True
                count_retry = 0
                print "##### submit JDL  CPU GPU ####"
                print wdir, jdl
                while serror:
                    time.sleep(count_retry)
                    count_retry = count_retry + 1
                    #sottomissione gpu

                    if session["usegpu"] == True:
                        status, output, error = jP.submitgpu(wdir, jdl)
                        print "USO  -------GPU----------- "
                    elif session["useclo"] == True:
                        print "CLOUD"
                        status, output, error = jP.submitclo(wdir, jdl)

                    else:
                        status, output, error = jP.submit(wdir, jdl)

                    print 'status ', status
                    print 'output ', output
                    print 'error ', error

                    if output:
                        output = '%s' % output.strip()

                    if (len(error) > 0) or ("glexec error" in output):
                        serror = True
                        print "######ERROR IN SUBMISSION --- RETRY #############"
                        print "NUMBER %d" %count_retry
                        print "##### ######"
                        if session["useclo"]:
                          serror = False
                          error = False
                    elif count_retry == 20:
                        serror = False
                        print "#### LIMIT of 20 resumittion #####"
                    else:
                        serror = False
                        print "## OK"
                #status, output, error = jP.submit(wdir, jdl)

                if output:
                    output = '%s' % output.strip()

                #print 'status ', status
                #print 'output ', output
                #print 'error ', error

                if error:
                    msg = 'Unable to start job %s' % (jb+1)
                    h.flash.set_message(msg, 'error')
                    h.redirect('/jobs/job_list/%s' % id)

                try:
                    if session["usegpu"] == True:
                        print output
                        match = re.search('.*(https:\/\/\S+:8443\/[0-9A-Za-z_\.\-]+)', output)
                        print "********* ",match.group(1)," **************"
                    elif session["useclo"] == True:
                        match = re.search('.*("task": "[0-9]+")',output)

                    else:
                        match = re.search('.*(https:\/\/\S+:9000\/[0-9A-Za-z_\.\-]+)', output)

                    calc = Session.query(Calculations).get(int(calc_id))
                    j = Jobs()
                    j.calculation = calc
                    if session["useclo"] == True:
                        j.guid =u'futuregateway %s' %match.group(1).split()[1].replace('"',"")
                    else:
                        j.guid = u'%s' % match.group(1)
                    j.start_date = datetime.now()
                    j.dir_name = wdir
                    if session["usegpu"] == True:
                        j.type = "gpu"
                    elif session["useclo"] == True:
                        j.type = "clo"
                    else:
                        j.type = "cpu"

                except AttributeError:
                    j.guid = u'No guid'
                    j.status = u'A'
                    j.log = u'%s' % error
                    msg = 'Job %s aborted' %(jb+1)

                if match:
                    j.status = u'S'
                    msg = '%s Job(s) successfully started' %(jb+1)
                    h.flash.set_message(msg, 'success')
                    #h.redirect('/jobs/job_list/%s' % id)
                else:
                    j.guid = u'No guid'
                    j.status = u'A'
                    j.log = u'%s' % error
                    msg = 'Job %s aborted' %(jb+1)
                    h.flash.set_message(msg, 'error')

                Session.add(j)
                Session.commit()

            h.redirect('/jobs/show/all')

    def checkalljobs(self):
        owner = Session.query(Users).get(session['REMOTE_USER'])
        projects = Session.query(Projects).filter(and_(Projects.owner_id == session['REMOTE_USER'], Projects.removed == False)).all()
        if projects:
            c_id = Session.query(CalculationTipology).filter(CalculationTipology.tipology == session['PORTAL']).all()
            if c_id[0].id == 5:
                c2_id = 6
            else:
                c2_id = c_id[0].id
            for p in projects:
                pid = p.id
                for c in p.calculation:
                    if (c.calc_type_id == c_id[0].id or c.calc_type_id == c2_id) and c.removed == False:
                        cid = c.id
                        for j in c.job:
                            if j:
                                jid =j.id
                                if j.status == 'R' or j.status == 'S':
                                    s = "%d_%d_%d" % (cid, pid, jid)
                                    self.job_status(s)

    def job_status(self, id=None):
        '''Keep a job status'''
        def isFloat(s):
            try:
                float(s)
            except ValueError:
                return False
            return True
        if id:
            (calc_id, prj_id, job_id) = id.split('_')
            job = Session.query(Jobs).get(int(job_id))
            if session['PORTAL'] == 'amps-nmr' or session['PORTAL'] == 'amber' or session['PORTAL'] == 'xplor-nih':
                job = Session.query(Jobs).get(int(job_id))
                j = JobsProcessing()
                usegpu = False
                useclo = False
                if re.search('.*(https:\/\/\S+:8443\/[0-9A-Za-z_\.\-]+)',job.guid ):
                    usegpu = True
                elif    re.search('.*(futuregateway [0-9]+)', job.guid):
                    useclo = True
                else:
                    usegpu = False

                if usegpu:
                    status, output, error = j.statusgpu(job.guid)
                elif useclo:
                    status, output, error = j.statusclo(job.guid)
                else:
                    status, output, error = j.status(job.guid)


                print 'status ', status
                print 'output ', output
                print 'error ', error
                reason = ''
                if output:

                    #ssox
                    print "SSOX INI"
                    userLid = session['REMOTE_USER']
                    member = Session.query(Users).filter(and_(Users.id == userLid, Users.removed==False)).first()
                    #ip = request.environ['REMOTE_ADDR']
                    ip = "150.217.163.184"
                    if member:
                        user_ssox = member.ssoxs_uid
                        print ip
                        print job_id
                        print user_ssox
                        if session['PORTAL'] == 'amps-nmr':
                            ssox.ssox_amber(user_ssox, ip, job_id, "0")
                        elif session['PORTAL'] == 'xplor-nih':
                            ssox.ssox_xplor(user_ssox, ip, job_id, "0")

                    print "SSOX _END"

                    output = '%s' % output.strip()
                    try:

                        if usegpu:
                            if "REALLY-RUNNING" in output:
                                status = 'Running'
                            elif "IDLE" in output:
                                status = 'Scheduled'
                            elif "DONE-OK" in output:
                                status = 'Success'
                            else:
                                status = 'Aborted'
                        elif useclo:
                            print "-----FACCIO IL CHECK DEL JOB CLOUD----"
                            print output
                            if "RUNNING" in output:
                                status ='Running'
                                print "----- ho messo status Running "
                            elif "DONE" in output:
                                status ='Success'
                                print "----- ho messo status Succes "
                            else:
                                status ='Scheduled'

                        else:
                            status = re.search('.*(Current Status:\ *[a-zA-Z].*)', output).group(1).split(':')[1].strip()

                        if status == 'Ready':
                            job.status = u'R'
                            if member:
                                user_ssox = member.ssoxs_uid
                                print ip
                                print job_id
                                print user_ssox
                                if session['PORTAL'] == 'amps-nmr':
                                    ssox.ssox_amber(user_ssox, ip, job_id, "2")
                                elif session['PORTAL'] == 'xplor-nih':
                                    ssox.ssox_xplor(user_ssox, ip, job_id, "2")

                        # else:
                        #     reason = re.search('.*(Status Reason:\ *[a-zA-Z].*)', output).group(1).split(':')[1].strip()
                        elif status == 'Running':
                            job.status = u'R'

                            if member:
                                user_ssox = member.ssoxs_uid
                                print ip
                                print job_id
                                print user_ssox
                                if session['PORTAL'] == 'amps-nmr':
                                    ssox.ssox_amber(user_ssox, ip, job_id, "4")
                                elif session['PORTAL'] == 'xplor-nih':
                                    ssox.ssox_xplor(user_ssox, ip, job_id, "4")

                        elif status == 'Scheduled':
                            job.status = u'S'

                            if member:
                                user_ssox = member.ssoxs_uid
                                print ip
                                print job_id
                                print user_ssox
                                if session['PORTAL'] == 'amps-nmr':
                                    ssox.ssox_amber(user_ssox, ip, job_id, "3")
                                elif session['PORTAL'] == 'xplor-nih':
                                    ssox.ssox_xplor(user_ssox, ip, job_id, "3")

                        elif 'Success' in status or '(Exit Code !=0)' in status:
                            job.status = u'F'

                            if member:
                                user_ssox = member.ssoxs_uid
                                print ip
                                print job_id
                                print user_ssox
                                if session['PORTAL'] == 'amps-nmr':
                                    ssox.ssox_amber(user_ssox, ip, job_id, "5")
                                elif session['PORTAL'] == 'xplor-nih':
                                    ssox.ssox_xplor(user_ssox, ip, job_id, "5")

                            if usegpu:
                                print " --------RETRIEVE GPU---------"
                                res = self.job_autoretrievegpu(job_id)
                                
                            elif useclo:
                                print "-------- RETRIVE CLOUD ---------"
                                res = self.job_autoretrieveclo(job_id) 
                            else:
                                print "-------RETRIVE CPU ---------"
                                res = self.job_autoretrieve(job_id)

                            print "####RES"
                            print res
                            if res:
                                job.status = u'E'
                                reason = 'Job successfully completed. Now, you can view/download the results.'
                                # if not (usegpu or useclo):
                                #     info_time = j.statusv3(job.guid)
                                #     # for read the time use dateutil.parser.parse('Tue Apr 23 17:07:25 2013 CEST')
                                #     # the format of glite-wms-job-status are in ctime
                                #     print "#######INFOTIME#########"
                                #     print info_time
                                #     if len(info_time["Submitted"] ) > 10:
                                #         job.submitted_date = parser.parse(info_time["Submitted"])
                                #         print parser.parse(info_time["Submitted"])
                                #     if len(info_time["Waiting"]) > 10:
                                #         job.waiting_date = parser.parse(info_time["Waiting"])
                                #         print parser.parse(info_time["Waiting"])
                                #     if len(info_time["Ready"]):
                                #         job.ready_date = parser.parse(info_time["Ready"])
                                #     if len(info_time["Scheduled"]) > 10:
                                #         job.scheduled_date = parser.parse(info_time["Scheduled"])
                                #     if len(info_time["Running"]) > 10:
                                #         job.running_date = parser.parse(info_time["Running"])
                                #     if len(info_time["Done"]) > 10:
                                #         job.done_date = parser.parse(info_time["Done"])
                                #     if len(info_time["Aborted"]) > 10:
                                #         job.aborted_date = parser.parse(info_time["Aborted"])
                                #     if len (info_time["Cancelled"]) > 10:
                                #         job.cancelled_date = parser.parse(info_time["Cancelled"])
                                #     if len(info_time["Unknown"]) > 10:
                                #         job.unknown_date = parser.parse(info_time["Unknown"])
                                #     if "CFP2000" in info_time.keys():
                                #         if isFloat(info_time["CFP2000"]):
                                #             job.cfp2000 = float(info_time["CFP2000"])
                                #     if "CINT2000" in info_time.keys():
                                #         if isFloat(info_time["CINT2000"]):
                                #             job.cint2000 = float(info_time["CINT2000"])
                                #     if "CE" in info_time.keys():
                                #         job.ce = info_time["CE"]

                            #elif '(Exit Code !=0)' in status:
                            #    job.status = u'F'
                            #    res = self.job_autoretrieve(job_id)
                            #    if res:
                            #        job.status = u'E'
                            #        reason = 'Job successfully completed. Now, you can view/download the results.'

                            elif 'Cancelled' in status:
                                job.status = u'C'
                            elif 'Aborted' in status:
                                job.status = u'A'
                            elif 'Cleared' in status:
                                job.status = u'L'
                            elif 'Ready' in status:
                                job.status = u'R'
                            if reason:
                                job.log = u'%s' % reason
                        Session.add(job)
                        Session.commit()
                    except AttributeError:
                        status = "Aborted"

                        ## modifica da rimettere
                        #job.status = u"A"
                        #job.log = "WMS submission failure."
                        #Session.add(job)
                        #Session.commit()
                    ##h.redirect('/jobs/job_list/%s' % id)
                    ##h.redirect('/jobs/show/run')
            elif session['PORTAL'] == 'maxocc':
                jj = JobsProcessing()
                proj = Session.query(Projects).get(int(prj_id))
                calc = Session.query(Calculations).get(int(calc_id))
                tip = Session.query(CalculationTipology).get(int(calc.calc_type_id))
                if calc.calc_type_id == 6:
                    print "ranch calculation"
                    status, output, error = jj.status(job.guid)
                    print 'status ', status
                    print 'output ', output
                    print 'error ', error
                    reason = ''
                    if output:
                        output = '%s' % output.strip()
                        try:
                            status = re.search('.*(Current Status:\ *[a-zA-Z].*)', output).group(1).split(':')[1].strip()
                            print "lo status: %s" %status
                            if status == 'Ready':
                                job.status = u'R'
                            else:
                                reason = re.search('.*(Status Reason:\ *[a-zA-Z].*)', output).group(1).split(':')[1].strip()
                                print "la reason: %s" % reason
                            if status == 'Running':
                                job.status = u'R'
                            elif status == 'Scheduled':
                                job.status = u'S'
                            elif 'Success' in status:
                                print "SUCCESSO"
                                job.status = u'F'
                                res = self.job_autoretrieve(job_id)
                                if res:
                                    job.status = u'E'
                                    reason = 'Job successfully completed. Now, you can view/download the results.'
                            elif '(Exit Code !=0)' in status:
                                job.status = u'F'
                                res = self.job_autoretrieve(job_id)
                                if res:
                                    job.status = u'E'
                                    reason = 'Job successfully completed. Now, you can view/download the results.'
                            elif 'Cancelled' in status:
                                job.status = u'C'
                            elif 'Aborted' in status:
                                job.status = u'A'
                            elif 'Cleared' in status:
                                job.status = u'L'
                            elif 'Ready' in status:
                                job.status = u'R'
                            if reason:
                                job.log = u'%s' % reason
                                Session.add(job)
                                Session.commit()
                        except AttributeError:
                            status = "Aborted"
                            job.status = "A"
                            job.log = "WMS submission failure."
                            Session.add(job)
                            Session.commit()
                else:
                    conto = calc.name
                    print "##########CHECK RISULTATI MAXOCC ANALISYS ############"
                    print "nome calcolo: %s" %conto

                    percentuale = 80.0
                    doc = etree.ElementTree(file=os.path.join(config['app_conf']['maxocc_data'], "STATUS.xml"))
                    #doc = etree.ElementTree(file="/opt/jobcontrol/STATUS.xml")
                    output = []
                    tot_jobs = 0
                    submitted = False
                    totOre = 0
                    for a in doc.getiterator():
                        if a.tag == "jobs":
                            if a.get("Project_name") == conto:
                                submitted = True
                                totOre = (time.mktime(time.strptime(time.asctime()))- time.mktime(time.strptime(a.get("Start_date"))))/3600
                                if a.get("Status") == "E":
                                    output.append(a.get("output"))
                                tot_jobs = a.get("num_job_project")
                    print "TOTALE ORE %d" %totOre
                    print 'calcolo %s - job terminati: %d su %s' %(conto, len(output), tot_jobs)
                    if ((len(output) >= int(round((percentuale*int(tot_jobs))/100))) and submitted):
                        print "calcoli maxocc finiti!"
                        job.status = u'E'
                        job.log = u'Job completed. Use the Project-->Manage menu to download data'
                        Session.add(job)
                        Session.commit()

                        #lanciare l'analisi
                        path_proj = ''
                        path_proj = path_proj + "/".join(output[0].split("/")[:-2])
                        print 'project path: %s' %path_proj
                        print "Lancio i subprocess per l'analisi"
                        #cmd_status = os.system("/home/webenmr/WebENMR/data/maxocc/templates/ana_script.sh")
                        #subprocess.Popen('cd %s; /bin/sh /home/webenmr/WebENMR/data/maxocc/templates/ana_script.sh' %path_proj, shell=True).wait()
                        cmd = 'cd %s; /bin/sh %s/ana_script.sh' %(path_proj,config['app_conf']['maxocc_templ'])
                        print cmd
                        #subprocess.Popen('cd %s; /bin/sh /home/webenmr/WebENMR/data/maxocc/templates/ana_script.sh' %path_proj, shell=True).wait()
                        print jj.exec_cmd(cmd)
                        #os.system('cd %s; sh /home/webenmr/WebENMR/data/maxocc/templates/ana_script.sh&' %path_proj)
                        #controllare size di 0.mo SE contiene righe run altro script
                        #subprocess.Popen('cd %s; python /home/webenmr/WebENMR/data/maxocc/templates/num3.py' %path_proj, shell=True).wait()
                        if os.path.exists(os.path.join(path_proj, '0.crv')):
                            ftemp = open(os.path.join(path_proj, '0.mo'))
                            str = ftemp.readline()
                            ftemp.close()
                            print str
                            print len(str)
                            if len(str) or os.path.exists(os.path.join(path_proj, "artificial.mo")):
                                cmd = 'cd %s; /usr/bin/python %s/num5.py' %(path_proj,config['app_conf']['maxocc_templ'])
                                #subprocess.Popen('cd %s; /usr/bin/python /home/webenmr/WebENMR/data/maxocc/templates/num4.py', shell=True).wait()
                                print jj.exec_cmd(cmd)
                        #os.system('cd %s; /usr/bin/python /home/webenmr/WebENMR/data/maxocc/templates/num3.py&' %path_proj)

                        #copiare i risultati, distinguere il caso 0.mo vuoto
                        if os.path.exists(os.path.join(path_proj, 'mo.png')):

                            pdir = os.path.join(config['app_conf']['working_dir'], proj.owner.home, proj.name, tip.tipology, calc.name, "output")
                            if not os.path.exists(pdir):
                                os.makedirs(pdir)
                            else:
                                shutil.rmtree(pdir)
                                os.makedirs(pdir)
                            shutil.copy(os.path.join(path_proj, 'mo.png'), pdir)
                            shutil.copy(os.path.join(path_proj, 'mo-usr.crv'), pdir)
                            shutil.copy(os.path.join(path_proj, 'mo.val'), pdir)
                            shutil.copy(os.path.join(path_proj, 'mo.log'), pdir)
                            shutil.copy(os.path.join(path_proj, 'mo-det.png'), pdir)
                        else:
                            print 'non esiste mo.png'
                        pdir = os.path.join(config['app_conf']['working_dir'], proj.owner.home, proj.name, tip.tipology, calc.name, 'output')
                        cmd = 'cd %s; /bin/sh %s/anaResultMaxocc.bash' %(path_proj,config['app_conf']['maxocc_templ'])
                        print "sto creando results.tgz"
                        #subprocess.Popen(cmd, shell=True).wait()
                        jj.exec_cmd(cmd)
                        if os.path.exists(os.path.join(path_proj, "results.tgz")):
                            print "ho creato results.tgz"
                            if not os.path.exists(pdir):
                                os.makedirs(pdir)
                            shutil.copy(os.path.join(path_proj, 'results.tgz'), pdir)
                            print "finito di copiare nella dir del progetto"
                        else:
                            print os.path.join(path_proj, "results.tgz")
                            print 'non ho trovato results.tgz'
                        #job.status = u'R'
                        #job.log = u'Job is running. %d on %s completed jobs.' %(len(output), tot_jobs)
                        #Session.add(job)
                        #Session.commit()
                    elif not submitted:
                        job.status = u'S'
                        job.log = u'Scheduled job. The server is submitting your job in Grid.'
                        Session.add(job)
                        Session.commit()
                    elif totOre > 72:
                        job.status = u'A'
                        job.log = u'Aborted job. Try to re-submit your job.'
                        Session.add(job)
                        Session.commit()
                    else:
                        job.status = u'R'
                        job.log = u'Calculation is running, with %d on %s completed jobs.' %(len(output), tot_jobs)
                        Session.add(job)
                        Session.commit()

    def job_kill(self, id=None):
        '''Kill a running job'''
        if id:
            (calc_id, prj_id, job_id) = id.split('_')
            job = Session.query(Jobs).get(int(job_id))
            if session['PORTAL'] == 'amps-nmr' or session['PORTAL'] == 'amber' or session['PORTAL'] == 'xplor-nih':
                j = JobsProcessing()

                status, output, error = j.kill(job.guid)
                print status, output, error

                if output:
                    output = '%s' % output.strip()
                    match = re.search('.*(glite-wms-job-cancel Success)', output)
                    if match:
                        print match.group(1)
                        job.status = u'C'
                        job.log = u''
                        Session.add(job)
                        Session.commit()
                        h.flash.set_message('Job(s) successfully killed.', 'success')
                        #h.redirect('/jobs/job_list/%s' % id)
                        h.redirect('/jobs/show/all')

                job.log = u'%s' % error
                Session.add(job)
                Session.commit()
                h.flash.set_message('Unable to kill the job.', 'error')
                #h.redirect('/jobs/job_list/%s' % id)
                h.redirect('/jobs/show/all')
            elif session['PORTAL'] == 'maxocc':
                job_list = Session.query(Jobs).filter(Jobs.calculation_id==int(calc_id))
                job_item = job_list[0]
                job_item.removed = True
                Session.add(job_item)
                calc = Session.query(Calculations).get(job.calculation_id)
                calc.removed = True
                Session.add(calc)
                Session.commit()
                h.flash.set_message('Job(s) successfully killed.', 'success')
                #h.redirect('/jobs/job_list/%s' % id)
                h.redirect('/jobs/show/all')

    # python 2.4's tarfile doesn't have extractall.
    def extractall(self, tf, path="."):
        for tarinfo in tf:
            if tarinfo.isdir():
                # Extract directories with a safe mode.
                tarinfo = copy.copy(tarinfo)
                tarinfo.mode = 0700
            tf.extract(tarinfo, path)


    def job_autoretrieveclo(self, id):
            '''Auto-Retrieve a terminated job'''
            if id:
                j = JobsProcessing()
    
                owner = Session.query(Users).get(session['REMOTE_USER'])
                job = Session.query(Jobs).get(int(id))
                c = Session.query(Calculations).filter(Calculations.id == job.calculation_id)
                calc = c[0]
                proj = Session.query(Projects).filter(Projects.id == calc.project_id)
                project = proj[0]
                output_num = job.dir_name
    
                if output_num != None:
                    output_num = os.path.basename(job.dir_name).split("_")[-1]
                else:
                    job_md5 = md5.new("%s" %job)
                    output_num = "output_%s" % job_md5.hexdigest()[0:10]
                if calc.calc_type.tipology == 'ranch':
                    tip = 'maxocc'
                else:
                    tip = calc.calc_type.tipology
                print calc.name, tip
                if not os.path.exists(os.path.join(config['app_conf']['working_dir'],
                                    owner.home,
                                    project.name, tip, calc.name)):
                    tip = 'amber'
    
                if not os.path.exists(os.path.join(config['app_conf']['working_dir'],
                                    owner.home,
                                    project.name,
                                    tip,
                                    calc.name, 'output')):
                    os.mkdir(os.path.join(config['app_conf']['working_dir'],
                                        owner.home,
                                        project.name,
                                        tip,
                                        calc.name, 'output'))
    
                #else:
                #        os.mkdir(os.path.join(config['app_conf']['working_dir'],
                #                    owner.home,
                #                    project.name,
                #                    calc.calc_type.tipology,
                #                    calc.name, 'output'))
                #        tip = calc.calc_type.tipology
                wdir = os.path.join(config['app_conf']['working_dir'],
                                    owner.home,
                                    project.name)
    
                outdir = os.path.join(config['app_conf']['working_dir'],
                                    owner.home,
                                    project.name,
                                    tip,
                                    calc.name, 'output',
                                    'output_%s' % output_num )
    
                if not os.path.exists(outdir):
                    os.mkdir(outdir)
                print outdir
                jobidn = job.guid.split()[1]
                status, output, error = j.retrieveclo(jobidn, outdir)
                print 'status ', status
                print 'output ', output
                print 'error ', error
                ret = 0
                if output:
                    untar_job = os.path.join(outdir, "pro.tgz")
                    if os.path.getsize(untar_job) > 0:
                        ret=1
    
                        #subprocess.Popen('cd %s; /bin/tar xvfz %s' %(outdir, untar_job), shell=True).wait()
                        cmd = 'cd %s;/bin/gunzip %s;/bin/tar xvf %s' %(outdir, "pro.tgz", "pro.tar")
                        print j.exec_cmd(cmd)
                        #tar_job = tarfile.open(untar_job, "r:gz")
                        #self.extractall(tar_job, outdir)
                        #tar_job.close()
                        os.remove(os.path.join(outdir, "pro.tar"))
                        #print "Ho finito di fare lo SSSTARRR di %s in %s" %(untar_job, outdir)
                        #ret = 1
                        h.flash.set_message('Job succesfully retrieved.', 'success')
                        #h.redirect('/jobs/job_list/%s' % id)
                job.log = u'%s' % error[:254]
                Session.add(job)
                Session.commit()
                #h.flash.set_message('Unable to retrieve the job.', 'error')
                #h.redirect('/jobs/job_list/%s' % id)
                return ret



    def job_autoretrievegpu(self, id):
        '''Auto-Retrieve a terminated job'''
        if id:
            j = JobsProcessing()

            owner = Session.query(Users).get(session['REMOTE_USER'])
            job = Session.query(Jobs).get(int(id))
            c = Session.query(Calculations).filter(Calculations.id == job.calculation_id)
            calc = c[0]
            proj = Session.query(Projects).filter(Projects.id == calc.project_id)
            project = proj[0]
            output_num = job.dir_name

            if output_num != None:
                output_num = os.path.basename(job.dir_name).split("_")[-1]
            else:
                job_md5 = md5.new("%s" %job)
                output_num = "output_%s" % job_md5.hexdigest()[0:10]
            if calc.calc_type.tipology == 'ranch':
                tip = 'maxocc'
            else:
                tip = calc.calc_type.tipology
            print calc.name, tip
            if not os.path.exists(os.path.join(config['app_conf']['working_dir'],
                                owner.home,
                                project.name, tip, calc.name)):
                tip = 'amber'

            if not os.path.exists(os.path.join(config['app_conf']['working_dir'],
                                owner.home,
                                project.name,
                                tip,
                                calc.name, 'output')):
                os.mkdir(os.path.join(config['app_conf']['working_dir'],
                                    owner.home,
                                    project.name,
                                    tip,
                                    calc.name, 'output'))

            #else:
            #        os.mkdir(os.path.join(config['app_conf']['working_dir'],
            #                    owner.home,
            #                    project.name,
            #                    calc.calc_type.tipology,
            #                    calc.name, 'output'))
            #        tip = calc.calc_type.tipology
            wdir = os.path.join(config['app_conf']['working_dir'],
                                owner.home,
                                project.name)

            outdir = os.path.join(config['app_conf']['working_dir'],
                                owner.home,
                                project.name,
                                tip,
                                calc.name, 'output',
                                'output_%s' % output_num )

            if not os.path.exists(outdir):
                os.mkdir(outdir)
            print outdir
            status, output, error = j.retrievegpu(job.guid, outdir)
            print 'status ', status
            print 'output ', output
            print 'error ', error
            ret = 0
            if output:
                ret = 1
                output = '%s' % output.strip()
                match = re.search('.*(output will be stored in the dir)', output)

                if match:
                    print "IF MATCH"
                    #regex = '.*(%s[a-zA-Z/].*)' % wdir
                    #s = re.compile(regex)
                    #where = os.path.basename(re.search(s, output).group(1))
                    #job.status = u'E'
                    #job.log = u'Retrieved in: output/%s' % outdir
                    #Session.add(job)
                    #Session.commit()
                    #if there is a ranch+calcall job

                    untar_job = os.path.join(outdir, "pro.tgz")
                    #subprocess.Popen('cd %s; /bin/tar xvfz %s' %(outdir, untar_job), shell=True).wait()
                    cmd = 'cd %s;/bin/gunzip %s;/bin/tar xvf %s' %(outdir, "pro.tgz", "pro.tar")
                    print j.exec_cmd(cmd)
                    #tar_job = tarfile.open(untar_job, "r:gz")
                    #self.extractall(tar_job, outdir)
                    #tar_job.close()
                    os.remove(os.path.join(outdir, "pro.tar"))
                    #print "Ho finito di fare lo SSSTARRR di %s in %s" %(untar_job, outdir)
                    #ret = 1
                    h.flash.set_message('Job succesfully retrieved.', 'success')
                    #h.redirect('/jobs/job_list/%s' % id)
            job.log = u'%s' % error[:254]
            Session.add(job)
            Session.commit()
            #h.flash.set_message('Unable to retrieve the job.', 'error')
            #h.redirect('/jobs/job_list/%s' % id)
            return ret

    def job_autoretrieve(self, id):
        '''Auto-Retrieve a terminated job'''
        if id:
            j = JobsProcessing()

            owner = Session.query(Users).get(session['REMOTE_USER'])
            job = Session.query(Jobs).get(int(id))
            c = Session.query(Calculations).filter(Calculations.id == job.calculation_id)
            calc = c[0]
            proj = Session.query(Projects).filter(Projects.id == calc.project_id)
            project = proj[0]
            output_num = job.dir_name

            if output_num != None:
                output_num = os.path.basename(job.dir_name).split("_")[-1]
            else:
                job_md5 = md5.new("%s" %job)
                output_num = "output_%s" % job_md5.hexdigest()[0:10]
            if calc.calc_type.tipology == 'ranch':
                tip = 'maxocc'
            else:
                tip = calc.calc_type.tipology
            print calc.name, tip
            if not os.path.exists(os.path.join(config['app_conf']['working_dir'],
                                owner.home,
                                project.name, tip, calc.name)):
                tip = 'amber'

            if not os.path.exists(os.path.join(config['app_conf']['working_dir'],
                                owner.home,
                                project.name,
                                tip,
                                calc.name, 'output')):
                os.mkdir(os.path.join(config['app_conf']['working_dir'],
                                    owner.home,
                                    project.name,
                                    tip,
                                    calc.name, 'output'))

            #else:
            #        os.mkdir(os.path.join(config['app_conf']['working_dir'],
            #                    owner.home,
            #                    project.name,
            #                    calc.calc_type.tipology,
            #                    calc.name, 'output'))
            #        tip = calc.calc_type.tipology
            wdir = os.path.join(config['app_conf']['working_dir'],
                                owner.home,
                                project.name)

            outdir = os.path.join(config['app_conf']['working_dir'],
                                owner.home,
                                project.name,
                                tip,
                                calc.name, 'output',
                                'output_%s' % output_num )

            if not os.path.exists(outdir):
                os.mkdir(outdir)
            print outdir
            status, output, error = j.retrieve(job.guid, outdir)
            print 'status ', status
            print 'output ', output
            print 'error ', error
            ret = 0
            if output:
                ret = 1
                output = '%s' % output.strip()
                match = re.search('.*(successfully retrieved)', output)
                if match:
                    print "IF MATCH"
                    #regex = '.*(%s[a-zA-Z/].*)' % wdir
                    #s = re.compile(regex)
                    #where = os.path.basename(re.search(s, output).group(1))
                    #job.status = u'E'
                    #job.log = u'Retrieved in: output/%s' % outdir
                    #Session.add(job)
                    #Session.commit()
                    #if there is a ranch+calcall job
                    untar_job = os.path.join(outdir, "pro.tgz")
                    #subprocess.Popen('cd %s; /bin/tar xvfz %s' %(outdir, untar_job), shell=True).wait()
                    cmd = 'cd %s; /bin/gunzip %s;/bin/tar xvf %s' %(outdir, "pro.tgz", "pro.tar")
                    print j.exec_cmd(cmd)
                    #tar_job = tarfile.open(untar_job, "r:gz")
                    #self.extractall(tar_job, outdir)
                    #tar_job.close()
                    os.remove(os.path.join(outdir, "pro.tar"))
                    #print "Ho finito di fare lo SSSTARRR di %s in %s" %(untar_job, outdir)
                    #ret = 1
                    h.flash.set_message('Job succesfully retrieved.', 'success')
                    #h.redirect('/jobs/job_list/%s' % id)
            job.log = u'%s' % error[:254]
            Session.add(job)
            Session.commit()
            #h.flash.set_message('Unable to retrieve the job.', 'error')
            #h.redirect('/jobs/job_list/%s' % id)
            return ret


    def job_retrieve(self, id=None):
        '''Retrieve a terminated job'''
        if id:

            (calc_id, prj_id, job_id) = id.split('_')

            j = JobsProcessing()

            owner = Session.query(Users).get(session['REMOTE_USER'])
            job = Session.query(Jobs).get(int(job_id))
            project = Session.query(Projects).get(int(prj_id))
            calc = Session.query(Calculations).get(int(calc_id))
            output_num = job.dir_name

            if output_num != None:
                output_num = os.path.basename(job.dir_name).split("_")[-1]
            else:
                job_md5 = md5.new("%s" %job)
                output_num = "output_%s" % job_md5.hexdigest()[0:10]

            if not os.path.isdir(os.path.join(config['app_conf']['working_dir'],
                                owner.home,
                                project.name,
                                calc.calc_type.tipology,
                                calc.name, 'output')):
                os.mkdir(os.path.join(config['app_conf']['working_dir'],
                                owner.home,
                                project.name,
                                calc.calc_type.tipology,
                                calc.name, 'output'))

            wdir = os.path.join(config['app_conf']['working_dir'],
                                owner.home,
                                project.name)

            outdir = os.path.join(config['app_conf']['working_dir'],
                                owner.home,
                                project.name,
                                calc.calc_type.tipology,
                                calc.name, 'output',
                                'output_%s' % output_num )

            if not os.path.isdir(outdir):
                os.mkdir(outdir)
            print outdir
            status, output, error = j.retrieve(job.guid, outdir)
            print 'status ', status
            print 'output ', output
            print 'error ', error
            if output:
                output = '%s' % output.strip()
                match = re.search('.*(successfully retrieved)', output)
                if match:
                    #regex = '.*(%s[a-zA-Z/].*)' % wdir
                    #s = re.compile(regex)
                    #where = os.path.basename(re.search(s, output).group(1))
                    job.status = u'E'
                    job.log = u'Retrieved in: output/%s' % outdir
                    Session.add(job)
                    Session.commit()
                    #decompress pro.tgz
                    untar_job = os.path.join(outdir, "pro.tgz")
                    tar_job = tarfile.open(untar_job, "r:gz")
                    for member in tar_job.getmembers():
                        print "Member ", member.name
                        #print "Where " , where
                        print "Outdir " , outdir
                        if not os.path.isfile( os.path.join(outdir, member.name)):
                            file_tar = tar_job.extractfile(member).read()
                            fout = open(os.path.join(outdir, member.name), "w")
                            fout.write(file_tar)
                            fout.close()
                    tar_job.close()
                    #remove tar file
                    if os.path.isfile(untar_job):
                        os.remove(untar_job)
                    ret = 1
                    h.flash.set_message('Job succesfully retrieved.', 'success')
                    h.redirect('/jobs/job_list/%s' % id)
            job.log = u'%s' % error
            Session.add(job)
            Session.commit()
            h.flash.set_message('Unable to retrieve the job.', 'error')
            h.redirect('/jobs/job_list/%s' % id)

    def checkGRID(self):
        dd = """( other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-verylong");"""
#        dd = """( other.GlueCEUniqueID == "gazon.nikhef.nl:8443/cream-pbs-medium" || other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-verylong");"""
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
        print ce_sub
        if len(ce_sub) > 0:
            list_cet = "("
            for i in ce_sub:
                list_cet = list_cet + ' other.GlueCEUniqueID == "%s" ||' %i
            list_ce = list_cet[:-2] + ")"
        else:
            list_ce = dd
#  MODIFICA PER LANCIARE CONTI SOLO SU PBS
#        return list_ce
        return dd

    def job_killall(self, id=None):
        '''Kill all calculation running jobs'''
        if id:
            (calc_id, prj_id, job_id) = id.split('_')
            if session["PORTAL"] == 'amps-nmr':
                jobs = Session.query(Jobs).filter(and_(Jobs.calculation_id==int(calc_id), Jobs.status=='R')).all()
                jp = JobsProcessing()
                with_error = False

                for j in jobs:
                    status, output, error = jp.kill(j.guid)
                    job = Session.query(Jobs).get(int(j.id))
                    if output:
                        output = '%s' % output.strip()

                        match = re.search('.*(glite-wms-job-cancel Success)', output)
                        if match:
                            print match.group(1)
                            job.status = u'C'
                            job.log = u''
                            Session.add(job)
                            Session.commit()
                    else:
                        job.log = u'%s' % error
                        Session.add(job)
                        Session.commit()
                        with_error = True

                if with_error:
                    h.flash.set_message('Job(s) killed with errors.', 'error')
                    h.redirect('/jobs/job_list/%s' % id)
                else:
                    h.flash.set_message('Job(s) successfully killed.', 'success')
                    h.redirect('/jobs/job_list/%s' % id)
            elif session['PORTAL'] == 'maxocc':
                job_list = Session.query(Jobs).filter(Jobs.calculation_id==int(calc_id, Jobs.removed == False))
                if job_list:
                    job_item = job_list[0]
                    job_item.removed = True
                    Session.add(job_item)
                    calc = Session.query(Calculations).get(job_item.calculation_id)
                    calc.removed = True
                    Session.add(calc)
                    Session.commit()
                    h.flash.set_message('Job(s) successfully killed.', 'success')
                    h.redirect('/jobs/job_list/%s' % id)
                else:
                    h.flash.set_message('Unable to kill job.', 'error')
                    h.redirect('/jobs/job_list/%s' % id)

    @check_access('Run Jobs')
    def show(self, id=None):
        '''Show jobs informations'''
        if id:
            c.show = id
            c.projects = Session.query(Projects).filter(and_(Projects.owner_id == session['REMOTE_USER'], Projects.removed == False)).all()
            if session['PORTAL'] == 'maxocc':
                ranch = 'ranch'
                calctype = Session.query(CalculationTipology).filter(or_(CalculationTipology.tipology == session['PORTAL'], CalculationTipology.tipology == ranch))
                c.calctype2_id = 6
            else:
                    calctype = Session.query(CalculationTipology).filter((CalculationTipology.tipology == session['PORTAL']))
                    c.calctype2_id = calctype[0].id
            c.calctype_id = calctype[0].id
            return render('/jobs/showall.mako')

    @check_access('Run Jobs')
    def show_calc(self):
        path = request.GET.get("path")
        pathList = path.split("::")
        proj = pathList[0]
        calc = pathList[1]
        prj = Session.query(Projects).filter(and_(Projects.name == proj, Projects.removed == False, Projects.owner_id == session['REMOTE_USER'])).all()
        if prj:
            calculation = Session.query(Calculations).filter(and_(Calculations.name == calc, Calculations.removed == False, Calculations.project_id == prj[0].id)).all();
            if calculation:
                prj[0].calculation = calculation
                c.projects = prj
                c.show = 'all'
                c.projects = prj
                c.calctype_id = calculation[0].calc_type_id
                return render('/jobs/showall.mako')
            else:
                h.flash.set_message('No calculation', 'error')
                h.redirect('/filemanager/')
        else:
            h.flash.set_message('No project', 'error')
            h.redirect('/filemanager/')

    @check_access('Run Jobs')
    def job_prepare(self):
        '''Prepare a job for submission

        steps:
        a) check for the calculation existance
        b) directory creation
        c) database new calculation entry creation
        d) put data into new directory
        e) start job
        '''
        #grid_req = """( other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-long" || other.GlueCEUniqueID == "ce01.dur.scotgrid.ac.uk:2119/jobmanager-lcgpbs-q6h" );"""
        #grid_req = """other.GlueCEPolicyMaxCPUTime > 2000 && (other.GlueCEInfoHostName == "deimos.htc.biggrid.nl" || other.GlueCEInfoHostName == "trekker.nikhef.nl" ||  other.GlueCEInfoHostName == "pbs-enmr.cerm.unifi.it" || other.GlueCEInfoHostName == "gazon.nikhef.nl" || other.GlueCEInfoHostName == "ce-enmr.chemie.uni-frankfurt.de" || other.GlueCEInfoHostName == "ce-enmr.chem.uu.nl" );"""
        #grid_req = """other.GlueCEPolicyMaxCPUTime > 2000 && (other.GlueCEInfoHostName == "deimos.htc.biggrid.nl" || other.GlueCEInfoHostName == "trekker.nikhef.nl"  || other.GlueCEInfoHostName == "gazon.nikhef.nl" || other.GlueCEInfoHostName == "ce-enmr.chemie.uni-frankfurt.de" || other.GlueCEInfoHostName == "ce-enmr.chem.uu.nl" );"""
        print "REQUEST POST INI"
        for key in request.POST:
            print(key)
            value = request.POST[key]
            print(value)
        print "REQUEST POST END"
        prj_id = request.POST.get('prj_id')
        calc_name = request.POST.get('calc_name')
        if session['PORTAL'] == 'amps-nmr':
            tipology = 'amber'
        else:
            tipology = session['PORTAL']
        #tipology = request.POST.get('tipology')
        multij = request.POST.get('multij')
        if multij == "on":
            multi_job = True
        else:
            multi_job = False

        #usegpu = False
        #usaclo = False
        calccpugpu = request.POST.get('calccpugpu')
        print "********* GPU **********"
        print calccpugpu
        print "********* GPU **********"
        if calccpugpu == "calcgpu":
            session["usegpu"] = True
            session["useclo"] = False

        elif calccpugpu == "calclo":
            session["useclo"] = True
            session["usegpu"] = False
        else:
            session["useclo"] = False
            session["usegpu"] = False

        session.save()
        numStep = request.POST.get('step')
        print "step %s" %numStep
        list_input_sander = list()
        for i in range(0, int(numStep)):
            list_input_sander.append("sander"+str(i)+".in")
        #print "###############List of Amber .in files###############"
        #print list_input_sander
        #print "numStep"
        #print numStep
        #print "#####################################################"
        #
        calc_name = calc_name.replace(' ', '_')
        owner = Session.query(Users).get(session['REMOTE_USER'])
        project = Session.query(Projects).get(int(prj_id))
        calc_type = Session.query(CalculationTipology).filter(CalculationTipology.tipology == session['PORTAL']).first()


        #cname = Session.query(Calculations).filter(and_(Calculations.name==calc_name, Calculations.project_id==int(prj_id))).first()
        #
        ## Check the existance of the calculation
        #if cname:
        #    h.flash.set_message('Calculation name already exists', 'Error')
        #    h.redirect('/calculations/%s' % tipology)

        # Directory creation
        if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.tgz")):
            #multi_job = True
            if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.tgz")):
                multi = tarfile.open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.tgz"),"r:gz")
        #else:
        #    multi_job = False
        print "######### EVALUATE MULTI_JOB ##################"
        if multi_job:
            print "################# MULTI_JOB TRUE ##########################"
            list_directory = []
            pdir = os.path.join(config['app_conf']['working_dir'], owner.home, project.name, tipology, calc_name)
            print pdir
            try:
                os.makedirs(pdir)
            except IOError, (errno, strerror):
                h.flash.set_message('An error occurred during calculation creation.', 'Error')
                h.redirect('/calculations/%s' % tipology)

            num_m = 0

            pdbo = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "amber_in.pdb")
            pdb_Am = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "out_leap.pdb")
            n_crd = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "prmcrd")
            ll_multi = multi_input(pdbo, pdb_Am, n_crd)

            print "############MEMBERSNAME###############"
            for member in multi.getmembers():
                print member.name

            for member in multi.getmembers():
                if member.name[-4:] == ".pdb":
                    if "pdb_" in member.name  and member.name.split("pdb_")[1][:-4].isdigit():
                        num_m = member.name.split("pdb_")[1][:-4]
                    else:
                        num_m = member.name[:-4]
                    #num_m += 1
                    f = multi.extractfile(member)
                    content = f.readlines()
                    m_dir = os.path.join(config['app_conf']['working_dir'], owner.home, project.name, tipology, calc_name, "input", "input_%s" %num_m)
                    print "********************MULTIJOB DIR**************************"
                    print m_dir
                    list_directory.append(m_dir)
                    try:
                        os.makedirs(m_dir)
                    except IOError, (errno, strerror):
                        h.flash.set_message('An error occurred during calculation creation.', 'Error')
                        h.redirect('/calculations/%s' % tipology)
                    new_ppdb = ll_multi.add(content)
                    #print new_ppdb
                    open(pdbo,"w").writelines(new_ppdb)
                    open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "amber_in_pre_leap_%s.pdb"%num_m),"w").writelines(new_ppdb)

                    os.environ["AMBER_HOME"] = "/prog/amber10"
                    amber_h_exe = "/prog/amber10/exe/"
                    leap_in = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "leap.in")
                    #leap_in = "leap1.in"
                    cmd = "%s/tleap -O -f %s "%(amber_h_exe, leap_in)
                    out_leap_s = os.popen(cmd).read()

                    if os.path.isfile(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb_solvent.pdb")):
                        shutil.copy(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb_solvent.pdb"),os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "amber_in_after_leap_%s.pdb"%num_m))
                    cmd = "%s/ambpdb -p %s < %s > %s"%(amber_h_exe, os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'),"prmtop"), os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'),"prmcrd"), os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'),"amber_in_after_leap_crd_%s.pdb"%num_m))
                    os.popen(cmd).read()

                    print out_leap_s

                    #print pdb2leap_ter

                    #ce_sub_list = app_globals.grid_req
                    ce_sub_list = self.checkGRID()

                    #GPU
                    if session["usegpu"]:
                        jdl = """[
executable = "run_amber.sh";
stdoutput = "std.out";
stderror = "std.err";
outputsandboxbasedesturi = "gsiftp://localhost";
inputsandbox = {"%s/in.tgz","%s/run_amber.sh"};
outputsandbox = {"std.out", "std.err","pro.tgz"};
    ]""" %(m_dir, m_dir)
                    #CPU
                    else:
                        jdl = """
Executable = "run_amber.sh";
StdOutput = "std.out";
StdError = "std.err";
VirtualOrganisation="enmr.eu";
InputSandbox = {"%s/in.tgz","%s/run_amber.sh"};
OutputSandbox = {"std.out", "std.err","pro.tgz"};
Requirements = %s
    """ %(m_dir, m_dir, ce_sub_list)

                    abs_fullpath = os.path.join(m_dir, "amber.jdl")
                    open(abs_fullpath,"w").write(jdl)
                    if session["usegpu"]:
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


#$DIRAE/sander -O -i sander.in -o sander.out -p prmtop -c prmcrd -r prm_out.crd
#$DIRAE/ambpdb -p prmtop < prm_out.crd > amber_final.pdb

tar cvfz pro.tgz ./* --exclude in.tgz --exclude run_amber.sh --exclude gettensor.pl

"""
                    elif session["useclo"]:
                        run_amber = """
#!/bin/bash
#
# amber_run.sh - This script is meant to run on Grid or Container
#

if ["$VO_ENMR_EU_SW_DIR" != "" ]; then
  echo "Running on Grid"
  /bin/uname -a | /bin/grep 'x86_64' > /dev/null && ARCH='64' || ARCH='32'
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/amber11/lib
  AMBERHOME=$VO_ENMR_EU_SW_DIR/CIRMMP/amber/11/$ARCH
  DIRAE=$AMBERHOME/exe/
else
  echo "Running on Container"
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/amber14/lib
  AMBERHOME=/usr/local/amber14
  DIRAE=$AMBERHOME/bin/
fi


tar xvfz in.tgz

#AMBER_COMMAND

#$DIRAE/sander -O -i sander.in -o sander.out -p prmtop -c prmcrd -r prm_out.crd
#$DIRAE/ambpdb -p prmtop < prm_out.crd > amber_final.pdb


tar cvfz pro.tgz ./* --exclude in.tgz --exclude run_amber.sh --exclude gettensor.pl
"""
                    else:
                         run_amber = """
#!/bin/bash
/bin/uname -a | /bin/grep 'x86_64' > /dev/null && ARCH='64' || ARCH='32'

if [ -d "$VO_ENMR_EU_SW_DIR/CIRMMP/amber/12/$ARCH" ]; then
AMBERHOME=$VO_ENMR_EU_SW_DIR/CIRMMP/amber/12/$ARCH
DIRAE=$AMBERHOME/bin/
else
AMBERHOME=$VO_ENMR_EU_SW_DIR/CIRMMP/amber/11/$ARCH
DIRAE=$AMBERHOME/exe/
fi

tar xvfz in.tgz


#AMBER_COMMAND


#$DIRAE/sander -O -i sander.in -o sander.out -p prmtop -c prmcrd -r prm_out.crd
#$DIRAE/ambpdb -p prmtop < prm_out.crd > amber_final.pdb

tar cvfz pro.tgz ./* --exclude in.tgz --exclude run_amber.sh --exclude gettensor.pl

# Notify end
echo "Done"

"""

                    abs_fullpath = os.path.join(m_dir, "run_amber.sh")
                    run_amber_post = []
                    for a in run_amber.split("\n"):
                        run_amber_post.append(a + "\n")
                        if "#AMBER_COMMAND" in a:
                            ct = 0
                            for i in list_input_sander:
                                ct = ct + 1
                                if ct == 1:
                                    if session["usegpu"]:
                                        run_amber_post.append("$DIRAE/pmemd.cuda -O -i %s -o %s -p prmtop -c prmcrd -r %s -ref  prmcrd \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-1) + ".crd"  ))
                                    else:
                                        run_amber_post.append("$DIRAE/sander -O -i %s -o %s -p prmtop -c prmcrd -r %s -ref  prmcrd \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-1) + ".crd"  ))

                                    run_amber_post.append("$DIRAE/ambpdb -p prmtop < %s > %s \n" %(i[:-4] + str(ct-1) + ".crd", "amber_final" + str(ct-1) + ".pdb"))
                                    run_amber_post.append("perl gettensor.pl sander0.out \n")
                                else:
                                    if session["usegpu"]:
                                        run_amber_post.append("$DIRAE/pmemd.cuda -O -i %s -o %s -p prmtop -c %s -r %s -ref  %s \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-2) + ".crd", i[:-4] + str(ct-1) + ".crd",i[:-4] + str(ct-2) + ".crd" ))
                                    else:
                                        run_amber_post.append("$DIRAE/sander -O -i %s -o %s -p prmtop -c %s -r %s -ref  %s \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-2) + ".crd", i[:-4] + str(ct-1) + ".crd",i[:-4] + str(ct-2) + ".crd" ))

                                    run_amber_post.append("$DIRAE/ambpdb -p prmtop < %s > %s \n" %(i[:-4] + str(ct-1) + ".crd", "amber_final" + str(ct-1) + ".pdb"))

                    open(abs_fullpath,"w").writelines(run_amber_post)

                    tar = tarfile.open(os.path.join(m_dir,"in.tgz"),"w:gz")
                    tar.add(os.path.join(config['app_conf']['amber_data'],"gettensor.pl"), arcname="gettensor.pl")
                    print os.path.join(config['app_conf']['amber_data'],"gettensor.pl")
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

#ELSE MULTIJOB

        else:

            num_m = 1
            pdir = os.path.join(config['app_conf']['working_dir'], owner.home, project.name, tipology, calc_name, "input", 'input_1')
            print pdir
            try:
                os.makedirs(pdir)
            except IOError, (errno, strerror):
                h.flash.set_message('An error occurred during calculation creation.', 'Error')
                h.redirect('/calculations/%s' % tipology)

            #ce_sub_list = app_globals.grid_req
            ce_sub_list = self.checkGRID()
            if session["usegpu"]:
                jdl = """[
executable = "run_amber.sh";
stdoutput = "std.out";
stderror = "std.err";
outputsandboxbasedesturi = "gsiftp://localhost";
inputsandbox = {"%s/in.tgz","%s/run_amber.sh"};
outputsandbox = {"std.out", "std.err","pro.tgz"};
    ]""" %(pdir, pdir)
                    #CPU
            else:
                jdl = """
Executable = "run_amber.sh";
StdOutput = "std.out";
StdError = "std.err";
VirtualOrganisation="enmr.eu";
InputSandbox = {"%s/in.tgz","%s/run_amber.sh"};
OutputSandbox = {"std.out", "std.err","pro.tgz"};
Requirements = other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-short";
#Requirements = %s
    """ %(pdir, pdir, ce_sub_list)

            abs_fullpath = os.path.join(pdir, "amber.jdl")
            open(abs_fullpath,"w").write(jdl)
            if session["usegpu"]:

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


#$DIRAE/sander -O -i sander.in -o sander.out -p prmtop -c prmcrd -r prm_out.crd
#$DIRAE/ambpdb -p prmtop < prm_out.crd > amber_final.pdb

tar cvfz pro.tgz ./* --exclude in.tgz --exclude run_amber.sh --exclude gettensor.pl

"""
            elif session["useclo"]:
                run_amber = """
#!/bin/bash
#
# amber_run.sh - This script is meant to run on Grid or Container
#

if ["$VO_ENMR_EU_SW_DIR" != "" ]; then
  echo "Running on Grid"
  /bin/uname -a | /bin/grep 'x86_64' > /dev/null && ARCH='64' || ARCH='32'
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/amber11/lib
  AMBERHOME=$VO_ENMR_EU_SW_DIR/CIRMMP/amber/11/$ARCH
  DIRAE=$AMBERHOME/exe/
else
  echo "Running on Container"
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/amber14/lib
  AMBERHOME=/usr/local/amber14
  DIRAE=$AMBERHOME/bin/
fi


tar xvfz in.tgz

#AMBER_COMMAND

#$DIRAE/sander -O -i sander.in -o sander.out -p prmtop -c prmcrd -r prm_out.crd
#$DIRAE/ambpdb -p prmtop < prm_out.crd > amber_final.pdb


tar cvfz pro.tgz ./* --exclude in.tgz --exclude run_amber.sh --exclude gettensor.pl

# Notify end
echo "Done"

"""

            else:
                run_amber = """
#!/bin/bash
/bin/uname -a | /bin/grep 'x86_64' > /dev/null && ARCH='64' || ARCH='32'

AMBERHOME=$VO_ENMR_EU_SW_DIR/CIRMMP/amber/PCS/$ARCH

DIRAE=$AMBERHOME/bin/

tar xvfz in.tgz


#AMBER_COMMAND


#$DIRAE/sander -O -i sander.in -o sander.out -p prmtop -c prmcrd -r prm_out.crd
#$DIRAE/ambpdb -p prmtop < prm_out.crd > amber_final.pdb

tar cvfz pro.tgz ./* --exclude in.tgz --exclude run_amber.sh --exclude gettensor.pl

"""
            abs_fullpath = os.path.join(pdir, "run_amber.sh")
            run_amber_post = []
            for a in run_amber.split("\n"):
                run_amber_post.append(a + "\n")
                if "#AMBER_COMMAND" in a:
                    ct = 0
                    for i in list_input_sander:
                        ct = ct + 1
                        if ct == 1:
                            if session["usegpu"]:
                                run_amber_post.append("$DIRAE/pmemd.cuda -O -i %s -o %s -p prmtop -c prmcrd -r %s -ref  prmcrd \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-1) + ".crd"  ))
                            else:
                                run_amber_post.append("$DIRAE/sander -O -i %s -o %s -p prmtop -c prmcrd -r %s -ref  prmcrd \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-1) + ".crd"  ))

                            run_amber_post.append("$DIRAE/ambpdb -p prmtop < %s > %s \n" %(i[:-4] + str(ct-1) + ".crd", "amber_final" + str(ct-1) + ".pdb"))
                            run_amber_post.append("perl gettensor.pl sander0.out \n")
                        else:
                            if session["usegpu"]:
                                run_amber_post.append("$DIRAE/pmemd.cuda -O -i %s -o %s -p prmtop -c %s -r %s -ref  %s \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-2) + ".crd", i[:-4] + str(ct-1) + ".crd",i[:-4] + str(ct-2) + ".crd" ))
                            else:
                               run_amber_post.append("$DIRAE/sander -O -i %s -o %s -p prmtop -c %s -r %s -ref  %s \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-2) + ".crd", i[:-4] + str(ct-1) + ".crd",i[:-4] + str(ct-2) + ".crd" ))

                            run_amber_post.append("$DIRAE/ambpdb -p prmtop < %s > %s \n" %(i[:-4] + str(ct-1) + ".crd", "amber_final" + str(ct-1) + ".pdb"))


            open(abs_fullpath,"w").writelines(run_amber_post)

            tar = tarfile.open(os.path.join(pdir,"in.tgz"),"w:gz")
            tar.add(os.path.join(config['app_conf']['amber_data'],"gettensor.pl"), arcname="gettensor.pl")
            print os.path.join(config['app_conf']['amber_data'],"gettensor.pl")
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

        if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.tar")):
            os.remove(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.tar"))
        if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.zip")):
            os.remove(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.zip"))
        # Submit job
        id = '%s_%s_0' % (new_calc.id, prj_id)
        h.redirect('/jobs/job_submit/%s' % id)

    @check_access('Run Jobs')
    def job_prepareXA(self):
        '''Prepare a job for submission

        steps:
        a) check for the calculation existance
        b) directory creation
        c) database new calculation entry creation
        d) put data into new directory
        e) start job
        '''
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

        #grid_req = """( other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-long" || other.GlueCEUniqueID == "ce01.dur.scotgrid.ac.uk:2119/jobmanager-lcgpbs-q6h" );"""
        #grid_req = """other.GlueCEPolicyMaxCPUTime > 2000 && (other.GlueCEInfoHostName == "deimos.htc.biggrid.nl" || other.GlueCEInfoHostName == "trekker.nikhef.nl" ||  other.GlueCEInfoHostName == "pbs-enmr.cerm.unifi.it" || other.GlueCEInfoHostName == "gazon.nikhef.nl" || other.GlueCEInfoHostName == "ce-enmr.chemie.uni-frankfurt.de" || other.GlueCEInfoHostName == "ce-enmr.chem.uu.nl" );"""
        #grid_req = """other.GlueCEPolicyMaxCPUTime > 2000 && (other.GlueCEInfoHostName == "deimos.htc.biggrid.nl" || other.GlueCEInfoHostName == "trekker.nikhef.nl"  || other.GlueCEInfoHostName == "gazon.nikhef.nl" || other.GlueCEInfoHostName == "ce-enmr.chemie.uni-frankfurt.de" || other.GlueCEInfoHostName == "ce-enmr.chem.uu.nl" );"""
        #prj_id = request.POST.get('prj_id')
        #prj_id = rrr #prendere da xml nome progetto
        calc_name = request.POST.get('name')
        #if session['PORTAL'] == 'amps-nmr':
        tipology = 'amber'
        #else:
        #    tipology = session['PORTAL']
        #tipology = request.POST.get('tipology')
        #multij = request.POST.get('multij')
        #if multij == "on":
        multi_job = True
        #else:
        #    multi_job = False

        xml_XA = etree.parse(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"XA.xml"))
        xml_XA_r = xml_XA.getroot()
        project_name = xml_XA_r.xpath("//info/xplor-calculation/project")[0].get("name")
        #numStep = request.POST.get('step')
        #numStep = ee # prendere da xml in dirache
        #print "step %s" %numStep
        #list_input_sander = list()
        #for i in range(0, int(numStep)):
        #    list_input_sander.append("sander"+str(i)+".in")
        #print "###############List of Amber .in files###############"
        #print list_input_sander
        #print "numStep"
        #print numStep
        #print "#####################################################"
        #
        calc_name = calc_name.replace(' ', '_')
        owner = Session.query(Users).get(session['REMOTE_USER'])
        project = Session.query(Projects).filter(Projects.name == project_name).first()
        calc_type = Session.query(CalculationTipology).filter(CalculationTipology.tipology == "amps-nmr").first()

        prj_id = project.id
        #cname = Session.query(Calculations).filter(and_(Calculations.name==calc_name, Calculations.project_id==int(prj_id))).first()
        #
        ## Check the existance of the calculation
        #if cname:
        #    h.flash.set_message('Calculation name already exists', 'Error')
        #    h.redirect('/calculations/%s' % tipology)

        # Directory creation
        if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.tgz")):
            #multi_job = True
            if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.tgz")):
                multi = tarfile.open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.tgz"),"r:gz")
        #else:
        #    multi_job = False
        print "######### EVALUATE MULTI_JOB ##################"
        if multi_job:
            print "################# MULTI_JOB TRUE ##########################"
            list_directory = []
            pdir = os.path.join(config['app_conf']['working_dir'], owner.home, project.name, tipology, calc_name)
            print pdir
            try:
                os.makedirs(pdir)
            except IOError, (errno, strerror):
                h.flash.set_message('An error occurred during calculation creation.', 'Error')
                h.redirect('/calculations/%s' % tipology)

            num_m = 0

            pdbo = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "amber_in.pdb")
            pdb_Am = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "out_leap.pdb")
            n_crd = os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "prmcrd")
            ll_multi = multi_input(pdbo, pdb_Am, n_crd)

            print "############MEMBERSNAME###############"
            for member in multi.getmembers():
                print member.name

            for member in multi.getmembers():
                if member.name[-4:] == ".pdb":
                    if "pdb_" in member.name  and member.name.split("pdb_")[1][:-4].isdigit():
                        num_m = member.name.split("pdb_")[1][:-4]
                    else:
                        num_m = member.name[:-4]
                    #num_m += 1
                    f = multi.extractfile(member)
                    content = f.readlines()
                    m_dir = os.path.join(config['app_conf']['working_dir'], owner.home, project.name, tipology, calc_name, "input", "input_%s" %num_m)
                    print "********************MULTIJOB DIR**************************"
                    print m_dir
                    list_directory.append(m_dir)
                    try:
                        os.makedirs(m_dir)
                    except IOError, (errno, strerror):
                        h.flash.set_message('An error occurred during calculation creation.', 'Error')
                        h.redirect('/calculations/%s' % tipology)
                    new_ppdb = ll_multi.add(content)
                    #print new_ppdb
                    open(pdbo,"w").writelines(new_ppdb)
                    open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "amber_in_pre_leap_%s.pdb"%num_m),"w").writelines(new_ppdb)

                    os.environ["AMBER_HOME"] = "/prog/amber10"
                    amber_h_exe = "/prog/amber10/exe/"
                    current_path = os.getcwd()
                    print current_path
                    leap_in = os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "leap.in")
                    #leap_in = "leap1.in"
                    os.chdir(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE')))
                    cmd = "%s/tleap -O -f %s "%(amber_h_exe, leap_in)
                    out_leap_s = os.popen(cmd).read()
                    os.chdir(current_path)

                    if os.path.isfile(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb_solvent.pdb")):
                        shutil.copy(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "pdb_solvent.pdb"),os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), "amber_in_after_leap_%s.pdb"%num_m))
                    cmd = "%s/ambpdb -p %s < %s > %s"%(amber_h_exe, os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'),"prmtop"), os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'),"prmcrd"), os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'),"amber_in_after_leap_crd_%s.pdb"%num_m))
                    os.popen(cmd).read()

                    print out_leap_s

                    #print pdb2leap_ter

                    #change tensor v

                    #ce_sub_list = app_globals.grid_req
                    ce_sub_list = self.checkGRID()
                    if session["usegpu"]:
                        jdl = """[
executable = "run_amber.sh";
stdoutput = "std.out";
stderror = "std.err";
outputsandboxbasedesturi = "gsiftp://localhost";
inputsandbox = {"%s/in.tgz","%s/run_amber.sh"};
outputsandbox = {"std.out", "std.err","pro.tgz"};
    ]""" %(m_dir, m_dir)
                    #CPU
                    else:
                        jdl = """
Executable = "run_amber.sh";
StdOutput = "std.out";
StdError = "std.err";
VirtualOrganisation="enmr.eu";
InputSandbox = {"%s/in.tgz","%s/run_amber.sh"};
OutputSandbox = {"std.out", "std.err","pro.tgz"};
Requirements = other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-short";
#Requirements = %s
    """ %(m_dir, m_dir, ce_sub_list)

                    abs_fullpath = os.path.join(m_dir, "amber.jdl")
                    open(abs_fullpath,"w").write(jdl)
#                    run_amber = """
##!/bin/bash
#/bin/uname -a | /bin/grep 'x86_64' > /dev/null && ARCH='64' || ARCH='32'
#
#AMBERHOME=$VO_ENMR_EU_SW_DIR/CIRMMP/amber/11/$ARCH
#
#DIRAE=$AMBERHOME/exe/
#
#tar xvfz in.tgz
#
#
##AMBER_COMMAND
#
#
##$DIRAE/sander -O -i sander.in -o sander.out -p prmtop -c prmcrd -r prm_out.crd
##$DIRAE/ambpdb -p prmtop < prm_out.crd > amber_final.pdb
#
#tar cvfz pro.tgz ./* --exclude in.tgz --exclude run_amber.sh --exclude gettensor.pl
#
#"""
#                    abs_fullpath = os.path.join(m_dir, "run_amber.sh")
#                    run_amber_post = []
#                    for a in run_amber.split("\n"):
#                        run_amber_post.append(a + "\n")
#                        if "#AMBER_COMMAND" in a:
#                            ct = 0
#                            for i in list_input_sander:
#                                ct = ct + 1
#                                if ct == 1:
#                                    run_amber_post.append("$DIRAE/sander -O -i %s -o %s -p prmtop -c prmcrd -r %s -ref  prmcrd \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-1) + ".crd"  ))
#                                    run_amber_post.append("$DIRAE/ambpdb -p prmtop < %s > %s \n" %(i[:-4] + str(ct-1) + ".crd", "amber_final" + str(ct-1) + ".pdb"))
#                                    run_amber_post.append("perl gettensor.pl sander0.out \n")
#                                else:
#                                    run_amber_post.append("$DIRAE/sander -O -i %s -o %s -p prmtop -c %s -r %s -ref  %s \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-2) + ".crd", i[:-4] + str(ct-1) + ".crd",i[:-4] + str(ct-2) + ".crd" ))
#                                    run_amber_post.append("$DIRAE/ambpdb -p prmtop < %s > %s \n" %(i[:-4] + str(ct-1) + ".crd", "amber_final" + str(ct-1) + ".pdb"))
#
#                    open(abs_fullpath,"w").writelines(run_amber_post)
                    shutil.copy(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), "run_amber.sh"),os.path.join(m_dir, "run_amber.sh"))
                    tar = tarfile.open(os.path.join(m_dir,"in.tgz"),"w:gz")
                    tar.add(os.path.join(config['app_conf']['amber_data'],"gettensor.pl"), arcname="gettensor.pl")
                    print os.path.join(config['app_conf']['amber_data'],"gettensor.pl")
                    tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"prmcrd"), arcname="prmcrd")
                    tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"prmtop"), arcname="prmtop")
                    if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in")):
                        tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in"),arcname="allNOE_allDIH.in")
                    if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"PCS.in")):
                        pcs_file_r = open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"PCS.in"),"r").readlines()
                        #change any pcs values to fantall fitting
                        new_pcs_file =[]
                        diz_pcs = {}
                        print ""
                        for iz in xml_XA_r.xpath("//pcsinfo/pcsfile"):
                            pcsnum = iz.get("PCSnumber")
                            for i in xml_XA_r.getiterator():
                                if i.tag == "pdbfile":
                                    if i.attrib["model"] == num_m:
                                        diz_pcs[pcsnum] = {}
                                        diz_pcs[pcsnum]["theta"] = i.attrib["theta"]
                                        diz_pcs[pcsnum]["phi"] = i.attrib["phi"]
                                        diz_pcs[pcsnum]["omega"] = i.attrib["omega"]
                                        diz_pcs[pcsnum]["a1"] = i.attrib["a1"]
                                        diz_pcs[pcsnum]["a2"] = i.attrib["a2"]

                        for z in pcs_file_r:
                            if "opttet" in z:
                                new_pcs_file.append(z.split("=")[0]+"=%s, \n" %diz_pcs[z.split(")")[0][-1]]["theta"])
                            elif "optomg" in z:
                                new_pcs_file.append(z.split("=")[0]+"=%s, \n" %diz_pcs[z.split(")")[0][-1]]["omega"])
                            elif "optphi" in z:
                                new_pcs_file.append(z.split("=")[0]+"=%s, \n" %diz_pcs[z.split(")")[0][-1]]["phi"])
                            elif "opta1" in z:
                                new_pcs_file.append(z.split("=")[0]+"=%s, \n" %diz_pcs[z.split(")")[0][-1]]["a1"])
                            elif "opta2" in z:
                                new_pcs_file.append(z.split("=")[0]+"=%s, \n" %diz_pcs[z.split(")")[0][-1]]["a2"])
                            else:
                                new_pcs_file.append(z)

                        open(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"PCS.in"),"w").writelines(new_pcs_file)

                        tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"PCS.in"),arcname="PCS.in")
                    if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allRDC.in")):
                        tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allRDC.in"),arcname="allRDC.in")
                    for i in glob.glob(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"sander*.in")):
                        tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), i), arcname=os.path.basename(i))
                    tar.close()

#ELSE MULTIJOB

#        else:
#
#            num_m = 1
#            pdir = os.path.join(config['app_conf']['working_dir'], owner.home, project.name, tipology, calc_name, "input", 'input_1')
#            print pdir
#            try:
#                os.makedirs(pdir)
#            except IOError, (errno, strerror):
#                h.flash.set_message('An error occurred during calculation creation.', 'Error')
#                h.redirect('/calculations/%s' % tipology)
#
#            #ce_sub_list = app_globals.grid_req
#            ce_sub_list = self.checkGRID()
#            jdl = """
#Executable = "run_amber.sh";
#StdOutput = "std.out";
#StdError = "std.err";
#VirtualOrganisation="enmr.eu";
#InputSandbox = {"%s/in.tgz","%s/run_amber.sh"};
#OutputSandbox = {"std.out", "std.err","pro.tgz"};
#Requirements = %s
#    """ %(pdir, pdir, ce_sub_list)
#
#            abs_fullpath = os.path.join(pdir, "amber.jdl")
#            open(abs_fullpath,"w").write(jdl)
#
#            run_amber = """
##!/bin/bash
#/bin/uname -a | /bin/grep 'x86_64' > /dev/null && ARCH='64' || ARCH='32'
#
#AMBERHOME=$VO_ENMR_EU_SW_DIR/CIRMMP/amber/11/$ARCH
#
#DIRAE=$AMBERHOME/exe/
#
#tar xvfz in.tgz
#
#
##AMBER_COMMAND
#
#
##$DIRAE/sander -O -i sander.in -o sander.out -p prmtop -c prmcrd -r prm_out.crd
##$DIRAE/ambpdb -p prmtop < prm_out.crd > amber_final.pdb
#
#tar cvfz pro.tgz ./* --exclude in.tgz --exclude run_amber.sh --exclude gettensor.pl
#
#"""
#            abs_fullpath = os.path.join(pdir, "run_amber.sh")
#            run_amber_post = []
#            for a in run_amber.split("\n"):
#                run_amber_post.append(a + "\n")
#                if "#AMBER_COMMAND" in a:
#                    ct = 0
#                    for i in list_input_sander:
#                        ct = ct + 1
#                        if ct == 1:
#                            run_amber_post.append("$DIRAE/sander -O -i %s -o %s -p prmtop -c prmcrd -r %s -ref  prmcrd \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-1) + ".crd"  ))
#                            run_amber_post.append("$DIRAE/ambpdb -p prmtop < %s > %s \n" %(i[:-4] + str(ct-1) + ".crd", "amber_final" + str(ct-1) + ".pdb"))
#                            run_amber_post.append("perl gettensor.pl sander0.out \n")
#                        else:
#                            run_amber_post.append("$DIRAE/sander -O -i %s -o %s -p prmtop -c %s -r %s -ref  %s \n" %(i, "sander" + str(ct-1) + ".out", i[:-4] + str(ct-2) + ".crd", i[:-4] + str(ct-1) + ".crd",i[:-4] + str(ct-2) + ".crd" ))
#                            run_amber_post.append("$DIRAE/ambpdb -p prmtop < %s > %s \n" %(i[:-4] + str(ct-1) + ".crd", "amber_final" + str(ct-1) + ".pdb"))
#
#
#            open(abs_fullpath,"w").writelines(run_amber_post)
#
#            tar = tarfile.open(os.path.join(pdir,"in.tgz"),"w:gz")
#            tar.add(os.path.join(config['app_conf']['amber_data'],"gettensor.pl"), arcname="gettensor.pl")
#            print os.path.join(config['app_conf']['amber_data'],"gettensor.pl")
#            tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"prmcrd"), arcname="prmcrd")
#            tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"prmtop"), arcname="prmtop")
#            if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in")):
#                tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allNOE_allDIH.in"),arcname="allNOE_allDIH.in")
#            if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"PCS.in")):
#                tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"PCS.in"),arcname="PCS.in")
#            if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allRDC.in")):
#                tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"allRDC.in"),arcname="allRDC.in")
#            for i in list_input_sander:
#                tar.add(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'), i), arcname=i)
#            tar.close()

        # New database entry creation
        new_calc = Calculations()
        new_calc.name = calc_name
        new_calc.project = project
        new_calc.calc_type = calc_type
        new_calc.creation_date = datetime.now()
        new_calc.jobs_to_submit = num_m
        Session.add(new_calc)
        Session.commit()

        if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.tar")):
            os.remove(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.tar"))
        if os.path.isfile(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.zip")):
            os.remove(os.path.join(config['app_conf']['amber_data'],session.get('DIR_CACHE'),"multijobs.zip"))
        # Submit job
        id = '%s_%s_0' % (new_calc.id, prj_id)
        h.redirect('/jobs/job_submit/%s' % id)
