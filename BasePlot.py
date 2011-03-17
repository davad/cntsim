import pylab
import xml.etree.ElementTree as ET
import numpy as np
## Example using both diameters and data

#The ElementTree library is a builtin library for XML manipulation


#Reads the xml contained in the specified file or thows an exception
FILE_NAME = "tritest.xml"
#FILE_NAME = "xmltest.xml"
POSITION_LENGTH = 3
X = 0
Y = 1
Z = 2

#Most of the magic happens here, and it's done automagically
xml = ET.parse(FILE_NAME)

#Set the root of the document, which contains attributes that describe 
#the properties of the forest, such as # of nodes.
#It is currently assumed that all tubes have the same number of nodes
CNTForest = xml.getroot()

#
nodeNum = int(CNTForest.attrib["nodenum"])
tubeNum = int(CNTForest.attrib["tubenum"])
minRadius = float(CNTForest.attrib["rmin"])
maxRadius = float(CNTForest.attrib["rmax"])
dimensions = [float(CNTForest.attrib["xmax"]),float(CNTForest.attrib["ymax"]),float(CNTForest.attrib["zmax"])]
print("Number of nodes in file: " + str(nodeNum))
print("Number of tubes in file: " + str(tubeNum))
print("Minimum radius of any tube in forest: " + str(minRadius))
print("Maximum radius of any tube in forest: " + str(maxRadius))
print("Dimensions of forest: " + str(dimensions))

#The data is separated into two arrays: radii is a (1, T) length array
#where T is the number of tubes
radii = np.zeros((tubeNum))
N = nodeNum/tubeNum
#positions contains the position data in the same order as radii
#it's shape is (T,N,3) where N is the number of nodes per tube, and T defined prior
positions = np.zeros((tubeNum, 2))

#Iterates over the XML tree and puts stuff where it's supposed to go in the separate arrays
indT = 0
for tube in CNTForest.getiterator("T"):
    radii[indT] = float(tube.attrib["r"])
    for node in tube.getiterator("N"):
        positions[indT] = np.array([float(node.attrib["x"]),float(node.attrib["y"])])
        break
    indT += 1

nGridX = int(dimensions[X]/(maxRadius*4)) #number of cells per side of grid
nGridY = int(dimensions[Y]/(maxRadius*4))
sGridX = maxRadius*4
sGridY = maxRadius*4

np.arange(dimensions[X],sGridX)

#positions[:,X] /= max(dimensions[X:Z])
#positions[:,Y] /= max(dimensions[X:Z])
#radii /= max(dimensions[X:Z])

pylab.axes()
#pylab.axes([0,dimensions[X],0,dimensions[Y]])
pylab.title('CNT Base Node Positions')
for i in range(np.size(radii)):
    cir = pylab.Circle((positions[i,X],positions[i,Y]), radius=radii[i],  fc='y')
    pylab.gca().add_patch(cir)

print np.arange(0.0,dimensions[X],sGridX)

pylab.axis('scaled')
pylab.xlim((0,dimensions[X]))
pylab.ylim((0,dimensions[Y]))
pylab.xticks(np.arange(0.0,dimensions[X],sGridX))
pylab.yticks(np.arange(0.0,dimensions[Y],sGridY))
pylab.grid(True)
pylab.show()
