#!/usr/bin/python
import os 
import sys
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read("../../etc/bgp-ranking.conf")
root_dir = config.get('directories','root')
sleep_timer = int(config.get('sleep_timers','long'))
sleep_timer_short = int(config.get('sleep_timers','short'))
sys.path.append(os.path.join(root_dir,config.get('directories','libraries')))
bgpdump = config.get('routing','bgpdump')
import syslog
syslog.openlog('Push_BGP_Routing', syslog.LOG_PID, syslog.LOG_USER)

import time
import redis
import subprocess


from whois_parser.bgp_parsers import *

"""
Push the BGP Updates
"""

def usage():
    print "push_update_routing.py filename"
    exit (1)

key = config.get('redis','key_temp_routing')
temp_db = redis.Redis(db=config.get('redis','temp_reris_db'))
routing_db = redis.Redis(db=config.get('redis','routing_redis_db'))

filename = sys.argv[1]
dir = os.path.dirname(filename)

from subprocess import Popen, PIPE
from multiprocessing import Process


from helpers.initscript import *
from helpers.files_splitter import *

def splitted_file_parser(fname):
    file = open(fname)
    entry = ''
    for line in file:
        if not line:
            break
        if line == '\n':
            parsed = BGP(entry,  'RIPE')
            asn = parsed.asn.split()[-1]
            block = parsed.prefix
            if block is not None:
                routing_db.sadd(asn, block)
                routing_db.sadd(block, asn)
            entry = ''
        else :
            entry += line
    syslog.syslog(syslog.LOG_INFO, 'Done')
    os.unlink(fname)

while 1:
    if not os.path.exists(filename):
        time.sleep(sleep_timer)
        continue
    output = open(dir + '/bview', 'wr')
    p = Popen([bgpdump , filename], stdout=PIPE)
    for line in p.stdout:
        output.write(line)
    output.close()
    fs = FilesSplitter(output.name, int(config.get('routing','processes_push')))
    splitted_files = fs.fplit()
    processes = []
    for file in splitted_files:
        p = Process(target=splitted_file_parser, args=(file,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    syslog.syslog(syslog.LOG_INFO, 'Done')
    os.unlink(output.name)
    os.unlink(filename)
    
