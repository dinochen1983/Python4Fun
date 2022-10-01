import math
import matplotlib.pyplot as plt
import wx


def Calculation():
    ## input
    pp=[]
    mm=[]
    a1=1.0 
    beta1=0.8 
    kxb=0.55 
    ##
    n1=a1*fc*b*kxb*h0
    nmax=a1*fc*b*h+2*area*fy
    for i in range(nstep+1):
        nu=(i/nstep)*nmax 
        if nu<=nmax:
            if nu<=n1: 
                mu=-nu*nu/(2*a1*fc*b)+(nu*h)/2+fy*area*(h0-as1) 
            else:
                l1=(beta1-kxb)/(a1*fc*b*h0*(beta1-kxb)+fy*area) 
                l2=(kxb*fy*area)/(a1*fc*b*h0*(beta1-kxb)+fy*area) 
                k1=(l1*nu+l2)-0.5*(l1*nu+l2)*(l1*nu+l2) 
                kx1= l1*nu+l2 
                mu=a1*fc*b*h0*h0*(k1)-(h/2-as1)*nu+fy*area*(h0-as1) 
            pp.append(nu/1000)
            mm.append(mu/1e6)

    ratio = area*2/(b*h)*100
    plt.style.use('ggplot')
    fig = plt.figure()
    fig.canvas.manager.set_window_title("Column PM curve")
    plt.plot(mm,pp,marker='o')
    plt.xlabel('Moment')
    plt.ylabel('Axial_Force')
    plt.title("PM curve, Ratio = {0:.3f}".format(ratio))
    plt.savefig('fig.png')
    ##plt.show()

    with open('result.txt', 'w') as f:
        for i in range(nstep+1):
            f.write('{0:.2f}'.format(pp[i])+','+'{0:.5e}\n'.format(mm[i]))

class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        #mosue location
        self.kx = 0
        self.ky = 0
        #windows form size 800x800#
        wx.Frame.__init__(self,  parent, id,  title="PM Calculation(Python)", pos=(50,50), size=(1250,  580))

        panel = wx.Panel(self)  # 创建面板

        #Delphi The Label
        self.title = wx.StaticText(panel, label="Rect Column Info", pos=(20, 15))

        #Delphi The Label
        self.label1 = wx.StaticText(panel, label="Concrete fc", pos=(20, 40))
        self.label2 = wx.StaticText(panel, label="Section b", pos=(20, 40+25))
        self.label3 = wx.StaticText(panel, label="Section h", pos=(20, 40+50))
        self.label4 = wx.StaticText(panel, label="Cover as1", pos=(20, 40+75))
        self.label5 = wx.StaticText(panel, label="Steel Area As", pos=(20, 40+100))
        self.label6 = wx.StaticText(panel, label="Steel Grade fy", pos=(20, 40+125))
        self.label7 = wx.StaticText(panel, label="Nstep", pos=(20, 40+150))

        #Delphi The EditBox
        self.edit1 = wx.TextCtrl(panel, pos=(120, 40), size=(60, 20), style=wx.TE_LEFT, value="14.3")
        self.edit2 = wx.TextCtrl(panel, pos=(120, 40+25), size=(60, 20), style=wx.TE_LEFT, value="500")
        self.edit3 = wx.TextCtrl(panel, pos=(120, 40+50), size=(60, 20), style=wx.TE_LEFT, value="600")
        self.edit4 = wx.TextCtrl(panel, pos=(120, 40+75), size=(60, 20), style=wx.TE_LEFT, value="35")
        self.edit5 = wx.TextCtrl(panel, pos=(120, 40+100), size=(60, 20), style=wx.TE_LEFT, value="5024.0")
        self.edit6 = wx.TextCtrl(panel, pos=(120, 40+125), size=(60, 20), style=wx.TE_LEFT, value="300.0")
        self.edit7 = wx.TextCtrl(panel, pos=(120, 40+150), size=(60, 20), style=wx.TE_LEFT, value="30")

        #StatusBar
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Developed by DinoChen',0)

        self.label8 = wx.StaticText(panel, label="Resutl:result.txt", pos=(900, 15))
        self.log = wx.TextCtrl(panel, wx.ID_ANY, pos=(900, 40), size=(250,450),style = wx.TE_MULTILINE|wx.VSCROLL)
        self.log.Clear()


        #Delphi Button
        self.bt_confirm = wx.Button(panel, label='Calculation', pos=(100, 50+175))  
        self.bt_confirm.Bind(wx.EVT_BUTTON, self.OnclickButton)
        self.bt_close = wx.Button(panel, label='Close', pos=(100, 50+200))  
        self.bt_close.Bind(wx.EVT_BUTTON, self.OnClickClose)


        image = wx.Image('fig.png', wx.BITMAP_TYPE_ANY)
        self.imageBitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.BitmapFromImage(image),pos=(220, 40), size=(650,500) )
        ##self.imageBitmap.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.imageBitmap.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnPaint(self,event):
        ##  
        dc = wx.PaintDC(self.imageBitmap)
        dc.DrawBitmap(wx.Bitmap("fig.png"),0,0,True) 




    def OnclickButton(self, event):
        global fc,b,h,as1,h0,area,fy,nstep
        fc=float(self.edit1.GetValue())
        b=float(self.edit2.GetValue())
        h=float(self.edit3.GetValue())
        as1=float(self.edit4.GetValue())
        h0=h-as1 
        area=float(self.edit5.GetValue())
        fy=float(self.edit6.GetValue())
        nstep=int(self.edit7.GetValue())
        ##
        Calculation()
        self.imageBitmap.Refresh()
        self.log.Clear()
        with open('result.txt') as f:
            lines = f.readlines()    

        for line in lines:
          self.log.AppendText(line)



    def OnClickClose(self, event):
        self.Close()




if __name__ == '__main__':  
    app = wx.App()                      # 初始化
    frame = MyFrame(parent=None, id=-1) # 实例MyFrame类，并传递参数    
    frame.Show()                        # 显示窗口
    app.MainLoop()                      # 调用主循环方法







## input section info

