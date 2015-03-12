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
        
        apt-get install python-pip
        apt-get install python-dev
        apt-get install python-plxml
        apt-get install python-crypto
        apt-get install python-eventlet
        apt-get install python-routes
        apt-get install python-webob
        apt-get install python-paramiko
        pip install pip --upgrade
        pip2 install six
        
