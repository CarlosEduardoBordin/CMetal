import wx
import wx.adv  #aboutbox
import wx.aui
# importa modulos
from configuracoes.configuracoes_child_frame import ConfiguracoesChildFrame
from sobre.sobre_child_frame import SobreChildFrame
from metalica.steel_child_frame import SteelChildFrame
# Declara Classe
class MDIFrame(wx.MDIParentFrame):

    # Declara Construtor
    def __init__(self):
        # Cria Formulario Pai
        wx.MDIParentFrame.__init__(self, None, -1, "CMetal", size=(wx.GetDisplaySize()))
        self.Maximize(True)
        self.SetIcon(icon = wx.Icon('icones/concreframe.png', wx.BITMAP_TYPE_PNG))  # Definindo o ícone para o MDIFrame
        #unidades de medida pre-definidas
        self.lenght_unit = "m"
        self.force_unit = "KN"
        self.moment_unit = "KNm"
        self.press_unit = "MPa"
        # Criar um item
        menu = wx.Menu()
        # Criar um item de menu
        menu_novo_perfil = wx.MenuItem(menu, 5000, "&Novo perfil")
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
        #wxpython classe comum para entrada de texto de linha unica - TextEntryDialog
        mensagem_dialogo = wx.TextEntryDialog(self,"De nome ao perfil:", caption = "Perfil", value = "Ex : Perfil 1", style=wx.TextEntryDialogStyle)
        if mensagem_dialogo.ShowModal() == wx.ID_OK:
            name_id_formulario_filho = mensagem_dialogo.GetValue()
            #abre o formulario filho
            steel_child_frame = SteelChildFrame(self, name_id_formulario_filho)
            steel_child_frame.Show()


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

    #variaveis de unidade de medidas
    def set_unit_lenght(self, unit):
        self.lenght_unit = unit

    def get_unit_lenght(self):
        return self.lenght_unit

    def set_unit_force(self, unit):
        self.force_unit = unit

    def get_unit_force(self):
        return self.force_unit

    def set_unit_moment(self, unit):
        self.moment_unit = unit

    def get_unit_moment(self):
        return self.moment_unit

    def set_unit_press(self, unit):
        self.press_unit = unit

    def get_unit_press(self):
        return self.press_unit

# Cria aplicacao Wx
app = wx.App(False)

# Cria formulario
formulario = MDIFrame()
formulario.Show()

# Loop do programa
app.MainLoop()
