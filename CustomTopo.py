'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 3 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"

#    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
    def __init__(self, fanout, **opts):
        """Init.
        fanout: fanout (number of child switch per parent switch)
        linkopts1: Core link options
        linkopts2: Aggregation link options
        linkopts3: Edge link options"""

#       super(CustomTopo, self).__init__(**opts)

        Topo.__init__(self, **opts)

        self.fanout = fanout

        fAggr = fanout
        fEdge = fAggr*2
        fHost = fEdge*2

        # Add Core switch

        swCore = self.addSwitch('c1')

        # Add Aggregation Layer

        lastSwitch = None 
        for i in irange (1, fanout):
            swAggr = self.addSwitch('a%s' % i)
            self.addLink( swCore, swAggr )

            for j in irange(1, fanout):
                swEdge = self.addSwitch('e%s' % i)
                self.addLink( swAggr, swEdge )

                for k in irange(1, fanout):
                    host = self.addHost( 'h%s' % i)
                    self.addLink ( host, swEdge )


def customTest():
    "Create and test a fanout network"
    topo = CustomTopo(fanout=2)
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    # Tell mininent to print useful information
    setLogLevel('info')
    customTest()
                    
topos = { 'custom': ( lambda: CustomTopo() ) }