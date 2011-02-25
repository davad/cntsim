
from OCC.gp import *
from OCC.BRepBuilderAPI import *
from OCC.GeomAPI import *
from OCC.Geom import *
from OCC.GeomAbs import *
from OCC.TColgp import *
from OCC.Geom2d import *
from OCC.gp import *
from OCC.BRepBuilderAPI import *
from OCC.TColgp import *
from OCC.BRepOffsetAPI import *
from OCC.GeomAbs import *
from OCC.BRepPrimAPI import *
from OCC.Utils.Topology import Topo
from OCC.BRep import *
from OCC.Precision import *
from OCC.BRepLib import *

import math, sys, random

from OCC.Display.SimpleGui import *
display, start_display, add_menu, add_function_to_menu = init_display()


def iterable(event=None):
#smooth
#  c1b = gp_Circ(gp_Ax2(gp_Pnt(100.,0.,-100.),gp_Dir(0.,0.,1.)),40.)
#  W1b = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(c1b).Edge()).Wire()
#
#  c2b = gp_Circ(gp_Ax2(gp_Pnt(210.,0.,-0.),gp_Dir(0.,0.,1.)),40.)
#  W2b = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(c2b).Edge()).Wire()
#
#  c3b = gp_Circ(gp_Ax2(gp_Pnt(275.,0.,100.),gp_Dir(0.,0.,1.)),40.)
#  W3b = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(c3b).Edge()).Wire()
#
#  c4b= gp_Circ(gp_Ax2(gp_Pnt(200.,0.,200.),gp_Dir(0.,0.,1.)),40.)
#  W4b = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(c4b).Edge()).Wire()
  xlist = []
  zlist = []
  for i in range(0,100):
    xlist.append(float(random.randint(0,1000)))
    zlist.append(float(random.randint(0,1000)))

  xlist = sorted(xlist)
  zlist = sorted(zlist)

  wiresA = []
  wiresB = []
  for i in range(0,100):
    circle = gp_Circ(gp_Ax2(gp_Pnt(xlist[i], 0, zlist[i]), gp_Dir(0.,0.,1.)), 40.)
    wire = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(circle).Edge()).Wire()
    wiresA.append(wire)
    
    circle = gp_Circ(gp_Ax2(gp_Pnt(xlist[i]+200, 0, zlist[i]+200), gp_Dir(0.,0.,1.)), 40.)
    wire = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(circle).Edge()).Wire()
    wiresB.append(wire)

  generatorA = BRepOffsetAPI_ThruSections(True, False)
  generatorB = BRepOffsetAPI_ThruSections(True, False)
  map(generatorA.AddWire, wiresA)
  map(generatorB.AddWire, wiresB)
  generatorA.Build()
  generatorB.Build()
  display.DisplayShape(generatorA.Shape())
  display.DisplayShape(generatorB.Shape())

add_menu('Testing')
add_function_to_menu('Testing', iterable)
start_display()
