import logging
import tarfile
import os
import time
import shutil
import re
from datetime import datetime
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config
from lxml import etree
import random
from webenmr.lib import files
from webenmr.lib.base import *
from webenmr.lib import return_values
from webenmr.lib.return_values import S_OK, S_ERROR
from webenmr.model import Projects, Users, CalculationTipology, Calculations

log = logging.getLogger(__name__)
os.umask(0002)

class ProtocolsController(BaseController):
    def __before__(self):
        """
        This __before__ method calls the parent method, and then sets up the
        tabs on the page.
        """
        
        #BaseController.__before__(self)
        
        c.page_base = u'Protocols'
        #if 'REMOTE_USER' in session:
        #    c.current_user = Session.query(Users).get(session['REMOTE_USER'])
        #    c.main_menu = Session.query(Menu).filter(and_(Menu.parent_id==None, Menu.sibling_id==None)).order_by(Menu.weight.asc()).all()
        c.page_title = u'Protocols'
        #cert = os.path.join(config['app_conf']['cert_dir'], 'x509up_u0')
        #os.environ['X509_USER_PROXY'] = cert

    
    def index(self):
        # Return a rendered template
        #return render('/protocols.mako')
        # or, return a response
        return render('/protocols/protocol2.mako')

    
    def load_protocols(self):
        owner = Session.query(Users).get(session['REMOTE_USER'])
        presetdir = os.path.join(config['app_conf']['template_dir'], "protocols")
        list_dir = os.listdir(pdir)
        pattern = '.dscr$'
        f = re.compile(pattern)
        t = [ 'preset::' + i[:-5] for i in list_dir if f.search(i)]
        t1 = sorted(t)
        preset_list = ';'.join(t)
        
        personaldir = os.path.join(config['app_conf']['working_dir'], owner.home, p.lower())
        if os.path.exists(pdir):
            list_dir = os.listdir(pdir)
            if len(list_dir):
                pattern = '.dscr$'
                f = re.compile(pattern)
                t = [ 'personal::' + i[:-5] for i in list_dir if f.search(i)]
                t1 = sorted(t)
                personal_list = ';'.join(t)
            else:
                personal_list = ''
        return preset_list + personal_list
    
    def protocols_list(self):
        owner = Session.query(Users).get(session['REMOTE_USER'])
        p = request.GET.get('prot')
        p = p.replace("/", "")
        if p == 'Preset':
            pdir = os.path.join(config['app_conf']['template_dir'], "protocols")
        else:
            pdir = os.path.join(config['app_conf']['working_dir'], owner.home, p.lower())
        if os.path.exists(pdir):
            list_dir = os.listdir(pdir)
            if len(list_dir):
                pattern = '.dscr$'
                f = re.compile(pattern)
                t = [ i[:-5] for i in list_dir if f.search(i)]
                t1 = sorted(t)
                return ','.join(t)
            else:
                return ''
        return ''
        
    def protocol_content_list(self):
        owner = Session.query(Users).get(session['REMOTE_USER'])
        p = request.GET.get('prot')
        p = p.replace("/", "")
        fp = request.GET.get('file')
        if p == 'Preset':
            pdir = os.path.join(config['app_conf']['template_dir'], "protocols")
        else:
            pdir = os.path.join(config['app_conf']['working_dir'], owner.home, p.lower())
        list_dir = os.listdir(pdir)
        if len(list_dir):
            pattern = '%s-[0-9].step$' %fp
            pattern1 = '%s.dscr$' %fp
            f = re.compile(pattern)
            g = re.compile(pattern1)
            t = [ i for i in list_dir if f.search(i) or g.search(i)]
            t1 = sorted(t)
            #t = []
            #for i in list_dir:
            #    if f.search(i):
            #        t.append(i[:-7])
            #    elif g.search(i):
            #        t.append(i[:-5])
            return ','.join(t1)
        else:
            return ''
        
    def get_dir_size(self):
         owner = Session.query(Users).get(session['REMOTE_USER'])
         home = owner.home
         path = request.POST.getall('path')
         totsize = 0
         for i in path:
              path_elem = i.replace("Projects/", "")
              pdir = os.path.join(config['app_conf']['working_dir'], home, path_elem)
              (filetype, perms, owner, group, size, mtime) = files.get_fileinfo(pdir, 0, 1)
              totsize = totsize + size
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
         if len(curNamePathList) > 3:
             #cambiare il nome al file o directory
             
             os.rename(pdir, ndir)
         else:
              if len(curNamePathList)  == 1:
                   #cambiare nome al progetto
                   proj = curNamePathList[0]
                   project = Session.query(Projects).filter(and_(Projects.name==proj, Projects.owner_id==session['REMOTE_USER'])).all()
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
                   prj = Session.query(Projects).filter(and_(Projects.name==proj, Projects.owner_id==session['REMOTE_USER'])).all()
                   print prj[0].id
                   if prj:
                        calculation = Session.query(Calculations).filter(and_(Calculations.name==calc, Calculations.project_id==prj[0].id)).all();
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
         print "path: %s" % path
         pathList = path.split("/")
         #pathList.pop()
         proj = pathList[0]
         project = Session.query(Projects).filter(and_(Projects.name==proj, Projects.owner_id==session['REMOTE_USER'])).all()
         if len(pathList) == 1:
              if project:
                   for u in project[0].users:
                       project[0].users.remove(u)
                   for c in project[0].calculation:
                       for j in c.job:
                           job = Session.query(Jobs).get(j.id)
                           Session.delete(job)
                       clc = Session.query(Calculations).get(c.id)
                       Session.delete(clc)
                       project[0].calculation.remove(c)
                   Session.delete(project[0])
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
                   c = Session.query(Calculations).filter(and_(Calculations.name==calc, Calculations.project_id==project[0].id)).all()
                   if c:
                        name = c[0].name
                        for j in c[0].job:
                           job = Session.query(Jobs).get(j.id)
                           Session.delete(job)
                        clc = Session.query(Calculations).get(c[0].id)
                        Session.delete(clc)
                        #project[0].calculation.remove(clc)
                        Session.commit()
                   # Remove the calculation from filesystem
                   pdir = os.path.join(config['app_conf']['working_dir'], project[0].owner.home, path)
                   files.rmall(pdir)
    
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
                   tgzname = '%s_%s_%s.tgz' %(proj, calc, itemname)
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
              tgzname = '%s_multisel.tgz' % owner.lastname
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
         
    def __compress(self, home, path, tgzname):
         tfile = os.path.join(
                 config['app_conf']['temp_dir'],
                 tgzname)
         t = tarfile.open(tfile, 'w:gz')
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
           tfilename = '%s_%s.tgz' % (owner.lastname, project.name)
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
         tfilename = '%s_%s_%s.tgz' % (owner.lastname, project.name, c[0].name)
         tfile = os.path.join(
                 config['app_conf']['temp_dir'],
                 tfilename)
     
         to_add = os.path.join(
             config['app_conf']['working_dir'],
             owner.home,
             project.name,
             'amber/'+c[0].name)
         
         t = tarfile.open(tfile, 'w:gz')
         t.add(to_add, arcname=c[0].name, recursive=True)
         t.close()
         return tfile, tfilename
    
    def project_compress(self, id=None):
         project = Session.query(Projects).get(int(id))
         owner = Session.query(Users).get(session['REMOTE_USER'])
         tfilename = '%s_%s.tgz' % (owner.lastname, project.name)
         tfile = os.path.join(
                 config['app_conf']['temp_dir'],
                 tfilename)
     
         to_add = os.path.join(
             config['app_conf']['working_dir'],
             owner.home,
             project.name)
         
         t = tarfile.open(tfile, 'w:gz')
         t.add(to_add, arcname=project.name, recursive=True)
         t.close()
    
    def read_protocol(self):
        owner = Session.query(Users).get(session['REMOTE_USER'])
        group = request.POST.get('group')
        file = request.POST.get('file')
        if group == 'Personal':
            pdir = os.path.join(config['app_conf']['working_dir'], owner.home, "personal", file)
        else:
            pdir = os.path.join(config['app_conf']['template_dir'], "protocols", file)
        permanent_file = open(pdir, 'r')
        data = permanent_file.read()
        permanent_file.close()
        return data
         