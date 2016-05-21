#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import os, time
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
    time.sleep(1)
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
            ct = 0
            for n in range(count):
		if n % 2 ==0:
		    ctl = 0
                else:
		    ctl = 1
		ct+=1
	        coreswitch.append(net.addSwitch('s10%s'%(n),controller=crtl[ctl],protocols='OpenFlow13'))
            info('Adding core switches: %s\n'%ct)
	elif sw_type is 'ag_switch':
            ct = 0
            for n in range(count):
		if n % 2 ==0:
                    ctl = 0
                else:
                    ctl = 1
		ct+=1
                ag_switch.append(net.addSwitch('s20%s'%(n),controller=crtl[ctl],protocols='OpenFlow13'))
            info('Adding AG switches: %s\n'%ct)
        elif sw_type is 'eg_switch':
            ct = 0
            for n in range(count):
		if n % 2 ==0:
                    ctl = 0
                else:
                    ctl = 1
		ct+=1
                eg_switch.append(net.addSwitch('s30%s'%(n),controller=crtl[ctl],protocols='OpenFlow13'))
            info('Adding EG switches: %s\n'%ct)
    def addHost(count):
	ct =0
        for n in range(count):
	    ct+=1
            host.append(net.addHost('h%s' % (n)))
        info('Adding Hosts: %s\n'%ct)

    def addLink(coreswitches,pods,ag_switches,eg_switches,hpe):
        info('Adding Switch Links\n')
        #core to ag
        for n in range(0,ag_switches*pods,2):
	    for m in range(0,coreswitches,2):
        	info('Link: Core:%s AG:%s\n'%(coreswitch[m].name,ag_switch[n].name))
	        net.addLink(coreswitch[m].name,ag_switch[n].name)
        	info('Link: Core:%s AG:%s\n'%(coreswitch[m+1].name,ag_switch[n+1].name))
	        net.addLink(coreswitch[m+1].name,ag_switch[n+1].name)
        #ag to eg
	for n in range(0,ag_switches*pods,2):
	    for m in range(n,n+eg_switches):
        	info('Link: AG:%s EG:%s\n'%(ag_switch[n].name,eg_switch[m].name))
		net.addLink(ag_switch[n].name,eg_switch[m].name)
        	info('Link: AG:%s EG:%s\n'%(ag_switch[n+1].name,eg_switch[m].name))
		net.addLink(ag_switch[n+1].name,eg_switch[m].name)
        #eg to host
	for n in range(0,eg_switches*pods*hpe,hpe):
            for m in range(n,n+hpe):
        	info('Link: EG:%s Host:%s\n'%(eg_switch[n].name,host[m].name))
	    	net.addLink(eg_switch[n].name,host[m].name)

    def addNetFunc(coreswitches,pods,ag_switches,eg_switches,hpe):
        addSwitch('coreswitch',coreswitches)
        addSwitch('ag_switch',ag_switches*pods)
        addSwitch('eg_switch',eg_switches*pods)
        addHost(eg_switches*pods*hpe)
        addLink(coreswitches,pods,ag_switches,eg_switches,hpe)
     
    addNetFunc(coreswitches,pods,ag_switches,eg_switches,hpe)
    info('Connect to controller\n')
    info('ON1: %s\n'%onos1)
    info('ON2: %s\n'%onos2)
    ct.append(net.addController('c0',controller=RemoteController,ip=onos1, port=6653))
    ct.append(net.addController('c1',controller=RemoteController,ip=onos2, port=6653))
    res = net.build()
    time.sleep(5)
    for n in range(0,len(coreswitch),2):
  	coreswitch[n].start([ct[0]])
	coreswitch[n+1].start([ct[1]])
    for n in range(0,len(ag_switch),2):
	ag_switch[n].start([ct[0]])
	ag_switch[n+1].start([ct[1]])
    for n in range(0,len(eg_switch),2):
        eg_switch[n].start([ct[0]])
        eg_switch[n+1].start([ct[1]])
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
