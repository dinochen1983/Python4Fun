import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull


kx = []
ky = []
kz = []
num = 0
with open('pmm_etesec.txt') as f:
    lines = f.readlines()

maxx=0.0
minx=0.0
maxy=0.0
miny=0.0
maxz=0.0
minz=0.0

for num in range(0, len(lines)-2):
    str1 = lines[num+2]
    str2 = str1[1:1+10]
    str3 = str1[13:13+10]
    str4 = str1[25:25+10]
    kz.append(float(str2))
    kx.append(float(str3))
    ky.append(float(str4))
    maxx = max(maxx,kx[num])
    minx = min(minx,kx[num])
    maxy = max(maxy,ky[num])
    miny = min(miny,ky[num])
    maxz = max(maxz,kz[num])
    minz = min(minz,kz[num])


points = []


for num in range(0,len(kx)):
    points.append(np.array([kx[num],ky[num],kz[num]]))


pts = np.array(points)
N = len(kx)
hull = ConvexHull(points)



fig = plt.figure()
ax = Axes3D(fig)
vertices = [pts[s] for s in hull.simplices]
color1 =color=[146/255,223/255,243/255]
triangles = Poly3DCollection(vertices, edgecolor='k', facecolors=color1, linewidths=0.2, alpha=0.5)
##facecolors='b' ,edgecolor='k',linewidths=0.2, alpha=0.2
ax.add_collection3d(triangles)


ftx = 1.2
fty = 1.2
ftz = 1.2

ax.set_xlim(minx*ftx, maxx*ftx)
ax.set_ylim(miny*fty, maxy*fty)
ax.set_zlim(minz*ftz, maxz*ftz)

fig.canvas.manager.set_window_title('PMM Curve')


plt.show()