import numpy as np
from numpy import random
import xml.etree.ElementTree as ET
from Bin import Bin

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

xInd = 0
yInd = 1
zInd  = 2
rInd = 3
nIter = 500;


nGrid = int(np.floor(cellLength/(tubeRadius*3))) #number of cells per side of grid
sGrid = float(cellLength)/nGrid #size of grid cells
binList = np.empty([nGrid,nGrid],dtype = np.object_)
	
def overCheck(testV):
	for node in tubeList:
		if np.inner( testV[0:3]-node[0:3],testV[0:3]-node[0:3] ) < 4*(tubeRadius)**2:
			return node
	# for node in binList[tI][tJ].nodeList:
		# if np.inner(testV[0:3]-node[0:3],testV[0:3]-node[0:3] ) < 4*(tubeRadius)**2:
			# return node
	# for nbr in binList[tI][tJ].neighborList:
		# for node in nbr.nodeList:
			# if np.inner(testV[0:3]-node[0:3],testV[0:3]-node[0:3] ) < 4*(tubeRadius)**2:
				# return node
	#return None
	testV2 = np.zeros(4)
	testV2[0:] = testV[0:]
	for i in range(2):
		if testV2[i] + tubeRadius > cellLength:
			testV2[i] = testV2[i] - cellLength
		elif testV2[i] - tubeRadius < 0:
			testV2[i] = testV2[i] + cellLength

	for node in tubeList:
		if np.inner( testV2[0:3]-node[0:3],testV2[0:3]-node[0:3] ) < 4*(tubeRadius)**2:
			return node

for bx in range(nGrid):
	for by in range(nGrid):
		binList[bx][by] = Bin(position = np.array([bx*sGrid, by*sGrid]), dims = np.array([sGrid, sGrid]))

for bx in range(nGrid):
	for by in range(nGrid):
		if bx is 0:
			xp = nGrid-1
		else: xp = bx-1
		if by is 0:
			yp = nGrid-1
		else: yp = by-1
		
		if bx is nGrid-1:
			xn = 0
		else: xn = bx+1
		if by is nGrid-1:
			yn = 0
		else: yn = by+1
		#Clockwise order starting from top
		binList[bx][by].neighborList.extend( [binList[bx][yn],binList[xn][yn],binList[xn][by],binList[xn][yp],binList[bx][yp],binList[xp][yp],binList[xp][by],binList[xp][yn]])
	
nT = 0
for j in range(tubeNy):
	for i in range(tubeNx):
		if nT == tubeNum:
			break
		else:
			tNode = np.array([i*tubeDx+tubeRadius,j*tubeDy+tubeRadius, 0, tubeRadius])
			tI = int(np.floor(tNode[xInd]/sGrid))
			tJ = int(np.floor(tNode[yInd]/sGrid))
			tubeList.append(tNode)
			binList[tI][tJ].nodeList.append(tNode)
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
	for n in tubeList:
		tv = np.zeros(4)
		tv[0:] = n[0:]
		tv[0:2] = tv[0:2] + random.uniform(-tubeDy,tubeDy,[1,2])
		for i in range(2):
			if tv[i] > cellLength:
				tv[i] = tv[i] - cellLength
			elif tv[i] < 0:
				tv[i] = tv[i] + cellLength
		overV = overCheck(tv)
		if overV is None:
			pI = int(np.floor(n[xInd]/sGrid))
			pJ = int(np.floor(n[xInd]/sGrid))
			nI = int(np.floor(tv[xInd]/sGrid))
			nJ = int(np.floor(tv[xInd]/sGrid))
			if pI != nI or pJ != nJ:
				nList = binList[int(np.floor(n[xInd]/sGrid))][int(np.floor(n[yInd]/sGrid))].nodeList
				for i in range(len(nList)) :
					if (nList[i] == n).all():
						nList.pop(i)
						break
				n[0:] = tv[0:]
				binList[int(np.floor(n[xInd]/sGrid))][int(np.floor(n[yInd]/sGrid))].nodeList.append(n)
			else:
				n[0:] = tv[0:]
			

edgeList = []
for n in tubeList:
	edgeX = False
	edgeY = False
	tv1 = np.zeros(4)
	tv1[0:] = n[0:]
	tList = []
	if n[xInd] + tubeRadius > cellLength:
		edgeX = True
		tv2 = np.zeros(4)
		tv2[0:] = n[0:]
		tv2[xInd] = tv2[xInd] - cellLength
		tv1[xInd] = tv1[xInd] - cellLength
		tList.append(tv2)
	elif n[xInd] - tubeRadius < 0:
		edgeX = True
		tv3 = np.zeros(4)
		tv3[0:] = n[0:]
		tv3[xInd] = tv3[xInd] + cellLength
		tv1[xInd] = tv1[xInd] + cellLength
		tList.append(tv3)
	if n[yInd] + tubeRadius > cellLength:
		edgeY = True
		tv4 = np.zeros(4)
		tv4[0:] = n[0:]
		tv4[yInd] = tv4[yInd] - cellLength
		tv1[yInd] = tv1[yInd] - cellLength
		tList.append(tv4)
	elif n[yInd] - tubeRadius < 0:
		edgeY = True
		tv5 = np.zeros(4)
		tv5[0:] = n[0:]
		tv5[yInd] = tv5[yInd] + cellLength
		tv1[yInd] = tv1[yInd] + cellLength
		tList.append(tv5)

	if edgeX and edgeY:
		tList.append(tv1)
		edgeList.extend(tList)
		print "corner!"
	elif edgeX or edgeY:
		edgeList.extend(tList)

tubeList.extend(edgeList)

tubeNum = tubeNum + len(edgeList)
		
			
CNT_Forest = ET.Element("CNTForest", xmax = str(cellLength), ymax = str(cellLength), zmax = str(0), tubenum = str(tubeNum), nodenum = str(tubeNum), rmax = str(tubeRadius), rmin = str(tubeRadius))
for n in tubeList:
    tempE = ET.Element("T", r = str(n[3]))
    tempN = ET.Element("N", x = str(n[0]), y = str(n[1]), z = str(n[2]))
    tempE.append(tempN)
    CNT_Forest.append(tempE)
    
# wrap it in an ElementTree instance, and save as XML
tree = ET.ElementTree(CNT_Forest)
tree.write("tritest.xml")

print tubeDx, tubeDy
			