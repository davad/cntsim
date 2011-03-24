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

class baseNode:
	def __init__(self, pos = np.array([0,0,0]), edgePos = np.array([0,0,0]), radius = 0.0, edge = False):
		self.pos = pos
		self.edgePos = edgePos
		self.radius = radius
		self.edge = edge
		

def overCheck(testV):
	tI = int(np.floor(testV[xInd]/sGrid))
	tJ = int(np.floor(testV[yInd]/sGrid))
	if tI < 0:
		tI = 0
	elif tI > nGrid-1:
		tI = nGrid-1
	if tJ < 0:
		tJ = 0
	elif tJ > nGrid-1:
		tJ = nGrid-1
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


field = [None]*nGrid

for i in range(nGrid):
    field[i] = [None]*nGrid
	
	
nT = 0
for j in range(tubeNy):
	for i in range(tubeNx):
		if nT == tubeNum:
			break
		else:
			tTube = np.array([i*tubeDx+tubeRadius,j*tubeDy+tubeRadius, 0, tubeRadius])
			tI = int(np.floor(tTube[xInd]/sGrid))
			tJ = int(np.floor(tTube[yInd]/sGrid))
			tubeList.append(tTube)
			binList[tI][tJ].nodeList.append(tTube)
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
		tv[0:2] = tv[0:2] + random.uniform(-tubeDy,tubeDy,[1,2])
		overV = overCheck(tv)
		for n in range(2):
			if tv[n] > cellLength:
				tv[n] = tv[n] - cellLength
			elif tv[n] < 0:
				tv[n] = tv[n] + cellLength
		#print tv
		if overV is None:
			overV = overCheck(tv)
		if overV is None:
			pI = int(np.floor(v[xInd]/sGrid))
			pJ = int(np.floor(v[xInd]/sGrid))
			nI = int(np.floor(tv[xInd]/sGrid))
			nJ = int(np.floor(tv[xInd]/sGrid))
			if pI != nI or pJ != nJ:
				nList = binList[int(np.floor(v[xInd]/sGrid))][int(np.floor(v[yInd]/sGrid))].nodeList
				for n in range(len(nList)) :
					if (nList[n] == v).all():
						nList.pop(n)
						break
				v[0:] = tv[0:]
				binList[int(np.floor(v[xInd]/sGrid))][int(np.floor(v[yInd]/sGrid))].nodeList.append(v)
			else:
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
			