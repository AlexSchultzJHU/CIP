
import time
import random
import socket
import netifaces as ni


import matplotlib.pyplot as plt
import numpy as np
import threading 


decSlice = None
mySlice = None

arraySize = 23


def refreshFormicariumSlice():
    global mySlice
    global decSlice

    mySlice = np.add( mySlice, decSlice )

    #Add bounds
    mySlice[mySlice < 0] = 0
    mySlice[mySlice > 20] = 20



def displayFormicariumSlice():

    global mySlice
    
    displayTime = 120
    i = 0
    while ( i < displayTime ):
        refreshFormicariumSlice()
        time.sleep(1)
        i = i + 1
        print("\nExamining at second: " + str( i) )
        print( mySlice )
        print("\n")
    return True

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

def updateeFormicariumSlice(a,b, value = 10 ):
    global mySlice
    mySlice[a][b] = value + mySlice[a][b]
    return True

def randomDirection( ):
    x = random.randint(-1,1)
    y = random.randint(-1,1)
    #print(str( x) + " " + str(y) )
    return x,y

def boundaryCheck( gridInput ):
    global arraySize
    if gridInput <= 0:
        return 0
    elif gridInput >= arraySize:
        return arraySize - 1
    else:
        return gridInput


#PortScan
def checkLocation( a,b ):
    if random.randint( 0, 12) + a + b % 7== 3:
        return True
    else:
        return False

def antForagesRandom( a,b, antLife = 255 ):
    #Start = a,b
    #Anyt Life is 
    x,y = randomDirection()
    a = boundaryCheck( a + x )
    b = boundaryCheck( b + y )
    if checkLocation( a,b ):
        updateeFormicariumSlice(a,b, 10)
    else:
        updateeFormicariumSlice(a,b, 3 )

    return a,b

def createForagingAnt( a,b, antLife = 255 ):
    currentA = a
    currentB = b
    while (antLife > 0):
        time.sleep(1)
        currentA,currentB = antForagesRandom( currentA,currentB )
        antLife = antLife - 1

    return True

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
    antOneThread = threading.Thread( target = createForagingAnt, args = (a,b) )

    #antOne will start here
    sliceThread.start()
    antOneThread.start()

    sliceThread.join()
    antOneThread.join()

    #Add nts as need
    antTwoThread = threading.Thread( target = createForagingAnt, args = (a,b) )
    antTwoThread.start()
    antTwoThread.join()
    
    antThrThread = threading.Thread( target = createForagingAnt, args = (a,b) )
    antThrThread.start()
    antThrThread.join()
 
    antForThread = threading.Thread( target = createForagingAnt, args = (a,b) )
    antForThread.start()
    antForThread.join()









main()

