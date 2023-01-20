
# Below imports all neccessary packages to make this Python Script run
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