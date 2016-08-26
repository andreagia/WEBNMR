import os, sys
import site
site.addsitedir('/home/webenmr/pyvirt/lib/python2.4/site-packages')

sys.path.append('/home/webenmr/WebENMR')
os.environ['PYTHON_EGG_CACHE'] = '/home/webenmr/WebENMR/python-eggs'

from paste.deploy import loadapp
application = loadapp('config:/home/webenmr/WebENMR/development.ini')

