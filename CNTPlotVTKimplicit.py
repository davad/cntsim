import vtk
import xml.etree.ElementTree as ET
import numpy as np

NUM_SIDES=10
print "parsing..."
FILENAME="secondtest.xml"
xml = ET.parse(FILENAME)
CNTForest = xml.getroot()
tubeNum=len(CNTForest.getiterator("T"))
nodeNum=len(CNTForest.getiterator("N"))
N = nodeNum/tubeNum
radii = np.zeros((tubeNum))
maxR = float(CNTForest.attrib["rmax"])
minR = float(CNTForest.attrib["rmin"])
print "generating positions"

positions = np.zeros((tubeNum, nodeNum/tubeNum, 3))
indT = 0
for tube in CNTForest.getiterator("T"):
    radii[indT] = float(tube.attrib["r"])
    indN = 0
    for node in tube.getiterator("N"):
        positions[indT,indN] = np.array([float(node.attrib["x"]),float(node.attrib["y"]),float(node.attrib["z"])])
        indN += 1
    indT += 1

print "generating pairs"

pairs=np.vstack((np.arange(nodeNum-1),np.arange(nodeNum)[1:]))
pairs=pairs.transpose()

print "generating scalars"

#This extends the array of radii to be the same size as the xyz arrays
scalars = np.zeros((tubeNum, N, 1))
for m in range(tubeNum):
    scalars[m,:] = radii[m]



print "parsed"
x = positions[:,:,0]
y = positions[:,:,1]
z = positions[:,:,2]

pairs=np.delete(pairs,0,0)

print "stacking things. . ."
scalars = np.ravel(scalars)

tubesX = np.hstack(x)
tubesY = np.hstack(y)
tubesZ = np.hstack(z)
xMax = np.max(tubesX)
yMax= np.max(tubesY)
zMax = np.max(tubesZ)

sTube = positions[0]
sTubeX = sTube[:,0]
sTubeY = sTube[:,1]
sTubeZ = sTube[:,2]

tPairs = []

for i in range(1,np.shape(positions[0])[0]):
    tPairs.append((i-1,i))


spheres = [None]*np.size(sTubeX)
sphereActs = [None]*np.size(sTubeX)
for i in range(len(spheres)):
    spheres[i] = vtk.vtkSphere()
    spheres[i].SetCenter(sTubeX[i], sTubeY[i], sTubeZ[i])
    spheres[i].SetRadius(scalars[0])


cyls = [None]*len(tPairs)
for c in range(len(cyls)):
    icyl = vtk.vtkCylinder()
    p1 = vtk.vtkPlane()
    p1.SetOrigin(sTubeX[tPairs[c][0]],sTubeY[tPairs[c][0]],sTubeZ[tPairs[c][0]])
    p1.SetNormal(sTubeX[tPairs[c][1]] - sTubeX[tPairs[c][0]],sTubeY[tPairs[c][1]] - sTubeY[tPairs[c][0]],sTubeZ[tPairs[c][1]] - sTubeZ[tPairs[c][0]])
    p2 = vtk.vtkPlane()
    p2.SetOrigin(sTubeX[tPairs[c][1]],sTubeY[tPairs[c][1]],sTubeZ[tPairs[c][1]])
    p2.SetNormal(sTubeX[tPairs[c][0]] - sTubeX[tPairs[c][1]],sTubeY[tPairs[c][0]] - sTubeY[tPairs[c][1]],sTubeZ[tPairs[c][0]] - sTubeZ[tPairs[c][1]])
    ccyl = vtk.vtkImplicitBoolean()
    ccyl.SetOperationTypeToIntersection()
    ccyl.AddFunction(icyl)
    ccyl.AddFunction(p1)
    ccyl.AddFunction(p2)
    

print np.shape(pairs)
print np.shape(positions)

tube = vtk.vtkImplicitBoolean()
tube.SetOperationTypeToUnion()

for s in spheres:
    tube.AddFunction(s)

tubeXMax = max(sTubeX) + scalars[0]
tubeYMax = max(sTubeY) + scalars[0]
tubeZMax = max(sTubeZ) + scalars[0]
tubeXMin = min(sTubeX) - scalars[0]
tubeYMin = min(sTubeY) - scalars[0]
tubeZMin = min(sTubeZ) - scalars[0]

sf = vtk.vtkSampleFunction()
sf.SetImplicitFunction(tube)
sf.SetModelBounds(tubeXMin, tubeXMax, tubeYMin, tubeYMax, tubeZMin, tubeZMax) 
sf.SetSampleDimensions(50, 50, 250)
sf.ComputeNormalsOff()
cf = vtk.vtkContourFilter()
cf.SetInputConnection(sf.GetOutputPort())
cf.SetValue(0, 0.0)
pm = vtk.vtkPolyDataMapper()
pm.SetInputConnection(cf.GetOutputPort())
a = vtk.vtkActor()
a.SetMapper(pm)


    
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the renderer, set the background and size
#
ren1.AddActor(a)  
ren1.SetBackground(1, 1, 1)
renWin.SetSize(800, 800)
ren1.ResetCamera
#ren1.GetActiveCamera().Roll(90)
#ren1.GetActiveCamera().Dolly(1.5)
#ren1.ResetCameraClippingRange()
iren.Initialize()

# render the image
#
renWin.Render()
iren.Start()