#!/usr/bin/env python
"""
Author:     Enrico Morelli <morelli@cerm.unifi.it>
Program:    xml_parser.py
Date:       Feb 6, 2009

Description:  parse an xml file and create a dictionary accessible using dot-notation

"""
from lxml import etree
import re

class dict_accessor(dict):
    """
    Allow accessing a dictionary content also using dot-notation.
    """
    def __getattr__(self, attr):
	try:
	    return super(dict_accessor, self).__getitem__(attr)
	except:
	    return None

    def __setattr__(self, attr, value):
        super(dict_accessor, self).__setitem__(attr, value)

c = re.compile(r'([A-Z]+[a-z_]+)')

def purify(s):
    """
    s is an etree.tag and contains also information on the namespace,
    if that information is present try to remove it, then convert the
    camelCaseTags to underscore_notation_more_python_friendly.
    """
    PREFIX=''
    if s.startswith(PREFIX):
        s = s[len(PREFIX):]
    return '_'.join(atom.lower() for atom in c.split(s) if atom) 

def parse_node(node):
    """
    Return a dict_accessor representation of the node.
    """
    new = dict_accessor({})
    if node.text and node.text.strip():
        t = node.text
        if isinstance(t, unicode):
            new['text_'] = t
        else:
            new['text_'] = t.decode('utf-8')
    if node.attrib:
        new['attrib_'] = dict_accessor(node.attrib)

    for child in node.getchildren():
        tag = purify(child.tag)
	#tag=child.tag
        child = parse_node(child)

        if tag not in new:
            new[tag] = child
        else:
            old = new[tag]
            if not isinstance(old, list):
                new[tag] = [old]
            new[tag].append(child)
    return new 

if __name__ == '__main__':
    doc = etree.parse('input.xml')
    ndoc = etree.tostring(doc)
    new=parse_node(etree.fromstring(ndoc))
    print new
    print len(new.calculation)
    print new.calculation.protocol.info.attrib_.init_t
    print new.calculation.protocol.structure.struct_file[0].text_
    print new.calculation.protocol.structure.struct_file[1].text_
    #for  elt in doc.getiterator():
    #	new=parse_node(elt)
    #	print new.init_t
