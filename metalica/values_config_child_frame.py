import wx
from metalica import widget_class
from metalica.widget_class import StaticBox


class ValuesConfiguration(wx.MDIChildFrame):
    def __init__(self, parent, frame_name ):
        super().__init__(parent, id=wx.ID_ANY, title=frame_name,
                         pos=wx.DefaultPosition, size=(400, 500))

        self.window_main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.box_values_cfg = StaticBox(self.window_main_panel, "Valores e variáveis", orientation = "vertical")

        self.main_sizer.Add(self.box_values_cfg,  proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5)
        self.window_main_panel.SetSizer(self.main_sizer)