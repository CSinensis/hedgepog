import time
import math
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

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


