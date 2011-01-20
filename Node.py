from numpy import Array

class Node:
    """A node representing one element of a model carbon nanotube"""
	def __init__(self):
		self.prev = [None, None, None]
		self.next = [None, None, None]
		self.loc = array([0 0 0])
		self.vel = array([0 0 0])
		self.force = array([0 0 0])
		self.midLoc = array([0 0 0])
		self.midVel = array([0 0 0])
		self.midForce = array([0 0 0])
		self.mass = 0
		self.fixed = false
		


	
