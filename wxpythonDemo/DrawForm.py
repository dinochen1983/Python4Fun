import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(650, 680))
        self.SetBackgroundColour(wx.WHITE)
        # 设置窗体图标
        icon = wx.Icon("myico.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # 创建一个面板
        #self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel = wx.Panel(self, pos=(50, 150), size=(400, 400))
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.on_panel_left_down)

        # 创建按钮_1
        self.button = wx.Button(self, wx.ID_ANY, "绘制圆形", pos=(20, 20) )
        self.button.Bind(wx.EVT_BUTTON, self.on_button_click)

        # 创建按钮_1
        self.button2 = wx.Button(self, wx.ID_ANY, "清空", pos=(20, 50) )
        self.button2.Bind(wx.EVT_BUTTON, self.on_button2_click)

        self.button3 = wx.Button(self, wx.ID_ANY, "保存", pos=(120, 80) )
        self.button3.Bind(wx.EVT_BUTTON, self.on_button3_click)

        # 创建一个文本框
        self.label = wx.StaticText(self, wx.ID_ANY, "Circle Diameter", pos=(20, 80))
        self.textbox = wx.TextCtrl(self, wx.ID_ANY, "", pos=(20, 110), size=(200, -1))

        # 显示窗体
        self.Show()

    def on_button_click(self, event):
        dc = wx.ClientDC(self.panel)
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.SetBrush(wx.Brush(wx.BLUE))
        kx = int(self.textbox.GetValue())
        dc.DrawCircle(100, 100, kx)

    def on_button2_click(self, event):
        dc = wx.ClientDC(self.panel)
        dc.SetPen(wx.Pen(wx.WHITE))
        dc.SetBrush(wx.Brush(wx.WHITE))
        dc.DrawRectangle(0, 0, 400-1,400-1)

    def on_button3_click(self, event):
        ##dc1 = wx.WindowDC(self.panel)
        ##dc.SetPen(wx.Pen(wx.WHITE))
        ##dc.SetBrush(wx.Brush(wx.YELLOW))
        ##dc.DrawRectangle(0, 0, 400-1,400-1)
        bitmap = wx.EmptyBitmap(400, 400)
        wdc = wx.WindowDC(self.panel)
        mdc = wx.MemoryDC(bitmap)
        mdc.Blit(0, 0, 400, 400, wdc, 0, 0)
        ##dc.SetPen(wx.Pen(wx.WHITE))
        ##dc.SetBrush(wx.Brush(wx.YELLOW))
        ##dc.DrawRectangle(0, 0, 400-1,400-1)

        bitmap.SaveFile ("image.bmp", wx.BITMAP_TYPE_BMP)

    def on_panel_left_down(self, event):
        pos = event.GetPosition()
        dc = wx.ClientDC(self.panel)
        dc.SetPen(wx.Pen(wx.RED))
        dc.SetBrush(wx.Brush(wx.RED))
        dc.DrawCircle(pos.x, pos.y, 5)
        print("Mouse clicked at:", pos)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, title="My Form")
    app.MainLoop()

    ##pyinstaller -F -w  DrawForm.py