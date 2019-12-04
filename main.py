

import socket
from arprequest  import ArpRequest

import imaplib
import netifaces as ni

#Test for new pc

def searchIP():
    ip = ni.ifaddresses('eth1')[2][0]['addr'].split(".")
    print(ip)
    x=ip[0]
    y=ip[1]
    a=ip[2]
    b=ip[3]

    for i in range( 64, 88 ):
        myip = ( str(x) + "." + str(y) + "." + str(a) + "." + str(i) )
 
        print (myip)
       
        #ar = ArpRequest( myip, 'eth1')
        #ar = ArpRequest( myip, 'eth0')
        
        print("A")
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
        print("A")
        s.bind(("eth0", myip))
        print("A")
        s.send(packet)
        print("A")




from scapy.all import*
def asdf():    
    ether=ETHER()
    arp=ARP()
    ether.dst='ff:ff:ff:ff:ff:ff'
    dst=raw_input('n enter the destination ip address=')
    arp.op=1
    arp.pdst=dst
    sendp(ether/arp)



#


#        if ar.request():
#            print("Arp succes at: " )
#        else:
#            print("Arp fail at: " )
    

def main():
    #searchIP()
    asdf()

main()
