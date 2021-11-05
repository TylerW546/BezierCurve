import math
import pygame
from pygame.locals import *
import random
import time

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SETTINGS_WIDTH = 300
settingsColor = (100,100,200)

white = (255, 255, 255)
black = (0,0,0)
red = (255,0,0)
blue = (0, 0, 255)
background = (30,30,40)

pygame.font.init()
myfont = pygame.font.SysFont('Times New Roman', 20)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + SETTINGS_WIDTH, SCREEN_HEIGHT))

def main():
    
    from Settings import Settings
    from Curve import BezierCurve
    
    Settings.startup()
    BezierCurve.mainCurve = BezierCurve()
    BezierCurve(20,20)

    while (True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            Settings.handle_event(event)
            for curve in BezierCurve.allCurves:
                curve.handle_event(event)
                
        screen.fill(background)

        Settings.update()
        Settings.draw(screen)
        Settings.writeInfo()
        
        for curve in BezierCurve.allCurves:
            if Settings.primaryLines:
                curve.drawPrimaryLines(screen, Settings.primaryLineWidth)
            if Settings.curve:
               if not Settings.animationFrozen:
                  if Settings.drawFullCurve:
                     curve.drawCurve(screen, Settings.curveWidth)
                  else:
                     curve.drawCurveUntil(screen, Settings.percent, Settings.curveWidth)
               else:
                  if Settings.animFullCurve:
                     curve.drawCurve(screen, Settings.curveWidth)
                  else:
                     curve.drawCurveUntil(screen, Settings.animationPercent, Settings.curveWidth)
            if Settings.otherLines:
                curve.drawLinesAtN(screen, Settings.percent, Settings.otherLineWidth, True)      
            if Settings.points:
               curve.setPointsRadius(Settings.pointRadius)
               curve.drawPoints(screen)
            
            curve.handleDuplicates()

        pygame.display.update()
        
        time.sleep(.025)

if __name__ == "__main__":
    main()