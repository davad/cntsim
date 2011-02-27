import xml.etree.ElementTree as ET
import Config

FILE_NAME = 'Test Data/A_For.xml'
xml = ET.parse(FILE_NAME)
CNTForest = xml.getroot()

nodeNum = int(CNTForest.attrib["nodenum"])
tubeNum = int(CNTForest.attrib["tubenum"])

minRadius = float(CNTForest.attrib["rmin"])
maxRadius = float(CNTForest.attrib["rmax"])

dimensions = [float(CNTForest.attrib["xmax"]),float(CNTForest.attrib["ymax"]),float(CNTForest.attrib["zmax"])]

N = nodeNum/tubeNum

radii = []
extracted_forest = []

for tube in CNTForest.getiterator("T"):
    radii.append(float(tube.attrib["r"]))
    extracted_tube = []
    for node in tube.getiterator("N"):
        extracted_tube.append([float(node.attrib["x"]),float(node.attrib["y"]),float(node.attrib["z"])])
    extracted_forest.append(extracted_tube)

Config.write(extracted_forest, 'extracted_forest.json')
Config.write(radii, 'extracted_radii.json')
