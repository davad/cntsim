from OCC.PAF.Context import ParametricModelingContext
from OCC.PAF.Parametric import Parameters

p = Parameters()
tc = ParametricModelingContext(p)
tc.init_display()
p.height = 43.3
p.radius = 12.9
tc.register_operations( tutorial_context.prim_operations)
my_box = tc.prim_operations.MakeCylinderRH(p.radius, p.height, name="Cylinder1", show=True)

