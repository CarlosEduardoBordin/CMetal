import wx
import wx.adv

#criando o frame filho
class SteelChildFrame(wx.MDIChildFrame):
    def __init__(self, parent, frame_name):
        #parametros iniciais da janela
        super().__init__(parent, id=wx.ID_ANY, title = frame_name,
                         pos=wx.DefaultPosition, size = (600,600), style = wx.DEFAULT_FRAME_STYLE)
