import logging
import os
import hashlib
import datetime
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config
import pycurl
from lxml import etree
from webenmr.lib.base import *
from webenmr.lib import Certificates
from webenmr.model import Menu, Users, Role
import MySQLdb
from dateutil import parser

log = logging.getLogger(__name__)
os.umask(0002)

def save_log(stri):
    os.umask(0006)
    file = open("/tmp/log_users_pylons", "a")
    file.writelines(stri)
    file.close()
    os.umask(0002)

def save_log_sso(stri):
    os.umask(0006)
    file = open("/tmp/SSO_log_users_pylons", "a")
    file.writelines(stri)
    file.close()
    os.umask(0002)

class GetCurl:
    def __init__(self):
        self.contents = ''
    def body_callback(self, buf):
        self.contents = self.contents + buf

class UsersController(BaseController):
    def __before__(self):
        """
        This __before__ method calls the parent method, and then sets up the
        tabs on the page.
        """
        #BaseController.__before__(self)
        
        c.page_base = u'Users'
        #c.main_menu = Session.query(Menu).filter(and_(Menu.parent_id==None, Menu.sibling_id==None)).order_by(Menu.weight.asc()).all()
        c.page_title = u'Welcome'
        
    def index(self):
        """Perform the following check:- Check if the user is a VOMS member
        - Check if the user is a new member. In that case update the db
        - Check if the user has a myproxy certificate. In that case check the expiration date
        - Check the Robot certificate expiration date
        Return the index page or a page with a message showing that the user is not a VOMS member"""
        
        save_log("############ INI LOG USERS.py " + str(datetime.datetime.now()) + " #####################\n")
        idx = request.GET.get('id', '')
        uid = request.GET.get("uid", "")
        #save_log(idx + " *******\n")
        #save_log(uid + " *******\n")
        #result = []
        #for k in request.environ.keys():
        # result.append("%s: %s" % (k, request.environ[k]))
        key = 'SSL_CLIENT_S_DN'
        exp_date = 'SSL_CLIENT_V_END'
        server_cert = '/home/webenmr/WebENMR/infn_certs/py-enmr.cerm.unifi.it.crt'
        server_key = '/home/webenmr/WebENMR/infn_certs/py-enmr.cerm.unifi.it.key'
        #server_cert = '/etc/httpd/conf/ssl.crt/py-enmr.cerm.unifi.it.crt'
        #server_key = '/etc/httpd/conf/ssl.key/py-enmr.cerm.unifi.it.key'
        c.message = ''
        c.IP = request.environ['REMOTE_ADDR']
        #if 'PROXY_INITIALIZED' in session:
        #    save_log("############ PROXY_INITIALIZED In session #######\n")
        #    c.current_user = Session.query(Users).get(session['REMOTE_USER'])
        #    return render('/users/index.mako')
        # Check for SSL_CLIENT_S_DN in the wsgi environment
        save_log("####request environ INI ######\n")
        for pino in request.environ:
            save_log("%s \n" %pino)
        save_log("####request environ END ######\n")
        if key in request.environ:
            save_log("############ VOMS REQUEST If END NOT SHOWED VOMS CONNECTION ERROR #######\n")
            ssl_client = request.environ[key]
            save_log(ssl_client + "\n")
            # Ask for a list of VOMS members
            t = GetCurl()
            cu = pycurl.Curl()
            cu.setopt(cu.URL, 'https://voms2.cnaf.infn.it:8443/voms/enmr.eu/services/VOMSCompatibility?method=getGridmapUsers')
            cu.setopt(cu.WRITEFUNCTION, t.body_callback)
            cu.setopt(cu.VERBOSE, True)
            cu.setopt(cu.PORT, 8443)
            cu.setopt(cu.SSLCERT, server_cert)
            cu.setopt(cu.SSLCERTPASSWD, '')
            cu.setopt(cu.SSLKEY, server_key)
            cu.setopt(cu.SSLKEYPASSWD, '')
            cu.setopt(cu.HTTPGET, 1)
            cu.setopt(cu.SSL_VERIFYPEER, False)
            cu.perform()
            cu.close()
            save_log("############ VOMS REQUEST END #######\n")
            save_log("#######USER DN from apache #########\n")
            save_log(ssl_client + "\n")
            save_log("####################################\n")
            # Check if the DN is in the VOMS members list
            save_log("####### INI VOMS list of users #######\n")
            save_log(etree.tostring(etree.fromstring(t.contents), pretty_print=True))
            save_log("\n")
            save_log("####### END VOMS list of users #######\n")
            
            if t.contents.find(ssl_client) != -1:
                if idx == '5':
                    rem_IP = request.environ['REMOTE_ADDR']
                    save_log_sso("####### SSO CONNECTION REQUEST at " + str(datetime.datetime.now()) + " FROM IP " + rem_IP +" #####################\n")
                    save_log_sso("SSO UID check request for: " + uid + "\n")
                    ssl_expdate = request.environ[exp_date]
                    try:
                        db = MySQLdb.connect(host="hostname",user="username",passwd="passwd", db="db")
                        crs = db.cursor()
                        crs.execute("""SELECT dn, expd FROM ssoxs_users WHERE uid=%s"""%uid)
                        res = crs.fetchone()
                        #check the if DN are present for other users
                        crs.execute("""SELECT uid FROM ssoxs_users WHERE dn='%s'"""%ssl_client)
                        res_m = crs.fetchall()
                        save_log_sso('SSO ENRICO: %s\n ' % res_m)
                        if len(res_m) > 1:
                            save_log_sso('SSO  DN  %s are present in differents users \n' %ssl_client)
                            save_log_sso('SSO user ')
                            for i in res_m:
                                save_log_sso(' %s'%i)
                            save_log_sso('\n')
                            return render('/users/SSO_8.mako', extra_vars={'uid': uid, 'dn1' : res[0]})
    
                        print "#############RES############"
                        print res
                        if res[0]:
                            if res[0] == ssl_client:
                                if  parser.parse(ssl_expdate) > parser.parse(res[1]):
                                    save_log_sso("SSO Certificate expiration date updated\n") 
                                    save_log_sso('SSO  DN: %s\n' %ssl_client)
                                    save_log_sso('SSO new certifciate expiration date: %s\n' %ssl_expdate)
                                    #crs.execute("""UPDATE users SET dn='%s' WHERE uid=%s""" %(ssl_client, uid))
                                    #db.commit()
                                    crs.execute("""UPDATE ssoxs_users SET expd='%s' WHERE uid=%s""" %(ssl_expdate, uid))
                                    db.commit()
                                    return render('/users/SSO_7.mako', extra_vars={'uid': uid, 'dn1' : res[0], 'expdate' : ssl_expdate })
                                    
                                save_log_sso('SSO USER DN present: %s \n' %res[0])
                                #SSO USER was present OK
                                #h.url_for('SSO_resp_6')
                                return render('/users/SSO_6.mako', extra_vars={'uid': uid, 'dn1' : res[0]})
                            else:
                                save_log_sso('SSO USER DN present but DN in certificate: %s  are different from the DB %s \n' %(res[0], ssl_client))
                                #SSO DN in certificate and DN in DB are differents
                                #h.url_for('SSO_resp_5')
                                return render('/users/SSO_5.mako', extra_vars={'uid': uid, 'dn1' : res[0], 'dn2' : ssl_client })
                                
                        else:
                            save_log_sso("SSO 'DN empty'\n") 
                            save_log_sso('SSO new DN: %s\n' %ssl_client)
                            save_log_sso('SSO certifciate expiration date: %s\n' %ssl_expdate)
                            crs.execute("""UPDATE ssoxs_users SET dn='%s' WHERE uid=%s""" %(ssl_client, uid))
                            db.commit()
                            crs.execute("""UPDATE ssoxs_users SET expd='%s' WHERE uid=%s""" %(ssl_expdate, uid))
                            db.commit()
                            
                            
                    except MySQLdb.Error, e:
                        save_log_sso("####### DB CONNECTION PROBLEM #######\n")
                        save_log_sso("Error %d: %s\n" % (e.args[0],e.args[1]))
                        #SSO exception Connection Problem
                        #h.url_for('SSO_resp_4')
                        return render('/users/SSO_4.mako', extra_vars={'uid': uid})
                    
                    save_log_sso("####### DB REGISTRATION OK #######\n")
                    #SSO everything OK
                    #h.url_for('SSO_resp_3')
                    return render('/users/SSO_3.mako', extra_vars={'uid': uid})
                    
                no_proxy = False
                save_log("USER NOT PRESENT IN DB\n")
                user = Session.query(Users).filter(Users.dn==ssl_client).first()
                # New user
                if not user:
                    try:
                        (f, l) = ssl_client.split('/CN=')[1].split()
                    except ValueError:
                        f = ssl_client.split('/CN=')[1].split()[0]
                        l = ' '.join(ssl_client.split('/CN=')[1].split()[1:])
        
                    role = Session.query(Role).filter(Role.name == 'Member').first()
                    save_log("NEW USER NAME " + f  + "\n")
                    save_log("NEW USER LASTNAME " + l + "\n")
                    new_user = Users()
                    new_user.firstname = f
                    new_user.lastname = l
                    new_user.dn = ssl_client
                    new_user.roles.append(role)
                    Session.add(new_user)
                    Session.commit()
                    session['REMOTE_USER'] = new_user.id
                    session.save()
                    c.current_user = Session.query(Users).get(new_user.id)
                    no_proxy = True
                    
                else:
                    # User already present in the database
                    save_log("USER ALRADY PRESENT IN DB \n")
                    
                    session['REMOTE_USER'] = user.id
                    session.save()
                    c.current_user = user
                    if user.removed:
                        return render('/users/user_removed_ssl.html')
                    # Check for the user's myproxy presence
                    #if user.myproxy:
                    ## Instantiate the X509Certificate class 
                    #x509 = x509_certificate.X509Certificate()
                    ## Load the myproxy certificate
                    #ret = x509.load(user.myproxy.myproxy)
                    #if ret['OK']:
                    ## Check if it's expired
                    #ret = x509.hasExpired()
                    #if ret['OK']:
                    #c.expired = True
                    #else:
                    ## Get the expiration date
                    #ret = x509.getNotAfterDate()
                    #if ret['OK']:
                    #c.expiration_date = ret['Value']
                    #else:
                    #c.message = ret['Message']
                    #else:
                    ## User hasn't a myproxy certificate
                    #no_proxy = True
                    no_proxy = True
                    
                # Home directory creation
                user = Session.query(Users).get(session['REMOTE_USER'])
                if user.home:
                    home = user.home
                else:
                    home = '%s%s' % (home_dir_prefix, user.id)
                session['HOME'] = os.path.join(config['app_conf']['working_dir'], home)
                session.save()
                if not os.path.isdir(session['HOME']):
                    os.makedirs(session['HOME'])
                # The user hasn't a proxy certificate
                # Perform Robot certificate checking
                if no_proxy:
                    # Set ROBOT Certificate
                    if session['PORTAL'] == 'amps-nmr':
                        attribute = "/enmr.eu/amber"
                    elif session['PORTAL'] == 'xplor-nih':
                        attribute = "/enmr.eu/xplornih"
                    else:
                        attribute = ""
                    ret = Certificates.proxy_initialize(attribute)
                    #ret = Certificates.proxy_initialize()
                    if ret['OK']:
                        #print "VOMS_PROXY ", session['voms_proxy']
                        c.message = ret['Value']
                    else:
                        c.message = 'voms-proxy-init problem: %s' % ret['Message']
            
                if id:
                    log.debug(session['REMOTE_USER'])
                    if 'REMOTE_USER' in session:
                        user = Session.query(Users).get(session['REMOTE_USER'])
                        if user.logname:
                            return render('/users/user_ssl_already_created.html')
                    return render('/users/create_user_ssl.html')
                else:
                    return render('/users/index.mako')
            else:
                save_log("USER NOT PRESENT IN VOMS\n")
                if idx == '5':
                    #SSO user not present in VOMS
                    save_log_sso("USER NOT PRESENT IN VOMS\n")
                    #h.url_for('SSO_resp_2')
                    return render('/users/SSO_2.mako', extra_vars={'uid': uid})
                return render('/users/no_voms_member.mako')
        
        # HTTP Connection. No certificate.
        else:
            if idx == '5':
                    #SSO certifciate not present in browser
                    save_log("USER CERTIFCATE NOT PRESENT IN THE BROWSER\n")
                    #h.url_for('SSO_resp_1')
                    return render('/users/SSO_1.mako', extra_vars={'uid': uid})
                
            if 'PROXY_INITIALIZED' in session:
                save_log("############ PROXY_INITIALIZED In session #######\n")
                c.current_user = Session.query(Users).get(session['REMOTE_USER'])
                return render('/users/index.mako')        
            if 'REMOTE_USER' in session:
                c.current_user = Session.query(Users).get(session['REMOTE_USER'])
                if c.current_user.logname == 'guest':
                    return render('/users/index.mako')
                # Set ROBOT Certificate
                print "VARIABILI DI SESSIONE"
                print session
                if session['PORTAL'] == 'amps-nmr':
                    attribute = "/enmr.eu/amber"
                elif session['PORTAL'] == 'xplor-nih':
                    attribute = "/enmr.eu/xplornih"
                else:
                    attribute = ""
                ret = Certificates.proxy_initialize(attribute)
                #ret = Certificates.proxy_initialize()
                if ret['OK']:
                    #print "VOMS_PROXY ", session['voms_proxy']
                    c.message = ret['Value']
                else:
                    c.message = 'voms-proxy-init problem: %s' % ret['Message']
                print '*'*40,c.message
                return render('/users/index.mako')
                    
            h.redirect('/access/index')
        
        #result = []
        #for k in request.environ.keys():
        #result.append("%s: %s" % (k, request.environ[k]))
        #return "<br>".join(result)
        #

    def logout(self):
        if 'REMOTE_USER' in session:
            del session['REMOTE_USER']
            session.save()
        if 'PROXY_INITIALIZED' in session:
            del session['PROXY_INITIALIZED']
            session.save()
        #if 'voms_proxy_file' in session:
        #del session['voms_proxy_file']
        #session.save()
        h.flash.set_message('Logged out successfully.', 'success')
        h.redirect('/access/index/'+session['PORTAL'])

    def pass_resetOrig(self):
        '''Reset the user password. Generate a new password and send it to
        the email address supplied by user using /users/reset_password.mako
        template.'''
        email = request.POST.get('yourv3ry3ma1l', '')
        if 'PORTAL' in session:
            c.title = session['PORTAL'].upper()
        else:
            c.title = ""
        if not email:
            return render('/users/reset_password.mako')
        else:
            user = Session.query(Users).filter(Users.email == email).all()
            if not user:
                h.flash.set_message(u'Your email address seems not registered.', u'error')
                h.redirect('/access/index')
            user = Session.query(Users).filter(and_(Users.email == email, Users.removed==False)).first()
            newpass = self.nicepass(alpha=4, numeric=2)
            user.password = unicode(hashlib.sha1(newpass).hexdigest(), 'utf-8')
            try:
                Session.add(user)
                Session.commit()
            except:
                h.flash.set_message(u'An error occurred during password generation.', u'error')
                h.redirect('/access/index')
                
            body = 'The new password is: %s' %newpass
            email_addr = user.email
            subject = '%s: Password reset' % session['PORTAL']
            sender = 'web-enmr@cerm.unifi.it'
            submit_cc = ''
            r = sendmail(email_addr, submit_cc, subject, sender, body)
            if r:
                h.flash.set_message(u'A new password has been sent to you.', u'success')
                h.redirect('/access/index')
            else:
                h.flash.set_message(u'Your password was reset. But an error occurred during sending you an email.', u'error')
                h.redirect('/access/index')

    def pass_reset(self):
        '''Reset the user password. Generate a new password and send it to
        the email address supplied by user using /users/reset_password.mako
        template.'''
        if 'pass_reset' in session:
            del session['pass_reset']
            session.save()
        emailBOT = request.POST.get('email', '')
        if emailBOT:
            print "Malicious BOT - tried to use %s" % emailBOT
        else:
            email = request.POST.get('3m61l', '')
            print email
            if 'PORTAL' in session:
                c.title = session['PORTAL'].upper()
            else:
                c.title = ""
            #if not email:
            #return render('/users/reset_password.mako')
            #else:
            user = Session.query(Users).filter(Users.email == email).all()
            if not user:
                print 'doesn\'t exist any user with this mail: %s' %email
                h.flash.set_message(u'Your email address seems not registered.', u'error')
                c.pass_reset = 'Doesn\'t exist any user with this email address.'
                session['pass_reset'] = 'Doesn\'t exist any user with this email address.'
                session.save()
                h.redirect('/users/forgotten')
            user = Session.query(Users).filter(and_(Users.email == email, Users.removed==False)).first()
            print "User %s %s is changing your password" %(user.firstname, user.lastname)
            oldpass = user.password
            newpass = self.nicepass(alpha=4, numeric=2)
            user.password = unicode(hashlib.sha1(newpass).hexdigest(), 'utf-8')
            try:
                Session.add(user)
                Session.commit()
            except:
                h.flash.set_message(u'An error occurred during password generation. Try again later.', u'error')
                c.pass_reset = 'An error occurred during password generation. Try again later.'
                session['pass_reset'] = 'An error occurred during password generation. Try again later.'
                session.save()
                h.redirect('/users/forgotten')
            body = 'Your account information:\n    email: %s\n    username: %s\n    new password: %s\n\nPlease keep the above information safe.' %(user.email, user.logname, newpass)
            email_addr = user.email
            subject = '%s: credentials' % session['PORTAL']
            sender = 'web-enmr@cerm.unifi.it'
            submit_cc = ''
            r = sendmail(email_addr, submit_cc, subject, sender, body)
            if r:
                h.flash.set_message(u'A new password has been sent to you.', u'success')
                del session['pass_reset']
                session.save()
                h.redirect('/access/index/%s'% session['PORTAL'].lower())
            else:
                print 'An error sending you an mail'
                user.password = oldpass
                Session.add(user)
                Session.commit()
                h.flash.set_message(u'An error occurred during sending you an email. Try again later', u'error')
                c.pass_reset = 'An error occurred during sending you an email. Try again later.'
                session['pass_reset'] = 'An error occurred during sending you an email. Try again later.'
                session.save()
                h.redirect('/users/forgotten')

    def forgotten(self):
        if 'PORTAL' in session:
            c.title = session['PORTAL'].upper()
        else:
            c.title = 'AMPS-NMR'
            session['PORTAL'] = 'AMPS-NMR'
            session.save()
        return render('/users/forgotten.mako')

    def nicepass(self, alpha=6, numeric=2):
        """
        returns a human-readble password (say rol86din instead of 
        a difficult to remember K8Yn9muL ) 
        """
        import string
        import random
        vowels = ['a','e','i','o','u']
        consonants = [a for a in string.ascii_lowercase if a not in vowels]
        digits = string.digits
        
        ####utility functions
        def a_part(slen):
            ret = ''
            for i in range(slen):
                if i%2 == 0:
                    randid = random.randint(0,20) #number of consonants
                    ret += consonants[randid]
                else:
                    randid = random.randint(0,4) #number of vowels
                    ret += vowels[randid]
            return ret
        
        def n_part(slen):
            ret = ''
            for i in range(slen):
                randid = random.randint(0,9) #number of digits
                ret += digits[randid]
            return ret
            
        ####
        fpl = alpha/2
        if alpha % 2 :
            fpl = int(alpha/2) + 1
        lpl = alpha - fpl
        
        start = a_part(fpl)
        mid = n_part(numeric)
        end = a_part(lpl)
        
        return "%s%s%s" % (start,mid,end)       
