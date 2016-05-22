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

def simTest():
    net = Mininet(topo=None,build=False)
    ct0 = net.addController('c0',
    	controller=RemoteController,
        ip=onos1, port=6653)
    ct1 = net.addController('c1',
        controller=RemoteController,
        ip=onos2, port=6653)
    ctrl = []
    ctrl.append(RemoteController('c0', ip = onos1, port=6653))
    ctrl.append(RemoteController('c1', ip = onos2, port=6653))
    switches=2
    hosts=2
    controllers=2
    switch = []
    host = []
    def addNetFunc(switches,hosts,controllers):
        for cc in range(controllers):
            for sn in range(switches):
                info('*** Adding Switch %s for controller %s\n'%(sn+1,cc+1))
                switch.append(net.addSwitch('sc%s%s'%(sn+1,cc+1),
                                         controller=ctrl[cc],
                                         protocols='OpenFlow13'))
            for hn in range(hosts):
                info('*** Adding Host %s\n'%(hn+1))
                host.append(net.addHost('hc%s%s' % (hn+1,cc+1)))
            k = 1
            km = int(hosts/switches)+1
            for i in range(1, switches+1):
                for j in range(k, km):
                    net.addLink('hc%s%s' % (j,cc+1), 'sc%s%s' % (i,cc+1))
                k = km
                km = km+int(hosts/switches)
                if (hosts%switches) != 0:
                    km += 1
            info('Adding Switch Link\n')
            for a in range(1, switches):
                net.addLink('sc%s%s'%(a,cc+1), 'sc%s%s'%(a+1,cc+1)) 
    addNetFunc(switches,hosts,controllers)
    net.addLink('sc11','sc12')
    net.addLink('sc21','sc22')
    net.build()
    net.build()
    switch[0].start([ct0]) 
    switch[1].start([ct0]) 
    switch[2].start([ct1]) 
    switch[3].start([ct1]) 
    print "NET BUILD"
#    net.start()
#    net.start()
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
    simTest()
