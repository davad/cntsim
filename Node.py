from numpy import array
class Node:
	"""A node representing one element of a model carbon nanotube"""
	def __init__(self, pos = array([0.0, 0.0, 0.0]), mass = 1, fixed = False):
		self.prev = [None, None]
		self.next = [None, None]
		self.springConst = array([0.0, 0.0 , 0.0, 0.0])
		self.restLength = array([0.0, 0.0 , 0.0, 0.0])
		self.pos = pos
		self.vel = array([0.0, 0.0, 0.0])
		self.force = array([0.0, 0.0, 0.0])
		self.midPos = array([0.0, 0.0, 0.0])
		self.midVel = array([0.0, 0.0, 0.0])
		self.midForce = array([0.0, 0.0, 0.0])
		self.mass = mass
		self.fixed = fixed
		


	
