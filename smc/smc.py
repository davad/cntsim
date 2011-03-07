def makeSMC():
	nodeNum = computeNodeNumber()
	if nodeNum is 0 or 1 or 2 or 8:
		#Config. 0; Config. 1; Configs. 2-4; Config. 22
		return 0 #No triangle
	elif nodeNum is 3:
		computeSums (Ci,Cj,Ck)
		if not (Ci%3 and Cj%3 and Ck%3)
		#Config. 5: One type I triangle
		buildTriangles(nodes)
		return 1
		else
		return 0 #Config. 6-7
		break
	elif nodeNum is 4:
		(Ci,Cj,Ck)  =  computeSums()
		if not (Ci%4 and Cj%4 and Ck%4)
			#Config.8: Two type I triangles on a face
			buildTriangles(nodes)
		return 2
		if Ci is 2 and Cj is 2 and Ck is 2:
			return 0 #Config. 10 and 13: No triangle
		if Ci is not 2 and Cj is not 2 and Ck is not 2:
		#	Config.9: One type III triangle
			buildTriangles(nodes,interfaceNodes)
			buildTriangles(interfaceNodes)
			return 1
		Ct = Ci%4 + Cj%4 + Ck%4
		if not (Ct%2):
			#Configs. 11, 14: Two type II triangles
			buildTriangles (nodes) #by nested loops
			return 2
		else:
			#Config.12: One type I triangle
			findIsolatedNodes(nodes,isolatedNodes)
			switchStatus(isolatedNode[0]) #We are in Config.5
			buildTriangles(nodes)
			return 1
		break
	elif nodeNum is 5:
		computeSums (Ci,Cj,Ck)
		if not ((Ci-1)%3 and (Cj-1)%3 and (Cj-1)%3):
			#Config.17: Two type II triangles
			buildTriangles(nodes,interfaceNodes)
			# only 4 nodes 
			buildTriangles(interfaceNodes) 
			#by nested loops
			return 2
		if findIsolatedNodes(nodes,isolatedNodes):
			#Config.15: 1 type III triangle
			switchStatus(isolatedNode[0]) #we are in Config. 9
			buildTriangles(nodes)
			return 1
		else:
			#Config.16: 2 type II and one type III triangles
			#Build all triangles, compute Nn2 for each of them
			buildTriangles(nodes,Triangles,NTriangles,Nn2[NTriangles])
			for iTriangle = 0 to NTriangles:
				if Nn2 = 3:
					storeTriangle(iTriangle)#type III identified
			#Construction of the remaining type II triangles
			#Find negative vertex with 3 positive neighbors
			for ivertex 0 to 7:
				if vertex[ivertex] = NEGATIVE:
					findPositiveNeighbors(ivertex,neighborNum,neighbors)
					if neighborNum:
						switchStatus (ivertex) #we are in Config. 20
						buildTriangles(nodes)
						addStoredTriangle()
						return 3
		break
	elif nodeNum is 6:
		(Ci,Cj,Ck) = computeSums()
		Ct  = Ci%6 + Cj%6 + Ck%6
		if Ct%2 and not (Ci%6 = Cj%6 and Ck%6 = Ci%6):
			#Config. 20: 2 type II triangles on a plane
			buildTriangles(nodes,interfaceNodes)
			buildTriangles(interfaceNodes)
			return 2
		else:
			#Config. 18-19: two type III triangles
			for ivertex 0 to 7
				if vertex[ivertex] = NEGATIVE
					findPositiveNeighbors(ivertex,neighborNum,neighbors)
					if neighborNum is 3:
						buildTriangle(neighbors)
			return 2
		break
	elif nodeNum is: 7
		#Config. 21: one type III triangle
		for ivertex in range(0, 7)
			if vertex[ivertex] = NEGATIVE
				findPositiveNeighbors(ivertex,neighborNum,neighbors)
				if neighborNum is 3:
					buildTriangle(neighbors)
			return 1
		break
		
		
def computeNodeNumber():
	pass
	
def computeSums():
	pass
	
def findPositiveNeighbors(ivertex,neighborNum,neighbors):
	pass
	
def buildTriangles():
	pass
	
def buildTriangle():
	pass

def switchStatus():
	pass
	
def findIsolatedNodes():
	pass
	
def storeTriangle():
	pass
	
def addStoredTriangle():
	pass
	
