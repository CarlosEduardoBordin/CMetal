import wx
#criando uma classe para os wx.StaticBox rotulo - orientacao do sizer
class StaticBox(wx.Panel):
    #criacao do box
    def __init__(self, parent, box_label, orientation):
        super().__init__(parent)
        self.box = wx.StaticBox(self, label = box_label) #cria o staticbox
        if orientation == "vertical":
            self.sizer_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        elif orientation == "horizontal":
            self.sizer_box_sizer = wx.StaticBoxSizer(self.box, wx.HORIZONTAL)
        elif orientation == "grid":
            self.sizer_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
            self.grid_sizer = wx.FlexGridSizer(rows=0, cols=2, vgap=5, hgap=10)
            self.grid_sizer.AddGrowableCol(1, proportion=1)
            self.sizer_box_sizer.Add(self.grid_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.sizer_box_sizer)
    # configuracao do widget interno
    def widgets_add(self, widget):
        self.sizer_box_sizer.Add(widget, flag=wx.ALL | wx.EXPAND, border=5 )
        self.Layout() #atualiza