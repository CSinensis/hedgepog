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

def initLimitSwitches(app):
    app.xSwitch = 1
    app.ySwitch = 2
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(app.xSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(app.ySwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
    app.stepsPerSecond = 100

def setPos(app):
    app.x = app.y = 0

def setMax(app):
    app.xMax = app.x
    app.yMax = app.y

def onKeyPress(app,key):
    if key == 'z':
        setPos(app)
        print("LOCATION ZEROED")
    elif key == 'm':
        setMax(app)
        print("MAX LOCATION SET")
    elif key == 'i':
        app.hedgeMode = 'idle'
    elif key == 'c':
        app.hedgeMode = 'circle'
        print("circlemode")
        circle(app,10)

#NOTE: 0,0 is at the BOTTOM LEFT
def onKeyHold(app,keys):
    if app.mode != 'input': return 
    if 'up' in keys and app.y + app.stepD < app.yMax:
        step(app,app.motY,1)
    elif 'down' in keys and app.y - app.stepD > 0:
        step(app,app.motY,-1)
    if 'right' in keys and app.x + app.stepD < app.xMax:
        step(app,app.motX,1)
    elif 'left' in keys and app.x - app.stepD > 0: 
        step(app,app.motX,-1)

def distance(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def generateNextPoint(app):
    x = random.randrange(max(0,int(app.x-20)),min(app.xMax,int(app.x+20)),5)
    y = random.randrange(max(0,int(app.y-20)),min(app.yMax,int(app.y+20)),5)
    totalT = random.randrange(10,50)/10
    steps = math.ceil(distance(x,y,app.x,app.y))
    dx, dy, timeStep = (x-app.x)/steps, (y-app.y)/steps, totalT/steps
    app.motionCommands += [(dx,dy,timeStep)]*steps


def onStep(app):
    # if app.hedgeMode == 'idle':
    #     app.hedgeMode = 'moving'
    #     x,y = random.randint(1,10),random.randint(1,10)
    #     print(x,y,app.x,app.y,'hi')
    #     moveDiag(app, x-app.x, y-app.y,1)
    if len(app.motionCommands) > 0:
        dx,dy,t = app.motionCommands.pop(0)
        moveDiag(app,dx,dy,t)
    elif app.hedgeMode == 'idle':
        generateNextPoint(app)
    
def redrawAll(app):
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
