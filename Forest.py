from numpy import Array
class Forest:
    """A model carbon nanotube forest"""
	def __init__(self):
		self.tubes = None
		self.gravity = None
		self.dragC = None
		self.forestDims = Array([0 0 0])
		#Stores minimum and maximum radius of tubes in Forest
		self.minR = 0
		self.meanR = 0
		self.maxR = 0
		self.sigmaR = 0
		self.cellSize = 0 #Side length of an individual cell in the Forest grid system
		self.fillFrac = 0 #fraction of floor area covered by CNT nodes
		self.segmentLength = 0 #Current scheme uses homogeneous segment length
		self.gridDims = Array([0 0 0])
		self.thetaMin = 0
		self.thetaMax = 0
		self.phiMean = 0
		self.phiSigma = 0
		self.segmentNum = 0 #Current scheme uses a fixed number of CNT lengths
		self.gridNumX = 0 #Number of rows and columns
		self.gridNumY = 0
		self.tubeNum = 0 #Number of tubes and nodes
		self.nodeNum = 0
		
	def generateBaseNodes():
		pass
		
	def loadConfig(filename):
		pass
		
	

	
	
