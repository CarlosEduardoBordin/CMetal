import wx
import wx.adv
import webbrowser
from widget_class import StaticBox, LinkButton


class SobreChildFrame(wx.MDIChildFrame):

    def __init__(self, parent):
        super().__init__(parent, -1, "Sobre", size=(300, 610), style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)
        # self.SetMinSize((300, 610))
        # self.SetMaxSize((300, 610))
        self.SetIcon(wx.Icon("icones/info.png", wx.BITMAP_TYPE_PNG))  # Definindo o ícone para o MDIFrame

        self.window_main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.desenvolvido = StaticBox(self.window_main_panel, "Desenvolvido por :", orientation="vertical")

        self.button_yt = LinkButton(self.desenvolvido, "Carlos Eduardo A. Bordin", "https://www.youtube.com/@carloseduardobordin", "icones/yt.png")
        self.desenvolvido.widgets_add(self.button_yt, 0, False)

        self.bibliotecas = StaticBox(self.window_main_panel, "Bibliotecas e ferramentas utilizadas :", orientation="vertical")

        self.b1 = LinkButton(self.bibliotecas, "wxPython", "https://wxpython.org/index.html", "icones/wxpython.png")
        self.bibliotecas.widgets_add(self.b1, 0, False)
        self.b2 = LinkButton(self.bibliotecas, "Pint", "https://pint.readthedocs.io/en/stable/")
        self.bibliotecas.widgets_add(self.b2, 0, False)
        self.b3 = LinkButton(self.bibliotecas, "Pandas", "https://pandas.pydata.org/", "icones/panda.png")
        self.bibliotecas.widgets_add(self.b3, 0, False)
        self.b4 = LinkButton(self.bibliotecas, "Openpyxl", "https://openpyxl.readthedocs.io/en/stable/")
        self.bibliotecas.widgets_add(self.b4, 0, False)
        self.b5 = LinkButton(self.bibliotecas, "Matplotlib", "https://matplotlib.org/", "icones/matplotlib.png")
        self.bibliotecas.widgets_add(self.b5, 0, False)
        self.b6 = LinkButton(self.bibliotecas, "Numpy", "https://numpy.org/", "icones/numpy.png")
        self.bibliotecas.widgets_add(self.b6, 0, False)
        self.b7 = LinkButton(self.bibliotecas, "PyLaTeX", "https://jeltef.github.io/PyLaTeX/current/")
        self.bibliotecas.widgets_add(self.b7, 0, False)
        self.b8 = LinkButton(self.bibliotecas, "PyInstaller", "https://pyinstaller.org/en/stable/", "icones/pyinstaller.png")
        self.bibliotecas.widgets_add(self.b8, 0, False)
        self.b9 = LinkButton(self.bibliotecas, "MikTex", "https://miktex.org/", "icones/mk.png")
        self.bibliotecas.widgets_add(self.b9, 0, False)
        self.b10 = LinkButton(self.bibliotecas, "Inno Setup", "https://jrsoftware.org/isinfo.php", "icones/jr.png")
        self.bibliotecas.widgets_add(self.b10, 0, False)

        self.report_box = StaticBox(self.window_main_panel, "Bibliotecas e ferramentas utilizadas :",
                                     orientation="vertical")
        self.report = wx.StaticText(self.report_box,
                                    label="Caso você identifique algum bug ou inconsistência nos cálculos do software,\npor favor, entre em contato pelo e-mail: \n",
                                    size=(200, -1))
        self.report_box.widgets_add(self.report, 0, False)

        self.hyperlink = wx.adv.HyperlinkCtrl(self.report_box, label="carlosbordin.pf023@academico.ifsul.edu.br",
                                              url="mailto:carlosbordin.pf023@academico.ifsul.edu.br")
        self.report_box.widgets_add(self.hyperlink, 0, False)
        self.report_obrigado = wx.StaticText(self.report_box, label="Agradecemos sua colaboração.",size=(200, -1))
        self.report_box.widgets_add(self.report_obrigado, 0, False)



        self.main_sizer.Add(self.desenvolvido, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        self.main_sizer.Add(self.bibliotecas, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        self.main_sizer.Add(self.report_box, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        self.window_main_panel.SetSizer(self.main_sizer)
