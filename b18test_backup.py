from cmu_cs3_graphics import *
import random
import math
import time
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

class projectVars():
    d = 1.75 #CENTIMETERS

def stepsToDist(steps):
    deg = steps*math.pi/100 #in radians
    return (projectVars.d/2)*deg #in centimeters

#input in CENTIMETERS
def distToSteps(dist):
    return int(dist*2/projectVars.d * 100/math.pi)
    
class Button():
    def __init__(self,x,y,w,h,color,text,font):
        self.x,self.y,self.w,self.h,= x,y,w,h
        self.color,self.text,self.font = color,text,font
    
    def inBounds(self,mx,my):
        return ((self.x < mx < self.x + self.w)
            and self.y < my < self.y + self.h)
    
    def draw(self,app):
        drawRect(self.x,self.y,self.w,self.h,fill=self.color,border='black')
        drawLabel(self.text,self.x + self.w/2, self.y + self.h/2,font = self.font,size=20,bold=True)
    
def onAppStart(app):
    initViewVars(app)
    app.x = app.y = 40
    app.xMax = 100
    app.yMax = 100
    app.xMot = 'xmot'
    app.yMot = 'ymot'
    app.stepD = stepsToDist(1)
    app.hedgeMode = 'input'
    app.motionCommands = []
    app.stepsPerSecond = 1000

def onKeyHold(app,keys):
    if 'up' in keys and app.y + app.stepD < app.yMax:
        app.y += app.stepD
    elif 'down' in keys and app.y - app.stepD > 0:
        app.y -= app.stepD
    if 'right' in keys and app.x + app.stepD < app.xMax:
        app.x += app.stepD
    elif 'left' in keys and app.x - app.stepD > 0: 
        app.x -= app.stepD

def drawHedgehog(app):
    relX = 2*app.margin + app.x/app.xMax * app.boxW
    relY = 600 - 2*app.margin - app.y/app.yMax * app.boxH
    drawCircle(relX,relY,10,fill='red')

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
        print("NOPE (moveDiag)")
        return
    numSteps = lcm(xSteps,ySteps)
    stepTime = t/numSteps #in seconds
    xRate,yRate = numSteps/xSteps,numSteps/ySteps
    #print(numSteps)
    xDir = -1 if dx < 0 else 1
    yDir = -1 if dy < 0 else 1
    for i in range(numSteps):
        print(i)
        if i%xRate == 0:
            step(app,app.xMot,xDir)
        if i%yRate == 0:
            step(app,app.yMot,yDir)
        #print(numSteps,stepTime)
        #time.sleep(stepTime)

def inBounds(app,motor,stepDir):
    if motor == app.xMot:
        if 0 < app.x + app.stepD*stepDir < app.xMax:
            app.x += app.stepD*stepDir
        else:
            #print(app.x)
            #print("PAST X LIMIT - maybe")
            return False
    else:
        if 0 < app.y + app.stepD*stepDir < app.yMax:
            app.y += app.stepD*stepDir
        else:
            #print(app.y)
            #print("PAST Y LIMIT - maybe")
            return False

    return True
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
        
def step(app,motor,stepDir):
    if not inBounds(app,motor,stepDir): return
    #motor.onestep(direction = stepper.FORWARD if stepDir == 1 else stepper.BACKWARD)

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
        

def initViewVars(app):
    app.margin = 20
    app.font = 'Courier New'
    
    width,height = 800,600
    
    app.w, app.h = width - 2*app.margin, height - 2*app.margin
    app.boxX = app.margin
    app.boxY = app.margin + 0.2*app.h
    app.boxW = app.w*3/4
    app.boxH = app.h*4/5
    
    app.butX = app.boxX + app.boxW + app.margin
    app.butW = width-app.margin-app.butX
    app.butH = 50
    print(app.boxY)
    
    app.b1 = Button(app.butX,app.boxY,app.butW,app.butH,
            'lightBlue','Go Home',app.font)
    app.b2 = Button(app.butX,app.boxY+2*app.butH,app.butW,app.butH,
            'lightBlue','Feed',app.font)
    app.b3 = Button(app.butX,app.boxY+4*app.butH,app.butW,app.butH,
            'lightBlue','Dance',app.font)
    
def drawStatus(app):
    drawRect(app.w/2,-2,800-app.w/2+2,app.boxY-app.margin+2,
        fill=None,border='black',dashes=True)

    drawImage('https://www.simpleimageresizer.com/_uploads/photos/3bcc4a0a/fotor_2023-1-21_0_40_3_1_90.png',
    app.w/2+app.margin/2,5)
    drawCircle(app.w/2 + app.margin/2 + 48,5+48,48,fill=None,border='black',borderWidth=2)
    
def redrawAll(app):
    drawRect(app.boxX,app.boxY,app.boxW,app.boxH,fill=None,border='black')
    drawLabel('HedgePog',app.margin,app.margin,
        align = 'left-top',font=app.font,size = 70)
    drawLabel('Did you hedge your pogs today (sorry its late)',
        app.margin,app.margin+70,align='left-top',font=app.font,size=12)
    drawStatus(app)
    app.b1.draw(app)
    app.b2.draw(app)
    app.b3.draw(app)
    drawHedgehog(app)
    
    pass

def main():
    runApp(width=800,height=600)


main()