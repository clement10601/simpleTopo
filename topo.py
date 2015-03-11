#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.log import setLogLevel, info

formatter = "%r"
block = "####################"
c0 = RemoteController('c0', ip='127.0.0.1', port=6633)
class dualSH(Topo):
    def __init__(self, n=2, s=2, **opts):
        Topo.__init__(self, **opts)
        for sn in range(s):
            info('*** Adding Switch %s\n'%(sn+1))
            switch = self.addSwitch('s%s'%(sn+1),
                                    controller=c0,
                                    protocols='OpenFlow13')

        for hn in range(n):
            info('*** Adding Host %s\n'%(hn+1))
            host = self.addHost('h%s' % (hn+1))
        k = 1
        km = int(n/s)+1
        for i in range(1, s+1):
            for j in range(k, km):
                self.addLink('h%s' % (j), 's%s' % (i))
            k = km
            km = km+int(n/s)
            if (n%s) != 0:
                km += 1

        info('Adding Switch Link\n')
        for a in range(2, s+1):
            self.addLink('s%s'%a, 's1')

def simTest():
    topo = dualSH()
    net = Mininet(topo=topo, build=False)
    ryu_ctl = net.addController('c0',
                                controller=RemoteController,
                                ip='127.0.0.1', port=6633)

    net.build()
    print "NET BUILD"
    net.start()
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
