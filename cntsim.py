'''
Created on Jan 17, 2010

@author: sahar
'''

'''


'''
from Bin import Bin
from Node import Node
import math
import numpy as np
import xml.etree.ElementTree as ET
import Config

settings = Config.read()

meanRad = 4 # Dimensional units in nm
minRad = meanRad/2.0
maxRad = meanRad*1.5
sigmaRad = .45 
bBoxWidth = 300
bBoxLength = 300
pDensity = .05 #Unitless fraction covered by particles
bBoxArea = bBoxLength*bBoxWidth
areaC = 0
ANGULAR_MEAN = np.pi/4.0
ANGULAR_SIGMA = 0.282387/2
THETA_MIN = 0
THETA_MAX = 2*np.pi
NODE_MASS = 10
SEGMENT_LENGTH = 8
TIME_STEP = .1
GROWTH_SPEED = 1
MAX_SEGMENTS = 20 #Defines the end condition
segmentNum = 0
TORSION_K = 1
TORSION_DAMP = 1
LINEAR_K = 1
LINEAR_DAMP = 1

nGrid = int(np.floor(bBoxLength/(maxRad*3))) #number of cells per side of grid
sGrid = float(bBoxWidth)/nGrid #size of grid cells

binList = np.empty([nGrid,nGrid,nGrid],dtype = np.object_)
for bx in range(nGrid):
	for by in range(nGrid):
		for bz in range(nGrid):
			binList[bx][by][bz] = Bin(position = np.array([bx*sGrid, by*sGrid, bz*sGrid]), dims = np.array([sGrid, sGrid, sGrid]))

for bx in range(nGrid):
	for by in range(nGrid):
		for bz in range(nGrid):
			if bx is 0:
				xp = nGrid-1
			else: xp = bx-1
			if by is 0:
				yp = nGrid-1
			else: yp = by-1
			if bz is 0:
				zp = nGrid-1
			else: zp = bz-1
			
			if bx is nGrid-1:
				xn = 0
			else: xn = bx+1
			if by is nGrid-1:
				yn = 0
			else: yn = by+1
			if bz is nGrid-1:
				zn = 0
			else: zn = bz+1
			
			binList[bx][by][bz].neighborList.extend([binList[bx][by][zn], binList[bx][by][zp], binList[bx][yn][bz], binList[bx][yp][bz], binList[xn][by][bz], binList[xp][by][bz]])
			binList[bx][by][bz].neighborList.extend([binList[bx][yn][zn], binList[bx][yn][zp], binList[bx][yp][zn], binList[bx][yp][zp], binList[xn][by][zn], binList[xp][by][zn], binList[xn][by][zp], binList[xp][by][zp], binList[xn][yn][bz], binList[xn][yp][bz], binList[xp][yn][bz], binList[xp][yp][bz]])
			binList[bx][by][bz].neighborList.extend([binList[xn][yn][zn], binList[xn][yn][zp], binList[xn][yp][zn], binList[xn][yp][zp], binList[xp][yn][zn], binList[xp][yn][zp], binList[xp][yp][zn], binList[xp][yp][zp]])


nodeNum = int(np.ceil(bBoxArea*pDensity/(np.pi*meanRad**2)))
tubeList = []
for i in range(nodeNum):
	added = False
	while not added:
		tx = np.random.randint(0,nGrid)
		ty = np.random.randint(0,nGrid)
		tz = 0
		if(binList[tx][ty][tz].nodeList == []):
			binList[tx][ty][tz].nodeList.append(Node(binList[tx][ty][tz].dimList + [.5*sGrid,.5*sGrid,meanRad], NODE_MASS, True))
			tTube = Tube()
			tTube.baseNode = binList[tx][ty][tz].nodeList[0]
			tTube.tipNode = tTube.baseNode
			tTube.radius = meanRad
			tTube.nodeNum = 1
			tTube.growthVel = GROWTH_SPEED
			tTube.springK = np.array([LINEAR_K,TORSION_K])
			tTube.springDamp = np.array([])
			tubeList.append(tTube)
			added = True

for baseNode in baseList:
	phi = np.random.normal(ANGULAR_MEAN, ANGULAR_SIGMA)
	theta = np.random.rand()*THETA_MAX
	newNode = Node(baseNode.pos + SEGMENT_LENGTH * np.array([np.sin(phi)*np.cos(theta), np.sin(phi)*np.sin(theta), np.cos(phi)]), NODE_MASS)
	baseNode.next[0] = newNode
	newNode.prev[0] = baseNode
	phi = np.random.normal(ANGULAR_MEAN, ANGULAR_SIGMA)
	theta = np.random.rand()*THETA_MAX
	newNode = Node(baseNode.next[0].pos + SEGMENT_LENGTH * np.array([np.sin(phi)*np.cos(theta), np.sin(phi)*np.sin(theta), np.cos(phi)]), NODE_MASS)
	baseNode.next[1] = newNode
	baseNode.next[0].next[0] = newNode
	newNode.prev[0] = baseNode.next[0]
	newNode.prev[1] = baseNode
	
segmentNum = segmentNum + 2	

running = False
while running:
	if segmentNum > MAX_SEGMENTS:
		running = False
	
	

	



			
			



