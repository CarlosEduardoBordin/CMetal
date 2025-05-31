import wx
from metalica.widget_class import StaticBox
from metalica.widget_class import TextBoxVrf


class ValuesConfiguration(wx.MDIChildFrame):
    def __init__(self, parent, frame_name ):
        super().__init__(parent, id=wx.ID_ANY, title=frame_name,
                         pos=wx.DefaultPosition, size=(400, 500))

        self.window_main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.box_values_cfg = StaticBox(self.window_main_panel, "Valores e variáveis", orientation = "grid")

        self.text_young_mod = wx.StaticText(self.box_values_cfg, id=wx.ID_ANY, label="Módulo de elasticidade (GPa)")
        self.box_values_cfg.widgets_add(self.text_young_mod, 0, False)
        self.young_mod = TextBoxVrf(self.box_values_cfg, value = "200", only_numeric=True)
        self.box_values_cfg.widgets_add(self.young_mod,1, False)
        self.text_y_um = wx.StaticText(self.box_values_cfg, id=wx.ID_ANY, label="γ1")
        self.box_values_cfg.widgets_add(self.text_y_um, 0, False)
        self.y_um = TextBoxVrf(self.box_values_cfg, value = "1.1", only_numeric=True)
        self.box_values_cfg.widgets_add(self.y_um,1, False)
        self.text_y_dois = wx.StaticText(self.box_values_cfg, id=wx.ID_ANY, label="γ2")
        self.box_values_cfg.widgets_add(self.text_y_dois, 0, False)
        self.y_dois = TextBoxVrf(self.box_values_cfg, value = "1.35", only_numeric=True)
        self.box_values_cfg.widgets_add(self.y_dois,1, False)



        self.main_sizer.Add(self.box_values_cfg,  proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5)
        self.window_main_panel.SetSizer(self.main_sizer)