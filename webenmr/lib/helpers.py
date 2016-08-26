"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from pylons import url
from webhelpers.html import escape, HTML, literal, url_escape
from webhelpers.html.tags import *
from webhelpers.date import *
from webhelpers.text import *
from webhelpers.html.converters import *
from webhelpers.html.tools import *
from webhelpers.util import *
from pylons.controllers.util import redirect
from routes import url_for

_suffixes = {0: u'B', 1: u'KB', 2: u'MB', 3: u'GB', 4: u'TB', 5: u'PB'}

class Flash(object):
    def set_message(self, message_text, message_type):
        session = self._get_session()
        session[u'flash.text'] = message_text
        session[u'flash.type'] = message_type
        session.save()

    def has_message(self):
        session = self._get_session()
        return u'flash.text' in session

    def get_message_text(self):
        session = self._get_session()
        message_text = session.pop(u'flash.text', None)
        if not message_text:
            return None
        session.save()
        return message_text

    def get_message_type(self):
        session = self._get_session()
        message_type = session.pop(u'flash.type', None)
        if not message_type:
            return None
        session.save()
        return message_type

    def _get_session(self):
        from pylons import session
        return session

def html_entities(raw_string):
    return escape(raw_string)

def shorten(description):
    if len(description) > 70:
        shortened = description[:67] + u'...'
    else:
        shortened = description
    return shortened


def pretty_size(original_size):
    original_size = float(original_size)
    multiplier = 0
    while original_size > 1024:
        multiplier = multiplier + 1
        original_size = original_size / 1024
    return u'%d%s' % (round(original_size, 1), _suffixes[multiplier])

def file_decode(file_data):
    string_data = StringIO(file_data)
    details = chardet.detect(string_data.getvalue())
    return unicode(string_data.getvalue(), details['encoding'])

def image_to(src, alt, url_=None, width=None, height=None, **attrs):
    src = url(src)
    if url_:
        url_ = url(url_)
    else:
        url_ = src
    return link_to(image(src, alt, width, height, **attrs), url_)

flash = Flash()
