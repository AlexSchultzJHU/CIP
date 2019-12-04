
import time
import random
import socket
import netifaces as ni


import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import imshow, show, colorbar

#import matplotlib.pyplot as plt
import numpy as np
import threading 

import pylab as plt


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
        
        #mshow( mySlice )
        #olorbar()
        #how()

        im = plt.imshow(mySlice, cmap='hot')
        plt.colorbar(im, orientation='horizontal')
        plt.show()

        
        #rint("\nExamining at second: " + str( i) )
        #rint( mySlice )
        #rint("\n")
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

def updateFormicariumSlice(a,b, value = 10 ):
    global mySlice
    mySlice[a][b] = value + mySlice[a][b]
    return True

def randomDirection( ):
    x = random.randint(-1,1)
    y = random.randint(-1,1)
    #print(str( x) + " " + str(y) )

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

    cardinal = [ n, e, s, w]
    myDir = max( cardinal )

    if n == myDir:
        x = -1
        y = randomDirection()[0]
    elif e == myDir:
        y = -1
        x = randomDirection()[0]
    elif s == myDir:
        x = +1
        y = randomDirection()[0]
    elif w == myDir:
        y = +1
        x = randomDirection()[0]

    if x == 0 and y == 0:
        x,y = randomDirection()

    return x,y



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
        updateFormicariumSlice(a,b, 10)
    else:
        updateFormicariumSlice(a,b, 3 )
    return a,b


def antForagesFollowPath( a,b, antLife = 255 ):
    #Start = a,b
    #Anyt Life is 
    x,y = bestDirection(a,b)
    a = boundaryCheck( a + x )
    b = boundaryCheck( b + y )
    if checkLocation( a,b ):
        updateFormicariumSlice(a,b, 10)
    else:
        updateFormicariumSlice(a,b, 3 )
    return a,b
 

def createScoutingAnt( a,b, antLife = 255 ):
    currentA = a
    currentB = b
    while (antLife > 0):
        time.sleep(1)
        currentA,currentB = antForagesRandom( currentA,currentB )
        antLife = antLife - 1

    return True


def createForagingAnt( a,b, antLife = 255 ):
    currentA = a
    currentB = b
    while (antLife > 0):
        time.sleep(1)
        currentA,currentB = antForagesFollowPath( currentA,currentB )
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
    sliceThread.start()




    print("Slice created")
    maxScoutingAnts = 3
    antScoutThreadArray = []
    print("Start ant scouts: " )
    for i in range( 0, maxScoutingAnts ):
        print(str(i) + " Started" )
        antScoutThread = threading.Thread( target = createScoutingAnt, args = (a,b) )
        antScoutThread.start()
        antScoutThreadArray.append( antScoutThread )
        print(str(i) + " Done" )
   
    maxForagingAnts = 6
    antForageThreadArray = []
    print("Start ant forages: " )
    for i in range( 0, maxForagingAnts ):
        print(str(i) + " Started" )
        antForageThread = threading.Thread( target = createForagingAnt, args = (a,b) )
        antForageThread.start()
        antForageThreadArray.append( antForageThread )
        print(str(i) + " Done" )
   
    for ant in antScoutThreadArray:
            print("Joining scout ant " ) 
            ant.join()

    for ant in antForageThreadArray:
            print("Joining forage ant " ) 
            ant.join()

    sliceThread.join()


    






main()

