import gmsh
import sys

gmsh.initialize()

gmsh.model.add("cilindro")

raio = 1.0
altura = 2.0
lc = 0.2  

p1 = gmsh.model.geo.addPoint(0, 0, 0, lc) 
p2 = gmsh.model.geo.addPoint(raio, 0, 0, lc)
p3 = gmsh.model.geo.addPoint(0, raio, 0, lc)
p4 = gmsh.model.geo.addPoint(-raio, 0, 0, lc)
p5 = gmsh.model.geo.addPoint(0, -raio, 0, lc)

a1 = gmsh.model.geo.addCircleArc(p2, p1, p3)
a2 = gmsh.model.geo.addCircleArc(p3, p1, p4)
a3 = gmsh.model.geo.addCircleArc(p4, p1, p5)
a4 = gmsh.model.geo.addCircleArc(p5, p1, p2)

loop_base = gmsh.model.geo.addCurveLoop([a1, a2, a3, a4])
surface_base = gmsh.model.geo.addPlaneSurface([loop_base])

volume = gmsh.model.geo.extrude([(2, surface_base)], 0, 0, altura, numElements=[10])[1][1]

gmsh.model.geo.synchronize()

group_cilindro = gmsh.model.addPhysicalGroup(3, [volume])
gmsh.model.setPhysicalName(3, group_cilindro, "Cilindro")

group_base = gmsh.model.addPhysicalGroup(2, [surface_base])
gmsh.model.setPhysicalName(2, group_base, "Base_Inferior")


gmsh.model.mesh.generate(3)

gmsh.write("cilindro.msh")

if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
