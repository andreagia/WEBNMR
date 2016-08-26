
import types
import os
import tempfile
from webenmr.lib.X509Chain import X509Chain, g_X509ChainType
from webenmr.lib import Locations, File
from webenmr.lib.return_values import S_OK, S_ERROR

class BaseSecurity:

  def __init__( self,
                server = False,
                serverCert = False,
                serverKey = False,
                voName = False,
                timeout = False ):
    if timeout:
      self._secCmdTimeout = timeout
    else:
      self._secCmdTimeout = 960
    if not server:
      self._secServer = "myproxy.cnaf.infn.it"
    else:
      self._secServer = server
    if not voName:
      self._secVO = 'eunmr.eu'
    else:
      self._secVO = voName
    ckLoc = Locations.getHostCertificateAndKeyLocation()
    if serverCert:
      self._secCertLoc = serverCert
    else:
      if ckLoc:
        self._secCertLoc = ckLoc[0]
      else:
        self._secCertLoc = "/etc/httpd/conf/ssl.crt/py-enmr.cerm.unifi.it.crt"
    if serverKey:
      self._secKeyLoc = serverKey
    else:
      if ckLoc:
        self._secKeyLoc = ckLoc[1]
      else:
        self._secKeyLoc = "/etc/httpd/conf/ssl.key/py-enmr.cerm.unifi.it.key"
    self._secRunningFromTrustedHost = "True"
    self._secMaxProxyHours = 168 

  def getMyProxyServer( self ):
    return self._secServer

  def getServiceDN( self ):
    chain = X509Chain()
    retVal = chain.loadChainFromFile( self._secCertLoc )
    if not retVal[ 'OK' ]:
      return retVal
    return chain.getCertInChain(0)['Value'].getSubjectDN()

  def _getExternalCmdEnvironment( self ):
    return dict( os.environ )

  def _unlinkFiles( self, files ):
    if type( files ) in ( types.ListType, types.TupleType ):
      for file in files:
        self._unlinkFiles( file )
    else:
      try:
        os.unlink( files )
      except:
        pass

  def _generateTemporalFile(self):
    try:
      fd, filename = tempfile.mkstemp()
      os.close(fd)
    except IOError:
      return S_ERROR('Failed to create temporary file')
    return S_OK( filename )

  def _getUsername( self, proxyChain ):
    retVal = proxyChain.getCredentials()
    if not retVal[ 'OK' ]:
      return retVal
    credDict = retVal[ 'Value' ]
    if not credDict[ 'isProxy' ]:
      return S_ERROR( "chain does not contain a proxy" )
    if not credDict[ 'validDN' ]:
      return S_ERROR( "DN %s is not known in dirac" % credDict[ 'subject' ] )
    if not credDict[ 'validGroup' ]:
      return S_ERROR( "Group %s is invalid for DN %s" % ( credDict[ 'group' ], credDict[ 'subject' ] ) )
    mpUsername = "%s:%s" % ( credDict[ 'group' ], credDict[ 'username' ] )
    return S_OK( mpUsername )
