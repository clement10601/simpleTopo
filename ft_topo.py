#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.log import setLogLevel, info

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
    crtl = []
    crtl.append(RemoteController('c0', ip=onos1, port=6653))
    crtl.append(RemoteController('c1', ip=onos2, port=6653))
    coreswitches = 4
    pods = 4
    ag_switches = 2
    eg_switches = 2
    hpe = 1
    coreswitch = []
    ag_switch = []
    eg_switch = []
    host = []
    def addSwitch(sw_type,count):
	if sw_type is 'coreswitch':
            for n in range(count):
		if n % 2 ==0:
		    ctl = 0
                else:
		    ctl = 1
	        coreswitch.append(net.addSwitch('c%s'%(n),controller=crtl[ctl],protocols='OpenFlow13'))
	elif sw_type is 'ag_switch':
            for n in range(count):
		if n % 2 ==0:
                    ctl = 0
                else:
                    ctl = 1
                ag_switch.append(net.addSwitch('a%s'%(n),controller=crtl[ctl],protocols='OpenFlow13'))
        elif sw_type is 'eg_switch':
            for n in range(count):
		if n % 2 ==0:
                    ctl = 0
                else:
                    ctl = 1
                eg_switch.append(net.addSwitch('e%s'%(n),controller=crtl[ctl],protocols='OpenFlow13'))
    def addHost(count):
        for n in range(count):
            host.append(net.addHost('h%s' % (n)))

    def addLink(coreswitches,pods,ag_switches,eg_switches,hpe):
        info('Adding Switch Links\n')
        #core to ag
        for n in range(0,ag_switches*pods,2):
	    for m in range(0,coreswitches,2):
	        net.addLink(coreswitch[m],ag_switch[n])
	        net.addLink(coreswitch[m+1],ag_switch[n+1])
        #ag to eg
	for n in range(0,eg_switches*pods,2):
	    for m in range(n,n+eg_switches):
		net.addLink(ag_switch[n],eg_switch[m])
		net.addLink(ag_switch[n+1],eg_switch[m])
        #eg to host
	for n in range(0,eg_switches*pods*hpe,hpe):
            for m in range(n,n+hpe):
	    	net.addLink(eg_switch[n],host[m])

    def addNetFunc(coreswitches,pods,ag_switches,eg_switches,hpe):
        addSwitch('coreswitch',coreswitches)
        addSwitch('ag_switch',ag_switches*pods)
        addSwitch('eg_switch',eg_switches*pods)
        addHost(eg_switches*pods*hpe)
        addLink(coreswitches,pods,ag_switches,eg_switches,hpe)
     
    addNetFunc(coreswitches,pods,ag_switches,eg_switches,hpe)
    ct.append(net.addController('c0',controller=RemoteController,ip=onos1, port=6653))
    ct.append(net.addController('c1',controller=RemoteController,ip=onos2, port=6653))
    net.build()
    print "NET BUILD"

    for n in range(0,len(coreswitch),2):
	coreswitch[n].start([ct[0]])
	coreswitch[n+1].start([ct[1]])
    for n in range(0,len(ag_switch),2):
	ag_switch[n].start([ct[0]])
	ag_switch[n+1].start([ct[1]])
    for n in range(0,len(eg_switch),2):
        eg_switch[n].start([ct[0]])
        eg_switch[n+1].start([ct[1]])
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    #net.pingAll()
    print "network CLI"
    CLI(net)
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    FatTree()
