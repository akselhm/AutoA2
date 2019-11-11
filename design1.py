#design1.py


from shapes.Cylinder import Cylinder
from shapes.Sphere import Sphere
import math
from GA import MyGA

class makeRobot: 

    def __init__(self, button_length, mid_length, top_length):
        self.button_length = button_length
        self.mid_length = mid_length
        self.top_length = top_length
    
    
    def startProtocol(self):
        
        angle1= 30
        angle2= 90
        endingDiameter = 40
        grabberDiameter = 5
        numberOfGrabbers = 20
        
        RadianAngle1= math.radians(angle1)
        
        setxVector=math.tan(math.radians(angle1))
        setxVectorTop=math.tan(math.radians(angle2))

        g1 = Cylinder(0, 0, 0, self.button_length, 15, [0, 0, 1], "RED", "Wood")
        g1.initForNX()

        a1 = Cylinder(0, 0, 0, 15, float(self.button_length), [0, 0, 1], "RED", "Wood")
        a1.initForNX()

        b1 = Sphere(0, 0, float(self.button_length), 20, "BLUE", "Wood")
        b1.initForNX()

        c1 = Cylinder(0, 0, self.button_length, 15, float(self.mid_length), [setxVector, 0, 1], "RED", "Wood")
        c1.initForNX()

        d1 = Sphere(math.sin(RadianAngle1)*self.mid_length, 0,
        math.cos(RadianAngle1)*self.mid_length+self.button_length, 20, "BLUE", "Wood")
        d1.initForNX()
        
        e1 = Cylinder(math.sin(RadianAngle1)*self.mid_length, 0
        ,math.cos(RadianAngle1)*self.mid_length+self.button_length, 15, self.top_length, [setxVectorTop, 0, 1], "RED", "Wood")
        e1.initForNX()
        
        f1= Cylinder(math.sin(RadianAngle1)*self.mid_length+ self.top_length, 0,
        math.cos(RadianAngle1)*self.mid_length+self.button_length, endingDiameter, 10, [setxVectorTop, 0, 1], "RED", "Wood")
        f1.initForNX()
        
        #making the grabber 
        for i in range(0,numberOfGrabbers): 
            #setting angle
            angle = 2*math.pi/numberOfGrabbers*i
            
            g1= Cylinder(math.sin(RadianAngle1)*self.mid_length+ self.top_length+ 10,
            math.cos(angle)*(endingDiameter/2-grabberDiameter/2),
            math.cos(RadianAngle1)*self.mid_length+self.button_length+math.sin(angle)*(endingDiameter/2-grabberDiameter/2),
            grabberDiameter, 30, [setxVectorTop, 0, 1], "RED", "Wood")
            g1.initForNX()
            


        #s1 = Sphere(10, 10, 50, 25, "BLUE", "Wood")
        #s1.initForNX()

        #Substract c1 from s1
        #s1.subtract(c1) 
        #c1.subtractFrom(s1)

popsize = 15
generations = 30 
mutProb = 0.01
radius = 20
myRobot = MyGA(15, 30, 0.01, 20)
arms = myRobot.run()


robotShow= makeRobot(arms[0]*25, arms[1]*25, arms[2]*25)
robotShow.startProtocol()
