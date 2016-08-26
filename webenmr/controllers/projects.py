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

from webenmr.lib.base import *
from webenmr.lib import files
from webenmr.lib import return_values
from webenmr.model import Projects, Users, CalculationTipology, Jobs, Calculations

log = logging.getLogger(__name__)
os.umask(0002)


class ProjectsController(BaseController):
    def __before__(self):
        """
        This __before__ method calls the parent method, and then sets up the
        tabs on the page.
        """
        #BaseController.__before__(self)
        
        c.page_base = u'Projects'
        #if 'REMOTE_USER' in session:
        #    c.current_user = Session.query(Users).get(session['REMOTE_USER'])
        #    c.main_menu = Session.query(Menu).filter(and_(Menu.parent_id==None, Menu.sibling_id==None)).order_by(Menu.weight.asc()).all()
        c.page_title = u'Projects'
        #cert = os.path.join(config['app_conf']['cert_dir'], 'x509up_u0')
        #os.environ['X509_USER_PROXY'] = cert
        
    def list(self):
        c.projects = Session.query(Projects).filter(Projects.owner_id == session['REMOTE_USER']).all()
        c.calc_type = Session.query(CalculationTipology).all()
        return render('/projects/list.mako')
    
    @check_access('Create Projects')
    def project_create(self):
        '''Method to create a new project in db and filesystem'''
        
        project = request.POST.get('project', '')
        if not project:
            return render('/projects/new.mako')
            
        calc_type = request.POST.get('calc_type')
        # Replace spaces with _
        project = project.replace(' ', '_')
    
        # Check the existance of another project with the same name
        p = Session.query(Projects).filter(and_(Projects.name == project, Projects.owner_id == session['REMOTE_USER'], Projects.removed == False)).first()
        if p:
            h.flash.set_message('Project already created.', 'error')
            h.redirect('/projects/project_create')
            
        owner = Session.query(Users).get(session['REMOTE_USER'])
        
        # Create the directory structure on the filesystem
        #calc_type = Session.query(CalculationTipology).get(int(calc_type))
        if session['PORTAL'] == 'amps-nmr':
            calc_type = 'amber'
        else:
            calc_type = session['PORTAL']
        pdir = os.path.join(config['app_conf']['working_dir'], owner.home)
        if os.path.isdir(pdir):
            pdir = os.path.join(pdir, project, calc_type)
        try:
            os.makedirs(pdir)
        except OSError, (errno, strerror):
            if errno == 17:
                pass
            else:
                err = 'An error occurred during project creation. (OSErros: %s)' % strerror
                h.flash.set_message(err, 'Error')
                #h.redirect('/projects/list')
                h.redirect('/filemanager/')

        p = Projects()
        p.name = project
        p.creation_date = datetime.now()
        p.owner = owner
        Session.add(p)
        Session.commit()
        h.flash.set_message('Project created successfully.', 'success')
        #h.redirect('/projects/list')
        h.redirect('/filemanager/')

            
    @check_access('Create Projects')      
    def project_remove(self, id=None):
        '''Method to remove the project from db and filesystem'''
        if id:
            project = Session.query(Projects).get(int(id))
            for u in project.users:
                project.users.remove(u)
            for c in project.calculation:
                for j in c.job:
                    job = Session.query(Jobs).get(j.id)
                    Session.delete(job)
                clc = Session.query(Calculations).get(c.id)
                Session.delete(clc)
                project.calculation.remove(c)
            Session.delete(project)
            Session.commit()
            # Remove the project from filesystem
            pdir = pdir = os.path.join(config['app_conf']['working_dir'], project.owner.home, project.name)
            files.rmall(pdir)
            h.flash.set_message('Project removed successfully.', 'success')
            h.redirect('/projects/list')
    
    @check_access('Create Projects')   
    def project_download(self, id=None):
        if id:
            project = Session.query(Projects).get(int(id))
            tfilename = '%s.tgz' % project.name
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
            
    
    @check_access('Create Projects')   
    def project_compress(self, id=None):
        if id:
            project = Session.query(Projects).get(int(id))
            owner = Session.query(Users).get(session['REMOTE_USER'])
            tfilename = '%s.tgz' % project.name
            tfile = os.path.join(
                    config['app_conf']['temp_dir'],
                    tfilename)

            to_add = os.path.join(
                config['app_conf']['working_dir'],
                owner.home,
                project.name
            )
            
            t = tarfile.open(tfile, 'w:gz')
            t.add(to_add, arcname=project.name, recursive=True)
            t.close()
    
            return "ok"
        
    @check_access('Create Projects')   
    def check_download(self, id=None):
        if id:
            project = Session.query(Projects).get(int(id))
            tfilename = '%s.tgz' % project.name
            if os.path.exists((os.path.join(config['app_conf']['temp_dir'], tfilename))):
                return "ok"
            else:
                return "notar"
            
    def get_idproj(self):
        name = request.POST.get("name");
        print "name project: %s" % name
        prj = Session.query(Projects).filter(and_(Projects.name == name, Projects.owner_id == session['REMOTE_USER'], Projects.removed == False)).all()
        print "nome progetto da db: %s" % prj[0].name
        return str(prj[0].id)
