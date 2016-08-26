import logging
import os
import tarfile
from mimetypes import guess_type
from datetime import datetime
from sqlalchemy.sql import and_
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config
import pycurl
from operator import itemgetter, attrgetter
#from collections import defaultdict
from webenmr.lib.base import *
from webenmr.lib import files
from webenmr.lib import return_values
#from webenmr.lib.xplor_analysis import *
from webenmr.model import Projects, Users, CalculationTipology, Jobs, Calculations
from webenmr.lib.base import BaseController, render
import subprocess
import cgi
import hashlib
#import simplejson
import mimetypes
import re
import shutil
import sys
import time

log = logging.getLogger(__name__)

class FilemanagerController(BaseController):

     def __before__(self):
          """
          This __before__ method calls the parent method, and then sets up the
          tabs on the page.
          """
          
          #BaseController.__before__(self)
          
          c.page_base = u'Filemanager'
          #if 'REMOTE_USER' in session:
          #    c.current_user = Session.query(Users).get(session['REMOTE_USER'])
          #    c.main_menu = Session.query(Menu).filter(and_(Menu.parent_id==None, Menu.sibling_id==None)).order_by(Menu.weight.asc()).all()
          c.page_title = u'Filemanager'
          #cert = os.path.join(config['app_conf']['cert_dir'], 'x509up_u0')
          #os.environ['X509_USER_PROXY'] = cert

     def __init__(self):
          projects = Session.query(Projects).filter(and_(Projects.owner_id == session['REMOTE_USER'], Projects.removed == False)).all()
          c.dirlist = sorted(projects, key=attrgetter('name'))
          #print session['PORTAL']
          #calc_type = Session.query(CalculationTipology).filter(CalculationTipology.tipology == session['PORTAL']).first()
          #calcs = Session.query(Calculations).filter(and_(Calculations.calc_type_id == calc_type.id, Calculations.removed == False)).subquery()
          #_proj = Session.query(Projects, calcs.c.project_id).filter(and_(Projects.owner_id == session['REMOTE_USER'], Projects.removed == False))\
          #.outerjoin((calcs, Projects.id == calcs.c.project_id)).order_by(Projects.name).all()
          #projects = [_proj[i][0] for i in  range(len(_proj)) if _proj[i][1]]
          c.dirlisttot = len(projects)
          #c.dirlist = projects
          #RESTITUIRE LA DIM ESATTA
          owner = Session.query(Users).get(session['REMOTE_USER'])
          home = owner.home
          #pdir = os.path.join(config['app_conf']['working_dir'], owner.home)
          #dirsize = 0
          #for i in projects:
          #     pdir = os.path.join(config['app_conf']['working_dir'], home, i.name)
          #     (filetype, perms, owner, group, size, mtime) = files.get_fileinfo(pdir, 0, 1)
          #     dirsize = dirsize + size
          #c.dirlistsize = str(h.pretty_size(dirsize))

     def index(self):
          # Return a rendered template
          #return render('/filemanager.mako')
          # or, return a response
          #abort(505, 'Internal SE')
          return render('/filesystem/finder.mako')
     
     
     def xploramber(self):
        path = request.POST.get("path").replace("Projects/", "")
        prj = path.split("/")[0]
        calc = path.split("/")[2]
        session["XPLORPRJ"] = prj
        session["XPLORCALC"] = calc
        session.save();
    
    
     def xplorambersetup(self):
        return render('/filesystem/xploramber.mako', extra_vars={'xplorprj': session["XPLORPRJ"], 'xplorcalc': session["XPLORCALC"]})
    
     def projects_list(self):
          #calcs = Session.query(Calculations).filter(and_(Calculations.calc_type_id == session['PORTAL'], Calculations.removed == False)).subquery()
          #_proj = Session.query(Projects, calcs.c.project_id).outerjoin((calcs,  Projects.id == calcs.c.project_id)).order_by(Projects.name).all()
          _proj = Session.query(Projects).filter(and_(Projects.owner_id == session['REMOTE_USER'], Projects.removed == False)).all()
          proj_list = sorted(_proj, key=attrgetter('name'))
          #proj_list = [_proj[i][0] for i in  range(len(_proj)) if _proj[i][1]]
          if proj_list:
               projs_name = proj_list[0].name
               for item in proj_list[1:]:
                    projs_name = projs_name + ','+item.name
               return projs_name
          
     
     def amber_calculations_list(self):
          proj = request.GET.get("proj")
          prj = Session.query(Projects).filter(and_(Projects.name == proj, Projects.removed == False, Projects.owner_id == session['REMOTE_USER'])).all()
          calcsAMPS = Session.query(Calculations).filter(and_(Calculations.project_id == prj[0].id, Calculations.removed == False, Calculations.calc_type_id == 2)).order_by(Calculations.name).all()
          #calculations = sorted(calcsAMPS +, key=attrgetter('name'))
          
          #l = defaultdict(list)
          #if calculations:
               #tip = Session.query(CalculationTipology).get(int(calculations[0].calc_type_id))
               #list = 'calc'#calculations[0].name+';;%s' %tip.name
          #     for item in calculations:
          #          tip = Session.query(CalculationTipology).get(int(item.calc_type_id))
          #          l[tip.name].append(item.name) 
                    #list = list+','+item.name +';;%s' %tip.name
               #return list
          #     print l
          l = ''
          if calcsAMPS:
               l = calcsAMPS[0].name
               for i in calcsAMPS[1:]:
                    l += ',%s' % i.name
                    #print l
          return l
     
     def calculations_list(self):
          proj = request.GET.get("proj")
          prj = Session.query(Projects).filter(and_(Projects.name == proj, Projects.removed == False, Projects.owner_id == session['REMOTE_USER'])).all()
          print len(prj)
          calcsAMPS = Session.query(Calculations).filter(and_(Calculations.project_id == prj[0].id, Calculations.removed == False, Calculations.calc_type_id == 2)).order_by(Calculations.name).all()
          calcsXPLOR = Session.query(Calculations).filter(and_(Calculations.project_id == prj[0].id, Calculations.removed == False, Calculations.calc_type_id == 1)).order_by(Calculations.name).all()
          calcsMAXOCC = Session.query(Calculations).filter(and_(Calculations.project_id == prj[0].id, Calculations.removed == False, Calculations.calc_type_id == 5)).order_by(Calculations.name).all()
          calcsRANCH = Session.query(Calculations).filter(and_(Calculations.project_id == prj[0].id, Calculations.removed == False, Calculations.calc_type_id == 6)).order_by(Calculations.name).all()
          #calculations = sorted(calcsAMPS +, key=attrgetter('name'))
          calcsMAXOCC += calcsRANCH 
          
          #l = defaultdict(list)
          #if calculations:
               #tip = Session.query(CalculationTipology).get(int(calculations[0].calc_type_id))
               #list = 'calc'#calculations[0].name+';;%s' %tip.name
          #     for item in calculations:
          #          tip = Session.query(CalculationTipology).get(int(item.calc_type_id))
          #          l[tip.name].append(item.name) 
                    #list = list+','+item.name +';;%s' %tip.name
               #return list
          #     print l
          l = ''
          if len(calcsAMPS):
               l = 'amber::' + calcsAMPS[0].name
               for i in calcsAMPS[1:]:
                    l = l + ','+i.name
          else:
               l = 'amber::'
          if len(calcsXPLOR):
               l = l + ';;xplor-nih::' + calcsXPLOR[0].name
               for j in calcsXPLOR[1:]:
                    l = l + ',' + j.name
          else:
               l = l + ';;xplor-nih::'
          if len(calcsMAXOCC):
               l = l + ';;maxocc::' + calcsMAXOCC[0].name
               for j in calcsMAXOCC[1:]:
                    l = l + ',' + j.name
          else:
               l = l + ';;maxocc::'
          
          #if len(calcsMAXOCC):
          #     l = calcsMAXOCC[0].name
          #     for i in calcsMAXOCC[1:]:
          #          l += ',%s' % i.name
          return l
     
     def dircontent(self):
          owner = Session.query(Users).get(session['REMOTE_USER'])
          r = []
          path = request.GET.get('path')
          path = path.replace("Projects/", "")
          pdir = os.path.join(config['app_conf']['working_dir'], owner.home, path)
          print "dircontent: %s" %pdir
          if not os.path.exists(pdir):
               pdir = pdir.replace("amber", "amps-nmr",1)
               if not os.path.exists(pdir):
                    pdir = pdir.replace("amps-nmr", "amber",1)
          list_dir = os.listdir(pdir)
          list_dir_dict = {}
          for i in list_dir:
               if not i.startswith("."):
                    #(filetype, perms, owner, group, size, mtime) = files.get_fileinfo(os.path.join(pdir, i), 0, 1)
                    size = 0
                    list_dir_dict[i] = size
          list_dir_sorted = files.sort_dir(list_dir_dict, 1, 1, 0)
          for f in list_dir_sorted:
               ff = os.path.join(pdir, f)
               if os.path.isdir(ff):
                    r.append('dir::%s' %ff.split("/")[-1])
               else:
                    r.append('file::%s' %f.split("/")[-1])
          if len(r):
              return ','.join(r)
          else:
              return ''
          
          #for f in os.listdir(pdir):
          #     ff = os.path.join(pdir, f)
          #     if os.path.isdir(ff):
          #          r.append('dir::%s' %ff.split("/")[-1])
          #     else:
          #          r.append('file::%s' %f.split("/")[-1])
          #if len(r):
          #    return ','.join(r)
          #else:
          #    return ''
        
     def get_dir_size(self):
          owner = Session.query(Users).get(session['REMOTE_USER'])
          home = owner.home
          path = request.POST.getall('path')
          totsize = 0
          #for i in path:
          #     path_elem = i.replace("Projects/", "")
          #     pdir = os.path.join(config['app_conf']['working_dir'], home, path_elem)
          #     if not os.path.exists(pdir):
          #          pdir = pdir.replace("amber", "amps-nmr")
          #     (filetype, perms, owner, group, size, mtime) = files.get_fileinfo(pdir, 0, 1)
          #     totsize = totsize + size
          return  str(h.pretty_size(totsize))
        
     def rename(self):
          owner = Session.query(Users).get(session['REMOTE_USER'])
          curNamePath = request.POST.get('curName')
          curName = curNamePath.replace("Projects/", "");
          newName = request.POST.get('newName')
          curNamePathList = curName.split("/")
          curNamePathList.pop()
          dirNewName = curName.replace(curNamePathList[-1], newName)
          pdir = os.path.join(config['app_conf']['working_dir'], owner.home, curName)
          ndir = os.path.join(config['app_conf']['working_dir'], owner.home, dirNewName)
          print "*"*10
          print curNamePath
          print pdir, ndir
          if len(curNamePathList) > 3:
              #cambiare il nome al file o directory
              
              os.rename(pdir, ndir)
          else:
               if len(curNamePathList)  == 1:
                    #cambiare nome al progetto
                    proj = curNamePathList[0]
                    project = Session.query(Projects).filter(and_(Projects.name==proj, Projects.removed == False, Projects.owner_id==session['REMOTE_USER'])).all()
                    if project:
                         p = Session.query(Projects).get(project[0].id)
                         print p
                         p.name = newName
                         Session.add(p)
                         Session.commit()
                         os.rename(pdir, ndir)
               else:
                    #cambiare nome al calcolo
                    proj = curNamePathList[0]
                    calc = curNamePathList[2]
                    prj = Session.query(Projects).filter(and_(Projects.name==proj, Projects.removed == False, Projects.owner_id==session['REMOTE_USER'])).all()
                    print prj[0].id
                    if prj:
                         calculation = Session.query(Calculations).filter(and_(Calculations.name==calc, Calculations.removed == False, Calculations.project_id==prj[0].id)).all();
                         if calculation:
                              c = Session.query(Calculations).get(calculation[0].id)
                              c.name = newName
                              Session.add(c)
                              Session.commit()
                              os.rename(pdir, ndir)
          
          return "" 
        
     def mkdir(self):
          owner = Session.query(Users).get(session['REMOTE_USER'])
          path = request.POST.get('path')
          path = path.replace("Projects/", "");
          pdir = os.path.join(config['app_conf']['working_dir'], owner.home, path)
          (ret1, ret2) = files.mkdir(pdir, "untitled folder")
          return str(ret1) + '::' + str(ret2)
     
     def mkfile(self):
          owner = Session.query(Users).get(session['REMOTE_USER'])
          path = request.POST.get('path')
          path = path.replace("Projects/", "");
          pdir = os.path.join(config['app_conf']['working_dir'], owner.home, path+"new file.txt")
          file = open(pdir, "w")
          file.close()
     
     def remove(self):
          owner = Session.query(Users).get(session['REMOTE_USER'])
          path = request.POST.get('path')
          path = path.replace("Projects/", "");
          if path.endswith(os.sep):
               path = path[:-1]
          #print "path: %s" % path
          pathList = path.split("/")
          #pathList.pop()
          proj = pathList[0]
          project = Session.query(Projects).filter(and_(Projects.name == proj, Projects.removed == False, Projects.owner_id == session['REMOTE_USER'])).all()
          if len(pathList) == 1:
               if project:
                    for u in project[0].users:
                        project[0].users.remove(u)
                    for c in project[0].calculation:
                        for j in c.job:
                            job = Session.query(Jobs).get(j.id)
                            job.removed = True
                            Session.add(job)
                        clc = Session.query(Calculations).get(c.id)
                        clc.removed = True
                        Session.add(clc)
                        #project[0].calculation.remove(c)
                    project[0].removed = True
                    Session.add(project[0])
                    Session.commit()
                    # Remove the project from filesystem
                    pdir = os.path.join(config['app_conf']['working_dir'], project[0].owner.home, project[0].name)
                    files.rmall(pdir)
          else:
               if(len(pathList) > 2):
                    calc = pathList[2]
               else:
                    calc = pathList[1]
               if project:
                    c = Session.query(Calculations).filter(and_(Calculations.name==calc, Calculations.removed == False, Calculations.project_id==project[0].id)).all()
                    if c:
                         name = c[0].name
                         for j in c[0].job:
                            job = Session.query(Jobs).get(j.id)
                            job.removed = True
                            Session.add(job)
                         clc = Session.query(Calculations).get(c[0].id)
                         clc.removed = True
                         Session.add(clc)
                         ##project[0].calculation.remove(clc)
                         Session.commit()
                    # Remove the calculation from filesystem
                    pdir = os.path.join(config['app_conf']['working_dir'], project[0].owner.home, path)
                    files.rmall(pdir)
     
     def getInfoPortal(self):
          return session['PORTAL']
          
     def download(self):
          owner = Session.query(Users).get(session['REMOTE_USER'])
          home = owner.home
          path = request.GET.getall('path')
          print "download path: %s" % path
          if len(path) == 1:
               path_list = path[0].split("/")
               if path_list[-1] == '':
                    path_list.pop()
               len_path_list = len(path_list)
               if len_path_list == 2:
                    #download project
                    proj = path_list[1]
                    prj = Session.query(Projects).filter(and_(Projects.name==proj, Projects.owner_id==session['REMOTE_USER'])).all()
                    self.project_compress(prj[0].id)
                    tfile, tfilename, data = self.project_download(prj[0].id)
                    response.content_type = guess_type(tfile)[0] or 'text/plain'
                    response.headers['Content-Lenght'] = len(data)
                    response.headers['Pragma'] = 'public'
                    response.headers['Cache-Control'] = 'max-age=0'
                    response.headers['Content-Disposition'] = 'attachment; filename="%s"'%(tfilename)
                    return data
                    
               elif len_path_list == 4:
                    #download calculation
                    proj = path_list[1]
                    prj = Session.query(Projects).filter(and_(Projects.name==proj, Projects.owner_id==session['REMOTE_USER'])).all()
                    calc = path_list[3]
                    tfile, tfilename = self.calculation_compress(prj[0].id, calc)
                    permanent_file = open(tfile, 'rb')
                    data = permanent_file.read()
                    permanent_file.close()
                    #self.calculation_download(prj[0].id, calc)
                    response.content_type = guess_type(tfile)[0] or 'text/plain'
                    response.headers['Content-Lenght'] = len(data)
                    response.headers['Pragma'] = 'public'
                    response.headers['Cache-Control'] = 'max-age=0'
                    response.headers['Content-Disposition'] = 'attachment; filename="%s"'%(tfilename)
                    return data     
               else:
                    #download file or directory within calculation
                    proj = path_list[1]
                    calc = path_list[3]
                    itemname = path_list[-1]
                    true_path = os.path.join(config['app_conf']['working_dir'], home, path[0].replace("Projects/", ""))
                    if os.path.isfile(true_path):
                         #exact_path = path[0].replace("Projects/", "")
                         #tgzname = '%s_%s_%s' %(proj, calc, itemname)
                         #tfile = os.path.join(
                         #config['app_conf']['working_dir'], home, exact_path)
                         tgzname = path_list[-1]
                         tfile = true_path
                    else:
                         tgzname = '%s_%s_%s.tar' %(proj, calc, itemname)
                         exact_path = path[0].replace("Projects/", "")
                         self.__compress(home, exact_path, tgzname)
                         tfile = os.path.join(
                         config['app_conf']['temp_dir'],
                         tgzname)
                    permanent_file = open(tfile, 'rb')
                    data = permanent_file.read()
                    permanent_file.close()
            
                    response.content_type = guess_type(tfile)[0] or 'text/plain'
                    response.headers['Content-Lenght'] = len(data)
                    response.headers['Pragma'] = 'public'
                    response.headers['Cache-Control'] = 'max-age=0'
                    response.headers['Content-Disposition'] = 'attachment; filename="%s"'%(tgzname)
                    return data
          else:
               tgzname = '%s_multisel.tar' % owner.lastname
               for i in range(len(path)):
                    path[i] = path[i].replace("Projects/", "")
               self.__compress(home, path, tgzname)
               tfile = os.path.join(
               config['app_conf']['temp_dir'],
               tgzname)
               permanent_file = open(tfile, 'rb')
               data = permanent_file.read()
               permanent_file.close()
       
               response.content_type = guess_type(tfile)[0] or 'text/plain'
               response.headers['Content-Lenght'] = len(data)
               response.headers['Pragma'] = 'public'
               response.headers['Cache-Control'] = 'max-age=0'
               response.headers['Content-Disposition'] = 'attachment; filename="%s"'%(tgzname)
               return data
     def prepare_violations(self):
          #calcola violazioni su tutti i job presenti nel calcolo
          #e permette di scaricare il file delle violazioni
          owner = Session.query(Users).get(session['REMOTE_USER'])
          home = owner.home
          path = request.POST.get('path')
          path = path[:-2]
          outPath = os.path.join(config['app_conf']['working_dir'], home, path.replace("Projects/", ""), 'output')
          if not os.path.exists(outPath):
               outPath = outPath.replace("amber", "amps-nmr",1)
               if not os.path.exists(outPath):
                    outPath = outPath.replace("amps-nmr", "amber",1)
          if os.path.isdir(outPath):
               violdir = os.path.join(config['app_conf']['temp_dir'], owner.lastname+'_viol')
               if os.path.exists(violdir):
                    shutil.rmtree(violdir)
               os.makedirs(violdir)
               loutPath = os.listdir(outPath)
               for item in loutPath:
                    l = os.listdir(os.path.join(outPath, item))
                    #print l
                    pattern3 = 'sander[0-9].in$'
                    f3 = re.compile(pattern3)
                    sanderIns = [ i for i in l if f3.search(i)]
                    numSanderIns = len(sanderIns)
                    #print "total step: %d" % numSanderIns
                    
                    pattern2 = 'sander%s.out' % (numSanderIns - 1)
                    if pattern2 in l:
                         shutil.copy(os.path.join(outPath, item, pattern2), os.path.join(violdir, pattern2.split(".")[0]+"_"+item.split("_")[1]+".out"))
               #problem with space in directory name
               #cmd = 'cd %s;/prog/amber10/bin/sviol *.out >%s'%(violdir, os.path.join(violdir, 'violations.txt'))
               #cmd1= []
               #cmd1.append("/prog/amber10/bin/sviol")
               #cmd1.append("*.out")
               #cmd1.append(">")
               #cmd1.append(os.path.join(violdir, 'violations.txt'))
               cmd = '/prog/amber10/bin/sviol *.out >violations.txt'
               print "BUG SPACE INI"
               print cmd
               dir_tmp = os.getcwd()
               print dir_tmp
               os.chdir(violdir)
               e = subprocess.Popen(cmd, shell=True).wait()
               print cmd
               print os.getcwd()
               os.chdir(dir_tmp)
               print "BUG SPACE END"
               
               return "violations.txt"
          
     def download_violations(self):
          owner = Session.query(Users).get(session['REMOTE_USER'])
          home = owner.home
          name = request.GET.get("name")
          tfile = os.path.join(config['app_conf']['temp_dir'], owner.lastname+'_viol', name)
          permanent_file = open(tfile, 'r')
          data = permanent_file.read()
          permanent_file.close()
          response.content_type = guess_type(tfile)[0] or 'text/plain'
          response.headers['Content-Lenght'] = len(data)
          response.headers['Pragma'] = 'public'
          response.headers['Cache-Control'] = 'max-age=0'
          response.headers['Content-Disposition'] = 'attachment; filename="%s"'% name
          shutil.rmtree(os.path.join(config['app_conf']['temp_dir'], owner.lastname+'_viol'))
          return data
          
     def prepare_results(self):
          owner = Session.query(Users).get(session['REMOTE_USER'])
          home = owner.home
          path = request.POST.get('path')
          outPath = os.path.join(config['app_conf']['working_dir'], home, path.replace("Projects/", ""), 'output')
            
            #if session['PORTAL'] == 'xplor-nih':
            #  loutdirs = os.listdir(outPath)
            #  tfilepath = os.path.join(config['app_conf']['temp_dir'], owner.lastname+"_Xplorresults.tar")
            #  t = tarfile.open(tfilepath, 'w')
            #  for idxdir, d in enum(loutdirs):
            #      outdir = os.listdir(os.path.join(outPath, d))
            #      idxpdb = 0
            #      for item in outdir:
            #          pattern = 'sa1_[1-99].pdb$'
            #          regexpr = re.compile(pattern)
            #          for i in outdir:
            #              if regexpr.search(i):
            #                  idxpdb += 1
            #                  tarname = 'out_%s_%s' %(idxdir+1, idxpdb)
            #                  print tarname
            #                  t.add(os.path.join(outdir, i), arcname=tarname, recursive=False)
            #  t.close()
            #else:
          if not os.path.exists(outPath):
               outPath = outPath.replace("amber", "amps-nmr",1)
               if not os.path.exists(outPath):
                    outPath = outPath.replace("amps-nmr", "amber",1)
          if os.path.isdir(outPath):
               loutPath = os.listdir(outPath)
               diz = []
               for item in loutPath:
                    l = os.listdir(os.path.join(outPath, item))
                    #print l
                    pattern3 = 'sander[0-9].in$'
                    f3 = re.compile(pattern3)
                    sanderIns = [ i for i in l if f3.search(i)]
                    numSanderIns = len(sanderIns)
                    #print "total step: %d" % numSanderIns
                    
                    pattern = 'amber_final%d.pdb' % (numSanderIns - 1)
                    pdb=''
                    if pattern in l:
                         pdb = pattern
                    pdblen = len(pdb)
                    #print "pdb: %d" % pdblen
               
                    pattern2 = 'sander[0-9].out$'
                    f2 = re.compile(pattern2)
                    outs = [ os.path.join(outPath, item, i) for i in l if f2.search(i)]
                    sortedOuts = sorted(outs)
                    #print "sander out: %s -- last: %s" %(sortedOuts, sortedOuts[-1])
                    
                    #tfile = os.path.join(config['app_conf']['temp_dir'], owner.lastname+"_results.tgz")
                    #t = tarfile.open(tfile, 'w:gz')
                    read_flag = False
                    if pdblen:
                         diz.append({'pdb': os.path.join(outPath, item, pdb), 'sander': sortedOuts[-1]})
                    else:
                         read_flag = True
                         readme = open(os.path.join(config['app_conf']['temp_dir'], owner.lastname+'_README'), 'w')
                         readme.write("Some errors occurred in Amber about your calculation, and probably"+
                                      " been due to bad input files or wrong protocol parameter setting."+
                                      " Please, check sander[0-9].out files to detect error(s) and re-submit"+
                                      " your calculation.")
                         readme.close()
                         out_tmp = []
                         diz.append({'pdb': os.path.join(config['app_conf']['temp_dir'], owner.lastname+'_README'), 'sander': out_tmp})
                    tfile = os.path.join(config['app_conf']['temp_dir'], owner.lastname+"_results.tar")
                    t = tarfile.open(tfile, 'w')
                    for i in diz:
                         if i['pdb'].endswith('README'):
                              t.add(i['pdb'], arcname='README', recursive=False)
                         else:
                              n = os.path.dirname(i['pdb']).split('/')[-1] + '.pdb'
                              t.add(i['pdb'], arcname=n, recursive=False)
                         if type(i['sander']).__name__== 'list':
                              for j in i['sander']:
                                   n = os.path.dirname(j).split('/')[-1] + '.out'
                                   t.add(j, arcname=n, recursive=False)
                         else:
                              n = os.path.dirname(i['sander']).split('/')[-1] + '.out'
                              t.add(i['sander'], arcname=n, recursive=False)
                    t.close()
                    if read_flag:
                       break  
               return owner.lastname+'_results.tar'
          else:
               return ''
          
     def prepare_results_xplor(self):
        owner = Session.query(Users).get(session['REMOTE_USER'])
        home = owner.home
        path = request.POST.get('path')
        outPath = os.path.join(config['app_conf']['working_dir'], home, path.replace("Projects/", ""), 'output')
        
        loutdirs = os.listdir(outPath)
        tfilepath = os.path.join(config['app_conf']['temp_dir'], owner.lastname+"_Xplorresults.tar")
        t = tarfile.open(tfilepath, 'w')
        pattern = 'sa1_[0-9]+.pdb'
        regexpr = re.compile(pattern)
        for d in loutdirs:
            outdir = os.listdir(os.path.join(outPath, d))
            idxpdb = 0
            for i in outdir:
                if regexpr.search(i):
                    tarname = 'out_%s_%s.pdb' %(d.split("_")[-1], i.split("_")[-1].split(".")[0])
                    #print tarname
                    fp = os.path.join(outPath, d, i)
                    t.add(fp, arcname=tarname, recursive=False)
        t.close()
        return owner.lastname+"_Xplorresults.tar"
        
        
          #owner = Session.query(Users).get(session['REMOTE_USER'])
          #home = owner.home
          #path = request.POST.get('path')
          #path = path.replace("Projects/", "")
          #absPath = os.path.join(config['app_conf']['working_dir'], home, path)
          #print "########XPLOR_ANAL PATH########"
          #print absPath
          #print "###############################"
          #analy = xplor_analysis.analysis(absPath)
          #
          #tfile = os.path.join(config['app_conf']['temp_dir'], owner.lastname+"_resultsxplor.tar")
          #t = tarfile.open(tfile, 'w')
          #
          #return owner.lastname+'_resultsxplor.tar'
     
     def download_results(self):
          owner = Session.query(Users).get(session['REMOTE_USER'])
          home = owner.home
          name = request.GET.get("name")
          tfile = os.path.join(config['app_conf']['temp_dir'], name)
          permanent_file = open(tfile, 'r')
          data = permanent_file.read()
          permanent_file.close()
          response.content_type = guess_type(tfile)[0] or 'text/plain'
          response.headers['Content-Lenght'] = len(data)
          response.headers['Pragma'] = 'public'
          response.headers['Cache-Control'] = 'max-age=0'
          response.headers['Content-Disposition'] = 'attachment; filename="%s"'% name.split('_')[1]
          return data
     
     def __compress(self, home, path, tgzname):
          tfile = os.path.join(
                  config['app_conf']['temp_dir'],
                  tgzname)
          t = tarfile.open(tfile, 'w')
          #if type(path).__name__=='list':
          if type(path) is list:
               for i in path:
                    if i.endswith(os.sep):
                         name = os.path.basename(i[:-1])
                    else:
                         name = os.path.basename(i)
                    to_add = os.path.join(
                         config['app_conf']['working_dir'],
                         home,
                         i
                    )
                    t.add(to_add, arcname=name, recursive=True)
          else:
               to_add = os.path.join(
                    config['app_conf']['working_dir'],
                    home,
                    path
               )
               path_split = path.split("/")
               if path_split[-1] == '':
                    path_split.pop()
               name = path_split[-1]
               t.add(to_add, arcname=name, recursive=True)
          t.close()
     
     
     def project_download(self, id=None):
        if id:
            project = Session.query(Projects).get(int(id))
            owner = Session.query(Users).get(session['REMOTE_USER'])
            tfilename = '%s_%s.tar' % (owner.lastname, project.name)
            tfile = os.path.join(
                    config['app_conf']['temp_dir'],
                    tfilename)
            permanent_file = open(tfile, 'rb')
            data = permanent_file.read()
            permanent_file.close()
    
            return (tfile, tfilename, data)
            
    
     def calculation_compress(self, idproj=None, namecalc=None):
          project = Session.query(Projects).get(int(idproj))
          c = Session.query(Calculations).filter(and_(Calculations.name==namecalc, Calculations.project_id==idproj)).all()
          owner = Session.query(Users).get(session['REMOTE_USER'])
          tfilename = '%s_%s_%s.tar' % (owner.lastname, project.name, c[0].name)
          tfile = os.path.join(
                  config['app_conf']['temp_dir'],
                  tfilename)
          c_type = Session.query(CalculationTipology).get(int(c[0].calc_type_id))
          to_add = os.path.join(
              config['app_conf']['working_dir'],
              owner.home,
              project.name,
              c_type.tipology,c[0].name)
          
          if not os.path.exists(to_add):
               to_add = to_add.replace("amber","amps-nmr",1)
               if not os.path.exists(to_add):
                    to_add = to_add.replace("amps-nmr", "amber",1)
               
          t = tarfile.open(tfile, 'w')
          t.add(to_add, arcname=c[0].name, recursive=True)
          t.close()
          return tfile, tfilename
     
     def project_compress(self, id=None):
          project = Session.query(Projects).get(int(id))
          owner = Session.query(Users).get(session['REMOTE_USER'])
          tfilename = '%s_%s.tar' % (owner.lastname, project.name)
          tfile = os.path.join(
                  config['app_conf']['temp_dir'],
                  tfilename)
      
          to_add = os.path.join(
              config['app_conf']['working_dir'],
              owner.home,
              project.name)
          
          t = tarfile.open(tfile, 'w')
          t.add(to_add, arcname=project.name, recursive=True)
          t.close()
     
     def read_jmol(self):
          owner = Session.query(Users).get(session['REMOTE_USER'])
          path = request.POST.get('path')
          path = path.replace("Projects/", "")
          pdir = os.path.join(config['app_conf']['working_dir'], owner.home, path)
          if not os.path.exists(pdir):
               pdir = pdir.replace("amber","amps-nmr",1)
               if not os.path.exists(pdir):
                    pdir = pdir.replace("amps-nmr", "amber",1)
          permanent_file = open(pdir, 'r')
          data = permanent_file.read()
          
          permanent_file.close()
          return data
     
     def exec_analysis(self):
        path = request.POST.get("path", "")
        print path
        owner = Session.query(Users).get(session['REMOTE_USER'])
        path = path.replace("Projects/", "")
        pdir = os.path.join(config['app_conf']['working_dir'], owner.home, path)
        print pdir
        x_analys = xplor_analysis(pdir)
          
