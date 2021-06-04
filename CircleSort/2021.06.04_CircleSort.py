#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Sort Circles and Display Largest/Smallest circle.
    Override DrawViewportWires method in SDK Mode.

    Input Parameter:
        Circles<list> : List of Circles.
    Output Paramter:
        Sorted<list> : List of Circles sorted in ascending order.
"""

# - - - - - - - - COMPONENT

__author__ = "Kaushik LS"
__copyright__ = "Copyright 2021, MODFIVE Labs"
__license__ = "None"
__email__ = "contact@modfivelabs.com"

ghenv.Component.Name = 'SortCircles'
ghenv.Component.NickName = 'SortCircles'
ghenv.Component.Message = '2021.06.04'

# - - - - - - - - IMPORTS

from ghpythonlib.componentbase import executingcomponent as component
import System
import Rhino

# - - - - - - - - SDK MODE COMPONENT

class SortCircles(component):

    # Method to use as sorting paramter
    def GetRadius(self, Circle):
        return Circle.Radius

    def GetArea(self, Circle):
        return round(3.14 * Circle.Radius * Circle.Radius, 2)

    def RunScript(self, Circles):
        
        self.SortedCircles = Circles
        self.SortedCircles.sort(key = self.GetRadius)

        self.SmallCircle = self.SortedCircles[0]
        self.LargeCircle = self.SortedCircles[-1]

        return self.SortedCircles

    def DrawViewportWires(self, args):

        # Preview BLUE colored small circle.
        SmallCircle = Rhino.Geometry.Brep.CreatePlanarBreps(self.SmallCircle.ToNurbsCurve())[0]
        args.Display.DrawBrepShaded(SmallCircle, Rhino.Display.DisplayMaterial(System.Drawing.Color.Blue))

        # Preview RED colored large circle.
        LargeCircle = Rhino.Geometry.Brep.CreatePlanarBreps(self.LargeCircle.ToNurbsCurve())[0]
        args.Display.DrawBrepShaded(LargeCircle, Rhino.Display.DisplayMaterial(System.Drawing.Color.Red))

        
        for i in range(len(self.SortedCircles)):
            # Preview all circles with BLACK Outline
            args.Display.DrawCircle(self.SortedCircles[i], System.Drawing.Color.Black, 2)

            # Preview sorted index numbers
            Text = Rhino.Display.Text3d(str(i), self.SortedCircles[i].Plane, self.GetRadius(self.SortedCircles[i])/2)
            # Text Alignment
            Text.HorizontalAlignment = Rhino.DocObjects.TextHorizontalAlignment.Center
            Text.VerticalAlignment   = Rhino.DocObjects.TextVerticalAlignment.Middle

            args.Display.Draw3dText(Text, System.Drawing.Color.Black, self.SortedCircles[i].Plane)

        # Screen Overlay Large Circle Info
        args.Display.Draw2dText('Large Circle\nArea: {} mm2'.format(self.GetArea(self.LargeCircle)), System.Drawing.Color.Red, Rhino.Geometry.Point2d(150,100), False, 35)

        # Screen Overlay Small Circle Info
        args.Display.Draw2dText('Small Circle\nArea: {} mm2'.format(self.GetArea(self.SmallCircle)), System.Drawing.Color.Blue, Rhino.Geometry.Point2d(150,200), False, 35)