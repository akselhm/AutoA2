#Basic class in Python
#NXPython/shapes/Block.py
import math
import NXOpen
import NXOpen.Annotations
import NXOpen.Features
import NXOpen.GeometricUtilities
import NXOpen.Preferences
class Block:

#    length = 0         # class variable shared by all instances
#	width = ...
	
	def getVolume(self):
		return self.length * self.width * self.height
    
	def __init__(self, x, y, z, length, width, height, color, material):
		self.length = length    # instance variable unique to each instance
		self.width = width
		self.height = height
		self.x = x    
		self.y = y
		self.z = z
		self.color = color
		self.material = material
		
	def initForNX(self, x, y, z, length, width, height, color, material):
		theSession  = NXOpen.Session.GetSession()
		workPart = theSession.Parts.Work
		
		#   The block
		blockfeaturebuilder1 = workPart.Features.CreateBlockFeatureBuilder(NXOpen.Features.Block.Null)
		blockfeaturebuilder1.Type = NXOpen.Features.BlockFeatureBuilder.Types.OriginAndEdgeLengths

		origBlock = NXOpen.Point3d(float(x), float(y), float(z))
		blockfeaturebuilder1.SetOriginAndLengths(origBlock, str(length), str(width), str(height))
		blockfeaturebuilder1.BooleanOption.Type = NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Create
		
		blockfeaturebuilder1.Commit()
		blockfeaturebuilder1.Destroy() 
		
	def initForNX(self):
		theSession  = NXOpen.Session.GetSession()
		workPart = theSession.Parts.Work
		
		#   The block
		blockfeaturebuilder1 = workPart.Features.CreateBlockFeatureBuilder(NXOpen.Features.Block.Null)
		blockfeaturebuilder1.Type = NXOpen.Features.BlockFeatureBuilder.Types.OriginAndEdgeLengths

		origBlock = NXOpen.Point3d(float(self.x), float(self.y), float(self.z))
		blockfeaturebuilder1.SetOriginAndLengths(origBlock, str(self.length), str(self.width), str(self.height))
		blockfeaturebuilder1.BooleanOption.Type = NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Create
		
		blockfeaturebuilder1.Commit()
		blockfeaturebuilder1.Destroy() 
		
		
#block1 = Block(10, 10, 10)
#block2 = Block(3, 5, 5)
#print("Block 1 volume:", block1.getVolume())
#print("Block 2 volume:", block2.getVolume())
#print("Accessing an attribute:", block1.length)

#for x in range(1, 30, 3):
#	print("x:", x)
