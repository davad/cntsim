from Bin import Bin
'''
Created on Jan 17, 2010

@author: sahar
'''
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

for bx in range(nGrid):
	for by in range(nGrid):
		for bz in range(nGrid):
			binList[bx][by][bz] = Bin(position = np.array([bx*sGrid, by*sGrid, bz*sGrid]), dims = np.array([sGrid, sGrid, sGrid]))
			



