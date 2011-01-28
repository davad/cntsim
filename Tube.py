from numpy import array
class Tube:
	"""A model carbon nanotube"""
	def __init__(self):
		self.baseNode = None
		self.tipNode = None
		self.growthVel = 0
		self.radius = 0
		self.nodeNum = 0
		self.springK = array([0,0])
		self.springLength = 0
		self.springDamp = array([0,0])
		self.maxStrain = 0
		self.stictionDist = 0
		
	
	
