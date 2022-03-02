import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull

import csv


kx = []
ky = []
kz = []

for ang in range(0, 6):
    with open('pmm_xtract.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            str2 = row['a'+str(ang*3+1)]
            str3 = row['a'+str(ang*3+2)]
            str4 = row['a'+str(ang*3+3)]
            kz.append(float(str2))
            kx.append(float(str3))
            ky.append(float(str4))

X = np.array(kx)
Y = np.array(ky)
Z = np.array(kz)

maxx=np.max(X)
minx=np.min(X)
maxy=np.max(Y)
miny=np.min(Y)
maxz=np.max(Z)
minz=np.min(Z)


points = []

for num in range(0,len(kx)):
    points.append(np.array([kx[num],ky[num],kz[num]]))

pts = np.array(points)
N = len(kx)
hull = ConvexHull(points)

fig = plt.figure()
ax = Axes3D(fig)
vertices = [pts[s] for s in hull.simplices]
color1 =color=[146/255,223/255,243/255]  ## color
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