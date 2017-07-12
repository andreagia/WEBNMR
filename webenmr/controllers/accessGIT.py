import logging
import os
import hashlib
import random
import shutil
from pylons import request,response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons import config
import pycurl
from sqlalchemy.sql import and_
from webenmr.lib.base import *
from webenmr.lib import x509_certificate
from webenmr.lib import return_values
from webenmr.model import Users, Menu, Role, CalculationTipology
from webenmr.lib import helpers as h
from datetime import *
from Crypto.Cipher import Blowfish
from Crypto import Random
from base64 import b64encode, b64decode, urlsafe_b64decode, urlsafe_b64encode, standard_b64decode, standard_b64encode, encodestring, decodestring, encode
from dateutil import parser
import pytz
import MySQLdb
from dateutil import parser
import httplib, urllib, random, string, pprint, urllib2, pycurl,cStringIO
import simplejson as json
from webenmr.lib import postpy
import base64


def mult4string(data):
    while (len(data) % 4 != 0):
        data = data + "="
    return data

def save_log(stri):
    os.umask(0006)
    file = open("/tmp/log_users_pylons", "a")
    file.writelines(stri)
    file.close()
    os.umask(0002)

log = logging.getLogger(__name__)
os.umask(0002)
portal = ['amps-nmr', 'xplor-nih', 'anisofit', 'antechamber', 'maxocc', 'sednmr']
class AccessController(BaseController):
    
    client_id = "###########"
    client_secret = "###########3"
    uspaswd = "###########"

    def __before__(self):
        """
        This __before__ method calls the parent method, and then sets up the
        tabs on the page.
        """
        #BaseController.__before__(self)
        c.page_base = u'Access'
        #if 'REMOTE_USER' in session:
        #    c.current_user = Session.query(Users).get(session['REMOTE_USER'])
        #    c.main_menu = Session.query(Menu).filter(and_(Menu.parent_id==None, Menu.sibling_id==None)).order_by(Menu.weight.asc()).all()
        c.page_title = u'Welcome'
        #cert = os.path.join(config['app_conf']['cert_dir'], 'x509up_u0')
        #os.environ['X509_USER_PROXY'] = cert
    
    def check_mail_local(self, uid):
        #mail:
        print "acces using email for uid " + uid
        print "retrive DB info"
        db = MySQLdb.connect(host="",user="",passwd="", db="")
        crs = db.cursor()
        crs.execute("""SELECT mail,name FROM ssoxs_users WHERE uid=%s"""%uid)
        res = crs.fetchone()
        if len(res[0]) > 1:
            mail = res[0].lower()
        #name:
        if len(res[1]) > 0:
            f = res[1].split()[0]
        if len(res[1]) > 0:
            if len(res[1].split()) > 1:
                l = res[1].split()[1]
            else:
                l = ""
        else:
            l = ""
        print res
        member = Session.query(Users).filter(and_(Users.email == mail, Users.removed==False)).first()
        if not member:
            print "########## SSO Create new User using mail ################"
            print mail
            logname = "SSO" + str(random.randint(100000, 999999))
            
            #try:
            #    (f, l) = DN.split('/CN=')[1].split()
            #except ValueError:
            #    f = DN.split('/CN=')[1].split()[0]
            #    l = ' '.join(DN.split('/CN=')[1].split()[1:])

            role = Session.query(Role).filter(Role.name == 'Member').first()
            save_log("NEW USER NAME " + f  + "\n")
            save_log("NEW USER LASTNAME " + l + "\n")
            new_user = Users()
            new_user.firstname = f
            new_user.lastname = l
            new_user.logname =  logname
            new_user.dn = ""
            new_user.email = mail
            new_user.password = "98vsfoiooioe"
            new_user.ssoxs_uid = int(uid)
            new_user.roles.append(role)
            Session.add(new_user)
            Session.commit()
            new_user.home = "user_%s" %new_user.id
            Session.commit()
            session['REMOTE_USER'] = new_user.id
            session.save()
            c.current_user = Session.query(Users).get(new_user.id)
            no_proxy = True
            user = Session.query(Users).get(session['REMOTE_USER'])
            if user.home:
                home = user.home
            else:
                home = '%s%s' % (home_dir_prefix, user.id)
            session['HOME'] = os.path.join(config['app_conf']['working_dir'], home)
            session.save()
            if not os.path.isdir(session['HOME']):
                os.makedirs(session['HOME'])
                
            h.flash.set_message('You have successfully logged in.', 'success')
            h.redirect('/users/index')
            
        else:
            # Check for the user home. If the user was created by the admin
            # the home field is not in the db. So it's the moment to create it.
            if not member.home:
                member.home = '%s%s' % (home_dir_prefix, member.id)
                Session.add(member)
                Session.commit()
            if not member.ssoxs_uid:
                member.ssoxs_uid = int(uid)
                Session.add(member)
                Session.commit()
                print "protocol mail add ssox_uid" + uid
            # Session variables binding    
            session['REMOTE_USER'] = member.id
            session['LOGNAME'] = member.logname
            session['HOME'] = os.path.join(config['app_conf']['working_dir'], member.home)
            session.save()
            # Home directory creation
            if not os.path.isdir(session['HOME']):
                os.makedirs(session['HOME'])
            
            h.flash.set_message('You have successfully logged in.', 'success')
            h.redirect('/users/index')
            
        session['PORTAL'] = 'oops!'
        session.save()
        c.title='Oops!'
        return render('/access/wrongportal.mako')
    
    def check_DN_local(self, DN, uid):
        member = Session.query(Users).filter(and_(Users.dn == DN, Users.removed==False)).first()
        if not member:
            print "########## SSO Create new User ################"
            print DN
            #retrive information using xml_rpc from DB
            #TODO
            #check validity of certifcate
            #check DN
            #if DN == DNfrom xml_rpc
            logname = "SSO" + str(random.randint(100000, 999999))
            mail = "SSO@SSO.it"
            try:
                (f, l) = DN.split('/CN=')[1].split()
            except ValueError:
                f = DN.split('/CN=')[1].split()[0]
                l = ' '.join(DN.split('/CN=')[1].split()[1:])

            role = Session.query(Role).filter(Role.name == 'Member').first()
            save_log("NEW USER NAME " + f  + "\n")
            save_log("NEW USER LASTNAME " + l + "\n")
            new_user = Users()
            new_user.firstname = f
            new_user.lastname = l
            new_user.logname =  logname
            new_user.dn = DN
            new_user.email = mail
            new_user.ssoxs_uid = int(uid)
            new_user.password = "98vsfoiooioe"
            new_user.roles.append(role)
            Session.add(new_user)
            Session.commit()
            new_user.home = "user_%s" %new_user.id
            Session.commit()
            session['REMOTE_USER'] = new_user.id
            session.save()
            c.current_user = Session.query(Users).get(new_user.id)
            no_proxy = True
            user = Session.query(Users).get(session['REMOTE_USER'])
            if user.home:
                home = user.home
            else:
                home = '%s%s' % (home_dir_prefix, user.id)
            session['HOME'] = os.path.join(config['app_conf']['working_dir'], home)
            session.save()
            if not os.path.isdir(session['HOME']):
                os.makedirs(session['HOME'])
                
            h.flash.set_message('You have successfully logged in.', 'success')
            h.redirect('/users/index')
            
        else:
            # Check for the user home. If the user was created by the admin
            # the home field is not in the db. So it's the moment to create it.
            if not member.home:
                member.home = '%s%s' % (home_dir_prefix, member.id)
                Session.add(member)
                Session.commit()
            #update ssoxs_uid
            if not member.ssoxs_uid:
                member.ssoxs_uid = int(uid)
                Session.add(member)
                Session.commit()
                print "protocol DN add ssox_uid"
            
            # Session variables binding    
            session['REMOTE_USER'] = member.id
            session['LOGNAME'] = member.logname
            session['HOME'] = os.path.join(config['app_conf']['working_dir'], member.home)
            session.save()
            # Home directory creation
            if not os.path.isdir(session['HOME']):
                os.makedirs(session['HOME'])
            
            h.flash.set_message('You have successfully logged in.', 'success')
            h.redirect('/users/index')
            
        session['PORTAL'] = 'oops!'
        session.save()
        c.title='Oops!'
        return render('/access/wrongportal.mako')
            
    def index_SSO(self, id_site ,string=None):
        #remeber to set as file
        key = "###############"
        #key = "mkllhgads8731ekglad7892qdq54345676567687665555476fdghe45"
        #key = "mkllhgads8731ekglad7892qdqkglkjgq89321dhcwdjhw9832jkhdfw781t62lcdnmnaq7860fw60"
        #string = request.GET.get("SSO","")
        print len(string)
        print len(string) % 8
        #if len(string) % 8 != 0:
        #    c.title = 'AMPS-NMR'
        #    return render('/access/intro.mako')
        print "##### SSO direct link access ###########"
        print "GET string"
        print len(string)
        print "----%s----" %string
        print "discard first 8 byte to remove encryption problem CBC"
        #add == in nth end of string and encode utf-8
        iv = Random.new().read(Blowfish.block_size)
        string1 = mult4string(string.encode("utf-8").strip("~"))
        print string1
        cipher = Blowfish.new(key, Blowfish.MODE_CBC,iv)
        #print urlsafe_b64decode(string.encode("utf-8"))
        try:
            encStrF = cipher.decrypt(urlsafe_b64decode(string1))
        except:
            print "error decripting get variables"
            session['PORTAL'] = 'oops!'
            session.save()
            c.title='Oops!'
            return render('/access/wrongportal.mako')
        print encStrF
        try:
            encStr = encStrF[8:].encode("utf-8")
        except:
            print "BAD unicode format"
            session['PORTAL'] = 'oops!'
            session.save()
            c.title='Oops!'
            return render('/access/wrongportal.mako')
            
        print encStrF[8:].encode("utf-8")
        print "OUT request"
        print len(encStr)
        print encStr
        #h.flash.set_message(u'Credentials %s'%encStr, u'success')
        c.IP = request.environ['REMOTE_ADDR']
        print "SSO IP request connection"
        print c.IP
        
        if id_site == 'xplor-nih':
            c.title = "Xplor-NIH"
        elif id_site == 'amps-nmr':
            c.title = 'AMPS-NMR'
        elif id_site == "maxocc":
            c.title = 'Maxocc'
        else:
            session['PORTAL'] = 'oops!'
            session.save()
            c.title='Oops!'
            return render('/access/wrongportal.mako')
        
        try:
            sso_info = encStr.split("##")
        except:
            session['PORTAL'] = 'oops!'
            session.save()
            c.title='Oops!'
            return render('/access/wrongportal.mako')
        if len(sso_info) == 5 :
            if sso_info[0] == "SSOOK":
                print "SSO connection OK"
                if sso_info[2] == c.IP:
                    print "IP OK"
                try:
                    date_sso = parser.parse(sso_info[4])
                    print parser.parse(sso_info[4])
                    print parser.parse(str((datetime.now() + timedelta(minutes=1))))
                except:
                    print "error in data try datetime"
                    try:
                        print sso_info[4]
                        date_sson = ""
                        for it in sso_info[4].encode('utf-8'):
                            if it == "0" or it == "1" or it == "2" or it == "3" or it =="4" or it == "5" or it == "6" or it == "7" or it == "8" or it == "9":
                                date_sson = date_sson + it
    
                        date_sso = datetime.fromtimestamp(int(date_sson))
                        print date_sso
                    except:
                        print "error in time"
                        session['PORTAL'] = 'oops!'
                        session.save()
                        c.title='Oops!'
                        return render('/access/wrongportal.mako')
                
                #Consider that SSO are in Dutch for locatime
                amsterdam = pytz.timezone('Europe/Amsterdam')
                #time of service location
                roma = pytz.timezone('Europe/Rome')
                roma_deltaM = roma.localize((datetime.now() - timedelta(minutes=30)))
                roma_deltaP = roma.localize((datetime.now() + timedelta(minutes=30)))
                amsterdam_request = amsterdam.localize(date_sso)
                if amsterdam_request < roma_deltaP and amsterdam_request > roma_deltaM:
                #if parser.parse(sso_info[3]) < parser.parse(str((datetime.datetime.now() + datetime.timedelta(minutes=20)))) and parser.parse(sso_info[3]) > parser.parse(str((datetime.datetime.now() - datetime.timedelta(minutes=20)))) :
                    print "TIME OK"
                    string_DN = sso_info[3].encode('utf-8').decode('string_escape').decode('utf-8')
                    string_UID = sso_info[1].encode('utf-8').decode('string_escape').decode('utf-8')
                    # info for mail account creation example
                    # mail:giachetti@cerm.unifi.it&&name:Andrea&&lastname:Giachetti
                    if len(string_DN) > 3:
                        print "USE DN to enter in the service " + string_DN
                        self.check_DN_local(string_DN, string_UID)
                    elif len(string_UID) > 0:
                        #retrive mail and user name from xmlrpc (now for DB)
                        self.check_mail_local(string_UID)
                        
                else:
                    print "The request is expired!"
                    print "Time of server creation", amsterdam_request
                    print "Time of client request", datetime.now()
                    
        session['PORTAL'] = 'oops!'
        session.save()
        c.title='Oops!'
        return render('/access/wrongportal.mako')
        #return render('/access/intro.mako')

    def index(self, id='amps-nmr'):
        # Return a rendered template
        #return render('/access.mako')
        # or, return a string
        #if 'type' in request.params:
        #    id = request.GET.get('type')
        if id in portal:
            session['PORTAL'] = id
            session.save()
            t = request.GET.get("type", "")
            string = request.GET.get("sso","")
            if string:
                self.index_SSO(id ,string)
            if id == 'anisofit' or id == 'pcs' or t=='anisofit' or t  == 'pcs':
                c.title = 'AnisoFit'
                session['PORTAL'] = 'anisofit'
                session.save()
                #c.num = 11
                random.seed()
                if session.get('DIR_CACHE', None) is None:
                    session['DIR_CACHE'] = os.path.join(config['app_conf']['amber_data'], str(random.randint(100000000, 999999999)))
                    session.save()
                elif 'amber_data' not in session.get('DIR_CACHE'):
                    session['DIR_CACHE'] = os.path.join(config['app_conf']['amber_data'], str(random.randint(100000000, 999999999)))
                    session.save()   
                if not os.path.isdir(session.get('DIR_CACHE')):
                    os.makedirs(session.get('DIR_CACHE'))
                else:
                    shutil.rmtree(session.get('DIR_CACHE'))
                    os.makedirs(session.get('DIR_CACHE'))
                # Return a rendered template
                c.dir = session.get('DIR_CACHE')
                return render('/calculations/pcs-rdc_fitting.mako')
            elif id == "maxocc":
                c.title = 'Maxocc'
                #c.num = 13
            elif id == 'xplor-nih':
                c.title = "Xplor-NIH"
            elif id == 'sednmr':
                c.title = "sedNMR"
                return render('/calculations/sedNMR.mako')
            else:
                c.title = 'AMPS-NMR'
                #c.num = 3
            return render('/access/intro.mako')
        else:
            session['PORTAL'] = 'oops!'
            session.save()
            c.title='Oops!'
            return render('/access/wrongportal.mako')
        #else:
        #    session['PORTAL'] = 'AMPS-NMR'
        #    session.save()
        #    c.title = 'AMPS-NMR'
        #    c.num = 3
        #    return render('/access/intro.mako')
           
        #return render('/access/intro.html')

    #def index(self):
    #    return render('/access/intro.html')

    def FGtoken(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(request.headers)
        pp.pprint(request.POST)
        print request.method

        print "-------"
        #uspaswd = "FGportal:e7hhryyturii"
        # encoded base64.b64encode(b"FGportal:e7hhryyturii").ecode("ascii")
        if (request.headers.get("Authorization")):

            print "decode"
            print request.headers.get("Authorization")
            try:
                print base64.decodestring(str(request.headers.get("Authorization").split()[1]))
            except:
                response.status_int = 400
                respo = {"error": "wrong encode"}
                return json.dumps(respo, indent=4, separators=(',', ': '))

            if(str(base64.decodestring(str(request.headers.get("Authorization").split()[1]))) != self.uspaswd):
                response.status_int = 400
                respo = {"error": "wrong pass"}
                return json.dumps(respo, indent=4, separators=(',', ': '))

            print request.headers
            print "POST"
            print request.POST
            print request.GET
            if (len(request.POST) != 0 and (request.POST.get("token") or request.POST.get("subject"))):
                if(request.POST.get("token")):
                    token = str(request.POST.get("token"))
                    url = "https://iam-test.indigo-datacloud.eu/userinfo"
                    quarto = postpy.getpyuserinfo(url, token)
                    if (quarto.get('sub')):
                        subj = str(quarto.get('sub'))
                        respo = {
                            "error": None,
                            "groups": [
                                "Users",
                                "Developers"
                            ],
                            "subject": subj
                        }
                        response.status_int = 200
                    else:
                        response.status_int = 400
                        respo = {"error": "bad call"}


                    print "token"
                elif (request.POST.get("subject")):
                    subject = str(request.POST.get("subject"))
                    print subject

                    #fare query db su iam_subject
                    subquery = Session.query(Users).filter(Users.iam_subject == subject).first()
                    if(subquery):

                        refresh_token = subquery.refresh_token
                        if(len(refresh_token)< 5):
                            print refresh_token
                            print "refresh tokn not present"

                        postpar = {"client_id": self.client_id,
                                   "grant_type": "refresh_token",
                                   "redirect_uri": "https://py-enmr.cerm.unifi.it/access/FGtoken",
                                   "client_secret": self.client_secret,
                                   "refresh_token": refresh_token}
                        url = "https://iam-test.indigo-datacloud.eu/token"
                        #richiesta refresh token
                        quarto = postpy.postpy(postpar,url)

                        pprint.pprint(quarto)
                        if (quarto.get('access_token')):
                            token = quarto.get('access_token')
                            respo = {
                                "error": None,
                                "groups": None,
                                "subject": subject,
                                "token": token
                            }
                            response.status_int = 200
                        else:
                            response.status_int = 400
                            respo = {"error": "bad call"}
                    else:
                        response.status_int = 400
                        respo = {"error": "bad subjetc"}


                    print "subject"
                else:
                    print "pippo"

                    response.status_int = 400
                    respo = {"error": ""}
            else:
                print "pippo"

                response.status_int = 400
                respo = {"error": "no values"}

        response.content_type = 'application/json'

        return json.dumps(respo, indent=4, separators=(',', ': '))


    def loginIAM(self):
        # Funzioannte
        # """Check logname and password to login the user"""
        # stateIAM = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(16))
        # session['STATE_IAM'] = stateIAM
        # session.save()
        # getpar={"client_id":"bfb79b5f-a4ad-4fd0-b182-72f8bfab6f39","response_type":"code+id_token",
        #         "scope":"openid+email+offline_access","redirect_uri":"http://py-enmr.cerm.unifi.it/access/redIAM","state":stateIAM}
        # conn = "https://iam-test.indigo-datacloud.eu/authorize?%s" % urllib.urlencode(getpar)
        # return conn
        """Check logname and password to login the user"""
        stateIAM = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(16))
        session['STATE_IAM'] = stateIAM
        session.save()
        #getpar={"client_id":"bfb79b5f-a4ad-4fd0-b182-72f8bfab6f39","response_type":"code",
        #        "scope":"openid+email+offline_access","redirect_uri":"https://py-enmr.cerm.unifi.it/access/redIAM","state":stateIAM}
        getpar={"client_id":self.client_id,"redirect_uri":"https://py-enmr.cerm.unifi.it/access/redIAM","state":stateIAM}
        #conn = "https://iam-test.indigo-datacloud.eu/authorize?%s" % urllib.urlencode(getpar)
        conn = "https://iam-test.indigo-datacloud.eu/authorize?response_type=code&scope=openid+profile+email+address+phone&%s"% urllib.urlencode(getpar)
        #conn = "https://iam-test.indigo-datacloud.eu/authorize?response_type=code&client_id=bfb79b5f-a4ad-4fd0-b182-72f8bfab6f39&scope=openid+email&%s"% urllib.urlencode(getpar)
        print conn
        return conn 

    def loginIAMaccess(self):
        # Funzioannte
        # """Check logname and password to login the user"""
        # stateIAM = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(16))
        # session['STATE_IAM'] = stateIAM
        # session.save()
        # getpar={"client_id":"bfb79b5f-a4ad-4fd0-b182-72f8bfab6f39","response_type":"code+id_token",
        #         "scope":"openid+email+offline_access","redirect_uri":"http://py-enmr.cerm.unifi.it/access/redIAM","state":stateIAM}
        # conn = "https://iam-test.indigo-datacloud.eu/authorize?%s" % urllib.urlencode(getpar)
        # return conn
        """Check logname and password to login the user"""
        stateIAM = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(16))
        session['STATE_IAM'] = stateIAM
        session.save()
        #getpar={"client_id":"bfb79b5f-a4ad-4fd0-b182-72f8bfab6f39","response_type":"code",
        #        "scope":"openid+email+offline_access","redirect_uri":"https://py-enmr.cerm.unifi.it/access/redIAM","state":stateIAM}
        getpar={"client_id":self.client_id,"redirect_uri":"https://py-enmr.cerm.unifi.it/access/redIAM","state":stateIAM}
        #conn = "https://iam-test.indigo-datacloud.eu/authorize?%s" % urllib.urlencode(getpar)
        conn = "https://iam-test.indigo-datacloud.eu/authorize?response_type=code&scope=openid+profile+email+address+phone+offline_access&%s"% urllib.urlencode(getpar)
        #conn = "https://iam-test.indigo-datacloud.eu/authorize?response_type=code&client_id=bfb79b5f-a4ad-4fd0-b182-72f8bfab6f39&scope=openid+email&%s"% urllib.urlencode(getpar)
        print conn
        return conn


    def redIAM(self):
        refresh_token =''
        access_token = ''
        access_token_expire = ''
        print "SONO in redIAM"
        pp = pprint.PrettyPrinter(indent=4)
        print "----- primi Rislutlati GET/POST -------"
        pp.pprint(request.GET)
        pp.pprint(request.POST)
        if(len(request.POST) == 0 and request.GET.get("state")):
            #esempio di pycurl
            #http://stackoverflow.com/questions/6554386/getting-html-with-pycurl
            print "faccio il POST"
            if (str(request.GET.get("state")) != session['STATE_IAM']):
                print"******* access.redIAM TENATIVO INTRUSIONE ******* " 
                c.title = session['PORTAL'].upper()
                return render('/access/intro.mako')
            
            pcode = request.GET.get("code")
            
            postpar = {"client_id":self.client_id,
                       "grant_type":"authorization_code",
                       "redirect_uri":"https://py-enmr.cerm.unifi.it/access/redIAM",
                       "client_secret":self.client_secret,
                       "code":str(pcode)}
            url = "https://iam-test.indigo-datacloud.eu/token"
            primo = postpy.postpy(postpar,url)
            print "  PRIMO   "
            pprint.pprint(primo)



            # scope richiesto"scope":"address phone openid email profile offline_access"
            if(primo.get('scope')):
                csco= str(primo.get('scope'))

                print "-----CSCO---------"
                print csco
                print "-----CSCO---------"

                if ( ("address" in csco and "email" in csco and "phone" in csco and "openid" in csco and "profile" in csco) and "offline_access" not in csco):
                    print "PRIMO CHECK"
                    if (primo.get('access_token')):
                        access_token = primo.get('access_token')
                    else:
                        print "ACCES TOKEN NON PRESENTE"
                        c.title = session['PORTAL'].upper()
                        return render('/access/intro.mako')

                    url = "https://iam-test.indigo-datacloud.eu/userinfo"

                    quarto = postpy.getpyuserinfo(url, access_token)

                    pprint.pprint(quarto)
                    if (quarto.get('sub')):
                        subj = str(quarto.get('sub'))
                        print "SUBJCT TROVATO"
                    else:
                        print "SUBJCT NON TROVATO"
                        c.title = session['PORTAL'].upper()
                        return render('/access/intro.mako')

                    user = Session.query(Users).filter(Users.iam_subject == subj).first()
                    if not user or len(user.refresh_token) < 5:
                        c.title = session['PORTAL'].upper()
                        return render('/access/introIAM.mako')

                        # User already present in the database
                        save_log("USER ALRADY PRESENT IN DB \n")
                    else:

                        session['REMOTE_USER'] = user.id
                        # user.access_token = access_token
                        # user.refresh_token = refresh_token
                        # user.iam_subject = subj
                        #session['ACCESS_TOKE'] = access_token
                        #session['REFRESH_TOKE'] = user.refresh_token
                        session['REMOTE_USER']
                        Session.add(user)
                        Session.commit()
                        session.save()
                        c.current_user = user
                        if user.removed:
                            return render('/users/user_removed_ssl.html')
                        # Check for the user's myproxy presence
                        # if user.myproxy:
                        ## Instantiate the X509Certificate class
                        # x509 = x509_certificate.X509Certificate()
                        ## Load the myproxy certificate
                        # ret = x509.load(user.myproxy.myproxy)
                        # if ret['OK']:
                        ## Check if it's expired
                        # ret = x509.hasExpired()
                        # if ret['OK']:
                        # c.expired = True
                        # else:
                        ## Get the expiration date
                        # ret = x509.getNotAfterDate()
                        # if ret['OK']:
                        # c.expiration_date = ret['Value']
                        # else:
                        # c.message = ret['Message']
                        # else:
                        ## User hasn't a myproxy certificate
                        # no_proxy = True
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

                    h.flash.set_message('You have successfully logged in.', 'success')
                    h.redirect('/users/index')


                if( not ("address" in csco and "email" in csco and "phone" in csco and "openid" in csco and "profile" in csco and "offline_access" in csco)):
                    print"******* access.redIAM the user doesen't approve all scope in the iam portalitu ******* "
                    h.flash.set_message('Please approve al access', 'error')
                    c.title = session['PORTAL'].upper()
                    return render('/access/intro.mako')
            
            if (primo.get('refresh_token')):
                refresh_token = primo.get('refresh_token')
            if (primo.get('access_token')):
                access_token = primo.get('access_token')
                access_token_expire = primo.get('expires_in')
            if(primo.get('id_token')):
                id_token=primo.get('id_token')  
            print refresh_token,access_token
            print "******************acces_token*******************"
            print access_token


            #https://cloud.digitalocean.com/v1/oauth/token?grant_type=refresh_token&client_id=CLIENT_ID&client_secret=CLIENT_SECRET&refresh_token=REFRESH_TOKEN

            # postpar = {"client_id":self.client_id,
            #            "grant_type":"refresh_token",
            #            "redirect_uri":"https://py-enmr.cerm.unifi.it/access/redIAM",
            #            "client_secret":self.client_secret,
            #            "refresh_token":refresh_token}
            #url = "https://iam-test.indigo-datacloud.eu/token"
            #richiesta refresh token
            #secondo = postpy.postpy(postpar,url)
            url = "https://iam-test.indigo-datacloud.eu/userinfo"

            quarto = postpy.getpyuserinfo(url,access_token)

            pprint.pprint(quarto)

            if (not quarto.get('email')):
                print"******* access.redIAM email not present ******* "
                c.title = session['PORTAL'].upper()
                return render('/access/intro.mako')

            print "-----EMAIL------"
            print str(quarto.get('email'))

            if(len(str(quarto.get('email')).split("@")) != 2 ):
                print"******* access.redIAM email not correct ******* "
                c.title = session['PORTAL'].upper()
                return render('/access/intro.mako')

            subj= str(quarto.get('sub'))

            email = str(quarto.get('email'))
            if(str(quarto.get('family_name'))):
                f = str(quarto.get('family_name'))
            else:
                f = "IAM USER"

            if (str(quarto.get('given_name'))):
                l = str(quarto.get('given_name'))
            else:
                l = "IAM USER"

            user = Session.query(Users).filter(Users.email == email).first()
            # New user
            print "*******ceck user*****"

            pprint.pprint(user)

            if not user:

                role = Session.query(Role).filter(Role.name == 'Member').first()
                save_log("NEW USER NAME " + f + "\n")
                save_log("NEW USER LASTNAME " + l + "\n")
                new_user = Users()
                new_user.firstname = f
                new_user.lastname = l
                new_user.access_token = access_token
                new_user.refresh_token = refresh_token
                new_user.iam_subject = subj
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
                user.access_token = access_token
                user.refresh_token = refresh_token
                user.iam_subject = subj
                session['ACCESS_TOKE'] = access_token
                session['REFRESH_TOKE'] = refresh_token
                session['REMOTE_USER']
                Session.add(user)
                Session.commit()
                session.save()
                c.current_user = user
                if user.removed:
                    return render('/users/user_removed_ssl.html')
                # Check for the user's myproxy presence
                # if user.myproxy:
                ## Instantiate the X509Certificate class
                # x509 = x509_certificate.X509Certificate()
                ## Load the myproxy certificate
                # ret = x509.load(user.myproxy.myproxy)
                # if ret['OK']:
                ## Check if it's expired
                # ret = x509.hasExpired()
                # if ret['OK']:
                # c.expired = True
                # else:
                ## Get the expiration date
                # ret = x509.getNotAfterDate()
                # if ret['OK']:
                # c.expiration_date = ret['Value']
                # else:
                # c.message = ret['Message']
                # else:
                ## User hasn't a myproxy certificate
                # no_proxy = True
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

            h.flash.set_message('You have successfully logged in.', 'success')
            h.redirect('/users/index')

        
        
        c.title = session['PORTAL'].upper()
        return render('/access/intro.mako') 
    
        
    
        
    def login(self):
        """Check logname and password to login the user"""
        logname = request.POST.get('user_name', '')
        password = request.POST.get('user_pwd', '')
        
        if password:
            password = hashlib.sha1(password).hexdigest()
            #c.password = password
        if logname:
            if password:
                
                member = Session.query(Users).filter(and_(Users.logname == logname, Users.removed==False)).first()
                if not member:
                    h.flash.set_message('Could not find your logname in the system.', 'error')
                elif member.password != password:
                    h.flash.set_message('Your password is incorrect.', 'error')
                else:
                    # Check for the user home. If the user was created by the admin
                    # the home field is not in the db. So it's the moment to create it.
                    if not member.home:
                        member.home = '%s%s' % (home_dir_prefix, member.id)
                        Session.add(member)
                        Session.commit()
                    
                    # Session variables binding    
                    session['REMOTE_USER'] = member.id
                    session['LOGNAME'] = member.logname
                    session['HOME'] = os.path.join(config['app_conf']['working_dir'], member.home)
                    session.save()
                    # Home directory creation
                    if not os.path.isdir(session['HOME']):
                        os.makedirs(session['HOME'])
                    
                    h.flash.set_message('You have successfully logged in.', 'success')
                    h.redirect('/users/index')
            else:
                h.flash.set_message('Please type in your password.', 'error')
        c.title = session['PORTAL'].upper()
        return render('/access/intro.mako')

    @check_access('Manage Account')
    def account_create(self):
        """Render the account creation page"""
        user = Session.query(Users).get(session['REMOTE_USER'])
        if user.logname:
            h.flash.set_message(u'You have a login', u'error')
            h.redirect('/users/index')
        return render('/access/account_create.mako')

    @check_access('Manage Account')
    def account_create_db(self):
        """Update current user record with accounting information
        coming from account_crete.mako form"""
        user = Session.query(Users).get(session['REMOTE_USER'])
        user.email = request.POST.get('email')
        user.logname = request.POST.get('logname')
        user.home = '%s%s' % (home_dir_prefix, user.id)
        user.start_date = datetime.now()
        frm = request.POST.get('from')
        if frm == 'creation':
            logname = Session.query(Users).filter(Users.logname == user.logname).all()
            if logname:
                h.flash.set_message('Logname already in use. Please choose another one', 'error')
                return render('/access/account_create.mako')
        user.password = unicode(hashlib.sha1(request.POST.get('password')).hexdigest(), 'utf-8')
        Session.add(user)
        Session.commit()
        h.flash.set_message(u'Account succesfully created/modified.', u'success')
        h.redirect('/users/index')
       
    @check_access('Manage Account')
    def account_create_db_ssl(self):
        """Update current user record with accounting information
        coming from account_crete.mako form"""
        user = Session.query(Users).get(session['REMOTE_USER'])
        user.email = request.POST.get('email')
        user.logname = request.POST.get('logname')
        user.home = '%s%s' % (home_dir_prefix, user.id)
        user.start_date = datetime.now()
        frm = request.POST.get('from')
        if frm == 'creation':
            logname = Session.query(Users).filter(Users.logname == user.logname).all()
            if logname:
                user.logname = user.logname
        user.password = unicode(hashlib.sha1(request.POST.get('password')).hexdigest(), 'utf-8')
        Session.add(user)
        Session.commit()
        return render('/users/user_ssl_created.html')
        
    @check_access('Manage Account') 
    def account_edit(self):
        """Render the account_edit.mako template to permit to the current
        user to edit his account informations"""
        c.user = Session.query(Users).get(session['REMOTE_USER'])
        return render('/access/account_edit.mako')
        
    def autologout(self):
        if 'REMOTE_USER' in session:
            del session['REMOTE_USER']
            session.save()
        if 'PROXY_INITIALIZED' in session:
            del session['PROXY_INITIALIZED']
            session.save()
        return render('/access/autologout.mako')
        
    def newaccount(self):
        if 'PORTAL' in session:
            c.title = session['PORTAL'].upper()
        else:
            c.title = 'AMPS-NMR'
            session['PORTAL'] = 'AMPS-NMR'
            session.save()
        return render('/access/newaccount.mako')
