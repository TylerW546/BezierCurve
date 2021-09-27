import pygame
from pygame.locals import *

from Texts import *
from Points import *

class Slider():
   pointColor = (100,200,100)
   lineColor = (255,255,255)
   font = pygame.font.SysFont('Arial', 10)
   
   def __init__(self,x=20,y=20,w=100,h=2,pR=4,pointC=pointColor,lineC=lineColor,min=0,max=1,subdivisions=3):
      self.x = x
      self.y = y
      self.width = w
      self.height = h
      
      self.pointRadius = pR
      self.pointColor = pointC
      self.lineColor = lineC
      
      self.value = .5
      
      self.min = min
      self.max = max
      self.subdivisions = subdivisions
      
      self.point = BoundaryPoint(self.x+self.width/2,self.y+self.height/2,self.pointColor,self.pointRadius,minX=self.x,maxX=self.x+self.width,minY=self.y+.5*self.height,maxY=self.y+.5*self.height)
   
   def handle_event(self, event):
      self.point.handle_event(event)
   
   def update(self):
      percent = (self.point.x-self.x)/self.width
      self.value = self.min+percent*(self.max-self.min)
   
   def setValue(self,value):
      self.value = value
      self.point.x = self.x + self.width*value
   
   def drawSub(self, screen, percent):
      pygame.draw.rect(screen, self.lineColor, (self.x+percent*self.width,self.y-self.height,self.height,self.height*3), 0)
   
   def textSub(self, screen, percent):
      textLayer = Slider.font.render(str(self.min+percent*(self.max-self.min)), False, (0, 0, 0))
      textCoord = textLayer.get_rect(center = (self.x+percent*self.width,self.y+2*self.height))
      textCoord.y = self.y+5
      screen.blit(textLayer,textCoord)
   
   def draw(self, screen):
      pygame.draw.rect(screen, self.lineColor, (self.x, self.y, self.width, self.height), 0)
      for i in range(0,1001,1000//(self.subdivisions+1)):
         self.drawSub(screen, i/1000)
         self.textSub(screen, i/1000)
      self.point.draw(screen)
      