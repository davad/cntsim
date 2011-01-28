import pylab
import xml.etree.ElementTree as ET
import numpy as np
## Example using both diameters and data

#The ElementTree library is a builtin library for XML manipulation






#Reads the xml contained in the specified file or thows an exception
FILE_NAME = "basetest.xml"
X = 0
Y = 1
R = 2

def overCheckV(testV1, testV2):
    global X, Y, R
    if (testV1[X] - testV2[X])**2+(testV1[Y] - testV2[Y])**2 < (testV1[R] + testV2[R])**2:
        outToop = (True, testV2)
    else: outToop = (False, None)
    
    return outToop

def eqCheck(v1, v2):
    outB = True
    for i in range(np.size(v1)):
        if v1[i] != v2[i]:
            outB = False
            break
    return outB

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
positions = np.zeros((tubeNum, 3))

#Iterates over the XML tree and puts stuff where it's supposed to go in the separate arrays
indT = 0
for tube in CNTForest.getiterator("T"):
    rad = float(tube.attrib["r"])
    for node in tube.getiterator("N"):
        positions[indT] = np.array([float(node.attrib["x"]),float(node.attrib["y"]), rad])
        break
    indT += 1

nGridX = int(dimensions[X]/(maxRadius*4)) #number of cells per side of grid
nGridY = int(dimensions[Y]/(maxRadius*4))
sGridX = maxRadius*4
sGridY = maxRadius*4

ovrCount = 0;
for v in positions:
    for c in positions:
        if not eqCheck(v,c) and overCheckV(v,c)[0]:
            ovrCount+=1
            print "grid index of bn1: " + str((int(np.floor(v[X]/sGridX)),int(np.floor(v[Y]/sGridY))))
            print "position of bn1: " + str((v[X],v[Y]))
            print "grid index of bn2: " + str((int(np.floor(c[X]/sGridX)),int(np.floor(c[Y]/sGridY))))
            print "position of bn2: " + str((c[X],c[Y]))

print "overlaps found:" + str(ovrCount)