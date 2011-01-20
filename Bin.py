from numpy import array
class Bin:
	"""A bin representing one unit of 3D space for fast collision handling"""
	def __init__(self, position = array([0,0,0]), dims = array([0,0,0])):
		self.nodeList = []
		self.neighborList = []
		self.origin = position
		self.dimList = dims
		
		


	
