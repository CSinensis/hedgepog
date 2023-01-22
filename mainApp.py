import time
import math
import board
import random
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
#NOTE: INSTALL THIS FIRST 
import RPi.GPIO as GPIO
from controlsHeader import *
from graphicsHeader import *
from cmu_graphics import *

#TODO: create app level representation of map obstacles
# split into grid, pathfind from start/finish while avoiding obstacles
# grab lines 
def testLimitSwitches(app):
    if (GPIO.input(app.xSwitchMax) == GPIO.HIGH or
        GPIO.input(app.xSwitchMin) == GPIO.HIGH or
        GPIO.input(app.ySwitchMax) == GPIO.HIGH or
        GPIO.input(app.ySwitchMin) == GPIO.HIGH):
        print(GPIO.input(app.xSwitchMax),GPIO.input(app.xSwitchMin),GPIO.input(app.ySwitchMax),GPIO.input(app.ySwitchMin))

def initLimitSwitches(app):
    app.xSwitchMin=  23 #23
    app.ySwitchMin = 25 #25
    app.xSwitchMax = 24 #24
    app.ySwitchMax = 22 #22
    GPIO.setmode(GPIO.BCM) # Use physical pin numbering
    GPIO.setup(app.xSwitchMin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(app.ySwitchMin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(app.xSwitchMax, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(app.ySwitchMax, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def onAppStart(app):
    initViewVars(app)
    app.xMot,app.yMot = initMotors()
    initLimitSwitches(app)

    app.x = app.y = 0
    app.xMax = 100
    app.yMax = 100
    app.stepD = stepsToDist(1)
    app.hedgeMode = 'input'
    app.motionCommands = []
    app.stepsPerSecond = 50
    app.move = False
    app.prevTime = None
    app.cycle = 0
    app.houseX = 2
    app.houseY = 28

def setPos(app):
    app.x = app.y = 0

def setMax(app):
    app.xMax = app.x
    app.yMax = app.y

def onMousePress(app,mouseX,mouseY):
    if ((2*app.margin < mouseX < app.boxW) and
        app.boxY + app.margin < mouseY < app.boxY + app.boxH - app.margin):
        x = app.xMax*(mouseX - app.margin)/(app.boxW - 2*app.margin)
        y = app.yMax*(600 - mouseY - app.margin)/(app.boxH - 2*app.margin)
        print(x,y)
        print(x - app.x,y - app.y)
        moveDiag(app,x - app.x,y - app.y,2)
    elif app.b1.inBounds(mouseX,mouseY):
        goHome(app)
        
        
def zero(app):
    app.x, app.y = 50,50
    while GPIO.input(app.xSwitchMin) != GPIO.HIGH:
        moveXY(app,app.xMot,-1,50,2)
    while GPIO.input(app.ySwitchMin) != GPIO.HIGH:
        moveXY(app,app.yMot,-1,50,2)
    setPos(app)
    print(app.x,app.y)

def goHome(app):
    moveDiag(app,app.houseX - app.x,app.houseY - app.y,2)
    
def getMaxBounds(app):
    while GPIO.input(app.xSwitchMax) != GPIO.HIGH:
        moveXY(app,app.xMot,1,50,2)
    while GPIO.input(app.ySwitchMax) != GPIO.HIGH:
        moveXY(app,app.yMot,1,50,2)
    setMax(app)
    print(app.xMax,app.yMax)

def onKeyPress(app,key):
    if key == 'z':
        zero(app)
        print("LOCATION ZEROED")
    elif key == 'm':
        getMaxBounds(app)
        print("MAX LOCATION SET")
    elif key == 'i':
        app.hedgeMode = 'idle'
    elif key == 'c':
        app.hedgeMode = 'circle'
        print("circlemode")
        circle(app,5)
    elif key == 'r':
        releaseMotors(app)
    '''
    elif key == 'w':
        app.move = not app.move
        pass
    '''


def onKeyRelease(app,key):
    return
    if key == 'w':
        app.move= not app.move


#NOTE: 0,0 is at the BOTTOM LEFT
def onKeyHold(app,keys):
    #print(keys)
    #if app.hedgeMode != 'input': return 
    if 'w' in keys and app.y + app.stepD < app.yMax:
        #print(app.y)
        app.motionCommands.append((0,1.5,0.4))

        #step(app,app.yMot,1)
    elif 's' in keys and app.y - app.stepD > 0:
        #step(app,app.yMot,-1)
        app.motionCommands.append((0,-0.5,0.4))
    if 'd' in keys and app.x + app.stepD < app.xMax:
        app.motionCommands.append((1.5,0,0.4))
    elif 'a' in keys and app.x - app.stepD > 0: 
        app.motionCommands.append((-1.50,0,0.4))

def distance(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def generateNextPoint(app):
    x = randrange(max(0,int(app.x-20)),min(int(app.xMax),int(app.x+20)),5)
    y = randrange(max(0,int(app.y-20)),min(int(app.yMax),int(app.y+20)),5)
    totalT = randrange(10,50)/10
    smoothLine(app,x,y,totalT)

def smoothLine(app,x,y,totalT):
    steps = math.ceil(distance(x,y,app.x,app.y))
    dx, dy, timeStep = (x-app.x)/steps, (y-app.y)/steps, totalT/steps
    app.motionCommands += [(dx,dy,timeStep)]*steps


def onStep(app):
    app.cycle += 1
    # if app.hedgeMode == 'idle':
    #     app.hedgeMode = 'moving'
    #     x,y = random.randint(1,10),random.randint(1,10)
    #     print(x,y,app.x,app.y,'hi')
    #     moveDiag(app, x-app.x, y-app.y,1)
    #testLimitSwitches(app)
    #print(app.motionCommands)
    if app.prevTime == None:
        app.prevTime = time.time()
        return
    if app.move:
        step(app,app.yMot,1)
    if len(app.motionCommands) > 0:
        #print(app.motionCommands)
        dx,dy,t = app.motionCommands.pop(0)
        moveDiag(app,dx,dy,t)
    elif app.hedgeMode == 'idle':
        generateNextPoint(app)
    nT = time.time()
    #print(nT - app.prevTime)
    app.prevTime = nT
    
def redrawAll(app):
    #if app.cycle % 10 != 0:
     #   return

    drawRect(app.boxX,app.boxY,app.boxW,app.boxH,fill=None,border='black')
    drawLabel('HedgePog',app.margin,app.margin,
        align = 'left-top',font=app.font,size = 70)
    drawLabel('Did you hedge your pogs today (sorry /./)',
        app.margin,app.margin+70,align='left-top',font=app.font,size=12)
    drawStatus(app)
    drawButtons(app)
    drawHedgehog(app)


def main():
    runApp(width=800,height=600)

if __name__ == '__main__':
    main()
