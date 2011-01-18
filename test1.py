'''
Created on May 19, 2010

@author: sahar
'''
import numpy as np
import xml.etree.ElementTree as ET

meanR = 4 # Dimensional units in nm
minR = meanR/2.0
maxR = meanR*1.5
sigmaR = .45 
bBoxWidth = 300
bBoxLength = 300
bBoxHeight = 288
xInd = 0
yInd = 1
zInd = 2
rInd = 3
vLength = 4
pFrac = .5 #Unitless fraction covered by particles
nPAvg = (pFrac*bBoxWidth*bBoxLength)/(np.pi*(meanR**2))
areaF = bBoxLength*bBoxWidth
areaC = 0;
retries = 4 #Not used yet

nGrid = int(np.floor(bBoxLength/(maxR*3))) #number of cells per side of grid
sGrid = float(bBoxWidth)/nGrid #size of grid cells

field = [None]*nGrid

for i in range(nGrid):
    field[i] = [None]*nGrid

####################################################
#                FUNCTION DEFINITIONS              #
####################################################

def positionCheck(testV):
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
    
'''  
def fixOverlap(vVar, vFix):
    cV = np.zeros(3);
    cV[xInd] = vVar[xInd]-vFix[xInd]
    cV[yInd] = vVar[yInd]-vFix[yInd]
    cV[zInd] = vVar[zInd]-vFix[zInd]
    unit = (cV*cV)
    mag = np.sqrt(unit[xInd]+unit[yInd]+unit[zInd])
    unit = cV/mag
    ovr = vVar[rInd]+vFix[rInd]-mag
    shift = ovr*unit
    vVar[xInd] += shift[xInd]
    vVar[yInd] += shift[yInd]
    vVar[zInd] += shift[zInd]
    for i in range(np.size(vVar)-1):
        if vVar[i] < 0 + vVar[rInd]: 
            vVar[i] = 0 + vVar[rInd]
        elif vVar[i] > bBoxWidth - vVar[rInd]:
            vVar[i] = bBoxWidth - vVar[rInd]
    vVar[zInd] = 0
    return vVar
 '''  
def fixOverlap(vVar, vFix):
    return vVar
def printField():
    index = 1  
    for i in range(nGrid):
        for j in range(nGrid):
            if field[i][j] != None:
                if len(np.shape(field[i][j])) >= 2:
                    print np.shape(field[i][j])
                    for v in field[i][j]:
                        print str(v)  + " " + str(index)
                        index+=1
                else:
                    print str((1,4))
                    print str(field[i][j]) + " " + str(index)
                    index+=1 
    

####################################################
#          CNT POSITION GENERATION SCRIPT          #
####################################################

coords = np.zeros(4)
tempR = np.random.normal(meanR, sigmaR)
if tempR < minR:
    tempR = minR
elif tempR > maxR:
    tempR = maxR

coords[rInd]= tempR
coords[xInd] = np.random.uniform(coords[rInd], bBoxWidth - coords[rInd])
coords[yInd] = np.random.uniform(coords[rInd], bBoxLength - coords[rInd])
coords[zInd] = 0
fI= int(np.floor(coords[xInd]/sGrid))
fJ= int(np.floor(coords[yInd]/sGrid))

areaC = (coords[rInd]**2)*np.pi
field[fI][fJ] = coords

del tempR, fI, fJ, i

while areaC/areaF < pFrac:
    addBool = True
    tempArray = np.zeros(4)
    tempR = np.random.normal(meanR, sigmaR)
    if tempR < minR:
        tempR = minR
    elif tempR > maxR:
        tempR = maxR
    tempArray[rInd] = tempR
    tempArray[xInd] = np.random.uniform(tempArray[rInd], bBoxWidth - tempArray[rInd])
    tempArray[yInd] = np.random.uniform(tempArray[rInd], bBoxLength - tempArray[rInd])
    tempArray[zInd] = 0
    overV = positionCheck(tempArray)
    if overV != None:
        tempArray = fixOverlap(tempArray, overV)
        if positionCheck(tempArray) != None:
            addBool = False
    if addBool:
        fI = int(np.floor(tempArray[xInd]/sGrid))
        fJ = int(np.floor(tempArray[yInd]/sGrid))
        if field[fI][fJ] == None:
            field[fI][fJ] = tempArray
        else:
            field[fI][fJ] = np.vstack((field[fI][fJ],tempArray))
        areaC += (tempArray[rInd]**2)*np.pi
        coords = np.vstack((coords, tempArray))
    del tempR, tempArray



#for v in coords:
#    print v

#print "Number of tubes: " + str(np.shape(coords))


#Write to XML File

tubeNum = np.shape(coords)[0]
nodeNum = tubeNum

print "Number of tubes in generated forest: " + str(tubeNum)
print "Number of nodes in generated forest: " + str(nodeNum)
    

# build a tree structure
CNT_Forest = ET.Element("CNTForest", xmax = str(bBoxWidth), ymax = str(bBoxLength), zmax = str(bBoxHeight), tubenum = str(tubeNum), nodenum = str(nodeNum), rmax = str(maxR), rmin = str(minR))
for v in coords:
    tempE = ET.Element("T", r = str(v[rInd]))
    tempN = ET.Element("N", x = str(v[xInd]), y = str(v[yInd]), z = str(v[zInd]))
    #print str(v)
    #tempstring = ""
    #for itr in range(len(v)-1):
        #tempstring += str(v[itr]) + ", "
    #tempstring += str(v[len(v)-1])
    #tempN.text = tempstring
    tempE.append(tempN)
    CNT_Forest.append(tempE)
    
# wrap it in an ElementTree instance, and save as XML
tree = ET.ElementTree(CNT_Forest)
tree.write("xmltest.xml")
