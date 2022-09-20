import pygame
from pygame.locals import *

from main import *

class Point():
   """Defines a point that can be drawn onto the screen, as well as dragged upon mouse click"""
   
   # Essentially creates a circular hitbox around the point, a certain factor larger than the point itself. 
   # Makes it much easier to click, especially when points are small.
   selectRadiusModifier = 1.5

   def __init__(self, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2, color=(255,255,255), radius=5):
      self.x = x
      self.y = y
      self.color = color

      self.clicked = False
      
      self.radius = radius
      self.selectRadius = self.radius * Point.selectRadiusModifier
      
      self.rect = pygame.Rect(self.x-self.selectRadius, self.y-self.selectRadius, self.selectRadius*2, self.selectRadius*2)

   def handle_event(self, event):
      """Checks whether the point is clicked, and moves the point if clicked"""
      if event.type == pygame.MOUSEBUTTONDOWN: # If clicked, set clicked to true
         if self.rect.collidepoint(event.pos):
            self.clicked = True
      if event.type == pygame.MOUSEBUTTONUP and self.clicked == True: # If mouse unclicked and this point was clicked, set clicked to false
         self.clicked = False
      if event.type == pygame.MOUSEMOTION and self.clicked == True: # If clicked and mouse is dragged, move point to mouse
         self.x=event.pos[0]
         self.y=event.pos[1]
         self.rect = pygame.Rect(self.x-self.selectRadius, self.y-self.selectRadius, self.selectRadius*2, self.selectRadius*2)
   
   def draw(self, screen):
      """Draws the point"""
      pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class BoundaryPoint(Point):
   """A Point that can only be moved within a specific bounding box. Is useful for creating Sliders"""
   def __init__(self,x=1,y=1,color=(255,255,255),radius=5,minX=0,maxX=SCREEN_WIDTH,minY=0,maxY=SCREEN_HEIGHT):
      super(BoundaryPoint, self).__init__(x,y,color,radius)
      self.minX = minX
      self.maxX = maxX
      self.minY = minY
      self.maxY = maxY
   
   def handle_event(self, event):
      """Moves like a normal point, but clamps x and y between the defined min and max values"""
      super(BoundaryPoint, self).handle_event(event)
      self.x = max(min(self.x, self.maxX), self.minX)
      self.y = max(min(self.y, self.maxY), self.minY)
      self.rect = pygame.Rect(self.x-self.selectRadius, self.y-self.selectRadius, self.selectRadius*2, self.selectRadius*2)
