#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.log import setLogLevel, info

formatter = "%r"
block = "####################"
onos1 = "10.0.3.86"
onos2 = "10.0.3.87"

def FatTree():
    """
    coreSwitch: Fat Free Topology Cores
    pods: group of switches
    ag_switches: aggregation switches per pod
    eg_switches: edge switches per pod
    hpe: hosts per edge
    """
    net = Mininet(topo=None,build=False)
    ct = []
    ct.append(net.addController('c0',controller=RemoteController,ip=onos1, port=6653))
    ct.append(net.addController('c1',controller=RemoteController,ip=onos2, port=6653))
    ctrl = []
    ctrl.append(RemoteController('c0', ip = onos1, port=6653))
    ctrl.append(RemoteController('c1', ip = onos2, port=6653))
    coreswitches = 4
    pods = 4
    ag_switches = 2
    eg_switches = 2
    hpe = 1
    coreswitch = []
    ag_switch = []
    eg_switch = []
    host = []
    
    def addNetFunc(switches,hosts,controllers):
        pass
     
    addNetFunc(switches,hosts,controllers)

    net.build()
    switch[0].start([ct0]) 
    switch[1].start([ct0]) 
    switch[2].start([ct1]) 
    switch[3].start([ct1]) 

    print "NET BUILD"
    print "NET START"
    print formatter % (block)
    print "Dumping host connections"
    print formatter % (block)
    dumpNodeConnections(net.hosts)
    print formatter % (block)
    print "Testing network connectivity"
    print formatter % (block)
    net.pingAll()
    print formatter % (block)
    print "network CLI"
    print formatter % (block)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    FatTree()
