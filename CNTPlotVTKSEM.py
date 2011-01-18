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

b=0
for i in range(len(CNTForest)-1):
    a=len(CNTForest[i].getiterator("N"))
    pairs=np.delete(pairs,b+a-i-1,0)
    b+=a

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

points = vtk.vtkPoints()
profileData = vtk.vtkPolyData()
scalarData = vtk.vtkFloatArray()

for i in range(0, np.size(tubesX)):
    points.InsertPoint(i, (tubesX[i], tubesY[i], tubesZ[i]))
    scalarData.InsertValue(i, scalars[i])

lineV = [None]*tubeNum
for L in range(tubeNum):
    lineV[L] = vtk.vtkCellArray()
    for n in range(N):
        pass
# Create the polyline.
lines = vtk.vtkCellArray()
for L in range(tubeNum):
    lines.InsertNextCell(N)
    for n in range(N):
        lines.InsertCellPoint(L*N+n)
#lines.InsertNextCell(numberOfInputPoints)
#for i in range(numberOfInputPoints):
#    lines.InsertCellPoint(i)
 
#create a plane to cut,here it cuts in the XZ direction (xz normal=(1,0,0);XY =(0,0,1),YZ =(0,1,0)
plane=vtk.vtkPlane()
plane.SetOrigin(xMax/2,0,0)
plane.SetNormal(1,0,0)
 

 

 
profileData.SetPoints(points)
profileData.SetLines(lines)
profileData.GetPointData().SetScalars(scalarData)

# Add thickness to the resulting line.
profileTubes = vtk.vtkTubeFilter()
profileTubes.SetNumberOfSides(50)
profileTubes.SetInput(profileData)
profileTubes.SetRadius(minR)

# Vary tube thickness with scalar
profileTubes.SetRadiusFactor(maxR/minR)
profileTubes.SetVaryRadiusToVaryRadiusByScalar()  

profileMapper = vtk.vtkPolyDataMapper()
profileMapper.SetInput(profileTubes.GetOutput())
profileMapper.SetScalarRange(0,maxR)   

#Set this to Off to turn off color variation with scalar
#profileMapper.ScalarVisibilityOn()
profileMapper.ScalarVisibilityOff()
profile = vtk.vtkActor()
profile.SetMapper(profileMapper)
#profile.GetProperty().SetSpecular(.3)
#profile.GetProperty().SetSpecularPower(30)
profile.GetProperty().SetOpacity(.5)
profile.GetProperty().SetColor(.3,.3,.3)

#create cutter
cutter=vtk.vtkCutter()
cutter.SetCutFunction(plane)
cutter.SetInput(profileMapper.GetInput())
cutter.Update()
cutterMapper=vtk.vtkPolyDataMapper()
cutterMapper.SetInputConnection( cutter.GetOutputPort())

#create plane actor
planeActor=vtk.vtkActor()
planeActor.GetProperty().SetColor(1.0,1,0)
planeActor.GetProperty().SetLineWidth(2)
planeActor.SetMapper(cutterMapper)

#camera = vtk.vtkCamera()
#camera.SetPosition(xMax/2, 0, zMax/2)

# Now create the RenderWindow, Renderer and Interactor
ren = vtk.vtkRenderer()
ren.SetBackground(.05,.05,.05)
ren.SetOcclusionRatio(.5)
#ren.SetActiveCamera(camera);
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors
ren.AddActor(profile)
ren.AddActor(planeActor)


renWin.SetSize(500, 500)

outFileName = "OBJTest"
iren.Initialize()
renWin.Render()
iren.Start()
#VRML = vtk.vtkVRMLExporter();
#VRML.SetInput(renWin);
#VRML.SetFileName("test.wrl");
#VRML.Write()
#del VRML
windowToImageFilter = vtk.vtkWindowToImageFilter()
windowToImageFilter.SetInput(renWin)
windowToImageFilter.SetMagnification(3) #set the resolution of the output image
windowToImageFilter.Update()

writer = vtk.vtkPNGWriter()
writer.SetFileName("screenshot2.png")
writer.SetInput(windowToImageFilter.GetOutput())
writer.Write()

renWin.Render()
ren.ResetCamera()
renWin.Render()
iren.Start()



#writer = vtk.vtkSTLWriter()
#writer.SetFileName(outFileName)
#writer.SetInputConnection(profileMapper.GetOutputPort())
#writer.Write()