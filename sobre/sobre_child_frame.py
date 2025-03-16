import wx
import wx.adv
import webbrowser


class SobreChildFrame(wx.MDIChildFrame):

    def __init__(self, parent):
        super().__init__(parent, -1, "Sobre", size=(300, 610), style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)
        self.SetMinSize((300, 610))
        self.SetMaxSize((300, 610))
        self.SetIcon(wx.Icon('icones/info.png', wx.BITMAP_TYPE_PNG))  # Definindo o ícone para o MDIFrame

        panel = wx.Panel(self)
        panel.SetBackgroundColour((255, 255, 255))

        static_box_dev = wx.StaticBox(panel, label="Desenvolvido por:")
        static_box_dev_sizer = wx.StaticBoxSizer(static_box_dev, wx.VERTICAL)

        def botao_link_um(event):
            webbrowser.open("https://www.youtube.com/@carloseduardobordin")

        self.botao_link_um = wx.Button(panel, id=wx.ID_ANY, label='Carlos Eduardo A. Bordin')
        self.botao_link_um.Bind(wx.EVT_BUTTON, botao_link_um)
        self.botao_link_um.SetBitmapPosition(wx.LEFT)  # Ícone à esquerda do texto
        self.botao_link_um.SetBitmap(wx.Bitmap("icones/yt.png", wx.BITMAP_TYPE_PNG))  # Define o ícone no botão
        static_box_dev_sizer.Add(self.botao_link_um, 0, wx.ALL | wx.EXPAND, 5)

        static_box_ref = wx.StaticBox(panel, label="Referências:")
        static_box_ref_sizer = wx.StaticBoxSizer(static_box_ref, wx.VERTICAL)

        self.botao_com_link(panel, static_box_ref_sizer, "REF 1", "http://www.example.com")
        self.botao_com_link(panel, static_box_ref_sizer, "REF 2", "http://www.example.com")
        self.botao_com_link(panel, static_box_ref_sizer, "REF 3", "http://www.example.com")
        self.botao_com_link(panel, static_box_ref_sizer, "REF 4", "http://www.example.com")

        static_box_bibliotecas = wx.StaticBox(panel, label="Bibliotecas:")
        static_box_bibliotecas_sizer = wx.StaticBoxSizer(static_box_bibliotecas, wx.VERTICAL)

        self.botao_com_link(panel, static_box_bibliotecas_sizer, "wxPython", "https://www.wxpython.org/")
        self.botao_com_link(panel, static_box_bibliotecas_sizer, "NumPy", "https://numpy.org/")
        self.botao_com_link(panel, static_box_bibliotecas_sizer, "Matplotlib", "https://matplotlib.org/")
        self.botao_com_link(panel, static_box_bibliotecas_sizer, "Pyinstaller", "https://pyinstaller.org/en/stable/")
        self.botao_com_link(panel, static_box_bibliotecas_sizer, "Inno Setup", "https://jrsoftware.org/isinfo.php")

        static_box_report = wx.StaticBox(panel, label="Reportar:")
        static_box_report_sizer = wx.StaticBoxSizer(static_box_report, wx.VERTICAL)

        self.report = wx.StaticText(panel,
                                    label="Caso você identifique algum bug ou inconsistência nos cálculos do software,\npor favor, entre em contato pelo e-mail: \n",
                                    size=(200, -1))
        self.hyperlink = wx.adv.HyperlinkCtrl(panel, label="carlosbordin.pf023@academico.ifsul.edu.br",
                                              url="mailto:carlosbordin.pf023@academico.ifsul.edu.br")
        self.report_obrigado = wx.StaticText(panel, label="Agradecemos sua colaboração.",size=(200, -1))

        static_box_report_sizer.Add(self.report, 0, wx.ALL | wx.EXPAND, 5)
        static_box_report_sizer.Add(self.hyperlink, 0, wx.ALL | wx.EXPAND, 5)
        static_box_report_sizer.Add(self.report_obrigado, 0, wx.ALL | wx.EXPAND, 5)

        # cria o sizer principal!
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(static_box_dev_sizer, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(static_box_ref_sizer, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(static_box_bibliotecas_sizer, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(static_box_report_sizer, 0, wx.ALL | wx.EXPAND, 5)


        panel.SetSizer(main_sizer)
    #criando funcao de botao que abre link
    def botao_com_link(self, panel, sizer, label, link):
        # Cria o botão
        botao = wx.Button(panel, label=label)
        # Associa o evento de clique do botão à função que abre o link
        botao.Bind(wx.EVT_BUTTON, lambda event: webbrowser.open(link))
        # Adiciona o botão ao sizer
        sizer.Add(botao, 0, wx.ALL | wx.EXPAND, 5)
