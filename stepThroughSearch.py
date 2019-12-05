
import time
import random
import socket
import netifaces as ni
import Queue

import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import imshow, show, colorbar

import concurrent.futures


#import matplotlib.pyplot as plt
import numpy as np
import threading 

import pylab as plt


decSlice = None
mySlice = None
deviceSlice = None

arraySize = 12

maxScoutingAnts = 5
antScoutThreadArray = []
antScoutPositionArray = []

maxForagingAnts = 5
antForageThreadArray = []
antForagePositionArray = []
 

def refreshFormicariumSlice():
    global mySlice
    global decSlice

    mySlice = np.add( mySlice, decSlice )

    #Add bounds
    mySlice[mySlice < 0] = 0
    mySlice[mySlice > 20] = 20


def displayDeviceSlice():
    print( deviceSlice )

def displayFormicariumSlice():
    refreshFormicariumSlice()
    print( mySlice )

def createFormicariumSlice(a,b):
    global mySlice
    global decSlice
    global deviceSlice
    
    global arraySize
    mySlice = np.zeros( shape = ([arraySize, arraySize]) ) 
    decSlice = np.ones( shape = ([arraySize, arraySize]) ) * -1 
    deviceSlice = np.zeros( shape = ([arraySize, arraySize]) ) 
    
    deviceSlice[a][b] = 3
    mySlice[a][b] = 10

def updateFormicariumSlice(a,b, value = 10, deviceFound = False ):
    global mySlice
    global deviceSlice
    mySlice[a][b] = value + mySlice[a][b]
    if  deviceSlice[a][b] > 0:
        pass
    elif 0 == deviceSlice[a][b] :
        if deviceFound :
            deviceSlice[a][b] = 2  
        else:
            deviceSlice[a][b] = -1
            
    return True

def randomDirection( ):
    x = random.randint(-1,1)
    y = random.randint(-1,1)
    
    #Eliminate staying still
    if x == 0 and y == 0:
        x,y = randomDirection()


    return x,y

def boundaryCheck( gridInput ):
    global arraySize
    if gridInput <= 0:
        return 0
    elif gridInput >= arraySize:
        return arraySize - 1
    else:
        return gridInput


#Logically, dont want to follow exact same path
#Will want to randomly pick left or right?
#Goal: Find highest neighboring value, go to lower value 'left' or 'right' of it, random if tie
# should not go backwards thus values of 9 or 10 should be 'behind' ant
def bestDirection( a,b ):
    global mySlice
    
    x = 0
    y = 0

    #Will revisit logic
    n = mySlice[ boundaryCheck(a+1) ][ boundaryCheck(b) ] 
    e = mySlice[ boundaryCheck(a) ][ boundaryCheck(b+1) ] 
    s= mySlice[ boundaryCheck(a-1) ][ boundaryCheck(b) ] 
    w = mySlice[ boundaryCheck(a) ][ boundaryCheck(b-1) ] 

    #head toward unknwon, vear off as scout may hit known 0
    cardinal = [ n, e, s, w]
    myDir = min( cardinal )

    if 0 == cardinal.index([ myDir ]):
        x = 1
        if myDir == 0:
            y = 0
        else:
            y = randomDirection()[0]
    elif 1 == cardinal.index([ myDir ]):
        y = 1
        if myDir == 0:
            x = 0
        else:
            x = randomDirection()[0]
    elif 2 == cardinal.index([ myDir ]):
        x = -1
        if myDir == 0:
            y = 0
        else:
            y = randomDirection()[0]
    elif 3 == cardinal.index([ myDir ]):
        y = -1
        if myDir == 0:
            x = 0
        else:
            x = randomDirection()[0]

    if x == 0 and y == 0:
        x,y = randomDirection()

    return x,y



#PortScan code placed here
def checkLocation( a,b ):
    # myip = "10.0." + str(a) +"." + str(b)
    # active_ip_mac=arp_scan(myip)
    # queue=Queue()
    # net=ipaddress.ip_network(network)
    # for ip in net:
    #     ip_addr=str(ip)
    #     arp_one=Process(target=arprequest,args=(ip_addr,queue))
    #     arp_one.start()
    # time.sleep(2)
    # ip_mac_list=[]
    # while True:
    #     if queue.empty():
    #         break;
    #     else:
    #         ip,mac=queue.get()
    #         ip_mac_list.append((ip,mac))
    # 
    # for ip,mac in active_ip_mac_list:
    #     print(ip,mac)
    #     print(str(len(active_ip_mac)))

    #Random generation
    if a*b*7%13 == 1:
        return True
    else:
        return False

def antForagesRandom( a,b ):
    #Start = a,b
    #Anyt Life is 
    x,y = randomDirection()
    a = boundaryCheck( a + x )
    b = boundaryCheck( b + y )
    if checkLocation( a,b ):
        updateFormicariumSlice(a,b, 10, True)
    else:
        updateFormicariumSlice(a,b, 3, False )
    return a,b


def antForagesFollowPath( a,b):
    #Start = a,b
    #Anyt Life is 
    x,y = bestDirection(a,b)
    a = boundaryCheck( a + x )
    b = boundaryCheck( b + y )
    if checkLocation( a,b ):
        updateFormicariumSlice(a,b, 10, True )
    else:
        updateFormicariumSlice(a,b, 3, False )
    return a,b
 

def createScoutingAnt( a,b, pos = -1, antScoutQueue = None, antLife = 255 ):
    currentA = a
    currentB = b
    
    currentA,currentB = antForagesRandom( currentA,currentB )
   
    try:
        if pos == antScoutQueue.qsize():
            return currentA,currentB
    except:
            return currentA,currentB
            
    if pos != -1:
        antScoutQueue.queue[pos] = ( [currentA, currentB] ) 
    
    return currentA,currentB


def createForagingAnt(  a,b, pos = -1, antForageQueue = None, antLife = 255 ):
    currentA = a
    currentB = b
    currentA,currentB = antForagesFollowPath( currentA,currentB )

    if pos != -1:
        antForageQueue.queue[pos] = ( [currentA, currentB] ) 
    return currentA,currentB

def stepAnts():
    antScoutQueue = Queue.Queue( maxScoutingAnts + 1 )
    for i in range( 0, maxScoutingAnts  ):
        antScoutQueue.put(1)
        a,b = antScoutPositionArray[i] 
        antScoutThread = threading.Thread( target = lambda myArg1, myArg2, pos, myAntScoutQueue:  createScoutingAnt( myArg1,myArg2, pos, myAntScoutQueue ) , args = ( a,b, i, antScoutQueue ) )
        antScoutThread.start()
    
    for ant in antScoutThreadArray:
        ant.join()
   
    pos = 0
    while(True):
            if pos >= maxScoutingAnts:
                return
            myPos = antScoutQueue.get()
            if myPos == None:
                return
            a = myPos[0]
            b = myPos[1]
            antScoutPositionArray[pos] = [ a,b ]
            pos = pos + 1

    antForageQueue = Queue.Queue( maxForagingAnts + 1 )
    for i in range( 0, maxForagingAnts ):
        antForageQueue.put(1)
        a,b = antForagePositionArray[i] 
        antForageThread = threading.Thread( target = lambda myArg1, myArg2, pos, antForageQueue:  createForagingAnt( myArg1,myArg2, pos, antForageQueue ) , args = ( a,b, i, antForageQueue ) )
        antForageThread.start()
    
    for ant in antForageThreadArray:
        ant.join()
   
    pos = 0
    while(True):
            if pos >= maxForagingAnts:
                return
            myPos = antForageQueue.get()
            if myPos == None:
                return
            a = myPos[0]
            b = myPos[1]
            antForagePositionArray[pos] = [ a,b ]
            pos = pos + 1
    return

def initializeAnts(a,b):
    global maxScoutingAnts 
    global antScoutThreadArray 
    global antScoutPositionArray 
    
    for i in range( 0, maxScoutingAnts  ):
        antScoutPositionArray.append(  [a,b] )
        antScoutThread = threading.Thread( target = createScoutingAnt, args = (a,b, -1, None) )
        antScoutThread.start()
        antScoutThreadArray.append( antScoutThread )
  
    for ant in antScoutThreadArray:
            ant.join()
    
    global maxForagingAnts 
    global antForageThreadArray 
    global antForagePositionArray 
    
    for i in range( 0, maxForagingAnts ):
        antForagePositionArray.append( [a,b] )
        antForageThread = threading.Thread( target = createForagingAnt, args = (a,b, -1, None) )
        antForageThread.start()
        antForageThreadArray.append( antForageThread )
  
    for ant in antForageThreadArray:
            ant.join()


    return



def stepThrough(a,b):
    print("Options:")
    print("P/p = display Ant phermones.")
    print("D/d = display devices found." )
    print("Else, step through next phase of ants." )

 
    intExit = 100
    boolExit = True
    while boolExit:
        intExit = intExit - 1
        myInput = raw_input("Next step? Press enter or 'N/n' : ") 
        if myInput == 'N' or  myInput == 'n':
            boolExit = False
        #if D/d displayFormic
        elif myInput == 'P' or  myInput == 'p':
            displayFormicariumSlice()
        elif myInput == 'D' or  myInput == 'd':
            displayDeviceSlice()
        else:
            stepAnts()

        if intExit <= 0:
            boolExit = False



def main():
    ip = ni.ifaddresses('eth1')[2][0]['addr'].split(".")
    print(ip)
    x=ip[0]
    y=ip[1]
    #a=ip[2]
    #b=ip[3]
    
    # For algorithm
    a=3
    b=3

    createFormicariumSlice(a,b)
    initializeAnts( a,b )
    stepThrough( a,b)



main()



