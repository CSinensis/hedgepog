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