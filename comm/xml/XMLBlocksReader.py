# blocks.xml reader
# NXPython/comm/xml/XMLBlocksReader.py
import xml.etree.ElementTree
import sys 
sys.path.append('...') # First going to the NXPython folder level

from shapes.Block import Block
from shapes.Cylinder import Cylinder
from shapes.Sphere import Sphere


class XMLBlocksReader:
	
	def __init__(self):
		print("XML Parser initialized")
		
	def parse(self, root):
		for node in root.findall('block'):
			theShape = None
			for elem in node:
				if(elem.tag == "type"):
					typeText = elem.text.strip() #removing extra spaces with strip() function
					if(typeText == "ug_block"):
						#Initialize block here
						theShape = Block(0, 0, 0, 10, 10, 10, "RED", "Wood")
					elif(typeText == "ug_cylinder"):
						#Initialize cylinder here
						theShape = Cylinder(0, 0, 0, 10, 10, [0, 0, 1], "YELLOW", "Plastic")
					else: #(typeText == "ug_sphere")
						#Initialize shpere here
						theShape = Sphere(0, 0, 0, 10, "GREEN", "Stone")
				elif(elem.tag=="x"):
					theShape.x = float(elem.text)
				elif(elem.tag=="y"):
					theShape.y = float(elem.text)
				elif(elem.tag=="z"):
					theShape.z = float(elem.text)
				elif(elem.tag=="length"):
					theShape.length = float(elem.text)
				elif(elem.tag=="width"):
					theShape.width = float(elem.text)
				elif(elem.tag=="heigth"):
					theShape.height = float(elem.text)
				elif(elem.tag=="direction"):
					theShape.direction = float(elem.text)
				elif(elem.tag=="color"):
					theShape.color = float(elem.text)
				else: #(elem.tag=="material")
					theShape.material = float(elem.text)
			theShape.initForNX()
			

		


