import wx
import wx.adv  #aboutbox
import wx.aui
# importa modulos
from configuracoes.configuracoes_child_frame import ConfiguracoesChildFrame
from sobre.sobre_child_frame import SobreChildFrame
#importa o script armadura longitudinal

# Declara Classe
class MDIFrame(wx.MDIParentFrame):

    # Declara Construtor
    def __init__(self):
        # Cria Formulario Pai
        wx.MDIParentFrame.__init__(self, None, -1, "CMetal", size=(wx.GetDisplaySize()))
        self.Maximize(True)
        self.SetIcon(icon = wx.Icon('icones/concreframe.png', wx.BITMAP_TYPE_PNG))  # Definindo o ícone para o MDIFrame
        # Criar um item
        menu = wx.Menu()
        # Criar um item de menu
        menu_novo_perfil = wx.MenuItem(menu, 5000, "&Novo perfil\tCtrl+N")
        # Adicionar um ícone ao item de menu
        menu_novo_perfil.SetBitmap(wx.Icon('icones/viga_iso.png', wx.BITMAP_TYPE_PNG))
        menu_abrir_configuracoes = wx.MenuItem(menu, 5003, "&Configurações")
        menu_abrir_configuracoes.SetBitmap(wx.Icon('icones/cfg.png', wx.BITMAP_TYPE_PNG))

        # Adicionar o item ao menu um sub menu
        menu.Append(menu_novo_perfil)
        menu.Append(menu_abrir_configuracoes)

        # Cria Menu Sobre
        menu_sobre = wx.Menu()
        menu_sobre.Append(5001, "&Sobre")

        # Cria Menu Sair
        menu_sair = wx.Menu()
        menu_sair.Append(6000, "&Sair")

        # Cria Barra de menus no topo da janela
        menubarra = wx.MenuBar()
        menubarra.Append(menu, "&Arquivo") #teste
        menubarra.Append(menu_sobre, "&Sobre")
        menubarra.Append(menu_sair, "&Sair")
        self.SetMenuBar(menubarra)

        # Declara Eventos dos menus
        self.Bind(wx.EVT_MENU, self.perfil, id=5000)
        self.Bind(wx.EVT_MENU, self.sobre, id=5001)
        self.Bind(wx.EVT_MENU, self.configuracoes, id=5003)
        self.Bind(wx.EVT_MENU, self.sair, id=6000)
        self.Bind(wx.EVT_CLOSE, self.sair)

    def perfil(self, evt):
        pass
    #verificar esse menu
    def configuracoes(self,evt):
        configuracoes_mdi = ConfiguracoesChildFrame(self)
        configuracoes_mdi.Show()
    #confirmacao de saida
    def sair(self, evt):
        dialogo = wx.MessageDialog(self, 'Você tem certeza que deseja sair?', 'Encerar o programa',
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dialogo.ShowModal() == wx.ID_YES:
            self.Destroy()  # Fecha a janela
        dialogo.Destroy()
    # Cria evento de informacao
    def sobre(self, evt):
        sobre_child_frame = SobreChildFrame(self)
        sobre_child_frame.Show()


# Cria aplicacao Wx
app = wx.App(False)

# Cria formulario
formulario = MDIFrame()
formulario.Show()

# Loop do programa
app.MainLoop()
