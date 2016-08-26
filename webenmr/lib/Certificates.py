import os
from datetime import datetime
from pylons import config, session
from webenmr.lib import x509_certificate
from webenmr.lib import robot_certificate
from webenmr.lib import return_values
from webenmr.lib.VOMS import VOMS
from webenmr.lib.MyProxy import MyProxy
from webenmr.lib.X509Chain import g_X509ChainType, X509Chain
from webenmr.lib.base import sendmail
    
class Certificates:
    '''Class to manage certificates'''

    def __init__(self, cert):
        self.cert = os.path.join(config['app_conf']['cert_dir'], cert)
        os.environ['X509_USER_PROXY'] = self.cert
        
    def load_robot_certificate(self):
        r = robot_certificate.Robot()
        ret = r.load(self.cert)
        exp = r.getNotAfterDate()       
        return ret, exp

    def load_certificate(self):
        c = x509_certificate.X509Certificate()
        ret = c.load(self.cert)
        return ret

    def voms_proxy_init(self, attribute):
        voms = VOMS()       
        ret = voms.setVOMSAttributes(self.cert, attribute)
        if ret['OK']:
            ret = ret['Value'].dumpAllToString()
        return ret
    
    def myproxy_init(self):
        myproxy = MyProxy()
        ret = myproxy.uploadProxy(self.cert, True)
        return ret
    
def proxy_initialize(attribute = ""):
	'''Initialize the proxy-certificate and myproxy.
	Check the validity of the robot certificate'''
	# Set ROBOT Certificate
	crt = Certificates('x509up_u1')
	ret, exp = crt.load_robot_certificate()
	print ret
	if ret['OK']:
		if exp['OK']:
			# Check expiration days
			expiration = (exp['Value'] - datetime.now()).days
			print expiration
			if expiration <= 7:
				send_expiration_warning(expiration)
		ret = crt.voms_proxy_init(attribute)
		print ret
		if ret['OK']:
			session['voms_proxy'] = ret['Value']
			session.save()
			cert_file = os.path.join(session['HOME'], '.voms_cert')
			f = open(cert_file, 'w')
			f.write(session['voms_proxy'])
			f.close()
			os.chmod(cert_file, 0660)
			session['voms_proxy_file'] = cert_file
			session.save()
			if 'PROXY_INITIALIZED' not in session:
				ret = crt.myproxy_init()
				if ret['OK']:
					session['PROXY_INITIALIZED'] = True
					session.save()
		else:
			return ret
	return ret
		
def send_expiration_warning(days):
		from_ = 'web-enmr@cerm.unifi.it'
		to_ = 'web-enmr@cerm.unifi.it'
		cc = ''
		subject = 'py-enmr: Certificate Robot expiration'
		body = '''The robot certificate used on py-enmr will expire in %d days''' % days
		ret = sendmail(to_, cc, subject, from_, body)
