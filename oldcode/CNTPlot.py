## Example using both diameters and data
from enthought.mayavi import mlab

#The ElementTree library is a builtin library for XML manipulation
import xml.etree.ElementTree as ET
import numpy as np

#Reads the xml contained in the specified file or throws an exception
FILE_NAME = "secondtest.xml"
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
positions = np.zeros((tubeNum, N, POSITION_LENGTH))

#Iterates over the XML tree and puts stuff where it's supposed to go in the separate arrays
indT = 0
for tube in CNTForest.getiterator("T"):
    radii[indT] = float(tube.attrib["r"])
    indN = 0
    for node in tube.getiterator("N"):
        positions[indT,indN] = np.array([float(node.attrib["x"]),float(node.attrib["y"]),float(node.attrib["z"])])
        indN += 1
    indT += 1


#Extracts the X, Y, and Z values from the position array
tubesX = positions[:,:,X]
tubesY = positions[:,:,Y]
tubesZ = positions[:,:,Z]

#generates a dummy array for the connection values to be appended to
pairs = np.zeros(2)

#This loop steps through and generates all the pairs
for i in range(tubeNum):
    for j in range(nodeNum/tubeNum):
        pairs = np.vstack((pairs,np.array([[i*N+j,i*N+j+1]])))
pairs=pairs[1:,:]


#This extends the array of radii to be the same size as the xyz arrays
scalars = np.zeros((tubeNum, N, 1))
for m in range(tubeNum):
    scalars[m,:] = radii[m]
    
    
#Turns all the matrices into 1D arrays
scalars = np.ravel(scalars)
tubesX = np.hstack(tubesX)
tubesY = np.hstack(tubesY)
tubesZ = np.hstack(tubesZ)
#print np.shape(tubesX)
#print np.shape(tubesY)
#print np.shape(tubesZ)
#print np.shape(radii)
#print np.shape(scalars)
#print pairs


# Create the points, this data type uses x,y,z values and a scalar data field
#They all have to be the same size
src = mlab.pipeline.scalar_scatter(tubesX, tubesY, tubesZ, scalars)

# Connect them
src.mlab_source.dataset.lines = pairs

# The tube filter makes lines into tubes
tubes = mlab.pipeline.tube(src,tube_sides = 12)

#Make the radius of the tube proportional to the scalar values and add caps
tubes.filter.capping = True
tubes.filter.vary_radius = 'vary_radius_by_scalar'
#tubes.filter.use_default_normal = True


# Finally, display the set of lines
mlab.pipeline.surface(tubes, colormap='Accent', opacity=1)



# And choose a nice view
mlab.show()