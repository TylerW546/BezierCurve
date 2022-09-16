# -----------------------------------------------------------
# Description: A Bezier Curve demonstration. Demonstrates how BezierCurves are calculated via cool animation.
# Bezier curves are created by connecting various points, and then linear interpolating by some value between 0 and 100% (defined as x) along the lines that those connections form.
# Then connect the points that result from the interpolation, and interpolate along those resulting lines by x.
# Continue until left with only one point. This can be thought of as the output of C(x). By finding and plotting the values of C(x) for many x's between 0 and 100%, we begin to form a complete curve
#
# For example, between points a,b, and c
# Step 1. Interpolate x% along lines ab and bc with x=50%
#    This gets point d subdividing line ab, and point e subdividing line bc
# Repeat step one until left with one point
#   Repeat #1. Interpolate x% along line de, still with x=50%
#       This gets point f, which can be drawn
# Because we have a single point, stop interpolating
#
# Complete these steps for any number of initial points and for many values of x evenly distributed between 0-100% to get a Bezier Curve
#
# Date Started: September 27, 2021
# Name: Tyler Weed
# -----------------------------------------------------------

import math
import pygame
from pygame.locals import *
import random
import time

# Screen sizes and 
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SETTINGS_WIDTH = 300

# Define some common/custom colors
settingsColor = (100,100,200)
white = (255, 255, 255)
black = (0,0,0)
red = (255,0,0)
blue = (0, 0, 255)
background = (30,30,40)

# Pygame initializations
pygame.font.init()
myfont = pygame.font.SysFont('Times New Roman', 20)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + SETTINGS_WIDTH, SCREEN_HEIGHT))

def main():
    from Settings import Settings
    from Curve import BezierCurve
    
    Settings.startup()
    
    # BezierCurve.mainCurve is always the active curve. There is only one curve right now, so it will always be that curve. To create another curve, uncomment the line with BezierCurve().
    # You can select another curve by clicking on one of its points.
    # Because 1 curve is suitable for a simple demonstration on how bezier curves work, I didn't add buttons to add curves, and I didn't spend time making it clear which curve was selected.
    # The feature for multiple curves was purely for playing around. When I was initially writing the program, I added in support from the start by storing just one curve in the BezierCurve.allCurves list
    # Once I finished coding the program, I had to add more curves because it felt like a waste to have support for multiple curves and not use them at least once.
    BezierCurve.mainCurve = BezierCurve()
    # BezierCurve()

    while (True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            Settings.handle_event(event)
            for curve in BezierCurve.allCurves:
                curve.handle_event(event)
        
        # Clears screen to background color
        screen.fill(background)

        # Updates, draws, and applies Settings
        Settings.update()
        Settings.draw(screen)
        Settings.writeInfo()
        
        # For every curve
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
        
        # Ensures that only one point is selected across all curves. Prioritizes the curve already selected. 
        # If no curves are selected in the mainCurve but there are points selected in another curve, the other curve will becoome the mainCurve
        BezierCurve.handleDuplicates()

        pygame.display.update()
        
        time.sleep(.025)

if __name__ == "__main__":
    main()