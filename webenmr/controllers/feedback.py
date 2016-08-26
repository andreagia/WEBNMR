import logging

import urllib2, urllib

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from webenmr.lib.base import BaseController, render
from webenmr.lib.base import *
import os
from webenmr.lib import helpers as h
# Import smtplib for the actual sending function
#import smtplib
## Import the email modules we'll need
#from email.mime.text import MIMEText

log = logging.getLogger(__name__)

class FeedbackController(BaseController):
    
    def __before__(self):
        """
        This __before__ method calls the parent method, and then sets up the
        tabs on the page.
        """
        #BaseController.__before__(self)
        
        c.page_base = u'Contact'
        if 'REMOTE_USER' in session:
            c.current_user = Session.query(Users).get(session['REMOTE_USER'])
            c.main_menu = Session.query(Menu).filter(and_(Menu.parent_id==None, Menu.sibling_id==None)).order_by(Menu.weight.asc()).all()
        c.page_title = u'Feedback'
    
    def index(self):
        # Return a rendered template
        #return render('/feedback.mako')
        # or, return a response
        if 'type' in request.params:
            t = request.GET.get('type')
            if t == 'anisofit':
                c.title="AnisoFIT"
                c.subtitle=""
                c.breadcrump = "anisofit"
            else:
                c.title="AMBER"
                c.subtitle="(including paramagnetic restraints plugin)"
                c.breadcrump = "amber"
        else:
            c.title='Feedback'
            c.subtitle=''
            c.breadcrump="feedback"

        return render('/contact/feedback2.mako')

    def sendMail(self):
        #check captcha
        recaptcha_challenge_field = request.POST.get('recaptcha_challenge_field') 
        recaptcha_response_field = request.POST.get('recaptcha_response_field')
        private_key = '6Leg-LwSAAAAAOm95rcbsmX7Ekhc-ehmY9bRW2-R'
        remoteip = request.environ['REMOTE_ADDR']
        retCaptcha = self.checkCaptcha (recaptcha_challenge_field,
            recaptcha_response_field,
            private_key,
            remoteip)
        isValid = retCaptcha.split("__")[0]
        if isValid == "True":
            #collect session variable and send mail to web-enmr@cerm.unifi.it
            first = request.POST.get('firstname')
            last = request.POST.get('lastname')
            univ = request.POST.get('university')
            dep = request.POST.get('department')
            
            #if 'address' in request.params:
            #    address = request.POST.get('address')
            #if 'postalcode' in request.params:
            #    postal = request.POST.get('postalcode')
            #if 'city' in request.params:
            #    city = request.POST.get('city')
            #if 'country' in request.params:
            #    country = request.POST.get('country')
            if 'type' in request.params:
                portal = request.GET.get('get')
            else:
                portal = 'Amber'
            email = request.POST.get('email')
            comments = request.POST.get('comments')
            scope = request.POST.get('subject')
            subject = '%s - %s Web portal' % (scope, portal)
            body = "University or Organization: %s\n Department: %s\n email: %s\n\n %s %s says: %s\n" %(univ, dep, email, first, last, comments)
            ret = sendmail('web-enmr@cerm.unifi.it', "", subject, email, body)
            
            if ret:
                msg = 'Your message was successfully delivered.'
                h.flash.set_message(msg, 'success')
                h.redirect('/users/index')
            else:
                msg = 'Mail System has encountered an error.If you still wish to proceed, please try again later.'
                h.flash.set_message(msg, 'error')
                return h.redirect('/feedback/index')
                
        else:
            return retCaptcha
    
    def checkCaptcha (self, recaptcha_challenge_field,
            recaptcha_response_field,
            private_key,
            remoteip):
        """
        Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
        for the request
    
        recaptcha_challenge_field -- The value of recaptcha_challenge_field from the form
        recaptcha_response_field -- The value of recaptcha_response_field from the form
        private_key -- your reCAPTCHA private key
        remoteip -- the user's ip address
        """
        
        if not (recaptcha_response_field and recaptcha_challenge_field and
                len (recaptcha_response_field) and len (recaptcha_challenge_field)):
            return "False__incorrect-captcha-sol"

        params = urllib.urlencode ({
                'privatekey': self.encode_if_necessary(private_key),
                'remoteip' :  self.encode_if_necessary(remoteip),
                'challenge':  self.encode_if_necessary(recaptcha_challenge_field),
                'response' :  self.encode_if_necessary(recaptcha_response_field),
                })
    
        request = urllib2.Request (
            url = "http://www.google.com/recaptcha/api/verify",
            data = params,
            headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "User-agent": "reCAPTCHA Python"
                }
            )
        
        httpresp = urllib2.urlopen (request)
    
        return_values = httpresp.read ().splitlines ();
        httpresp.close();
    
        return_code = return_values [0]
    
        if (return_code == "true"):
            return "True"
        else:
            return "False__%s" %return_values[1]

    def encode_if_necessary(self, s):
            if isinstance(s, unicode):
                return s.encode('utf-8')
            return s