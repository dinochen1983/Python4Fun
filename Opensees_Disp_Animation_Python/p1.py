# Importing packages
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import csv
import imageio

def create_gif(image_list, gif_name, duration = 1.0):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))

    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return

#main parameter start
nstep = 1000  ##opensees step
step_size = 100
num_step = int(nstep/step_size)
scr_factor=250.0
zone_height = 60*1000.0 ##60m
center_x = 9000.0
center_y = 9000.0
step_duration_gif = 0.02
#main parameter end

nodex = []
nodey = []
nodez = []
frame_i = []
frame_j = []
with open('node.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        str2 = row['px']
        str3 = row['py']
        str4 = row['pz']
        nodex.append(float(str2))
        nodey.append(float(str3))
        nodez.append(float(str4))

with open('element.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        str2 = row['ki']
        str3 = row['kj']
        frame_i.append(int(str2))
        frame_j.append(int(str3))

node_num = len(nodex)
nframe = len(frame_i)
df1 = pd.read_csv('node0x.out',sep='\s+',header=None)
df2 = pd.read_csv('node0y.out',sep='\s+',header=None)
df3 = pd.read_csv('node0z.out',sep='\s+',header=None)
node_dispx=[]
node_dispy=[]
node_dispz=[]


for j in range(node_num):
    dispx=[]
    dispy=[]
    dispz=[]
    for i in range(len(df1[j+1])):
        dispx.append(df1[j+1][i])
    for i in range(len(df2[j+1])):
        dispy.append(df2[j+1][i])
    for i in range(len(df3[j+1])):
        dispz.append(df3[j+1][i])
    node_dispx.append(dispx)
    node_dispy.append(dispy)
    node_dispz.append(dispz)


fig = plt.figure()
ax1 = Axes3D(fig)

for j in range(num_step):
        plt.clf()
        step = j*step_size
        scr = scr_factor
        ax = fig.add_subplot(111,projection='3d')
        ax.set_zlim(0,zone_height)
        ax.set_xlim(-zone_height/2+center_x,zone_height/2+center_x)
        ax.set_ylim(-zone_height/2+center_y,zone_height/2+center_y)
        str1 = str('step=')+str(j*step_size)
        ax.set_title('time step = '+str(j*step_size))
        for i in range(nframe):
            x1 = nodex[frame_i[i]-1]+node_dispx[frame_i[i]-1][step]*scr
            y1 = nodey[frame_i[i]-1]+node_dispy[frame_i[i]-1][step]*scr
            z1 = nodez[frame_i[i]-1]+node_dispz[frame_i[i]-1][step]*scr
            x2 = nodex[frame_j[i]-1]+node_dispx[frame_j[i]-1][step]*scr
            y2 = nodey[frame_j[i]-1]+node_dispy[frame_j[i]-1][step]*scr
            z2 = nodez[frame_j[i]-1]+node_dispz[frame_j[i]-1][step]*scr
            plt.plot([x1 ,x2],[y1,y2],[z1,z2], 'b',  linewidth=1)   
        ##plt.pause(0.001)
        plt.savefig('images/foo'+str(j)+'.jpg')
        print("step",str(j))
        plt.clf()
        
print("finish gen images")

##gen num_step gif file

fstr = ""
kstr = []
for i in range(num_step):
    fstr = f"images/foo{i}.jpg"
    kstr.append(fstr)
image_list = kstr
gif_name = 'animation.gif'
duration = step_duration_gif

create_gif(image_list, gif_name, duration)
print("finish gif animation")