
import time
import socket
import netifaces as ni


import matplotlib.pyplot as plt
import numpy as np
import threading 


decSlice = None
mySlice = None

arraySize = 12


def refreshFormicariumSlice():
    global mySlice
    global decSlice

    mySlice = np.add( mySlice, decSlice )

    #Add bounds
    mySlice[mySlice < 0] = 0
    mySlice[mySlice > 20] = 20



def displayFormicariumSlice():

    global mySlice
    
    i = 0
    while ( i < 10 ):
        refreshFormicariumSlice()
        time.sleep(1)
        i = i + 1
        print("\nExamining at second: " + str( i) )
        print( mySlice )
        print("\n")
    return
#    ctr = 0
#    for i in mySlice:
#        try:
#            print( str(i) + " - " + str( mySlice[i] ) )
#        except:
#            pass

def createFormicariumSlice(a,b):
    global mySlice
    global decSlice
    #mySlice = 
    
    global arraySize

    #myTuple = 1,2,3
    #myTuple = [ 0, False ]
    #yAxis = ( myTuple ) * arraySize
    #xAxis = yAxis * arraySize

    mySlice = np.zeros( shape = ([arraySize, arraySize]) ) 
    decSlice = np.ones( shape = ([arraySize, arraySize]) ) * -1 

    mySlice[a][b] = 10


def createForagingAnt( a,b, antLife = 255 ):
    #Start = a,b
    #Anyt Life is 



def main():
    ip = ni.ifaddresses('eth1')[2][0]['addr'].split(".")
    print(ip)
    x=ip[0]
    y=ip[1]
    #a=ip[2]
    #b=ip[3]
    a=3
    b=3




    createFormicariumSlice(a,b)
    
    
    sliceThread = threading.Thread( target = displayFormicariumSlice, args = () )

    #antOne will start here
    sliceThread.start()

    sliceThread.join()

main()


