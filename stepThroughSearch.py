
'''
   #!/usr/bin/python
   # -*- coding: utf-8 -*-
   '''
import sys
from socket import *
import time




import os
import time
import random
import socket
import netifaces as ni
import queue

import concurrent.futures


import numpy as np
import threading 
import subprocess


decSlice = None
mySlice = None
deviceSlice = None

arraySize = 16
maxScoutingAnts = 5
antScoutThreadArray = []
antScoutPositionArray = []

maxForagingAnts = 5
antForageThreadArray = []
antForagePositionArray = []

portScanDict = {}

x=0
y=0

def refreshFormicariumSlice():
    global mySlice
    global decSlice

    mySlice = np.add( mySlice, decSlice )

    #Add bounds
    mySlice[mySlice < 0] = 0
    mySlice[mySlice > 99] = 99

def displayReports():
    print("AntMapper Report:")
    for i in portScanDict:
        if portScanDict[i]:
            print( str(i) + " - " + str( portScanDict[i] ))

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
    mySlice[a][b] = 50

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
    i = str(x) + "." + str(y) + "." + str(a) + "." + str(b)


    #r = subprocess.call(  ["ping","-c", "3", i ], stdout=open(os.devnull )  )
    #r = subprocess.run(  ["arp", "-a", i ]  )
    
    r = subprocess.check_output(  ["arp", "-a", i ]  )
    #r = subprocess.call(  ["ping","-c", "3", i ], stdout=open(os.devnull )  )
    print("Line: " + str(r ) )
    print("Line: " + str(r )[2:5] )
    if str(r)[2:5] == 'arp' :
        print( "Caught bad arp" )
        return False

    defRet = False

    target_ip = socket.gethostbyname(i)
    start_port = 50
    end_port = 80
 
    #the list to record open ports
    opened_ports = []
    connect_suc = "False"
    bConnect = False
 
    for port in range(start_port, end_port):
        sock = socket.socket(AF_INET, SOCK_DGRAM)
        sock.settimeout(3000)
        result = sock.connect_ex((target_ip, port))
        #print( str(target_ip) + " " + str(port) + " " + str(result))
        #result = 1 means this port is open?
        if result == 0:
            opened_ports.append(port)
            defRet = True
        sock.close() 
        
        #connect_suc = "True"
        #bConnect = True
 
#    #Create/Send report


    portScanDict[i] = opened_ports
#    print("whether it can access to", i,": ",connect_suc)
#   # print("\nOpened ports:",opened_ports)
# 
# 
#    return bConnect
#    # for i in opened_ports:
#   # print(i)
    return defRet

def testPortScan():
    global x
    global y
    x = 10
    y = 0
    
    checkLocation( 3,9 )
  #  checkLocation( 3,19 )
    
def antForagesRandom( a,b ):
    #Start = a,b
    #Anyt Life is 
    x,y = randomDirection()
    a = boundaryCheck( a + x )
    b = boundaryCheck( b + y )
    if checkLocation( a,b ):
        updateFormicariumSlice(a,b, 25, True)
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
        updateFormicariumSlice(a,b, 25, True )
    else:
        updateFormicariumSlice(a,b, 3, False )
    return a,b
 

def createScoutingAnt( a,b, pos = -1, antScoutQueue = None, antLife = 255 ):
    currentA = a
    currentB = b
   
    
    currentA,currentB = antForagesRandom( currentA,currentB )
   
    
    if pos != -1: 
        antScoutQueue.queue[pos] = ( [currentA, currentB] ) 
    
    return currentA,currentB


def createForagingAnt(  a,b, pos = -1, antForageQueue = None, antLife = 255 ):
    currentA = a
    currentB = b
    currentA,currentB = antForagesFollowPath( currentA,currentB )


    #try:
    if pos != -1 and pos < maxForagingAnts:
        antForageQueue.queue[pos] = ( [currentA, currentB] ) 
    #except:
    #        pass
    return currentA,currentB



def stepGeneric( maxAnts, antPositionArray, antThreadArray, createAnt ):
    antQueue = queue.Queue( maxAnts + 1 )
    antQueue.put(1)
    for i in range( 0, maxAnts   ):
        #print(i)
        antQueue.put(1)
        a,b = antPositionArray[i] 
        antThread = threading.Thread( target = lambda myArg1, myArg2, pos, myAntQueue:  createAnt( myArg1,myArg2, pos, myAntQueue ) , args = ( a,b, i, antQueue ) )
        antThread.start()
        antThreadArray.append( antThread )
    
    for ant in antThreadArray:
        ant.join()
   
    try:
        for pos in range( maxAnts ) :
            myPos = antQueue.get()
            #print("testMyPos")
            if type( myPos ) == int:
                break
            if myPos == None:
                break
            #print("testMyPos done")
            a = myPos[0]
            #print("testMyPos[a] - " + str(a) )
            b = myPos[1]
            antPositionArray[pos] = [ a,b ]
    except: 
        #print("excepption at generic ants")
        pass





def stepAnts():

    stepGeneric( maxScoutingAnts, antScoutPositionArray, antScoutThreadArray, createScoutingAnt )
    stepGeneric( maxForagingAnts, antForagePositionArray, antForageThreadArray, createForagingAnt )
#    
#    antScoutQueue = queue.Queue( maxScoutingAnts + 1 )
#    antScoutQueue.put(1)
#    for i in range( 0, maxScoutingAnts  ):
#        antScoutQueue.put(1)
#        a,b = antScoutPositionArray[i] 
#        antScoutThread = threading.Thread( target = lambda myArg1, myArg2, pos, myAntScoutQueue:  createScoutingAnt( myArg1,myArg2, pos, myAntScoutQueue ) , args = ( a,b, i, antScoutQueue ) )
#        antScoutThread.start()
#    
#    for ant in antScoutThreadArray:
#        ant.join()
#   
#    pos = 0
#    try:
#        #w#hile(True):
#        for pos in maxScoutingAnts:
#                #if pos >= maxScoutingAnts:
#                #    break
#                myPos = antScoutQueue.get()
#                if type( myPos ) == int:
#                    break
#                if myPos == None:
#                    break
#                a = myPos[0]
#                b = myPos[1]
#                antScoutPositionArray[pos] = [ a,b ]
#                #pos = pos + 1
#
#    except:
#        pass
#
#    antForageQueue = queue.Queue( maxForagingAnts + 1 )
#    antForageQueue.put(1)
#    for i in range( 0, maxForagingAnts ):
#        antForageQueue.put(1)
#        a,b = antForagePositionArray[i]
#        print(a)
#        print(b)
#        print(i)
#
#        antForageThread = threading.Thread( target = lambda myArg1, myArg2, pos, antForageQueue:  createForagingAnt( myArg1,myArg2, pos, antForageQueue ) , args = ( a,b, i, antForageQueue ) )
#        antForageThread.start()
#    
#    for ant in antForageThreadArray:
#        ant.join()
#  
#    try:
#        for pos in range( maxForagingAnts) :
#        #pos = 0
#        #while(True):
#                #if pos >= maxForagingAnts:
#                #    return
#                myPos = antForageQueue.get()
#                if myPos is None:
#                    return
#                a = myPos[0]
#                b = myPos[1]
#                antForagePositionArray[pos] = [ a,b ]
#                pos = pos + 1
#    except:
#            pass
#    return
#
def initializeAnts(a,b):
    global maxScoutingAnts 
    global antScoutThreadArray 
    global antScoutPositionArray 
    
#        antScoutQueue.put(1)
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
    print("P/p = display Ant phermones in grid.")
    print("D/d = display devices found in grid." )
    print("R/r = display report." )
    print("N/n = exit." )
    print("Else, any input to step through next phase of ants." )

 
    intExit = 400
    boolExit = True
    while boolExit:
        intExit = intExit - 1
        myInput = input("Next step? Press enter or 'N/n' : \n") 
        if myInput == 'N' or  myInput == 'n':
            boolExit = False
        #if D/d displayFormic
        elif myInput == 'P' or  myInput == 'p':
            displayFormicariumSlice()
        elif myInput == 'D' or  myInput == 'd':
            displayDeviceSlice()
        elif myInput == 'R' or  myInput == 'r':
        
            displayReports()
        
        else:
            stepAnts()

        if intExit <= 0:
            boolExit = False



def main():
    global x
    global y

    ip = ni.ifaddresses('enp0s3')[2][0]['addr'].split(".")
    x=int(ip[0])
    y=int(ip[1])
    a=int(ip[2])
    b=int(ip[3])
    
    print("Create formicarium slice:")
    createFormicariumSlice(a,b)
    print("Initialize ants:")
    initializeAnts( a,b )
    stepThrough( a,b)



main()

#testPortScan()


