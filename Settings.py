import pygame
from pygame.locals import *

from main import *
from Buttons import *
from Slider import *
from Texts import *

class Settings():
   backgroundColor = settingsColor
   panelWidth = SETTINGS_WIDTH
   
   buttons = []
   texts = []
   textBoxes = []
   
   curve = True
   points = True
   primaryLines = False
   otherLines = False
   
   curveWidth = 1
   pointRadius = 5
   primaryLineWidth = 2
   otherLineWidth = 1
   
   percent = .5
   
   animationFrozen = False
   animationPercent = 0
   animationStep = .01
   pointBefore = .5
   
   animFullCurve = True
   drawFullCurve = True
   
   maxInt = 200
   
   @staticmethod
   def startup():
      Settings.buttons.append(NewPointButton(x=SCREEN_WIDTH+Settings.panelWidth/2-75, y=20, w=150, text = "New Point"))
      Settings.buttons.append(RemovePointButton(x=SCREEN_WIDTH+Settings.panelWidth/2-75, y=50, w=150, text = "Remove Point"))
      
      Settings.buttons.append(ToggleButton(y = 90, text="Bezier Curve", initialValue=Settings.curve))
      Settings.buttons.append(ToggleButton(y = 120, text="Points", initialValue=Settings.points))
      Settings.buttons.append(ToggleButton(y = 150, text="Primary Lines", initialValue=Settings.primaryLines))
      Settings.buttons.append(ToggleButton(y = 180, text="Other Lines", initialValue=Settings.otherLines))
      
      
      Settings.texts.append(Text(y=90, text="Width: "))
      Settings.texts.append(Text(y=120, text="Radius: "))
      Settings.texts.append(Text(y=150, text="Width: "))
      Settings.texts.append(Text(y=180, text="Width: "))
      
      Settings.textBoxes.append(TextBox(y = 90, text=str(Settings.curveWidth)))
      Settings.textBoxes.append(TextBox(y = 120, text=str(Settings.pointRadius)))
      Settings.textBoxes.append(TextBox(y = 150, text=str(Settings.primaryLineWidth)))
      Settings.textBoxes.append(TextBox(y = 180, text=str(Settings.otherLineWidth)))
      
      
      Settings.buttons.append(Slider(x=SCREEN_WIDTH+20, y=230, w=Settings.panelWidth-40, h=2))
      Settings.buttons.append(AnimateLineButton(x=SCREEN_WIDTH+Settings.panelWidth/2-75, y=255, w=150, text = "Animate Curve"))
      Settings.buttons.append(ToggleButton(x=SCREEN_WIDTH+10, y = 300, text="Animate Full Curve", initialValue=Settings.animFullCurve))
      Settings.buttons.append(ToggleButton(x=SCREEN_WIDTH+Settings.panelWidth/2+10, y = 300, text="Draw Full Curve", initialValue=Settings.drawFullCurve))

   @staticmethod
   def handle_event(event):
      if not Settings.animationFrozen:
         for button in Settings.buttons:
            button.handle_event(event)
         for box in Settings.textBoxes:
            box.handle_event(event)
      else:
         Settings.buttons[7].handle_event(event)
   
   @staticmethod
   def update():
      if Settings.animationFrozen:
         if Settings.animationPercent == 0:
            Settings.pointBefore = Settings.buttons[6].value
         Settings.buttons[6].setValue(Settings.animationPercent)
         Settings.animationPercent += Settings.animationStep
         if Settings.animationPercent > 1:
            Settings.buttons[6].setValue(Settings.pointBefore)
            Settings.animationPercent = 0
            Settings.animationFrozen = False
            Settings.buttons[7].setText(Settings.buttons[7].defaultText)
      else:
         Settings.animationPercent = 0
      
      for button in Settings.buttons:
         button.update()
   
   @staticmethod
   def draw(screen):
      pygame.draw.rect(screen, Settings.backgroundColor, (SCREEN_WIDTH, 0, Settings.panelWidth, SCREEN_HEIGHT), 0)
      for button in Settings.buttons:
         button.draw(screen)
      for box in Settings.textBoxes:
         box.draw(screen)
      for text in Settings.texts:
         text.draw(screen)
      
   @staticmethod
   def writeInfo():
      Settings.curve = Settings.buttons[2].on
      Settings.points = Settings.buttons[3].on
      Settings.primaryLines = Settings.buttons[4].on
      Settings.otherLines = Settings.buttons[5].on
      Settings.percent = Settings.buttons[6].value
      
      try:
         Settings.curveWidth = int(Settings.textBoxes[0].text)
         Settings.curveWidth = min(Settings.curveWidth, Settings.maxInt)
      except:
         pass
      try:
         Settings.pointRadius = int(Settings.textBoxes[1].text)
         Settings.pointRadius = min(Settings.pointRadius, Settings.maxInt)
      except:
         pass
      try:
         Settings.primaryLineWidth = int(Settings.textBoxes[2].text)
         Settings.primaryLineWidth = min(Settings.primaryLineWidth, Settings.maxInt)
      except:
         pass
      try:
         Settings.otherLineWidth = int(Settings.textBoxes[3].text)
         Settings.otherLineWidth = min(Settings.otherLineWidth, Settings.maxInt)
      except:
         pass
      
      Settings.animFullCurve = Settings.buttons[8].on
      Settings.drawFullCurve = Settings.buttons[9].on