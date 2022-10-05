import pygame
from pygame.locals import *
pygame.font.init()

from main import *
from Curve import BezierCurve
from Points import *

class ButtonBase():
   """This is button with no update methods. Stores some things needed for updating based on pygame events, but doesn't use them in this class."""
   # Does not update on hover because the ButtonBase can be used as a nice way to display static text
   # Stores position, text, width, height, some color infromation, and the textLayer that pygame can render
   
   offColor = (50,100,100)
   hoverColor = (100,50,50)
   onColor = (200,100,100)
   
   font = pygame.font.SysFont('Arial', 15)
   
   def __init__(self, x=SCREEN_WIDTH+20, y=20, text="Null", w=130, h=20, offC=offColor, hC=hoverColor, onC=onColor, initialValue=False):
      self.x = x
      self.y = y
      self.text = text
      self.defaultText = self.text
      
      self.width = w
      self.height = h
      
      self.offColor = offC
      self.hoverColor = hC
      self.onColor = onC
      
      self.currentColor = self.offColor
      
      self.on = initialValue
      self.currentColor = self.onColor if self.on else self.offColor

      self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

      self.textLayer = ButtonBase.font.render(self.text, False, (0, 0, 0))
      self.textCoord = self.textLayer.get_rect(center = (self.x+self.width/2, self.y + self.height/2))
      
   def update(self):
      pass
   
   def setText(self, text):
      self.text = text
      self.textLayer = ButtonBase.font.render(self.text, False, (0, 0, 0))
   
   def draw(self, screen):
      pygame.draw.rect(screen, self.currentColor, (self.x, self.y, self.width, self.height), 0)
      screen.blit(self.textLayer,self.textCoord)

class ToggleButton(ButtonBase):
   offColor = (50,100,100)
   hoverColor = (100,50,50)
   onColor = (200,100,100)
   
   def __init__(self, x=SCREEN_WIDTH+20, y=20, text="Null", w=130, h=20, offC=offColor, hC=hoverColor, onC=onColor, initialValue=False):
      super(ToggleButton, self).__init__(x,y,text,w,h,offC=offC, hC=hC, onC=onC, initialValue=initialValue)
      
   def handle_event(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos): # When mouse clicks on the button
         # Toggle on/off and set color
         self.on = not self.on
         if self.on:
            self.currentColor = self.onColor
         else:
            self.currentColor = self.offColor
      if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP) and self.on == False:
         if self.rect.collidepoint(event.pos):
            self.currentColor = self.hoverColor
         else:
            self.currentColor = self.offColor

class ClickerButton(ButtonBase):
   offColor = (50,100,100)
   hoverColor = (100,50,50)
   onColor = (200,100,100)
   
   maxCool = 2

   def __init__(self, x=SCREEN_WIDTH+20, y=20, text="Null", w=130, h=20, offC=offColor, hC=hoverColor, onC=onColor, initialValue=True):
      super(ClickerButton, self).__init__(x,y,text,w,h,offC=offC, hC=hC, onC=onC, initialValue=initialValue)
      self.cooldown = 0
   
   def handle_event(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
         if self.on:
            self.on = False
            self.currentColor = self.offColor
            self.cooldown = ClickerButton.maxCool
            self.onClick()
   
   def update(self):
      if self.cooldown > 0:
         self.cooldown -= 1
      else:
         self.on = True
         self.currentColor = self.onColor
   
   def onClick(self):
      pass
         
class NewPointButton(ClickerButton):
   """Creates a new point for the active curve"""
   def onClick(self):
      BezierCurve.mainCurve.points.append(BoundaryPoint(BezierCurve.mainCurve.x, BezierCurve.mainCurve.y))

class RemovePointButton(ClickerButton):
   """Removes the end point of the active curve"""
   def onClick(self):
      if len(BezierCurve.mainCurve.points) > 1:
         BezierCurve.mainCurve.points.pop()

class AnimateLineButton(ClickerButton):
   """Runs the animation of the line"""
   def onClick(self):
      from Settings import Settings
      if not Settings.animationFrozen:
         Settings.animationFrozen = True
         self.setText("Stop Animation")
      else:
         Settings.animationFrozen = False
         self.setText(self.defaultText)

class NewCurveButton(ClickerButton):
   """Creates a new point for the active curve"""
   def onClick(self):
      BezierCurve.mainCurve = BezierCurve()

class RemoveCurveButton(ClickerButton):
   """Creates a new point for the active curve"""
   def onClick(self):
      BezierCurve.allCurves.remove(BezierCurve.mainCurve)
      if len(BezierCurve.allCurves) > 0:
         BezierCurve.mainCurve = BezierCurve.allCurves[0]

