import wx
import os
from metalica.widget_class import StaticBox

class EditChildFrame(wx.MDIChildFrame):
    def __init__(self, parent, frame_name):
        super().__init__(parent, id=wx.ID_ANY, title = frame_name,
                         pos=(0,0), size = (300,300), style = wx.DEFAULT_FRAME_STYLE)
        #----------------------------------------------------- sizer principal
        self.window_main_panel = wx.Panel(self) #cria o painel para por os objetos
        self.main_sizer = wx.BoxSizer(wx.VERTICAL) #define a organizacao das formas no sizer principal
        # ----------------------------------------------------- box
        self.edit_box = StaticBox(self.window_main_panel, "Editar",orientation = "vertical")
        self.img_box = StaticBox(self.edit_box,"Tensão deformação fy - fu", orientation = "vertical")
        self.edit_box.widgets_add(self.img_box)
        path = os.path.join(os.getcwd(), "icones", "fyfu.bmp") #----------------------------------------------------------------------
        self.img_crtl = wx.StaticBitmap(self.img_box, bitmap = wx.Bitmap(path))
        self.img_box.widgets_add(self.img_crtl)
        self.img_box.widgets_add(wx.StaticText(self.img_box, id = wx.ID_ANY, label = "fy - Resistência ao escoamento do aço",style = wx.ALIGN_CENTER))
        self.img_box.widgets_add(wx.StaticText(self.img_box, id=wx.ID_ANY, label = "fu - Resistência a ruptura do aço", style = wx.ALIGN_CENTER))
        self.main_sizer.Add(self.edit_box,proportion =  0, flag = wx.ALL | wx.EXPAND, border = 5) #adiciona o primeiro staticbox ao sizer principal da janela
        self.window_main_panel.SetSizer(self.main_sizer)
