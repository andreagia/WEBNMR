# $HeadURL$
__RCSID__ = "$Id$"

# Encoding and decoding for dirac
#
# Ids
# i -> int
# I -> long
# f -> float
# b -> bool
# s -> string
# z -> datetime
# n -> none
# l -> list
# t -> tuple
# d -> dictionary


import sys
import types
import struct
import datetime

_dateTimeObject = datetime.datetime.utcnow()
_dateTimeType = type( _dateTimeObject )
_dateType     = type( _dateTimeObject.date() )
_timeType     = type( _dateTimeObject.time() )

g_dEncodeFunctions = {}
g_dDecodeFunctions = {}

#Encoding and decoding ints
def encodeInt( iValue, eList ):
  eList.extend( ( "i", str( iValue ), "e" ) )

def decodeInt( buffer, i ):
  i += 1
  end  = buffer.index( 'e', i )
  n = int( buffer[i:end] )
  return ( n, end + 1 )

g_dEncodeFunctions[ types.IntType ] = encodeInt
g_dDecodeFunctions[ "i" ] = decodeInt

#Encoding and decoding longs
def encodeLong( iValue, eList ):
  # corrected by KGG   eList.extend( ( "l", str( iValue ), "e" ) )
  eList.extend( ( "I", str( iValue ), "e" ) )

def decodeLong( buffer, i ):
  i += 1
  end  = buffer.index( 'e', i )
  n = long( buffer[i:end] )
  return ( n, end + 1 )

g_dEncodeFunctions[ types.LongType ] = encodeLong
g_dDecodeFunctions[ "I" ] = decodeLong

#Encoding and decoding floats
def encodeFloat( iValue, eList ):
  eList.extend( ( "f", str( iValue ), "e" ) )

def decodeFloat( buffer, i ):
  i += 1
  end  = buffer.index( 'e', i )
  if end+1 < len( buffer ) and buffer[end+1] in ( '+', '-' ):
    eI = end
    end = buffer.index( 'e', end+1 )
    n = float( buffer[i:eI] ) * 10 ** int( buffer[eI+1:end] )
  else:
    n = float( buffer[i:end] )
  return ( n, end + 1 )

g_dEncodeFunctions[ types.FloatType ] = encodeFloat
g_dDecodeFunctions[ "f" ] = decodeFloat

#Encoding and decoding booleand
def encodeBool( bValue, eList ):
  if bValue:
    eList.append( "b1" )
  else:
    eList.append( "b0" )

def decodeBool( buffer, i ):
  if buffer[ i + 1 ] == "0":
    return ( False, i + 2 )
  else:
    return ( True, i + 2 )

g_dEncodeFunctions[ types.BooleanType ] = encodeBool
g_dDecodeFunctions[ "b" ] = decodeBool

#Encoding and decoding strings
def encodeString( sValue, eList ):
  eList.extend( ( 's', str( len( sValue ) ), ':', sValue ) )

def decodeString( buffer, i ):
  i += 1
  colon = buffer.index( ":", i )
  n = int( buffer[ i : colon ] )
  colon += 1
  end = colon + n
  return ( buffer[ colon : end] , end )

g_dEncodeFunctions[ types.StringType ] = encodeString
g_dDecodeFunctions[ "s" ] = decodeString

#Encoding and decoding unicode strings
def encodeUnicode( sValue, eList ):
  valueStr = sValue.encode( 'utf-8' )
  eList.extend( ( 'u', str( len( valueStr ) ), ':', valueStr ) )

def decodeUnicode( buffer, i ):
  i += 1
  colon = buffer.index( ":", i )
  n = int( buffer[ i : colon ] )
  colon += 1
  end = colon + n
  return ( unicode( buffer[ colon : end], 'utf-8' ) , end )

g_dEncodeFunctions[ types.UnicodeType ] = encodeUnicode
g_dDecodeFunctions[ "u" ] = decodeUnicode

#Encoding and decoding datetime
def encodeDateTime( oValue, eList ):
  prefix = "z"
  if type( oValue ) == _dateTimeType:
    tDateTime = ( oValue.year, oValue.month, oValue.day, \
                      oValue.hour, oValue.minute, oValue.second, \
                      oValue.microsecond, oValue.tzinfo )
    eList.append( "za" )
    # corrected by KGG encode( tDateTime, eList )
    g_dEncodeFunctions[ type( tDateTime) ]( tDateTime, eList )
  elif type( oValue ) == _dateType:
    tData = ( oValue.year, oValue.month, oValue. day )
    eList.append( "zd" )
    # corrected by KGG encode( tData, eList )
    g_dEncodeFunctions[ type( tData) ]( tData, eList )
  elif type( oValue ) == _timeType:
    tTime = ( oValue.hour, oValue.minute, oValue.second, oValue.microsecond, oValue.tzinfo )
    eList.append( "zt" )
    # corrected by KGG encode( tTime, eList )
    g_dEncodeFunctions[ type( tTime) ]( tTime, eList )
  else:
    raise Exception( "Unexpected type %s while encoding a datetime object" % str( type( oValue ) ) )

def decodeDateTime( buffer, i ):
  i += 1
  type = buffer[i]
  # corrected by KGG tupleObject, i = decode( buffer, i + 1 )
  tupleObject, i = g_dDecodeFunctions[ buffer[ i+1 ] ]( buffer, i+1 )
  if type == 'a':
    dtObject = datetime.datetime( *tupleObject )
  elif type == 'd':
    dtObject = datetime.date( *tupleObject )
  elif type == 't':
    dtObject = datetime.time( *tupleObject )
  else:
    raise Exception( "Unexpected type %s while decoding a datetime object" % type )
  return ( dtObject, i )

g_dEncodeFunctions[ _dateTimeType ] = encodeDateTime
g_dEncodeFunctions[ _dateType ] = encodeDateTime
g_dEncodeFunctions[ _timeType ] = encodeDateTime
g_dDecodeFunctions[ 'z' ] = decodeDateTime

#Encoding and decoding None
def encodeNone( oValue, eList ):
  eList.append( "n" )

def decodeNone( buffer, i ):
  return ( None, i + 1 )

g_dEncodeFunctions[ types.NoneType ] = encodeNone
g_dDecodeFunctions[ 'n' ] = decodeNone

#Encode and decode a list
def encodeList( lValue, eList ):
  eList.append( "l" )
  for uObject in lValue:
    g_dEncodeFunctions[ type( uObject ) ]( uObject, eList )
  eList.append( "e" )

def decodeList( buffer, i ):
  oL = []
  i += 1
  while buffer[ i ] != "e":
    ob, i = g_dDecodeFunctions[ buffer[ i ] ]( buffer, i )
    oL.append( ob )
  return( oL, i + 1 )

g_dEncodeFunctions[ types.ListType ] = encodeList
g_dDecodeFunctions[ "l" ] = decodeList

#Encode and decode a tuple
def encodeTuple( lValue, eList ):
  eList.append( "t" )
  for uObject in lValue:
    g_dEncodeFunctions[ type( uObject ) ]( uObject, eList )
  eList.append( "e" )

def decodeTuple( buffer, i ):
  oL, i = decodeList( buffer, i )
  return ( tuple( oL ), i )

g_dEncodeFunctions[ types.TupleType ] = encodeTuple
g_dDecodeFunctions[ "t" ] = decodeTuple

#Encode and decode a dictionary
def encodeDict( dValue, eList ):
  eList.append( "d" )
  for key in sorted( dValue ):
    g_dEncodeFunctions[ type( key ) ]( key, eList )
    g_dEncodeFunctions[ type( dValue[key] ) ]( dValue[key], eList )
  eList.append( "e" )

def decodeDict( buffer, i ):
  oD = {}
  i += 1
  while buffer[ i ] != "e":
    k, i = g_dDecodeFunctions[ buffer[ i ] ]( buffer, i )
    oD[ k ], i = g_dDecodeFunctions[ buffer[ i ] ]( buffer, i )
  return ( oD, i + 1 )

g_dEncodeFunctions[ types.DictType ] = encodeDict
g_dDecodeFunctions[ "d" ] = decodeDict


#Encode function
def encode( uObject ):
  try:
    eList = []
    #print "ENCODE FUNCTION : %s" % g_dEncodeFunctions[ type( uObject ) ]
    g_dEncodeFunctions[ type( uObject ) ]( uObject, eList )
    return "".join( eList )
  except Exception, e:
    raise

def decode( buffer ):
  if not buffer:
    return buffer
  try:
    #print "DECODE FUNCTION : %s" % g_dDecodeFunctions[ sStream [ iIndex ] ]
    return g_dDecodeFunctions[ buffer[ 0 ] ]( buffer, 0 )
  except Exception, e:
    raise


if __name__=="__main__":
  uObject = {2:"3", True : (3,None), 2.0*10**20 : 2.0*10**-10 }
  print "Initial: %s" % uObject
  sData = encode( uObject )
  print "Encoded: %s" % sData
  print "Decoded: %s, [%s]" % decode( sData )


