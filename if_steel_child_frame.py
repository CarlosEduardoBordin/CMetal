import wx
import os
from widget_class import StaticBox


class IFSeel(wx.MDIChildFrame):
    def __init__(self,parent):
        #nao colocar no init o parent child
        super().__init__(parent, id=wx.ID_ANY, title="",
                         pos=wx.DefaultPosition, size=(745, 700), style=wx.NO_BORDER | wx.STAY_ON_TOP | wx.STAY_ON_TOP)
        self.Center()
        self.Disable() # para nao ser clicada
        self.window_main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.img_box = wx.StaticBitmap(self.window_main_panel,bitmap = wx.Bitmap(os.path.join(os.getcwd(), "icones", "ifsteel.bmp")))
        self.main_sizer.Add(self.img_box,  proportion = 0, flag = wx.ALL | wx.EXPAND, border = 0)
        self.window_main_panel.SetSizer(self.main_sizer)