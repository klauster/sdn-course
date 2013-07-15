#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"

#    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout, **opts):
        """Init.
        fanout: fanout (number of child switch per parent switch)
        linkopts1: Core link options
        linkopts2: Aggregation link options
        linkopts3: Edge link options"""

#       super(CustomTopo, self).__init__(**opts)

        Topo.__init__(self, **opts)

        self.fanout = fanout
	self.linkopts1 = linkopts1
	self.linkopts2 = linkopts2
	self.linkopts3 = linkopts3

        kAggr = 1
	kEdge = 1
	kHost = 1

        # Add Core switch

        swCore = self.addSwitch('c1')
	print swCore 

        # Add Aggregation Layer

        lastSwitch = None 
        for i in irange (1, fanout):
            swAggr = self.addSwitch('a%s' % kAggr)
	    print swAggr
            self.addLink( swCore, swAggr, **linkopts1 )
	    kAggr += 1

            for j in irange(1, fanout):
                swEdge = self.addSwitch('e%s' % kEdge)
                print swEdge
		self.addLink( swAggr, swEdge, **linkopts2 )
	  	kEdge += 1

                for k in irange(1, fanout):
                    host = self.addHost( 'h%s' % kHost)
                    print host
		    self.addLink ( host, swEdge, **linkopts3 )
		    kHost += 1


def customTest():
    "Create and test a fanout network."

#    linkopts1 = {'bw':50, 'delay':'5ms', 'loss':0, 'max_queue_size':1000, 'use_htb':True}
    linkopts1 = {'bw':50, 'delay':'5ms'}
    linkopts2 = {'bw':30, 'delay':'10ms'}
    linkopts3 = {'bw':10, 'delay':'15ms'}

    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=3)
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    print "Dumping switch connections"
    dumpNodeConnections(net.switches)
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
#    net.pingAll()
    print "Testing bandwidth between h1 and h27"
    h1, h27 = net.get('h1', 'h27')
    net.iperf((h1, h27))
    print h1.cmd('ping', '-c6', h27.IP())

    net.stop()

if __name__ == '__main__':
    # Tell mininent to print useful information
    setLogLevel('info')
    customTest()
                    
topos = { 'custom': ( lambda: CustomTopo() ) }
