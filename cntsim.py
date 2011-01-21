'''
Created on Jan 17, 2010

@author: sahar
'''
from Bin import Bin
from Node import Node
import math
import numpy as np
import xml.etree.ElementTree as ET

meanRad = 4 # Dimensional units in nm
minRad = meanRad/2.0
maxRad = meanRad*1.5
sigmaRad = .45 
bBoxWidth = 300
bBoxLength = 300
pDensity = .05 #Unitless fraction covered by particles
bBoxArea = bBoxLength*bBoxWidth
areaC = 0

nGrid = int(np.floor(bBoxLength/(maxRad*3))) #number of cells per side of grid
sGrid = float(bBoxWidth)/nGrid #size of grid cells

binList = np.empty([nGrid,nGrid,nGrid],dtype = np.object_)
index = 0
for bx in range(nGrid):
	for by in range(nGrid):
		for bz in range(nGrid):
			binList[bx][by][bz] = Bin(position = np.array([bx*sGrid, by*sGrid, bz*sGrid]), dims = np.array([sGrid, sGrid, sGrid]))
			
nodeNum = int(np.ceil(bBoxArea*pDensity/(np.pi*meanRad**2)))
nodeMap = {}
for i in range(nodeNum):
	added = False
	while not added:
		tx = np.random.randint(0,nGrid)
		ty = np.random.randint(0,nGrid)
		tz = 0
		if(binList[tx][ty][tz].nodeList == []):
			binList[tx][ty][tz].nodeList.append(Node(binList[tx][ty][tz].dimList + [.5*sGrid,.5*sGrid,meanRad]))
			nodeMap[(tx,ty)] = binList[tx][ty][tz].nodeList[0]
			added = True

print nodeMap.keys()


			
			



