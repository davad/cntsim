import numpy as np
import xml.etree.ElementTree as ET

cellLength = 100
tubeRadius = 4
fillFraction = .5

tubeList = []

tubeNum = int(np.floor(fillFraction*cellLength**2/(np.pi*tubeRadius**2)))
#tubeDx = np.floor(cellLength/np.sqrt(tubeNum))
tubeDx = np.sqrt(np.pi)*tubeRadius/(np.sqrt(fillFraction))
tubeDy = tubeDx*np.sqrt(3)/2.0
tubeNx = int(np.floor(cellLength)/np.ceil(tubeDx))
tubeNy = int(np.floor(cellLength)/np.ceil(tubeDy))


nT = 0
# for j in range(tubeNy):
	# for i in range(tubeNx):
		# if nT == tubeNum:
			# break
		# else:
			# tubeList.append(np.array([i*tubeDx+tubeRadius,j*tubeDy+tubeRadius, 0, tubeRadius]))
			# nT = nT + 1
			
for j in range(tubeNy):
	for i in range(tubeNx):
		if nT == tubeNum:
			break
		elif j%2 is 0:
			tubeList.append(np.array([i*tubeDx+tubeRadius,j*tubeDy+tubeRadius, 0, tubeRadius]))
			nT = nT + 1
		else:
			tubeList.append(np.array([i*tubeDx+tubeRadius + tubeDx/2,j*tubeDy+tubeRadius, 0, tubeRadius]))
			nT = nT + 1
			
CNT_Forest = ET.Element("CNTForest", xmax = str(cellLength), ymax = str(cellLength), zmax = str(0), tubenum = str(tubeNum), nodenum = str(tubeNum), rmax = str(tubeRadius), rmin = str(tubeRadius))
for v in tubeList:
    tempE = ET.Element("T", r = str(v[3]))
    tempN = ET.Element("N", x = str(v[0]), y = str(v[1]), z = str(v[2]))
    tempE.append(tempN)
    CNT_Forest.append(tempE)
    
# wrap it in an ElementTree instance, and save as XML
tree = ET.ElementTree(CNT_Forest)
tree.write("tritest.xml")

print tubeDx, tubeDy
			