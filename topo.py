#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch,RemoteController
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.log import setLogLevel, info

formatter = "%r"
block = "####################"
#c0 = RemoteController( 'c0', ip='127.0.0.1',port=6633 )
class dualSH(Topo):
    def __init__(self,n=2,s=2,**opts):
        Topo.__init__(self,**opts)
        for sn in range(s):
            info('*** Adding Switch %s'%(sn+1))
            switch = self.addSwitch('s%s'%(sn+1))
        
        for hn in range(n):
            info('*** Adding Host %s'%(hn+1))
            host = self.addHost('h%s' % (hn+1))

        for j in range(1,3):
            info('*** Adding Links')
            self.addLink('h%s' % (j), 's%s' % (j))
        
        info('Adding Switch Link')
        self.addLink('s1','s2')

def simTest():
    topo =  dualSH()
    net = Mininet(topo=topo,build=False)
    
    info('*** Adding Controller\n')
    ryu_ctl = net.addController('c0',controller=RemoteController,ip='127.0.0.1',port=6633)
    
    net.build()
    print "NET BUILD"
    sw1 = net.getNodeByName('s1')
    sw2 = net.getNodeByName('s2')
    sw1.protocols = 'OpenFlow13'
    sw2.protocols = 'OpenFlow13'
    
    net.getNodeByName('s1').start([ryu_ctl])
    net.getNodeByName('s2').start([ryu_ctl])
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
    CLI( net )
    net.stop()
        
if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simTest()
