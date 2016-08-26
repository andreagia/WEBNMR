
import time
import os
import re

from webenmr.lib.return_values import S_OK, S_ERROR
from webenmr.lib.Subprocess import shellCall
from webenmr.lib import List
from webenmr.lib import Locations
from webenmr.lib import FileSec
from webenmr.lib.BaseSecurity import BaseSecurity
from webenmr.lib.X509Chain import X509Chain
from webenmr.lib.X509Chain import g_X509ChainType


class MyProxy( BaseSecurity ):

  def uploadProxy( self, proxy = False, useDNAsUserName = False ):
    """
    Upload a proxy to myproxy service.
      proxy param can be:
        : Default -> use current proxy
        : string -> upload file specified as proxy
        : X509Chain -> use chain
    """
    retVal = FileSec.multiProxyArgument( proxy )
    if not retVal[ 'OK' ]:
      return retVal
    proxyDict = retVal[ 'Value' ]
    chain = proxyDict[ 'chain' ]
    proxyLocation = proxyDict[ 'file' ]

    #timeLeft = int( chain.getRemainingSecs()[ 'Value' ] / 3600 )

    cmdArgs = [ '-n' ]
    cmdArgs.append( '-s "%s"' % self._secServer )
    #cmdArgs.append( '-c "%s"' % ( timeLeft - 1 ) )
    #cmdArgs.append( '-t "%s"' % self._secMaxProxyHours )
    cmdArgs.append( '-C "%s"' % proxyLocation )
    cmdArgs.append( '-y "%s"' % proxyLocation )
    cmdArgs.append( ' -n -R wms-enmr.cerm.unifi.it ')
    #cmdArgs.append( ' -n -R prod-wms-01.pd.infn.it ')
    if useDNAsUserName:
      cmdArgs.append( '-d' )
    else:
      retVal = self._getUsername( chain )
      if not retVal[ 'OK' ]:
        FileSec.deleteMultiProxy( proxyDict )
        return retVal
      mpUsername = retVal[ 'Value' ]
      cmdArgs.append( '-l "%s"' % mpUsername )

    mpEnv = self._getExternalCmdEnvironment()
    #Hack to upload properly
    mpEnv[ 'GT_PROXY_MODE' ] = 'old'
  
    os.environ['PATH'] = '/opt/globus/bin/'
    cmd = "/opt/globus/bin/myproxy-init %s" % " ".join( cmdArgs )
    result = shellCall( self._secCmdTimeout, cmd, env = mpEnv )

    FileSec.deleteMultiProxy( proxyDict )

    if not result['OK']:
      errMsg = "Call to myproxy-init failed: %s" % retVal[ 'Message' ]
      return S_ERROR( errMsg )

    status, output, error = result['Value']

    # Clean-up files
    if status:
      errMsg = "Call to myproxy-init failed"
      extErrMsg = 'Command: %s; StdOut: %s; StdErr: %s' % ( cmd, result, error )
      return S_ERROR( "%s %s" % ( errMsg, extErrMsg ) )

    return S_OK( output )

  def getDelegatedProxy( self, proxyChain, lifeTime = 604800, useDNAsUserName = False ):
    """
      Get delegated proxy from MyProxy server
      return S_OK( X509Chain ) / S_ERROR
    """
    #TODO: Set the proxy coming in proxyString to be the proxy to use

    #Get myproxy username diracgroup:diracuser
    retVal = FileSec.multiProxyArgument( proxyChain )
    if not retVal[ 'OK' ]:
      return retVal
    proxyDict = retVal[ 'Value' ]
    chain = proxyDict[ 'chain' ]
    proxyLocation = proxyDict[ 'file' ]

    retVal = self._generateTemporalFile()
    if not retVal[ 'OK' ]:
      FileSec.deleteMultiProxy( proxyDict )
      return retVal
    newProxyLocation = retVal[ 'Value' ]

    # myproxy-get-delegation works only with environment variables
    cmdEnv = self._getExternalCmdEnvironment()
    if self._secRunningFromTrustedHost:
      cmdEnv['X509_USER_CERT'] = self._secCertLoc
      cmdEnv['X509_USER_KEY'] = self._secKeyLoc
      if 'X509_USER_PROXY' in cmdEnv:
        del cmdEnv['X509_USER_PROXY']
    else:
      cmdEnv['X509_USER_PROXY'] = proxyLocation

    cmdArgs = []
    cmdArgs.append( "-s '%s'" % self._secServer )
    cmdArgs.append( "-t '%s'" % ( int( lifeTime / 3600 ) ) )
    cmdArgs.append( "-a '%s'" % proxyLocation )
    cmdArgs.append( "-o '%s'" % newProxyLocation )
    if useDNAsUserName:
      cmdArgs.append( '-d' )
    else:
      retVal = self._getUsername( chain )
      if not retVal[ 'OK' ]:
        FileSec.deleteMultiProxy( proxyDict )
        return retVal
      mpUsername = retVal[ 'Value' ]
      cmdArgs.append( '-l "%s"' % mpUsername )

    cmd = "myproxy-logon %s" % " ".join( cmdArgs )
    gLogger.verbose( "myproxy-logon command:\n%s" % cmd )

    result = shellCall( self._secCmdTimeout, cmd, env = cmdEnv )

    FileSec.deleteMultiProxy( proxyDict )

    if not result['OK']:
      errMsg = "Call to myproxy-logon failed: %s" % result[ 'Message' ]
      FileSec.deleteMultiProxy( proxyDict )
      return S_ERROR( errMsg )

    status, output, error = result['Value']

    # Clean-up files
    if status:
      errMsg = "Call to myproxy-logon failed"
      extErrMsg = 'Command: %s; StdOut: %s; StdErr: %s' % ( cmd, result, error )
      FileSec.deleteMultiProxy( proxyDict )
      return S_ERROR( "%s %s" % ( errMsg, extErrMsg ) )

    chain = X509Chain()
    retVal = chain.loadProxyFromFile( newProxyLocation )
    if not retVal[ 'OK' ]:
      FileSec.deleteMultiProxy( proxyDict )
      return S_ERROR( "myproxy-logon failed when reading delegated file: %s" % retVal[ 'Message' ] )

    FileSec.deleteMultiProxy( proxyDict )
    return S_OK( chain )

  def getInfo( self, proxyChain, useDNAsUserName = False ):
    """
      Get info from myproxy server
      return S_OK( { 'username' : myproxyusername,
                     'owner' : owner DN,
                     'timeLeft' : secs left } ) / S_ERROR
    """
    #TODO: Set the proxy coming in proxyString to be the proxy to use

    #Get myproxy username diracgroup:diracuser
    retVal = FileSec.multiProxyArgument( proxyChain )
    if not retVal[ 'OK' ]:
      return retVal
    proxyDict = retVal[ 'Value' ]
    chain = proxyDict[ 'chain' ]
    proxyLocation = proxyDict[ 'file' ]

    # myproxy-get-delegation works only with environment variables
    cmdEnv = self._getExternalCmdEnvironment()
    if self._secRunningFromTrustedHost:
      cmdEnv['X509_USER_CERT'] = self._secCertLoc
      cmdEnv['X509_USER_KEY'] = self._secKeyLoc
      if 'X509_USER_PROXY' in cmdEnv:
        del cmdEnv['X509_USER_PROXY']
    else:
      cmdEnv['X509_USER_PROXY'] = proxyLocation

    cmdArgs = []
    cmdArgs.append( "-s '%s'" % self._secServer )
    if useDNAsUserName:
      cmdArgs.append( '-d' )
    else:
      retVal = self._getUsername( chain )
      if not retVal[ 'OK' ]:
        FileSec.deleteMultiProxy( proxyDict )
        return retVal
      mpUsername = retVal[ 'Value' ]
      cmdArgs.append( '-l "%s"' % mpUsername )

    cmd = "myproxy-info %s" % " ".join( cmdArgs )
    gLogger.verbose( "myproxy-info command:\n%s" % cmd )

    result = shellCall( self._secCmdTimeout, cmd, env = cmdEnv )

    FileSec.deleteMultiProxy( proxyDict )

    if not result['OK']:
      errMsg = "Call to myproxy-info failed: %s" % result[ 'Message' ]
      FileSec.deleteMultiProxy( proxyDict )
      return S_ERROR( errMsg )

    status, output, error = result['Value']

    # Clean-up files
    if status:
      errMsg = "Call to myproxy-info failed"
      extErrMsg = 'Command: %s; StdOut: %s; StdErr: %s' % ( cmd, result, error )
      return S_ERROR( "%s %s" % ( errMsg, extErrMsg ) )

    infoDict = {}
    usernameRE = re.compile( "username\s*:\s*(\S*)" )
    ownerRE = re.compile( "owner\s*:\s*(\S*)" )
    timeLeftRE = re.compile( "timeleft\s*:\s*(\S*)" )
    for line in List.fromChar( output, "\n" ):
      match = usernameRE.search( line )
      if match:
        infoDict[ 'username' ] = match.group( 1 )
      match = ownerRE.search( line )
      if match:
        infoDict[ 'owner' ] = match.group( 1 )
      match = timeLeftRE.search( line )
      if match:
        try:
          fields = List.fromChar( match.group( 1 ), ":" )
          fields.reverse()
          secsLeft = 0
          for iP in range( len( fields ) ):
            if iP == 0:
              secsLeft += int( fields[ iP ] )
            elif iP == 1:
              secsLeft += int( fields[ iP ] ) * 60
            elif iP == 2:
              secsLeft += int( fields[ iP ] ) * 3600
          infoDict[ 'timeLeft' ] = secsLeft
        except Exception, x:
          print x

    return S_OK( infoDict )