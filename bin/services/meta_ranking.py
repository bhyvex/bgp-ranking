#!/usr/bin/python

"""
Main process starting the ranking. It manages a pool of processes computing the ranking.

Using the number of processes defined in the config file, the interval assigned
to each process is computed. 


FIXME: run the process on smaller intervalls and loop: the firsts ASNs 
of the database take a lot more time than the last one to compute. 
"""

import os 
import sys
import ConfigParser
config = ConfigParser.RawConfigParser()
config.optionxform = str
config.read("../../etc/bgp-ranking.conf")
root_dir = config.get('directories','root')
sys.path.append(os.path.join(root_dir,config.get('directories','libraries')))
services_dir = os.path.join(root_dir,config.get('directories','services'))

sleep_timer = int(config.get('sleep_timers','short'))
sleep_timer_long = int(config.get('sleep_timers','long'))
ranking_timer = int(config.get('ranking','sleep'))

from db_models.ranking import *
from helpers.initscript import *

import time
import syslog
syslog.openlog('Compute_Ranking', syslog.LOG_PID, syslog.LOG_USER)


processes = int(config.get('ranking','processes'))
def intervals(nb_of_asns):
    """
    Compute the size of each intervals based on the number of ASNs found in the database
    and the number of processes defined in the configuration file
    FIXME: is it possible to use the same function than the one used for the ris/whois entries ? 
    """
    interval = nb_of_asns / processes
    first = 0 
    intervals = []
    while first < nb_of_asns:
        intervals.append([first, first + interval])
        first += interval + 1
    return intervals

service = os.path.join(services_dir, "ranking_process")

while 1:
    syslog.syslog(syslog.LOG_INFO, 'Start compute ranking')
    nb_of_asns = ASNs.query.count()
    all_intervals = intervals(nb_of_asns)
    pids = []
    for interval in all_intervals:
        pids.append(service_start(servicename = service, param = str(interval[0]) + ' ' + str(interval[1])))

    while len(pids) > 0:
        # Wait until all the processes are finished
        pids = update_running_pids(pids)
        time.sleep(sleep_timer)
    syslog.syslog(syslog.LOG_INFO, 'Ranking computed')
    time.sleep(ranking_timer)

    
