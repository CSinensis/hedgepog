from cmu_graphics import *
import time
import math
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

d = 1.75 #CENTIMETERS

kit = MotorKit(i2c=board.I2C())
kit.stepper1.release()
kit.stepper2.release()

xMot = kit.stepper1
yMot = kit.stepper2

def stepsToDist(steps):
    deg = steps*math.pi/100 #in radians
    return (d/2)*deg #in centimeters

#input in CENTIMETERS
def distToSteps(dist):
    return int(dist*2/d * 100/math.pi)

#moves smoothly? along dx,dy (CM) over time==t (s)
def moveDiag(dx,dy,t):
    xSteps,ySteps = distToSteps(abs(dx)),distToSteps(abs(dy))
    numSteps = math.lcm(xSteps,ySteps)
    stepTime = t/numSteps #in seconds
    xRate,yRate = numSteps/xSteps,numSteps/ySteps
    for i in range(numSteps):
        if i%xRate == 0:
            xDir = stepper.BACKWARD if dx < 0 else stepper.FORWARD
            xMot.onestep(direction = xDir)
        if i%yRate == 0:
            yDir = stepper.BACKWARD if dy < 0 else stepper.FORWARD
            yMot.onestep(direction = yDir)
        time.sleep(stepTime)

def onAppStart(app):
    
    

def main():
    runApp(width=800,height=800)
    
if __name__=='__main__':
    main()