from arprequest import ArpRequest

import netifaces as ni

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
       
        ar = ArpRequest( myip, 'eth1')
#        
#        if ar.request():
#            print("Arp succes at: " )
#        else:
#            print("Arp fail at: " )
    

def main():
    searchIP()


main()
