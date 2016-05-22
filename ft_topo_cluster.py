#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import os, time

onos = []
onos.append("10.0.3.86")
onos.append("10.0.3.87")
onos.append("10.0.3.88")
onos.append("10.0.3.89")

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
    for i in range(len(onos)):
	crtl.append(RemoteController('c%s'%(i), ip=onos[i], port=6653))
    coreswitches = 8
    pods = 16
    ag_switches = 4
    eg_switches = 4
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
        totalAG = ag_switches*pods
        for m in range(coreswitches):
            l = m % ag_switches
            for n in range(pods):
                j = n*ag_switches + l
                info('Link: Core: %s to Pod: %s switch: %s\n'%(m,n,j))
                net.addLink(coreswitch[m],ag_switch[j])
        #ag to eg
        for m in range(pods):
            i = m * ag_switches
            j = m * eg_switches
            for n in range(i,i+ag_switches):
		for l in range(j,j+eg_switches):
            	    info('Link: AG:%s EG:%s\n'%(ag_switch[n],eg_switch[l]))
                    net.addLink(ag_switch[n].name,eg_switch[l])
        #eg to host
	for n in range(0,eg_switches*pods,1):
            for m in range(n*hpe,(n*hpe)+hpe):
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
    for i in range(len(onos)):
        info('ON%s: %s\n'%(i,onos[i]))
    for i in range(len(onos)):
	ct.append(net.addController('c%s'%(i),controller=RemoteController,ip=onos[i], port=6653))
    info('Building Network\n')
    net.build()
    time.sleep(1)
    info('starting ag switches\n')
    for n in range(pods):
        l = n * ag_switches
        for m in range(eg_switches):
            t = l+m
            ag_switch[t].start([ct[n%4]])
            info('ag switch: %s\n'%t)

    info('all ag switches online\n')
    time.sleep(2)
     
    info('starting eg switches\n')
    for n in range(pods):
        l = n * eg_switches
        for m in range(eg_switches):
            t = l+m
	    eg_switch[l+m].start([ct[n%4]])
            info('eg switch: %s\n'%t)
	    time.sleep(2)
    info('all eg switches online\n')
    info('wait 10s to start core switches\n')
    for i in range(10,0,-1):
        info('%s\n'%i) 
	time.sleep(1)
    
    info('starting core switches\n')
    for n in range(len(coreswitch)):
        coreswitch[n].start([ct[n%4]])
        info('start core switch: %s\n'%n)
        time.sleep(3)
    info('all core switches online\n')
    time.sleep(3)
    info('Dumping host connections\n')
    dumpNodeConnections(net.hosts)
    info("Testing network connectivity\n")
    #net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    FatTree()
