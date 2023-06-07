from pyautocad import Autocad, APoint
import math
import array
acad = Autocad(create_if_not_exists=True)
acad.prompt("Hello, Autocad from Python\n")
print(acad.doc.Name) 

for i in range(36):
    p1 = APoint(0, 0)
    p2 = APoint(100*math.sin(i/36*2*math.pi), 100*math.cos(i/36*2*math.pi))
    #text = acad.model.AddText(u'Hi %s!' % i, p1, 2.5)
    acad.model.AddLine(p1, p2)


##for i in range(36):
##    p2 = APoint(100*math.sin(i/36*2*math.pi), 100*math.cos(i/36*2*math.pi))
##    #text = acad.model.AddText(u'Hi %s!' % i, p1, 2.5)
##    circle = acad.model.AddCircle(p2, 2)

p = []

for i in range(36+1):
    px = 100*math.sin(i/24*2*math.pi) 
    py = 100*math.cos(i/24*2*math.pi)
    p.append(px)
    p.append(py)

poly = acad.model.AddLightWeightPolyline(array.array("d", p))


  
