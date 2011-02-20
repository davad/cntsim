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


CurvePoles = TColgp_Array1OfPnt(1,6)
pt1 = gp_Pnt(0.,0.,0.);
pt2 = gp_Pnt(20.,50.,0.);
pt3 = gp_Pnt(60.,100.,0.);
pt4 = gp_Pnt(150.,0.,0.);
CurvePoles.SetValue(1, pt1)
CurvePoles.SetValue(2, pt2)
CurvePoles.SetValue(3, pt3)
CurvePoles.SetValue(4, pt4)

curve = Geom_BezierCurve(CurvePoles)
print type(curve)
E = BRepBuilderAPI_MakeEdge(curve).Edge()
W = BRepBuilderAPI_MakeWire(E).Wire()
 
ais1 = AIS_Shape(W)
self.interactive_context.Display(ais1,1)
 
c = gp_Circ(gp_Ax2(gp_Pnt(0.,0.,0.),gp_Dir(0.,1.,0.)),10.)
Ec = BRepBuilderAPI_MakeEdge(c).Edge()
Wc = BRepBuilderAPI_MakeWire(Ec).Wire()
ais3 = AIS_Shape(Wc)
self.interactive_context.Display(ais3,1)
 
F = BRepBuilderAPI_MakeFace(gp_Pln(gp_Ax3(gp().ZOX())),Wc,1).Face()
S = BRepOffsetAPI_MakePipe(W,F).Shape()
ais2 = AIS_Shape(S)
self.interactive_context.SetMaterial(ais2,Graphic3d_NOM_PLASTIC,0)
self.interactive_context.SetColor(ais2,Quantity_NOC_MATRABLUE,0)
self.interactive_context.SetDisplayMode(ais2,AIS_Shaded,0)
self.interactive_context.Display(ais2,1)
