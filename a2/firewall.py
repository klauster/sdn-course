'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 4 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''

# import 'csv' module to handle reading of firewall-policies.csv file
import csv


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        
        msg = of.ofp_flow_mod()
        match = of.ofp_match()

        # Read lines from CSV file
        with open(policyFile) as csvfile:
            macFilter = csv.DictReader(csvfile)

            # For each row create a 
            for row in macFilter:
                msg.match.dl_src = row['mac_1']
                msg.match.dl_dst = row['mac_2']
                log.debug('installing filter for %s -> %s' (row['mac_1']), row['mac_2']))
                msg.actions.append(of.ofp_action_output())
                self.connection.send(msg)

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
