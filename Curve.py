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
      
      # Points is the list of all points
      self.points = []
      # Active points is the list of points within a layer of linear interpolation. Starts with all points, then interpolates between them again and again until one point left.
      self.active_points = []
      
      # Points are defined as boundary points so they cannot be dragged outside of the screen.
      for i in range(numPoints):
         self.points.append(BoundaryPoint(self.x, self.y))
      
      BezierCurve.allCurves.append(self)

   def handle_event(self, event):
      """Send events to all points"""
      for point in self.points:
         point.handle_event(event)
   
   def drawPoints(self, screen):
      """Calls the draw function for all points"""
      for point in self.points:
         point.draw(screen)
   
   def drawPrimaryLines(self, screen, width):
      """Connects the points with straight lines"""
      for i in range(len(self.points)-1):
         pygame.draw.lines(screen, BezierCurve.primaryLineColor, False, [(self.points[i].x,self.points[i].y), (self.points[i+1].x, self.points[i+1].y)], width)
   
   def getNewPoints(self, n):
      """Linear Interpolates by n all lines created by active_points. Sets active points to the resulting values"""
      new_points = []
      for i in range(len(self.active_points)-1):
         vector = [self.active_points[i+1][0] - self.active_points[i][0], self.active_points[i+1][1] - self.active_points[i][1]]
         vector[0] *= n
         vector[1] *= n
         new_points.append([self.active_points[i][0]+vector[0], self.active_points[i][1]+vector[1]])
      # Now, self.active_points is equal to a linear interpolation of the lines defined by the values it held previously 
      self.active_points = new_points
   
   def setPointsRadius(self, radius):
      """Changes the radius of points"""
      for point in self.points:
         point.radius = radius
   
   def drawPointAtN(self, screen, n, radius):
      """Draw the point on the actual bezier curve at n, where n is the decimal value between 0 and 1 used for every linear interpolation"""
      self.active_points = []
      for point in self.points:
         self.active_points.append([point.x, point.y])
      while len(self.active_points) > 1:
         self.getNewPoints(n)
      point = self.active_points[0]
      pygame.draw.circle(screen, BezierCurve.curveColor, (int(point[0]), int(point[1])), radius)
   
   def drawLinesAtN(self, screen, n, width, drawEndPoints=False):
      """Draw the lines and points that show every step of the linear interpolation process"""
      self.active_points = []
      for point in self.points:
         self.active_points.append([point.x, point.y])
      while len(self.active_points) > 1:
         for i in range(len(self.active_points)-1):
            point1 = self.active_points[i]
            point2 = self.active_points[i+1]
            pygame.draw.lines(screen, BezierCurve.otherLineColor, True, [(point1[0], point1[1]), (point2[0], point2[1])], width)
            if drawEndPoints:
               pygame.draw.circle(screen, BezierCurve.otherLineColor, (int(point1[0]), int(point1[1])), 2)
               pygame.draw.circle(screen, BezierCurve.otherLineColor, (int(point2[0]), int(point2[1])), 2)
         self.getNewPoints(n)
      if drawEndPoints:
         point = self.active_points[0]
         pygame.draw.circle(screen, BezierCurve.otherLineColor, (int(point[0]), int(point[1])), 4)
   
   def drawCurve(self, screen, width):
      """Draw the point on the bezier curve at n for a large number of n's between 0 and 1"""
      for intn in range(0,1001,1):
         n = intn / 1000
         self.drawPointAtN(screen, n, width)
   
   def drawCurveUntil(self, screen, endPercent, width):
      """Draw the point on the curve at n for a large number of n's between 0 and some end value between 0 and 1"""
      for intn in range(0,int(endPercent*1001),1):
         n = intn / 1000
         self.drawPointAtN(screen, n, width)

   @staticmethod
   def handleDuplicates():
      """Handles the case where multiple curves from the same or different curves are selected at once. Removes these duplicates, leaving only one point selected."""
      # Checks if the main curve has a selected point. If so, this point and main curve have the priority
      # Clear the selection of all other points in mainCurve, and all other points in all other curves
      for i in range(len(BezierCurve.mainCurve.points)):
         if BezierCurve.mainCurve.points[i].clicked == True:
            for point in BezierCurve.mainCurve.points[i+1:]:
               point.clicked = False
            for curve in BezierCurve.allCurves:
               if curve != BezierCurve.mainCurve:
                  for point in curve.points:
                     point.clicked = False
            return
      
      # Nothing selected in main curve, check for selected points in other curves.
      # If found, clear the selection of all other points in this curve, and all other points in all other curves.
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
   