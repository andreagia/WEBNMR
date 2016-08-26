
import os
fileDict = {}

def getProxyLocation():
  """ Get the path of the currently active grid proxy file
  """
  for envVar in [ 'GRID_PROXY_FILE', 'X509_USER_PROXY' ]:
    if os.environ.has_key( envVar ):
      proxyPath = os.path.realpath( os.environ[ envVar ] )
      if os.path.isfile( proxyPath ):
        return proxyPath
  #/tmp/x509up_u<uid>
  proxyName = "x509up_u%d" % os.getuid()
  if os.path.isfile( "/tmp/%s" % proxyName ):
    return "/tmp/%s" % proxyName

  #No gridproxy found
  return False

#Retrieve CA's location
def getCAsLocation():
  """ Retrieve the CA's files location
  """
  # Look up the X509_CERT_DIR environment variable
  if os.environ.has_key( 'X509_CERT_DIR' ):
    casPath = os.environ[ 'X509_CERT_DIR' ]
    return casPath

  #/etc/grid-security/certificates
  casPath = "/etc/grid-security/certificates"
  if os.path.isdir( casPath ):
    return casPath
  #No CA's location found
  return False

#Retrieve certificate
def getHostCertificateAndKeyLocation():
  """ Retrieve the host certificate files location
  """
  
  fileDict["cert"] = "/etc/httpd/conf/ssl.crt/py-enmr.cerm.unifi.it.crt"
  fileDict["key"] = "/etc/httpd/conf/ssl.key/py-enmr.cerm.unifi.it.key"
  return (fileDict["cert"], fileDict["key"])

def getCertificateAndKeyLocation():
  """ Get the locations of the user X509 certificate and key pem files
  """

  certfile = ''
  if os.environ.has_key("X509_USER_CERT"):
    if os.path.exists(os.environ["X509_USER_CERT"]):
      certfile = os.environ["X509_USER_CERT"]
  if not certfile:
    if os.path.exists(os.environ["HOME"]+'/.globus/usercert.pem'):
      certfile = os.environ["HOME"]+'/.globus/usercert.pem'

  if not certfile:
    return False

  keyfile = ''
  if os.environ.has_key("X509_USER_KEY"):
    if os.path.exists(os.environ["X509_USER_KEY"]):
      keyfile = os.environ["X509_USER_KEY"]
  if not keyfile:
    if os.path.exists(os.environ["HOME"]+'/.globus/userkey.pem'):
      keyfile = os.environ["HOME"]+'/.globus/userkey.pem'

  if not keyfile:
    return False

  return (certfile,keyfile)

def getDefaultProxyLocation():
  """ Get the location of a possible new grid proxy file
  """

  for envVar in [ 'GRID_PROXY_FILE', 'X509_USER_PROXY' ]:
    if os.environ.has_key( envVar ):
      proxyPath = os.path.realpath( os.environ[ envVar ] )
      return proxyPath

  #/tmp/x509up_u<uid>
  proxyName = "x509up_u%d" % os.getuid()
  return "/tmp/%s" % proxyName