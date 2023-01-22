from cmu_graphics import *

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

class status():
    def __init__(self,label,x,y,w,h,rate,text):
        self.label = label
        self.x,self.y,self.w,self.h = x,y,w,h
        self.value = 1
        self.rate = rate
        self.messages = []
        self.text = text
    
    def show(self):
        drawLabel(f'{self.label}',self.x,self.y,align='left-top',size=18)
        drawRect(self.x,self.y + self.h/2,self.w*self.value,self.h/2,fill = self.getColor())
        drawRect(self.x,self.y + self.h/2,self.w,self.h/2,fill = None,border='black')
    
    def getColor(self):
        if self.value > 0.75:
            return 'lightGreen'
        elif self.value > 0.25:
            return 'khaki'
        else:
            return 'darkRed'
    
    def inc(self):
        if self.value <= 0.9:
            self.value += 0.1
        else: self.value = 1

    def dec(self):
        if self.value > self.rate+0.01:
            self.value -= self.rate
    
    def getMessage(self):
        if self.value > 0.5:
            return self.messages[0]
        elif self.value > 0.25:
            return self.messages[1]
        else:
            return self.messages[2]

    @staticmethod
    def mostUrgent(s1,s2,s3):
        minVal = min(s1.value,s2.value,s3.value)
        if minVal > 0.75: return None

        if s1.value == minVal:
            return s1
        elif s2.value == minVal:
            return s2
        else:
            return s3

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
    #print(app.boxY)
    
    app.b1 = Button(app.butX,app.boxY,app.butW,app.butH,
            'lightBlue','Go Home',app.font)
    app.b2 = Button(app.butX,app.boxY+2*app.butH,app.butW,app.butH,
            'lightBlue','Feed',app.font)
    app.b3 = Button(app.butX,app.boxY+4*app.butH,app.butW,app.butH,
            'lightBlue','Dance',app.font)

def drawStatus(app):
    drawRect(app.w/2,-2,800-app.w/2+2,app.boxY-app.margin+2,
        fill=None,border='black',dashes=True)
    #https://www.simpleimageresizer.com/_uploads/photos/3bcc4a0a/fotor_2023-1-21_0_40_3_1_90.png
    drawImage('hedgepogIcon.png',app.w/2+app.margin/2,5)
    drawCircle(app.w/2 + app.margin/2 + 48,5+48,48,fill=None,border='black',borderWidth=2)

def drawButtons(app):
    app.b1.draw(app)
    app.b2.draw(app)
    app.b3.draw(app)

def drawHedgehog(app):
    relX = 2*app.margin + app.x/app.xMax * (app.boxW-2*app.margin)
    relY = 600 - 2*app.margin - app.y/app.yMax * (app.boxH-2*app.margin)
    drawCircle(relX,relY,10,fill='red')


def initBehaviorVars(app):
    app.toIncrease = None
    app.feeding = False
    app.hedgeStatus = 'Alive (for now)'
    app.energy = status('Energy',app.butX,app.statY,app.butW,app.statH/3,0.00005,'Tired')
    app.energy.messages = ['Feeling a bit tired', 'Wanna go home','let me sleep please']
    app.hunger = status('Hunger',app.butX,app.statY+app.statH/3+app.margin,app.butW,app.statH/3,0.0001,'Hungry')
    app.hunger.messages = ['Feeling a bit hungry', 'Can I has food?','FEEEEEEEEED MEEEE']
    app.mood = status('Mood',app.butX,app.statY+2*app.statH/3+2*app.margin,app.butW,app.statH/3,0.0002,'Bored')
    app.mood.messages = ["I'm bored! Entertain me!","*sighs* you're no fun","ugh I might play league or something"]
    app.hedgeMessage = "Hello!!!!!!"
    app.houseX = 2
    app.houseY = 28
    app.foodX = 10
    app.foodY = 10

def drawStatus(app):
    drawRect(app.w/2,-2,800-app.w/2+2,app.boxY-app.margin+2,
        fill=None,border='black',dashes=True)
    drawImage('hedgepogIcon.png',app.w/2+app.margin/2,5)
    drawCircle(app.w/2 + app.margin/2 + 48,5+48,48,fill=None,border='black',borderWidth=2)
    drawLabel(f'Status: {app.hedgeStatus}',app.w/2 + app.margin + 2*48,app.margin,align = 'left-top',size=25)
    drawRect(app.butX,app.statY,app.butW,app.statH,fill=None)
    drawLabel(f'HedgePog Says:',app.w/2 + app.margin + 2*48,app.statH/2-app.margin,align='left-top',size=15)
    drawLabel(f'{app.hedgeMessage}',app.w/2 + app.margin + 2*48,app.statH/2,align='left-top',size=15)
    app.energy.show()
    app.hunger.show()
    app.mood.show()