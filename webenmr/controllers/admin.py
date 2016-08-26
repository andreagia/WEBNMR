import logging
import os
import hashlib
from datetime import datetime
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config
import pycurl
from sqlalchemy.sql import and_, desc
from webenmr.lib.base import *
from webenmr.model import Menu, Users, Role
import webhelpers.paginate as paginate

log = logging.getLogger(__name__)
os.umask(0002)

class AdminController(BaseController):
    def __before__(self):
        """
        This __before__ method calls the parent method, and then sets up the
        tabs on the page.
        """
        #BaseController.__before__(self)

        c.page_base = u'Admin'
        #if 'REMOTE_USER' in session:
        #    c.current_user = Session.query(Users).get(session['REMOTE_USER'])
        #    c.main_menu = Session.query(Menu).filter(and_(Menu.parent_id==None, Menu.sibling_id==None)).order_by(Menu.weight.asc()).all()
        c.page_title = u'Admin'
        #
    @check_access('Manage Members')
    def users(self):
        '''If called display the number of current users'''
        c.users = len(Session.query(Users).filter(and_(Users.removed==False, Users.firstname!='Admin', Users.firstname!='Guest')).all())
        return render('/admin/users_index.mako')
    
    @check_access('Manage Members')
    def users_list(self):
        '''Render the users_list.mako template to display the list of users'''
        c.users = Session.query(Users).filter(Users.firstname!='Admin').all()
        return render('/admin/users_list.mako')
    
    @check_access('Manage Members')
    def create_user(self):
        '''Render user creation page'''
        return render('/admin/create_user.mako')
        
    @check_access('Manage Members')
    def save_user(self, id=None):
        '''Create a new user with the informations coming from
        /admin/create_user.mako template or update user with informations
        coming from /admin/edit_user.mako template'''
        
        if id:
            # Modify user
            new_user = Session.query(Users).get(int(id))
            new_user.firstname = request.POST.get('firstname')
            new_user.lastname = request.POST.get('lastname')
            new_user.email = request.POST.get('email').strip()
            new_user.logname = request.POST.get('logname').strip()
            pw = request.POST.get('password', '')
            if pw:
                new_user.password = unicode(hashlib.sha1(pw).hexdigest(), 'utf-8')
        else:
            # Create user
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email').strip()
            logname = request.POST.get('logname').strip()
            passw = unicode(hashlib.sha1(request.POST.get('password')).hexdigest(), 'utf-8')
            
            # Check for the existance of the user
            user = Session.query(Users).filter(Users.email==email).all()
            if user:
                h.flash.set_message('User already exist.', 'error')
                h.redirect('/admin/create_user')
            # Check for the existance of the logname
            user = Session.query(Users).filter(Users.logname==logname).all()
            if user:
                h.flash.set_message('Logname already in use.', 'error')
                h.redirect('/admin/create_user')
            
            # Select role Member 
            role = Session.query(Role).filter(Role.name == 'Member').first()
            # Create new user
            new_user = Users()
            new_user.firstname = firstname
            new_user.lastname = lastname
            new_user.logname = logname
            new_user.email = email
            new_user.password = passw
            new_user.roles.append(role)
        
        Session.add(new_user)
        Session.commit()
        
        h.flash.set_message('User created/modified succesfully.', 'success')
        h.redirect('/admin/users_list')
        
    @check_access('Manage Members')
    def edit_user(self, id=None):
        if id:
            c.user = Session.query(Users).get(int(id))
            return render('/admin/edit_user.mako')
            
    @check_access('Manage Members')
    def remove_user(self, id=None):
        if id:
            user = Session.query(Users).get(int(id))
            user.removed = True
            Session.add(user)
            Session.commit()
            h.flash.set_message('User removed succesfully.', 'success')
            h.redirect('/admin/users_list')
            
    @check_access('Manage Members')
    def enable_user(self, id=None):
        if id:
            user = Session.query(Users).get(int(id))
            user.removed = False
            Session.add(user)
            Session.commit()
            h.flash.set_message('User enabled succesfully.', 'success')
            h.redirect('/admin/users_list')
   
   
