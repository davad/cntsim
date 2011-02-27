
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

import math, sys, random, json

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
  forest = []
  try:
    fp = open('test_forest.json', 'r')
    forest = json.load(fp)
    fp.close()
  except IOError:
    print "No json file found"
  
  print "Simulating " + str(len(forest)) + " tubes"
  for tube in forest:
    if(len(tube) < 2):
      continue
    wires = []
    for point in tube:
      circle = gp_Circ(gp_Ax2(gp_Pnt(point[0], point[1], point[2]), gp_Dir(0.,0.,1.)), 8.)
      wire = BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(circle).Edge()).Wire()
      wires.append(wire)
    
    generator = BRepOffsetAPI_ThruSections(True, False)
    map(generator.AddWire, wires)
    try:
      generator.Build()
    except:
      print tube
      continue
    display.DisplayShape(generator.Shape())

add_menu('Testing')
add_function_to_menu('Testing', iterable)
start_display()
