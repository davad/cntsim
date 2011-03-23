import numpy as np
from numpy import random
import xml.etree.ElementTree as ET

cellLength = 100
tubeRadius = 4
fillFraction = .5

tubeList = []

tubeNum = int(np.floor(fillFraction*cellLength**2/(np.pi*tubeRadius**2)))
#tubeDx = np.floor(cellLength/np.sqrt(tubeNum))
tubeDx = np.sqrt(np.pi)*tubeRadius/(np.sqrt(fillFraction))
tubeDy = tubeDx*np.sqrt(3)/2.0
tubeNx = int(np.floor(cellLength)/np.ceil(tubeDx))
tubeNy = int(np.floor(cellLength)/np.ceil(tubeDy))

nGrid = int(np.floor(cellLength/(tubeRadius*3))) #number of cells per side of grid
sGrid = float(cellLength)/nGrid #size of grid cells
xInd = 0
yInd = 1
zInd  = 2
rInd = 3
nIter = 500;


field = [None]*nGrid

for i in range(nGrid):
    field[i] = [None]*nGrid


def overCheckF(testV):
    #Checks for overlaps among nodes placed with the grid cell of the new node
    # and also the 8 cells surrounding it
    
    global field, sGrid, xInd, yInd
    fIT = int(np.floor(testV[xInd]/sGrid))
    fJT = int(np.floor(testV[yInd]/sGrid))
    
    #test tubes in same block, if any
    outToop = overCheckG(testV, (fIT, fJT))
    if outToop[0]:
        return outToop[1]
#Cases are processed as follows:
##O######xmax        
###|6|7|8|###       
###|5|0|1|###
###|4|3|2|###
#ymax########     
    if (fIT > 0 and fIT < nGrid-1) and (fJT > 0 and fJT < nGrid-1): #xmid & ymid
        outToop = overCheckG(testV, (fIT + 1, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT - 1, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT + 1, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT - 1, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT + 1, fJT))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT - 1, fJT))
        if outToop[0]:
            return outToop[1]
    elif (fIT == nGrid-1) and (fJT > 0 and fJT < nGrid-1): #xmax & ymid
        outToop = overCheckG(testV, (fIT - 1, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT - 1, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT - 1, fJT))
        if outToop[0]:
            return outToop[1]
    elif (fIT == nGrid-1) and (fJT == nGrid-1): #xmax & ymax
        outToop = overCheckG(testV, (fIT - 1, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT - 1, fJT))
        if outToop[0]:
            return outToop[1]
    elif (fIT > 0 and fIT < nGrid-1) and (fJT == nGrid-1): #xmid & ymax
        outToop = overCheckG(testV, (fIT - 1, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT + 1, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT + 1, fJT))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT - 1, fJT))
        if outToop[0]:
            return outToop[1]
    elif (fIT == 0) and (fJT == nGrid-1): #xmin & ymax
        outToop = overCheckG(testV, (fIT + 1, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT + 1, fJT))
        if outToop[0]:
            return outToop[1]
    elif (fIT == 0) and (fJT > 0 and fJT < nGrid-1): #xmin & ymid
        outToop = overCheckG(testV, (fIT + 1, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT + 1, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT, fJT - 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT + 1, fJT))
        if outToop[0]:
            return outToop[1]
    elif (fIT == 0) and (fJT == 0): #xmin & ymin
        outToop = overCheckG(testV, (fIT + 1, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT + 1, fJT))
        if outToop[0]:
            return outToop[1]
    elif (fIT > 0 and fIT < nGrid-1) and (fJT == 0): #xmid & ymin
        outToop = overCheckG(testV, (fIT + 1, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT - 1, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT + 1, fJT))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT - 1, fJT))
        if outToop[0]:
            return outToop[1]
    elif (fIT == nGrid-1) and (fJT == 0): #xmax & ymin
        outToop = overCheckG(testV, (fIT - 1, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT, fJT + 1))
        if outToop[0]:
            return outToop[1]
        outToop = overCheckG(testV, (fIT - 1, fJT))
        if outToop[0]:
            return outToop[1]

    return None
    
def overCheckG(testV, indices):
    #tests is the position vector will overlap with a previously existing position
    # by default, this function returns 
    global field, sGrid, xInd, yInd
    fIT = indices[xInd]
    fJT = indices[yInd]
    outToop = (False, None)
    #test tubes in block indicated by indices
    if field[fIT][fJT]!= None:
        if len(np.shape(field[fIT][fJT])) < 2:
            outToop = overCheckV(testV, field[fIT][fJT])
        else:
            for v in field[fIT][fJT]:
                outToop = overCheckV(testV, v)
                if outToop[0]:
                    break
    
    return outToop

def overCheckV(testV1, testV2):
    global xInd, yInd, rInd
    if pow(testV1[xInd] - testV2[xInd],2)+pow(testV1[yInd] - testV2[yInd],2) < (testV1[rInd] + testV2[rInd])**2:
        outToop = (True, testV2)
    else: outToop = (False, None)
    
    return outToop	
	
	
	
nT = 0
for j in range(tubeNy):
	for i in range(tubeNx):
		if nT == tubeNum:
			break
		else:
			tubeList.append(np.array([i*tubeDx+tubeRadius,j*tubeDy+tubeRadius, 0, tubeRadius]))
			nT = nT + 1
			
# for j in range(tubeNy):
	# for i in range(tubeNx):
		# if nT == tubeNum:
			# break
		# elif j%2 is 0:
			# tubeList.append(np.array([i*tubeDx+tubeRadius,j*tubeDy+tubeRadius, 0, tubeRadius]))
			# nT = nT + 1
		# else:
			# tubeList.append(np.array([i*tubeDx+tubeRadius + tubeDx/2,j*tubeDy+tubeRadius, 0, tubeRadius]))
			# nT = nT + 1
			
for i in range(nIter):
	for v in tubeList:
		tv = np.zeros(4)
		tv[0:] = v[0:]
		tv[0:3] = tv[0:3] + random.uniform(-tubeDy,tubeDy,[1,3])
		#print tv
		overV = overCheckF(tv)
		if overV is None:
			v[0:] = tv[0:]
			
CNT_Forest = ET.Element("CNTForest", xmax = str(cellLength), ymax = str(cellLength), zmax = str(0), tubenum = str(tubeNum), nodenum = str(tubeNum), rmax = str(tubeRadius), rmin = str(tubeRadius))
for v in tubeList:
    tempE = ET.Element("T", r = str(v[3]))
    tempN = ET.Element("N", x = str(v[0]), y = str(v[1]), z = str(v[2]))
    tempE.append(tempN)
    CNT_Forest.append(tempE)
    
# wrap it in an ElementTree instance, and save as XML
tree = ET.ElementTree(CNT_Forest)
tree.write("tritest.xml")

print tubeDx, tubeDy
			