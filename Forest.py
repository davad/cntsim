import numpy as np
import Config
from Bin import Bin
from Node import Node
from Tube import Tube
class Forest:
	"""A model carbon nanotube forest"""
	def __init__(self, configFile = None):
		if configFile is None:
			settings = Config.read()
		else:
			settings = Config.read(configFile)
		
		self.meanRad = settings['NODE']['MIN_RADIUS'] # Dimensional units in nm
		self.minRad = settings['NODE']['MEAN_RADIUS']
		self.maxRad = settings['NODE']['MAX_RADIUS']
		self.sigmaRad = settings['NODE']['SIGMA_RADIUS']
		self.bBoxDims = np.array([settings['FOREST']['DIMENSIONS']['MAX_X'],settings['FOREST']['DIMENSIONS']['MAX_Y'],settings['FOREST']['DIMENSIONS']['MAX_Z']])
		self.pDensity = settings['FOREST']['SURFACE_DENSITY'] #Unitless fraction covered by particles
		self.bBoxArea = self.bBoxDims[0]*self.bBoxDims[1]
		self.areaC = 0
		self.ANGULAR_MEAN = settings['SPRINGS']['ANGLES']['MEAN_PHI']
		self.ANGULAR_SIGMA = settings['SPRINGS']['ANGLES']['SIGMA_PHI']
		self.THETA_MIN = settings['SPRINGS']['ANGLES']['MIN_THETA']
		self.THETA_MAX = settings['SPRINGS']['ANGLES']['MAX_THETA']
		self.NODE_MASS = settings['NODE']['MASS']
		self.SEGMENT_LENGTH = 8
		self.TIME_STEP = .1
		self.GROWTH_SPEED = 1
		self.MAX_SEGMENTS = 20 #Defines the end condition
		self.segmentNum = 0
		self.TORSION_K = 1
		self.TORSION_DAMP = 1
		self.LINEAR_K = 1
		self.LINEAR_DAMP = 1

	def loadConfig(self, fileName):
		settings = Config.read(fileName)
		
	def initializeGrid(self):
		self.nGrid = int(np.floor(self.bBoxDims[0]/(self.maxRad*3))) #number of cells per side of grid
		self.sGrid = float(self.bBoxDims[0])/self.nGrid #size of grid cells
		self.binList = np.empty([self.nGrid,self.nGrid,self.nGrid],dtype = np.object_)
		
		for bx in range(self.nGrid):
			for by in range(self.nGrid):
				for bz in range(self.nGrid):
					self.binList[bx][by][bz] = Bin(position = np.array([bx*self.sGrid, by*self.sGrid, bz*self.sGrid]), dims = np.array([self.sGrid, self.sGrid, self.sGrid]))
	
		for bx in range(self.nGrid):
					for by in range(self.nGrid):
						for bz in range(self.nGrid):
							if bx is 0:
								xp = self.nGrid-1
							else: xp = bx-1
							if by is 0:
								yp = self.nGrid-1
							else: yp = by-1
							if bz is 0:
								zp = self.nGrid-1
							else: zp = bz-1
							
							if bx is self.nGrid-1:
								xn = 0
							else: xn = bx+1
							if by is self.nGrid-1:
								yn = 0
							else: yn = by+1
							if bz is self.nGrid-1:
								zn = 0
							else: zn = bz+1
							
							self.binList[bx][by][bz].neighborList.extend([self.binList[bx][by][zn], self.binList[bx][by][zp], self.binList[bx][yn][bz], self.binList[bx][yp][bz], self.binList[xn][by][bz], self.binList[xp][by][bz]])
							self.binList[bx][by][bz].neighborList.extend([self.binList[bx][yn][zn], self.binList[bx][yn][zp], self.binList[bx][yp][zn], self.binList[bx][yp][zp], self.binList[xn][by][zn], self.binList[xp][by][zn], self.binList[xn][by][zp], self.binList[xp][by][zp], self.binList[xn][yn][bz], self.binList[xn][yp][bz], self.binList[xp][yn][bz], self.binList[xp][yp][bz]])
	
						self.binList[bx][by][bz].neighborList.extend([self.binList[xn][yn][zn], self.binList[xn][yn][zp], self.binList[xn][yp][zn], self.binList[xn][yp][zp], self.binList[xp][yn][zn], self.binList[xp][yn][zp], self.binList[xp][yp][zn], self.binList[xp][yp][zp]])
	
	def generateBaseNodes(self):
		self.nodeNum = int(np.ceil(self.bBoxArea*self.pDensity/(np.pi*self.meanRad**2)))
		self.tubeList = []
		for i in range(self.nodeNum):
			added = False
			while not added:
				tx = np.random.randint(0,self.nGrid)
				ty = np.random.randint(0,self.nGrid)
				tz = 0
				if(self.binList[tx][ty][tz].nodeList == []):
					self.binList[tx][ty][tz].nodeList.append(Node(self.binList[tx][ty][tz].dimList + [.5*self.sGrid,.5*self.sGrid,self.meanRad], self.NODE_MASS, True))
					tTube = Tube()
					tTube.baseNode = self.binList[tx][ty][tz].nodeList[0]
					tTube.tipNode = tTube.baseNode
					tTube.radius = self.meanRad
					tTube.nodeNum = 1
					tTube.growthVel = self.GROWTH_SPEED
					tTube.springK = np.array([self.LINEAR_K,self.TORSION_K])
					tTube.springDamp = np.array([])
					self.tubeList.append(tTube)
					added = True
	
	def addBaseSegments(self):
		for tube in self.tubeList:
			phi = np.random.normal(self.ANGULAR_MEAN, self.ANGULAR_SIGMA)
			theta = np.random.rand()*self.THETA_MAX
			newNode = Node(tube.baseNode.pos + self.SEGMENT_LENGTH * np.array([np.sin(phi)*np.cos(theta), np.sin(phi)*np.sin(theta), np.cos(phi)]), self.NODE_MASS)
			tube.baseNode.next[0] = newNode
			newNode.prev[0] = tube.baseNode
			phi = np.random.normal(self.ANGULAR_MEAN, self.ANGULAR_SIGMA)
			theta = np.random.rand()*self.THETA_MAX
			newNode = Node(tube.baseNode.next[0].pos + self.SEGMENT_LENGTH * np.array([np.sin(phi)*np.cos(theta), np.sin(phi)*np.sin(theta), np.cos(phi)]), self.NODE_MASS)
			tube.baseNode.next[1] = newNode
			tube.baseNode.next[0].next[0] = newNode
			newNode.prev[0] = tube.baseNode.next[0]
			newNode.prev[1] = tube.baseNode
			
		self.segmentNum = self.segmentNum + 2	
	
	def collisionCheck():
		pass
		
	
	def integrateForces():
		pass
	
	def step():
		pass
	
	
	