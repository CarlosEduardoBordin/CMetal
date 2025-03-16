import wx

class ConfiguracoesChildFrame(wx.MDIChildFrame):
    def __init__(self, parent):
        # Inicializa a janela filha com o título nome_formulario
        super().__init__(parent, -1, "Configurações", size=(250, 325), style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)
        self.SetMinSize((250, 325))
        self.SetMaxSize((250, 325))
        self.SetIcon( wx.Icon('icones/cfg.png', wx.BITMAP_TYPE_PNG))  # Definindo o ícone para o MDIFrame

        panel = wx.Panel(self)
        panel.SetBackgroundColour((255, 255, 255))

        static_box_cfg = wx.StaticBox(panel, label="Coeficientes:")
        static_box_cfg_sizer = wx.StaticBoxSizer(static_box_cfg, wx.VERTICAL)

        grid_sizer = wx.FlexGridSizer(rows=0, cols=2, vgap=5, hgap=10)
        grid_sizer.AddGrowableCol(1, proportion=1)  # Permite que a coluna das caixas de texto se expanda

        static_box_arquivo = wx.StaticBox(panel, label="Configurações:")
        static_box_arquivo_sizer = wx.StaticBoxSizer(static_box_arquivo, wx.VERTICAL)

        static_box_cfg_sizer.Add(grid_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        static_box_cfg_sizer.Add(static_box_arquivo_sizer, flag=wx.EXPAND | wx.ALL, border=10)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(static_box_cfg_sizer, 0, wx.ALL | wx.EXPAND, 10)
        panel.SetSizer(main_sizer)

