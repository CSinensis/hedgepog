import time
import math
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
from cmu_graphics import *

class projectVars():
    d = 1.75 #CENTIMETERS

def stepsToDist(steps):
    deg = steps*math.pi/100 #in radians
    return (projectVars.d/2)*deg #in centimeters

#input in CENTIMETERS
def distToSteps(dist):
    return int(dist*2/projectVars.d * 100/math.pi)

def initMotors():
    kit = MotorKit(i2c=board.I2C())
    kit.stepper1.release()
    kit.stepper2.release()
    return(kit.stepper1,kit.stepper2)


#TODO: CHECK IF DIRECTION OF MOTOR MOVEMENT CORRESPONDS PROPERLY W/LIMIT SWITCH STUFF
def inBounds(app,motor,stepDir):
    if (GPIO.input(app.xSwitch) == GPIO.HIGH and 
        motor == app.xMot and stepDir == 1):
        print("PAST X LIMIT")
        return False
    elif (GPIO.input(app.xSwitch) == GPIO.HIGH 
        and motor == app.yMot and stepDir == 1):
        print("PAST Y LIMIT")
        return False
    
    if motor == app.xMot:
        if 0 < app.x + app.stepD*stepDir < app.xMax:
            app.x += app.stepD*stepDir
        else:
            print("PAST X LIMIT - maybe")
            return False
    else:
        if 0 < app.y + app.stepD*stepDir < app.yMax:
            app.y += app.stepD*stepDir
        else:
            print("PAST Y LIMIT - maybe")
            return False

    return True

def step(app,motor,stepDir):
    if not inBounds(app,motor,stepDir): return

    motor.onestep(direction = stepper.FORWARD if stepDir == 1 else stepper.BACKWARD)

def moveXY(app,motor,direc,steps,t):
    stepTime = t/steps
    for i in range(steps):
        step(app,motor,direc)
        time.sleep(stepTime)

def moveDiag(app,dx,dy,t):
    xSteps,ySteps = distToSteps(abs(dx)),distToSteps(abs(dy))
    if xSteps == 0 or ySteps == 0: 
        if xSteps == 0 and ySteps != 0:
            moveXY(app,app.yMot,-1 if dy < 0 else 1,ySteps,t)
        elif ySteps == 0 and xSteps != 0:
            moveXY(app,app.xMot,-1 if dx < 0 else 1,xSteps,t)
        #print("NOPE (moveDiag)")
        return
    numSteps = math.lcm(xSteps,ySteps)
    #stepTime = t/numSteps #in seconds
    xRate,yRate = numSteps/xSteps,numSteps/ySteps
    xDir = -1 if dx < 0 else 1
    yDir = -1 if dy < 0 else 1
    for i in range(numSteps):
        print(i)
        if i%xRate == 0:
            step(app,app.xMot,xDir)
        if i%yRate == 0:
            step(app,app.yMot,yDir)
        #time.sleep(stepTime)

# def moveDiag(app,dx,dy,t):
#     xSteps,ySteps = distToSteps(abs(dx)),distToSteps(abs(dy))
#     numSteps = math.lcm(xSteps,ySteps)
#     stepTime = t/numSteps #in seconds
#     xRate,yRate = numSteps/xSteps,numSteps/ySteps
#     xDir = -1 if dx < 0 else 1
#     yDir = -1 if dy < 0 else 1
#     for i in range(numSteps):
#         if i%xRate == 0:
#             step(app,app.xMot,xDir)
#         if i%yRate == 0:
#             step(app,app.yMot,yDir)
#         time.sleep(stepTime)

#radius in CENTIMETERS
def circle(app,r):
    cx, cy = app.x - r , app.y
    prevX,prevY = None,None
    for deg in range(37):
        rad = math.pi*20*deg/360
        x = cx + math.cos(rad)*r
        y = cy + math.sin(rad)*r
        if prevX == None or prevY == None:
            prevX,prevY = x,y
            continue
        app.motionCommands.append((x - prevX,y-prevY,1/36))
        prevX, prevY = x,y
        #moveDiag(app,x-app.x,y-app.y,1/360)
    #app.hedgeMode = 'idle'

# def circle(app,r):
#     cx, cy = app.x - r , app.y
#     for deg in range(360):
#         rad = math.pi*2*deg/360
#         x = cx + math.cos(rad)*r
#         y = cy + math.sin(rad)*r
#         moveDiag(app,x-app.x,y-app.y,1/360)
#     app.hedgeMode = 'idle'

def lcm(x, y):
   # choose the greater number
   if x > y:
       greater = x
   else:
       greater = y

   while(True):
       if((greater % x == 0) and (greater % y == 0)):
           lcm = greater
           break
       greater += 1

   return lcm

def zigZag(app):
    pass


