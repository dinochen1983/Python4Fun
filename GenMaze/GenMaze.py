import math
import random
from PIL import Image, ImageFont,ImageDraw
import wx


class Tgrid:
    def __init__(self,px,py,visited,wall1,wall2,wall3,wall4):
        self.px=px
        self.py=py
        self.visited=visited
        self.wall1=wall1
        self.wall2=wall2
        self.wall3=wall3
        self.wall4=wall4

class Ttank:
    def __init__(self,px,py,dir):
        self.px = px 
        self.py = py
        self.dir = dir


class Tpath:
    def __init__(self,px,py):
        self.px = px 
        self.py = py




def creat_grid():
    global grids
    global ng
    for i in range(ng+1):
        xgrids=list()
        for j in range(ng+1):
            px=i
            py=j
            visited=False
            wall1=True
            wall2=True
            wall3=True
            wall4=True
            grid = Tgrid(px,py,visited,wall1,wall2,wall3,wall4)
            xgrids.append(grid)
        grids.append(xgrids)


def set_first_grid():
    global grids
    grids[0][0].visited = True


def draw_grid():
    global grids
    global ng
    maze_size = 160.0
    sx = 250
    sy = 250
    sz = maze_size/ng
    im01 =Image.open("image1.jpg")
    draw =ImageDraw.Draw(im01)
    centerx = im01.size[0]/2
    centery = im01.size[1]/2


    for i in range(ng):
        for j in range(ng):
            ex=-centerx+grids[i][j].px*sz*2
            ey=-centery+grids[i][j].py*sz*2     
            ax=sx+ex-sz
            ay=sy+ey-sz
            bx=sx+ex+sz
            by=sy+ey+sz
            if grids[i][j].wall1:
                draw.line((ax,ay,ax,by), fill ="black", width = 2) 
            if grids[i][j].wall3:
                draw.line((bx,ay,bx,by), fill ="black", width = 2) 
            if grids[i][j].wall4:
                draw.line((ax,ay,bx,ay), fill ="black", width = 2) 
            if grids[i][j].wall2:
                draw.line((ax,by,bx,by), fill ="black", width = 2)  

    ##font = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 12)  
    ##text = 'GEN MAZE'
    ##draw.text((5, 5), text, font = font, align ="left", fill="black")    
    im01.save("image2.jpg")   



def check_near_grid(x,y):
    global ng
    global grids
    dir1 = True
    dir2 = True
    dir3 = True
    dir4 = True
    if (x<=0):
        dir2 = False
    if (y<=0):
        dir3 = False
    if (x>=ng-1):
        dir1 = False
    if (y>=ng-1):
        dir4 = False
    #check grid visited
    if (grids[x+1][y].visited == True):
        dir1= False
    if (grids[x-1][y].visited == True):
        dir2= False
    if (grids[x][y-1].visited == True):
        dir3= False
    if (grids[x][y+1].visited == True):
        dir4= False    

    dir0 = False
    if (dir1)or(dir2)or(dir3)or(dir4):
        dir0= True
    
    return dir1,dir2,dir3,dir4,dir0


def gen_maze():
    global ng
    global grids
    global npath
    global path
    global tank
    path1=Tpath(0,0)
    dir0 = False
    dir1 = False
    dir2 = False
    dir3 = False
    dir4 = False
    tank.dir = random.randint(1,4)
   
    dir1,dir2,dir3,dir4,dir0 = check_near_grid(tank.px,tank.py)
    go_back=False

    if (not dir1)and(not dir2)and (not dir3) and (not dir4):
        go_back=True
    
    if (tank.dir==1)and(dir1):
        grids[tank.px][tank.py].wall3=False
        grids[tank.px+1][tank.py].wall1=False
        tank.px = tank.px +1
        path1.px = tank.px
        path1.py = tank.py
        path.append(path1)
        npath = npath+1

    if (tank.dir==2)and(dir2):
        grids[tank.px][tank.py].wall1=False
        grids[tank.px-1][tank.py].wall3=False
        tank.px = tank.px -1
        path1.px = tank.px
        path1.py = tank.py
        path.append(path1)
        npath = npath+1

    if (tank.dir==3)and(dir3):
        grids[tank.px][tank.py].wall4=False
        grids[tank.px][tank.py-1].wall2=False
        tank.py = tank.py -1
        path1.px = tank.px
        path1.py = tank.py
        path.append(path1)
        npath = npath+1     

    if (tank.dir==4)and(dir4):
        grids[tank.px][tank.py].wall2=False
        grids[tank.px][tank.py+1].wall4=False
        tank.py = tank.py +1
        path1.px = tank.px
        path1.py = tank.py
        path.append(path1)
        npath = npath+1

    if (go_back):
        for j in range(npath):
            dir1,dir2,dir3,dir4,dir0 = check_near_grid(path[j].px,path[j].py) 
            if (dir0):
                go_back=False
                tank.px = path[j].px
                tank.py = path[j].py
                break
    grids[tank.px][tank.py].visited = True


#############################
##                         ##
##     Main windows        ##  
##                         ##
#############################


class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        #mosue location
        self.kx = 0
        self.ky = 0
        #windows form size 800x800#
        wx.Frame.__init__(self,  parent, id,  title="Gen Maze", pos=(50,50), size=(650,500))

        panel = wx.Panel(self)  # 创建面板

        #Delphi The Label
        self.title = wx.StaticText(panel, label="Gen Maze Size", pos=(20, 20))
        #Delphi The EditBox
        self.edit1 = wx.TextCtrl(panel, pos=(20, 40), size=(100, 25), style=wx.TE_LEFT)

        #Delphi Button
        self.bt_confirm = wx.Button(panel, label='Gen Maze', pos=(20, 80))  
        self.bt_confirm.Bind(wx.EVT_BUTTON, self.OnclickButton)
        self.bt_cancel = wx.Button(panel, label='Close', pos=(20, 110)) 
        self.bt_cancel.Bind(wx.EVT_BUTTON, self.OnclickCloseButton)
        #Delphi statusbar
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Gen Maze Developed by dinochen.com',0)

        #Image
        image = wx.Image('image1.jpg', wx.BITMAP_TYPE_ANY)
        self.imageBitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.BitmapFromImage(image),pos=(150, 30), size=(400,400) )
        self.imageBitmap.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self,event):
        ##  
        dc = wx.PaintDC(self.imageBitmap)
        dc.DrawBitmap(wx.Bitmap("image2.jpg"),0,0,True) 

#############################
##                         ##
##     Main Operation      ##  
##                         ##
#############################  

    def OnclickButton(self, event):
        global ng
        global grids
        global path
        global tank
        global npath
        ng = int(self.edit1.GetValue())
        grids=list()
        path = list()
        grids.clear()
        npath = 1
        path1 = Tpath(0,0)
        path.append(path1)
        tank = Ttank(0,0,1)
        creat_grid()
        set_first_grid()

        while (npath<ng*ng):
            gen_maze()

        draw_grid()
        self.Refresh()

        

 
    def OnclickCloseButton(self, event):
        yesNobox = wx.MessageDialog(None,"Are you Sure to Close Program?",'Question',wx.YES_NO)
        yesNoAnswer = yesNobox.ShowModal()
        if (yesNoAnswer == wx.ID_YES):
            self.Close() 


if __name__ == '__main__':  
    app = wx.App()                      # 初始化
    frame = MyFrame(parent=None, id=-1) # 实例MyFrame类，并传递参数    
    frame.Show()                        # 显示窗口
    app.MainLoop()                      # 调用主循环方法




