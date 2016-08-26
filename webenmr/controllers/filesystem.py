import logging
import os
import time
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config

from mimetypes import guess_type

from webenmr.lib.base import *
from webenmr.lib import return_values
from webenmr.lib import files
from webenmr.model import Projects, Users

log = logging.getLogger(__name__)
os.umask(0002)

class FilesystemController(BaseController):
    def __before__(self):
        """
        This __before__ method calls the parent method, and then sets up the
        tabs on the page.
        """
        
        #BaseController.__before__(self)
        
        c.page_base = u'Filesystem'
        #if 'REMOTE_USER' in session:
        #    c.current_user = Session.query(Users).get(session['REMOTE_USER'])
        #    c.main_menu = Session.query(Menu).filter(and_(Menu.parent_id==None, Menu.sibling_id==None)).order_by(Menu.weight.asc()).all()
        c.page_title = u'Explorer'
        #cert = os.path.join(config['app_conf']['cert_dir'], 'x509up_u0')
        #os.environ['X509_USER_PROXY'] = cert

    def explore(self, id=None):
        """Set the directory entry point to the exploration"""
        if id:
            project = Session.query(Projects).get(int(id))
            if project:
                c.pdir = os.path.join(config['app_conf']['working_dir'], project.owner.home, project.name)
                c.pname = project.name
                return render('/filesystem/explore.mako')
        
    def dirlist(self):
        """Prepare the input for jqueryTree to display the directory tree"""
        r = ['<ul class="jqueryFileTree" style="display: none;">']
        try:
            r = ['<ul class="jqueryFileTree" style="display: none;">']
            d1=request.POST.get('dir', '')
            d = os.path.join(config['app_conf']['template_dir'], d1)
            for f in os.listdir(d):
                ff = os.path.join(d, f)
                if os.path.isdir(ff):
                    r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
                else:
                    e = os.path.splitext(f)[1][1:] # get .ext and remove dot
                    r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,ff,f))
            r.append('</ul>')
        except Exception,e:
            r.append('Could not load directory: %s' % str(e))
        r.append('</ul>')
        return ''.join(r)
        
    def checkfile(self):
        """Check the file informations and return the results in html format"""
        file = request.POST.get('file', '')
        output = ''
        if file:
            (type, mode, owner, group, size, mtime) = files.get_fileinfo(file)
            
            html = "type: %s<br />mode: %s<br />size: %s<br />mtime: %s<br />" % (type, mode, h.pretty_size(size), time.ctime(int(mtime)))
            return html
        
    def download(self):
        filepath = request.params['requested_filename']
        
        if not os.path.exists(filepath):
            return 'No such file'
        permanent_file = open(filepath, 'rb')
        data = permanent_file.read()
        permanent_file.close()
        response.content_type = guess_type(filepath)[0] or 'text/plain'
        
        namelist = filepath.split("/")
        name = namelist[len(namelist)-1]
        response.headers['Content-Disposition'] = 'attachment; filename="%s"'%(name)
        return data
    
    def jmol_file(self):
        file_name = request.GET.get('file_name')
        permanent_file = open(file_name, 'r')
        return permanent_file