#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Whois Parsers
    ~~~~~~~~~~~~~

    Initialize the Whois parsers.

    It is not really used because the whole whois entry is put in the database.
"""

from abstract_parser import AbstractParser

RIS = {
    'route':       'route[6]?:[ ]*([^\n]*)',
    'origin':      'origin:[ ]*AS([^\n]*)',
    'description': 'descr:[ ]*([^\n]*)'
}

RIPE = {
    'inetnum':  'inetnum:[ ]*([^\n]*)',
    'netname':  'netname:[ ]*([^\n]*)',
    'descr':    'descr:[ ]*([^\n]*)',
    'country':  'country:[ ]*([^\n]*)'
}

Afrinic = {
    'netname':  'netname:[ ]*([^\n]*)'
}

class Whois(AbstractParser):
    """
    This class return a dump of the Whois.
    Until we have a real implementation of whois in python,
    we will use this class to return all the informations
    """
    possible_regex = {
        'riswhois.ripe.net' : RIS,
        'whois.ripe.net'    : RIPE,
        'whois.afrinic.net' : Afrinic
        }

