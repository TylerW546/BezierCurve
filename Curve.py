import pygame
from pygame.locals import *

from main import *
from Points import *

class BezierCurve():
   allCurves = []
   mainCurve = None
   
   primaryLineColor = (100,200,100)
   
   otherLineColor = (100,100,200)
   
   curveColor = (200,100,100)
   
   def __init__(self, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2, numPoints=1):
      self.x = x
      self.y = y
      
      self.points = []
      self.activePoints = []
      
      for i in range(numPoints):
         self.points.append(BoundaryPoint(self.x, self.y))
      
      BezierCurve.allCurves.append(self)

   def handle_event(self, event):
      for point in self.points:
         point.handle_event(event)
   
   def drawPoints(self, screen):
      for point in self.points:
         point.draw(screen)
   
   def drawPrimaryLines(self, screen, width):
      for i in range(len(self.points)-1):
         pygame.draw.lines(screen, BezierCurve.primaryLineColor, False, [(self.points[i].x,self.points[i].y), (self.points[i+1].x, self.points[i+1].y)], width)
   
   def getNewPoints(self, n):
      new_points = []
      for i in range(len(self.activePoints)-1):
         vector = [self.activePoints[i+1][0] - self.activePoints[i][0], self.activePoints[i+1][1] - self.activePoints[i][1]]
         vector[0] *= n
         vector[1] *= n
         new_points.append([self.activePoints[i][0]+vector[0], self.activePoints[i][1]+vector[1]])
      self.activePoints = new_points
   
   @staticmethod
   def handleDuplicates():
      # for main curve
      for i in range(len(BezierCurve.mainCurve.points)):
         if BezierCurve.mainCurve.points[i].clicked == True:
            for point in BezierCurve.mainCurve.points[i+1:]:
               point.clicked = False
            for curve in BezierCurve.allCurves:
               if curve != BezierCurve.mainCurve:
                  for point in curve.points:
                     point.clicked = False
            return
      
      # Nothing selected in main curve
      for curve in BezierCurve.allCurves:
         if curve != BezierCurve.mainCurve:
            for i in range(len(curve.points)):
               if curve.points[i].clicked == True:
                  for point in curve.points[i+1:]:
                     point.clicked = False
                  BezierCurve.mainCurve = curve
                  for curveToShutOff in BezierCurve.allCurves:
                     if curveToShutOff != curve:
                        for point in curveToShutOff.points:
                           point.clicked = False
                  return
   
   def setPointsRadius(self, radius):
      for point in self.points:
         point.radius = radius
   
   def drawPointAtN(self, screen, n, radius):
      self.activePoints = []
      for point in self.points:
         self.activePoints.append([point.x, point.y])
      while len(self.activePoints) > 1:
         self.getNewPoints(n)
      point = self.activePoints[0]
      pygame.draw.circle(screen, BezierCurve.curveColor, (int(point[0]), int(point[1])), radius)
   
   def drawLinesAtN(self, screen, n, width, drawEndPoints=False):
      self.activePoints = []
      for point in self.points:
         self.activePoints.append([point.x, point.y])
      while len(self.activePoints) > 1:
         for i in range(len(self.activePoints)-1):
            point1 = self.activePoints[i]
            point2 = self.activePoints[i+1]
            pygame.draw.lines(screen, BezierCurve.otherLineColor, True, [(point1[0], point1[1]), (point2[0], point2[1])], width)
            if drawEndPoints:
               pygame.draw.circle(screen, BezierCurve.otherLineColor, (int(point1[0]), int(point1[1])), 2)
               pygame.draw.circle(screen, BezierCurve.otherLineColor, (int(point2[0]), int(point2[1])), 2)
         self.getNewPoints(n)
      if drawEndPoints:
         point = self.activePoints[0]
         pygame.draw.circle(screen, BezierCurve.otherLineColor, (int(point[0]), int(point[1])), 4)
   
   def drawCurve(self, screen, width):
      for intn in range(0,1001,1):
         n = intn / 1000
         self.drawPointAtN(screen, n, width)
   
   def drawCurveUntil(self, screen, endPercent, width):
      for intn in range(0,int(endPercent*1001),1):
         n = intn / 1000
         self.drawPointAtN(screen, n, width)