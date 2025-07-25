import wx
import wx.grid
import os
from widget_class import StaticBox


class ImgHelpButton(wx.MDIChildFrame):
    def __init__(self, parent, frame_name):
        super().__init__(parent, id=wx.ID_ANY, title = frame_name,
                         pos=wx.DefaultPosition, size = (400,430), style = wx.DEFAULT_FRAME_STYLE & ~(wx.MAXIMIZE_BOX | wx.RESIZE_BORDER))


        self.window_main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL) #define a organizacao das formas no sizer principal

        self.box_help = StaticBox(self.window_main_panel, "Ajuda",orientation = "vertical")
        self.img_box = wx.StaticBitmap(self.box_help,bitmap = wx.Bitmap(os.path.join(os.getcwd(), "icones", "whp.bmp")))
        self.box_help.widgets_add(self.img_box, 0, True)
        texto = ("d - altura \n d'- altura da alma (sem o raio de laminação) \n "
                 "h - altura total da alma (com o raio de laminação) \n"
                 " tf - espessura da mesa \n tw - espessura da alma \n "
                 "bf - largura total da mesa \n R - Raio de concordância / laminação ")

        self.text_ctrl = wx.TextCtrl(self.box_help, value = texto, style=wx.TE_CENTER | wx.TE_MULTILINE |  wx.TE_READONLY)
        self.text_ctrl.SetBackgroundColour(wx.Colour(240, 240, 240)) # mudar para o rgb da janela para nao ficar piscando
        self.text_ctrl.Enable(False)

        self.box_help.widgets_add(self.text_ctrl, 0, False)

        self.main_sizer.Add(self.box_help,  proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5)
        self.window_main_panel.SetSizer(self.main_sizer)
