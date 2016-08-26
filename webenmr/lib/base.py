"""The base Controller API

Provides the BaseController class for subclassing.
"""
import logging
from decorator import decorator
from paste.request import construct_url
from paste.httpexceptions import HTTPMovedPermanently
from pylons import request, session, response, tmpl_context as c
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render 
from sqlalchemy.sql.expression import asc, desc
from sqlalchemy.sql import and_
from pylons import url
from pylons.controllers.util import redirect

from webenmr.lib import helpers as h
from webenmr.model.meta import Session
from webenmr.model import Users, Menu, CalculationTipology

log = logging.getLogger(__name__)

home_dir_prefix = 'user_'
portalwithmenu = ['amps-nmr', 'xplor-nih', 'maxocc']
class BaseController(WSGIController):
    public_urls = ['/users/index', '/users/logout', '/users/pass_reset']
    def __before__(self):
        """
        Check if a user is logged in, and if not, redirect them to the
        login page.
        """
        
        if not u'REMOTE_USER' in session:           
            if not request.environ[u'PATH_INFO'] in self.public_urls:
                log.debug('PATH_INFO: %s' % request.environ[u'PATH_INFO'])
                #session[u'path_before_login'] = request.environ[u'PATH_INFO']
                #session.save()
                redirect(url('/users/index'))
                
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        try:
            id = ''
            if 'type' in request.params:
                id = request.GET.get('type')
                #if id == 'amps-nmr':
                #    c.num = 3
                #elif id == 'maxocc':
                #    c.num = 12
                #elif id == 'anisofit':
                #    c.num = 11
            elif 'id' in request.params:
                id = request.GET.get('id')
                #print '*'*40,id
            elif session.has_key('PORTAL'):
                id = session['PORTAL']
            else:
                id = 'amps-nmr'
                #c.num = 3
            #if session.has_key('PORTAL'):
            #    if session['PORTAL'] == 'amps-nmr':
            #        c.num = 3
            #        id = session['PORTAL']
            #    elif session['PORTAL'] == 'maxocc':
            #        c.num = 13
            #        id = session['PORTAL']
            #    elif session['PORTAL'] == 'anisofit':
            #        c.num = 11
            #        id = session['PORTAL']
            #f = open('/tmp/mah', 'w')
            #f.write(id)
            #f.close()
            
            if id == '1' or id == '5':
                
                return WSGIController.__call__(self, environ, start_response)
            if id in portalwithmenu:
                if id == 'amber':
                    print "someone use amber yet!"
                    id = 'amps-nmr'
                ca = Session.query(CalculationTipology).filter(CalculationTipology.tipology == id)
                type_id = ca[0].id
                portal_menu = Session.query(Menu).filter(and_(Menu.parent_id==None, Menu.sibling_id==None, Menu.calctype_id == type_id)).order_by(Menu.weight.asc()).all()
                all_menu = Session.query(Menu).filter(and_(Menu.parent_id==None, Menu.sibling_id==None, Menu.calctype_id == 4)).order_by(Menu.weight.asc()).all()
                c.main_menu = sorted(portal_menu + all_menu, key=lambda menu: menu.weight)
            if u'REMOTE_USER' in session:
                c.current_user = Session.query(Users).get(session[u'REMOTE_USER']) 
            
            #log.debug(len(c.main_menu))
            #if u'REMOTE_USER' in session:
                #c.current_user = Session.query(Users).get(session[u'REMOTE_USER'])
            #if not environ[u'PATH_INFO'].endswith(u'/'):
                #environ[u'PATH_INFO'] += u'/'
                #url = construct_url(environ)
                #log.debug('PATH_INFO: %s URL: %s' % (environ[u'PATH_INFO'], url))
                #raise HTTPMovedPermanently(url)
            print "*******************", id
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

def check_access(permission):
    """
    A decorator used to check the access level of a member against a permission.
    """
    def validate(func, self, *args, **kwargs):
        if u'REMOTE_USER' in session:
            user = Session.query(Users).get(session[u'REMOTE_USER'])
            if user.has_access(permission):
                return func(self, *args, **kwargs)
            else:
                h.flash.set_message(u'You don\'t have access to that area.', 'error')
                h.redirect(h.url('/'))
                #h.redirect_to(u'/')
        else:
            return func(self, *args, **kwargs)
    return decorator(validate)

     
def sendmail(submit_to, submit_cc, subject, sender, body):
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email.Utils import COMMASPACE, formatdate
    from email import Encoders

    to = submit_to
    cc = submit_cc
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = submit_to
    msg['Cc'] = cc
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    try:
        server = smtplib.SMTP("alpha.cerm.unifi.it")
        
        server.sendmail(msg['From'], to, msg.as_string())
        #server.sendmail(sender, submit_to, msg.as_string())
        server.quit()
        return True
    except:
        return False
    
