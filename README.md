# simpleTopo
SimpleTopo

Environment:

    Ubuntu 14.04.2
    Mininet 2.2.0
    Ryu Controller 3.19
    Openvswitch 2.0.2
  
Attention:

Latest Openvswitch version 2.3.1 did not support Linux Kernal which version is greater than 3.14
    
    Kernal Downgrade(aptitude installed)
    
        Search for Packages:
        
            aptitude search linux-image
            aptitude search linux-headers
        
        Install Package:
            
            aptitude install linux-image-3.13.0-46-generic linux-headers-3.13.0-31-generic
        
        Remove Kernal:
            
            aptitude remove linux-image-3.16.0-XX-generic linux-image-3.16.0-XX-generic
    
        Reboot
        
    
RYU Controller need several dependencies

    Dependencies:
    
        Main:
    
            python-eventlet python-routes python-webob python-paramiko python-netaddr 
            python-lxml python-oslo-config python-msgpack
            
        Secondary:
        
            python-pip python-dev python-crypto python-ecdsa python-greenlet python-paramiko python-six
        
Usage:
    
Start RYU controller
        
        ryu-manager ryu_apps/simple_switch_13.py
        
Run topo:
    
        ./topo.py
        
or
    
        python topo.py
