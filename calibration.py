import time
import math
import board
import random
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
from dependencies import *
from cmu_graphics import *

def onAppStart(app):
    app.xMot,app.yMot = initMotors()
    app.x = app.y = 0
    app.xMax = 100
    app.yMax = 100
    app.stepD = stepsToDist(1)
    app.hedgeMode = 'input'

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

def step(app,motor,stepDir):
    motor.onestep(direction = stepper.FORWARD if stepDir == 1 else stepper.BACKWARD)
    if motor == app.xMot:
        app.x += app.stepD*stepDir
    else:
        app.y += app.stepD*stepDir

def moveDiag(app,dx,dy,t):
    xSteps,ySteps = distToSteps(abs(dx)),distToSteps(abs(dy))
    numSteps = math.lcm(xSteps,ySteps)
    stepTime = t/numSteps #in seconds
    xRate,yRate = numSteps/xSteps,numSteps/ySteps
    #print(xSteps,ySteps,stepTime)
    xDir = -1 if dx < 0 else 1
    yDir = -1 if dy < 0 else 1
    for i in range(numSteps):
        if i%xRate == 0:
            step(app,app.xMot,xDir)
        if i%yRate == 0:
            step(app,app.yMot,yDir)
        time.sleep(stepTime)

#radius in CENTIMETERS
def circle(app,r):
    cx, cy = app.x - r , app.y
    for deg in range(360):
        rad = math.pi*2*deg/360
        x = cx + math.cos(rad)*r
        y = cy + math.sin(rad)*r
        moveDiag(app,x-app.x,y-app.y,1/360)

def zigZag(app):
    pass

def onStep(app):
    if app.hedgeMode == 'idle':
        x,y = random.randint(0,app.xMax),(0,app.yMax)
        




def redrawAll(app):

    pass

def main():
    runApp(width=800,height=800)

if __name__ == '__main__':
    main()







kit = MotorKit(i2c=board.I2C())

kit.stepper1.release()
kit.stepper2.release()

xMot = kit.stepper1
yMot = kit.stepper2 


#moves smoothly? along dx,dy (CM) over time==t (s)
def moveDiag(dx,dy,t):
    xSteps,ySteps = distToSteps(abs(dx)),distToSteps(abs(dy))
    numSteps = math.lcm(xSteps,ySteps)
    stepTime = t/numSteps #in seconds
    xRate,yRate = numSteps/xSteps,numSteps/ySteps
    print(xSteps,ySteps,stepTime)

    for i in range(numSteps):
        if i%xRate == 0:
            xDir = stepper.BACKWARD if dx < 0 else stepper.FORWARD
            xMot.onestep(direction = xDir)
        if i%yRate == 0:
            yDir = stepper.BACKWARD if dy < 0 else stepper.FORWARD
            yMot.onestep(direction = yDir)
        time.sleep(stepTime)

def singleStepTest():
    print("SINGLE STEP TEST\n")
    while True:
        try:
            dir = input("direction: ")
            if dir == 'a':
                xMot.onestep(direction = stepper.BACKWARD)
            elif dir == 'd':
                xMot.onestep()
            elif dir == 'w':
                yMot.onestep()
            elif dir == 's':
                yMot.onestep(direction = stepper.BACKWARD)
            else:
                break
        except Exception as e:
            print(e)
            kit.stepper1.release()
            kit.stepper2.release()
            break
    kit.stepper1.release()
    kit.stepper2.release()

def moveXY(motor,direc,steps):
    for i in range(steps):
        motor.onestep(direction = direc)
        #time.sleep(0.05)

def multStepTest():
    print("MULTI STEP TEST\n")
    while True:
        try:
            dir = input("direction: ")
            numSteps = int(input("number of steps: "))
            if dir == 'a':
                moveXY(xMot,stepper.BACKWARD,numSteps)
            elif dir == 'd':
                moveXY(xMot,stepper.FORWARD,numSteps)
            elif dir == 'w':
                moveXY(yMot,stepper.FORWARD,numSteps)
            elif dir == 's':
                moveXY(yMot,stepper.BACKWARD,numSteps)
            else:
                break
        except Exception as e:
            print(e)
            kit.stepper1.release()
            kit.stepper2.release()
            break
    kit.stepper1.release()
    kit.stepper2.release()

def diagMoveTest():
    while True:
        try:
            dx = int(input("direction x: "))
            dy = int(input("direction y: "))
            t = int(input("time: "))
            moveDiag(dx,dy,t)
        except Exception as e:
            print(e)
            kit.stepper1.release()
            kit.stepper2.release()
            break
    kit.stepper1.release()
    kit.stepper2.release()

#NOTE ONLY DO 'Y' MOTION FOR NOW (w/s keys) bc that corresponds to the thing on top
def main():
    #singleStepTest()
    #multStepTest()
    diagMoveTest()

            
        
    
if __name__ == '__main__':
    main()