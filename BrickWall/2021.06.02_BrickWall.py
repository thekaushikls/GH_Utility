#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Create Brick Wall Component.
    Input Parameters:    
        Profile<Curve> : Profile Curve acts as guide for masonry units.
        Mortar<float>  : Mortar Thickness.
        Course<int>   : Number of Masonry Courses.
        
        Width<float>   : Width of Brick.
        Depth<float>   : Depth of Brick.
        Height<float>  : Height of Brick.
"""

# - - - - - - - - COMPONENT

__author__ = "Kaushik LS"
__copyright__ = "Copyright 2021, MODFIVE Labs"
__license__ = "None"
__email__ = "contact@modfivelabs.com"

ghenv.Component.Name = 'BrickWall'
ghenv.Component.NickName = 'BrickWall'
ghenv.Component.Message = '2021.06.02'

# - - - - - - - - IMPORTS

import Rhino
from ghpythonlib import treehelpers
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

# Create a Brick Object
class BrickUnit:

    def __init__(self, Plane = Rhino.Geometry.Plane.WorldXY, Length = 230, Width = 90, Depth = 110):
        self.Plane = Plane
        self.DimX = Length
        self.DimY = Width
        self.DimZ = Depth
        self.Geometry = self._GetBrick()

    def _GetBrick(self):
        Rectangle =  Rhino.Geometry.Rectangle3d(self.Plane, self.DimX, self.DimY)
        Geometry = Rhino.Geometry.Extrusion.Create(Rectangle.ToNurbsCurve(), self.DimZ, True)
        return Geometry
            
    def __str__(self):
        return self.__class__.__name__

# Create the Wall
class Wall:
    
    def __init__(self, Curve, Course = 5, MortarThickness = 10):
        self.Curve = Curve
        self.Course = Course
        self.MortarThickness = MortarThickness
    
    def SetSampleBrick(self, Brick):
        self.SampleBrick = Brick
    
    def _GetBasePlanes(self):
        Planes = []
        # Curve is divided by net length of brick unit. Net length is the sum of the length of the Brick and Mortar Thickness. Net Length if divided by two, to create twice the number of points, to create staggered arrangement.
        Params = self.Curve.DivideByLength((self.SampleBrick.DimX + self.MortarThickness) / 2, True)
        Points = [self.Curve.PointAt(param) for param in Params]
        Tangents = [self.Curve.TangentAt(param) for param in Params]
        Perps = [Rhino.Geometry.Vector3d.CrossProduct(Rhino.Geometry.Vector3d(0,0,1), Tangent) for Tangent in Tangents]
        # Creating Planes aligned to the Curve, marks location of each Brick/ Masonry Unit on the lower-most course.
        for i in range(len(Points)):
            Plane = Rhino.Geometry.Plane(Points[i], Tangents[i], Perps[i])
            Planes.append(Plane)
        return Planes
    
    def _GetCoursePlanes(self):
        self.CoursePlanes = []
        # For each course, a copy of the base planes is moved to the respective Net Height. 
        for count in range(self.Course):
            Planes = self._GetBasePlanes()
            # Net Height = Height of Brick + Mortar Thickness
            xform = Rhino.Geometry.Transform.Translation(0, 0, (self.SampleBrick.DimZ + self.MortarThickness) * count)
            [Plane.Transform(xform) for Plane in Planes]
            self.CoursePlanes.append(Planes)
        return self.CoursePlanes
    
    def BuildWall(self):
        self._GetCoursePlanes()
        OddCourse = []
        EvenCourse = []
        # Sorting Courses into Even and Odd, for staggering.
        for num in range(self.Course):
            if num % 2:
                # Even courses have bricks only in even positions.
                for plane_index in range(0, len(self.CoursePlanes[num]), 2):
                    EvenCourse.append(self.CoursePlanes[num][plane_index])
            else:
                # Odd Courses have bricks only in odd positions.
                for plane_index in range(1, len(self.CoursePlanes[num]), 2):
                    OddCourse.append(self.CoursePlanes[num][plane_index])
        
        # Creating New Brickas in sorted Planes and Courses.
        EvenBrickCourse = [BrickUnit(Plane, self.SampleBrick.DimX, self.SampleBrick.DimY, self.SampleBrick.DimZ).Geometry for Plane in EvenCourse]
        OddBrickCourse  = [BrickUnit(Plane, self.SampleBrick.DimX, self.SampleBrick.DimY, self.SampleBrick.DimZ).Geometry for Plane in OddCourse]

        return OddBrickCourse,  EvenBrickCourse



# Check if All inputs are provided.
if Profile and Course and Mortar and Width and Depth and Height:
    myBrick = BrickUnit(Length = Width, Width = Depth, Depth = Height)
    
    myWall = Wall(Profile, Course, Mortar)
    myWall.SetSampleBrick(myBrick)
    Wall = treehelpers.list_to_tree(myWall.BuildWall())
else:
    ghenv.Component.AddRuntimeMessage(RML.Warning, 'Inputs not valid')
