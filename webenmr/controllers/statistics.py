import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config
from webenmr.lib.base import BaseController, render

from webenmr.model import Projects, Calculations, Jobs, CalculationTipology, Users
import os
from webenmr.model.meta import Session
from sqlalchemy.sql import and_
from datetime import datetime, date, time
from dateutil import parser

log = logging.getLogger(__name__)

class StatisticsController(BaseController):
    def __before__(self):
        """
        This __before__ method calls the parent method, and then sets up the
        tabs on the page.
        """
        c.page_base = u'Statistics'
        c.page_title = u'Portal statistics'
        
        
    def index(self):
        # Return a rendered template
        #return render('/statistics.mako')
        # or, return a string
        self.statDB(1)
        AMPSStartDate = date(2012, 11, 01)
        c.stringResults = self.stat3({'amber': 2}, AMPSStartDate)
        weNMRStartDate = date(2010, 11, 01)
        #c.stringResults2 = self.stat({'amber': 2}, weNMRStartDate)
        
        c.stringResults2 = self.stat({'amber': 2}, weNMRStartDate)
        
        return render('/statistics/stathome.mako')
    
    def index2(self):
        # Return a rendered template
        #return render('/statistics.mako')
        # or, return a string
        
        AMPSStartDate = date(2012, 11, 01)
        c.stringResults = self.stat3({'xplor': 1}, AMPSStartDate)
        weNMRStartDate = date(2010, 11, 01)
        #c.stringResults2 = self.stat({'amber': 2}, weNMRStartDate)
        
        c.stringResults2 = self.stat({'xplor': 2}, weNMRStartDate)
        
        return render('/statistics/stathome.mako')
    
    def index3(self):
        # Return a rendered template
        #return render('/statistics.mako')
        # or, return a string
        
        AMPSStartDate = date(2012, 11, 01)
        c.stringResults = self.stat3({'maxocc': 5}, AMPSStartDate)
        weNMRStartDate = date(2010, 11, 01)
        #c.stringResults2 = self.stat({'amber': 2}, weNMRStartDate)
        
        c.stringResults2 = self.stat({'maxocc': 5}, weNMRStartDate)
        
        return render('/statistics/stathome.mako')
    
    def stat(self, portals, dt):
        #portals = {'amber': 2, 'xplor': 1, 'maxocc' : 5}
        #portals = {'amber': 2}
        
        htmlcode = ''
        for pkey in portals.keys():
            #print pkey

            tot_users = 0
            tot_activeUsers = 0
            tot_runs = 0
            tot_runsForUser = {} #user->runs
            tot_jobs = 0
            
            users_list = Session.query(Users).all()
            #print portals[pkey] 
            #print "UTENTI %d" %len(users_list)
            
            for u in users_list:
                portalUser = False
                projects_list = Session.query(Projects).filter(and_(Projects.owner_id==u.id)).all()
                if projects_list:
                    active = False
                    for p in projects_list:
                        calculations_list = Session.query(Calculations).filter(and_(Calculations.project_id==p.id, Calculations.calc_type_id == portals[pkey], Calculations.creation_date >= dt)).all()
                        if calculations_list:
                            if not active:
                                active = True
                                tot_activeUsers += 1
                                tot_users += 1
                                portalUser = True
                            tot_runs += len(calculations_list)
                            if tot_runsForUser.has_key(u.id):
                                tot_runsForUser[u.id] += len(calculations_list)
                            else:
                                tot_runsForUser[u.id] = len(calculations_list)
                            for c in calculations_list:
                                tot_jobs += int(c.jobs_to_submit)
                        if not portalUser:
                            tot_users += 1
                            portalUser = True
                            
            htmlcode += '<ul>'
            htmlcode += '<li>number of registered users: <b>%d</b></li>' %tot_users
            htmlcode += '<li>number of active users (those who have run at least one job): <b>%d</b></li>' %tot_activeUsers
            htmlcode += '<li>total number of runs: <b>%d</b></li>' %tot_runs
            htmlcode += '<li>an estimate of the number of grid jobs corresponding to one "run": <b>%d</b></li>' % (tot_jobs/tot_runs)
            userlist = '<ul>'
            for r in tot_runsForUser.keys():
                userlist += "<li>user_%d - <b>%d</b></li>" %(r ,tot_runsForUser[r])
            userlist += '</ul>'
            htmlcode += '<li>number of runs per user: %s</li>' %userlist
            htmlcode += '</ul>'
            
            return htmlcode
            #print tot_users
            #print tot_activeUsers
            #print tot_runs
            #tot = 0
            #
            #print len(tot_runsForUser)
            #print tot
            #print tot_jobs
                                
    def stat2(self):
        tot_users = 0
        tot_activeUsers = 0
        tot_runs = 0
        tot_runsForUser = {} #user->runs
        tot_jobs = 0
        jobs_user = {}
        users_list = Session.query(Users).all()
        for u in users_list:
                portalUser = False
                projects_list = Session.query(Projects).filter(and_(Projects.owner_id==u.id)).all()
                jobs = []
                if projects_list:
                    active = False
                    for p in projects_list:
                        calculations_list = Session.query(Calculations).filter(and_(Calculations.project_id==p.id, Calculations.calc_type_id == 2)).all()
                        if calculations_list:
                            for c in calculations_list:
                                jobs_list = Session.query(Jobs).filter(and_(Jobs.calculation_id==c.id)).all()
                                if jobs_list:
                                    for j in jobs_list:
                                        if j.start_date:
                                            jobs.append(j.start_date.strftime("%A %d %B %Y %I:%M:%S%p"))
                    jobs_user[u.email] = jobs
        print jobs_user
        opnfl = open(os.path.join(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), 'statJobUser.txt')), 'w')
        for k in jobs_user:
            if k:
                opnfl.write('****'+k+'\n')
                if jobs_user[k]:
                    opnfl.write('\n'.join(jobs_user[k]))
                    opnfl.write('\n')
                else:
                    opnfl.write('[no jobs]\n')
        opnfl.close()
                     

    def stat3(self, portals, dt):
        #portals = {'amber': 2, 'xplor': 1, 'maxocc' : 5}
        #portals = {'amber': 2}
        
        htmlcode = ''
        users_list = Session.query(Users).all()
        for pkey in portals.keys():
            #print pkey

            tot_users = 0
            tot_activeUsers = 0
            tot_runs = 0
            tot_runsForUser = {} #user->runs
            tot_jobs = 0
            
            
            for u in users_list:
                portalUser = False
                projects_list = Session.query(Projects).filter(and_(Projects.owner_id==u.id)).all()
                if projects_list:
                    active = False
                    for p in projects_list:
                        calculations_list = Session.query(Calculations).filter(and_(Calculations.project_id==p.id, Calculations.calc_type_id == portals[pkey], Calculations.creation_date >= dt)).all()
                        if calculations_list:
                            if not active:
                                active = True
                                tot_activeUsers += 1
                                tot_users += 1
                                portalUser = True
                            tot_runs += len(calculations_list)
                            if tot_runsForUser.has_key(u.id):
                                tot_runsForUser[u.id] += len(calculations_list)
                            else:
                                tot_runsForUser[u.id] = len(calculations_list)
                            for c in calculations_list:
                                tot_jobs += int(c.jobs_to_submit)
                        if not portalUser:
                            tot_users += 1
                            portalUser = True
                            
            htmlcode += '<ul>'
            htmlcode += '<li>number of registered users: <b>%d</b> (%d)</li>' %(tot_users, len(users_list))
            htmlcode += '<li>number of active users (those who have run at least one job): <b>%d</b></li>' %tot_activeUsers
            htmlcode += '<li>total number of runs: <b>%d</b></li>' %tot_runs
            htmlcode += '<li>an estimate of the number of grid jobs corresponding to one "run": <b>%d</b></li>' % (tot_jobs/tot_runs)
            userlist = '<ul>'
            for r in tot_runsForUser.keys():
                userlist += "<li>user_%d - <b>%d</b></li>" %(r ,tot_runsForUser[r])
            userlist += '</ul>'
            htmlcode += '<li>number of runs per user: %s</li>' %userlist
            htmlcode += '</ul>'
            
            return htmlcode
    def stat5(self):

        """ dal db di jobcontroll
            
            sqlite> .mode list
            sqlite> .separator |
            sqlite> .output test_file_1.txt
            sqlite> select project_name,start_date from jobs;
        """
        jobco_fi = open("/home/webtest/WebENMR/data/temp/maxocc.txt", "r").readlines()
        jobco = []
        #jobco contain calculation name and date if submittion
        for i in jobco_fi:
            jobco.append((i.split("|")[0], i.split("|")[1]))
            
        tot_users = 0
        tot_activeUsers = 0
        tot_runs = 0
        tot_runsForUser = {} #user->runs
        tot_jobs = 0
        jobs_user = {}
        users_list = Session.query(Users).all()
        for u in users_list:
                portalUser = False
                projects_list = Session.query(Projects).filter(and_(Projects.owner_id==u.id)).all()
                jobs = []
                if projects_list:
                    active = False
                    for p in projects_list:
                        calculations_list = Session.query(Calculations).filter(and_(Calculations.project_id==p.id, Calculations.calc_type_id == 5, Calculations.creation_date >= dt)).all()
                        if calculations_list:
                            for c in calculations_list:
                                for z in jobco:
                                    if c.name == z[0]:
                                        print "trovato" + z[0]
                                        jobs.append(parser.parse(z[1]).strftime("%A %d %B %Y %I:%M:%S%p"))
                                    
                                
                                #jobs_list = Session.query(Jobs).filter(and_(Jobs.calculation_id==c.id)).all()
                                #if jobs_list:
                                #    for j in jobs_list:
                                #        if j.start_date:
                                           # jobs.append(j.start_date.strftime("%A %d %B %Y %I:%M:%S%p"))
                                           
                    jobs_user[u.email] = jobs
        print jobs_user
        opnfl = open("/home/webenmr/WebENMR/data/temp/statJobUsermaxocc.txt", "w")
        #opnfl = open(os.path.join(config['app_conf']['amber_data'], session.get('DIR_CACHE'), 'statJobUsermaxocc.txt'), 'w')
        opnfl.write(str(len(jobs_user))+'\n')
        totjobs = 0
        for k in jobs_user:
            if k:
                totjobs = totjobs + len(jobs_user[k])
        opnfl.write(str(totjobs))
        
        #for k in jobs_user:
        #    if k:
        #        opnfl.write('****'+k+'\n')
        #        if jobs_user[k]:
        #            opnfl.write('\n'.join(jobs_user[k]))
        #            opnfl.write('\n')
        #        else:
        #            opnfl.write('[no jobs]\n')
        opnfl.close()
        
    def statDB(self, portal):
        #portals = {'amber': 2, 'xplor': 1, 'maxocc' : 5}
        dt = date(2013, 8, 01)
        #users_list = []
        #users_list.append({337: 337})
        #users_list.append({5: 10})
        
        pippo = '''| /O=dutchgrid/O=users/O=universiteit-utrecht/OU=chem/CN=Alexandre Bonvin                   |    3 |
| /O=dutchgrid/O=users/O=universiteit-utrecht/OU=chem/CN=Adrien Samuel Jacky Melquiond      |   12 |
| /C=IT/O=INFN/OU=Personal Certificate/L=CIRMMP/CN=Andrea Giachetti                         |   16 |
| /C=DE/O=GermanGrid/OU=UniFrankfurt/CN=Peter Guentert                                      |   23 |
| /O=dutchgrid/O=users/O=universiteit-utrecht/OU=chem/CN=Nuno Loureiro Ferreira             |   45 |
| /C=TW/O=AS/OU=GRID/CN=SHU-JU HSIEH 692179                                                 |  273 |
| /C=TW/O=AS/OU=GRID/CN=Pomin Shih 933244                                                   |  274 |
| /C=TW/O=AS/OU=GRID/CN=Steve Yu 741725                                                     |  577 |
| /DC=org/DC=doegrids/OU=People/CN=yazan akkam 321744                                       |  586 |
| /C=IT/O=INFN/OU=Personal Certificate/L=CIRMMP/CN=Linda Cerofolini                         |  609 |
| /C=IT/O=INFN/OU=Personal Certificate/L=CIRMMP/CN=Daniela Lalli                            |  611 |
| /C=TW/O=AS/OU=GRID/CN=Chia-Cheng Chou 142039                                              |  618 |
| /C=TW/O=AS/OU=GRID/CN=Iren Wang 953069                                                    |  649 |
| /C=TW/O=AS/OU=GRID/CN=Chih-Ta Henry Chien 856297                                          |  650 |
| /C=PL/O=GRID/O=AMU/CN=Malgorzata Szelag                                                   |  651 |
| /C=TW/O=AS/OU=GRID/CN=Chung-ke Chang 238145                                               |  657 |
| /C=TW/O=AS/OU=GRID/CN=Yu Chiang Pan 837647                                                |  667 |
| /C=TW/O=AS/OU=GRID/CN=Yuan-Chao Lou 498134                                                |  671 |
| /C=TW/O=NCU/OU=GRID/CN=KUANFU Lin 558253                                                  |  674 |
| /C=TW/O=AS/OU=GRID/CN=Hsin-Yen Chen 132111                                                |  684 |
| /DC=com/DC=DigiCert-Grid/O=Open Science Grid/OU=People/CN=Jeffrey Lee 1225                |  723 |
| /DC=com/DC=DigiCert-Grid/O=Open Science Grid/OU=People/CN=Valjean Raiden Bacot-Davis 1321 |  744 |
| /C=DE/O=GermanGrid/OU=UniFrankfurt/CN=Nina Alexandra Christ                               |  858 |
| /DC=IN/DC=GARUDAINDIA/O=C-DAC/OU=CTSF/CN=SRINIDHI R (srinidhira@gmail.com)                |  859 |
| /DC=IN/DC=GARUDAINDIA/O=C-DAC/OU=CTSF/CN=Biswajit Gorai (biswajit@scbt.sastra.edu)        |  885 |
| /DC=com/DC=DigiCert-Grid/O=Open Science Grid/OU=People/CN=Oren Rosenberg 1688             |  893 |
| /DC=IN/DC=GARUDAINDIA/O=C-DAC/OU=CTSF/CN=Surajit Debnath (surajit03@yahoo.co.in)          |  894 |
| /C=TW/O=AP/OU=GRID/CN=Mukesh Mahajan 127570                                               |  988 |
| /O=GRID-FR/C=FR/O=CNRS/OU=IMOPA/CN=Benjamin Chagot                                        | 1024 |
| /C=IT/O=INFN/OU=Personal Certificate/L=CIRMMP/CN=Lucio Ferella                        |   67 | 
| /C=UK/O=eScience/OU=Oxford/L=OeSC/CN=jonathan elegheert                                   | 1080 |'''

        diz ={}        
        for i in pippo.split("\n"):
            if len(i) > 1:
                b = i.split("|")
                diz[b[1].strip()] = b[2].strip()
            
        opnfl = open("/home/webenmr/WebENMR/data/temp/statXplorDB.txt", "w")
        for u in diz.keys():
                #portalUser = False
                user = Session.query(Users).filter(and_(Users.dn==u)).first()
                if user:
                    print "-" + u + "-"
                    projects_list = Session.query(Projects).filter(and_(Projects.owner_id==user.id)).all()
                    jobs = []
                    if projects_list:
                        #active = False
                        for p in projects_list:
                            calculations_list = Session.query(Calculations).filter(and_(Calculations.project_id==p.id, Calculations.calc_type_id == portal, Calculations.creation_date >= dt)).all()
                            if calculations_list:
                                for c in calculations_list:
                                    jobs_list = Session.query(Jobs).filter(and_(Jobs.calculation_id==c.id, Jobs.status == 'E')).all()
                                    if jobs_list:
                                        for j in jobs_list:
                                            opnfl.write("INSERT INTO ssoxs_amber_stats(uid, jid, sdate, fdate, ip, country, status, message) VALUES("+diz[u]+", "+str(j.id)+", "+j.running_date.strftime('%s')+", "+j.done_date.strftime('%s')+", '150.217.163.184', 'XX', 5, "");\n")
        opnfl.close()