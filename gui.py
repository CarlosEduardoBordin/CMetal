import wx
import wx.adv  #aboutbox
import wx.aui
import pint
# importa modulos
from configuracoes.configuracoes_child_frame import ConfiguracoesChildFrame
from sobre.sobre_child_frame import SobreChildFrame
from metalica.steel_child_frame import SteelChildFrame
from metalica.edit_child_frame import EditChildFrame
from table_manipulation import ReadExcelFile
# Declara Classe
ureg = pint.UnitRegistry()

class MDIFrame(wx.MDIParentFrame):

    # Declara Construtor
    def __init__(self):
        # Cria Formulario Pai
        wx.MDIParentFrame.__init__(self, None, -1, "CMetal", size=(wx.GetDisplaySize()))
        self.Maximize(True)
        self.SetIcon(icon = wx.Icon("icones/concreframe.png", wx.BITMAP_TYPE_PNG))  # Definindo o ícone para o MDIFrame
        #unidades de medida pre-definidas
        self.data_si = ReadExcelFile("steel.xlsx","unidades")

        self.lenght_unit = self.data_si.get_name_and_return_col_value_str("Tipo", f"Comprimento", ["Unidade"])
        self.decimal_lenght = self.data_si.get_name_and_return_col_value_str("Tipo", f"Comprimento", ["Casas"])
        #novo
        self.area_unit = self.data_si.get_name_and_return_col_value_str("Tipo", f"Area", ["Unidade"])
        self.decimal_area = self.data_si.get_name_and_return_col_value_str("Tipo", f"Area", ["Casas"])

        self.volume_unit = self.data_si.get_name_and_return_col_value_str("Tipo", f"Volume", ["Unidade"])
        self.decimal_volume = self.data_si.get_name_and_return_col_value_str("Tipo", f"Volume", ["Casas"])

        self.inercia_unit = self.data_si.get_name_and_return_col_value_str("Tipo", f"Inercia", ["Unidade"])
        self.decimal_inercia = self.data_si.get_name_and_return_col_value_str("Tipo", f"Inercia", ["Casas"])

        self.six_unit = self.data_si.get_name_and_return_col_value_str("Tipo", f"Empenamento", ["Unidade"])
        self.decimal_six = self.data_si.get_name_and_return_col_value_str("Tipo", f"Empenamento", ["Casas"])

        self.force_unit = self.data_si.get_name_and_return_col_value_str("Tipo", f"Forca", ["Unidade"])
        self.decimal_force = self.data_si.get_name_and_return_col_value_str("Tipo", f"Empenamento", ["Casas"])

        self.moment_unit = self.data_si.get_name_and_return_col_value_str("Tipo", f"Momento", ["Unidade"])
        self.decimal_moment = self.data_si.get_name_and_return_col_value_str("Tipo", f"Momento", ["Casas"])


        self.press_unit = self.data_si.get_name_and_return_col_value_str("Tipo", f"Pressao", ["Unidade"])
        self.decimal_press = self.data_si.get_name_and_return_col_value_str("Tipo", f"Pressao", ["Casas"])

        self.g_modulo = self.data_si.get_name_and_return_col_value_str("Tipo", f"g", ["Unidade"])
        self.e_modulo = self.data_si.get_name_and_return_col_value_str("Tipo", f"e", ["Unidade"])
        self.y_um = self.data_si.get_name_and_return_col_value_str("Tipo", f"y1", ["Unidade"])

        # Criar um item
        self.menu = wx.Menu() # Criar um item de menu
        self.novo_perfil = wx.NewIdRef() #cria um codigo novo para cada item dentro do menu
        self.configuracoes_id = wx.NewIdRef()
        self.editor_aco_id = wx.NewIdRef()
        self.sobre_id = wx.NewIdRef()
        self.sair_id = wx.NewIdRef()


        #novo perfil
        menu_novo_perfil = wx.MenuItem(self.menu, self.novo_perfil, "&Novo perfil\tF1")
        menu_novo_perfil.SetBitmap(wx.Icon("icones/perfil.bmp"))
        #cfg
        menu_abrir_configuracoes = wx.MenuItem(self.menu, self.configuracoes_id, "&Configurações\tF2")
        menu_abrir_configuracoes.SetBitmap(wx.Icon("icones/cfg.png", wx.BITMAP_TYPE_PNG)) #tem que deixar em png fica bugado
        # Adicionar o item ao menu um sub menu
        self.menu.Append(menu_novo_perfil)
        self.menu.Append(menu_abrir_configuracoes)

        # Cria Menu Sobre
        menu_sobre = wx.Menu()
        menu_sobre.Append(self.sobre_id, "&Sobre")

        # Cria Menu Sair
        menu_sair = wx.Menu()
        menu_sair.Append(self.sair_id, "&Sair")

        # Cria Barra de menus no topo da janela
        self.menubarra = wx.MenuBar()
        self. menubarra.Append(self.menu, "&Arquivo") #teste
        self.menubarra.Append(menu_sobre, "&Sobre")
        self.menubarra.Append(menu_sair, "&Sair")
        self.SetMenuBar(self.menubarra)
        #Criando a ToolBox
        self.toolbox = self.CreateToolBar()
        self.toolbox.AddTool(self.novo_perfil, "Novo perfil",  wx.Bitmap("icones/perfil.bmp", wx.BITMAP_TYPE_BMP))
        self.toolbox.AddTool(self.configuracoes_id, "Configurações",  wx.Icon("icones/cfg.png", wx.BITMAP_TYPE_PNG))
        self.toolbox.AddTool(self.editor_aco_id, "Editor aço",  wx.Bitmap("icones/lapiz.bmp", wx.BITMAP_TYPE_BMP))
        self.toolbox.AddSeparator()
        self.toolbox.Realize()


        # Declara Eventos dos menus
        self.Bind(wx.EVT_MENU, self.perfil, id=self.novo_perfil)
        self.Bind(wx.EVT_MENU, self.sobre, id=self.sobre_id)
        self.Bind(wx.EVT_MENU, self.editor_aco, id=self.editor_aco_id)
        self.Bind(wx.EVT_MENU, self.configuracoes, id=self.configuracoes_id)
        self.Bind(wx.EVT_MENU, self.sair, id=self.sair_id)
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

    def editor_aco(self, evt):
        edit_child = EditChildFrame(self, "Editor")
        edit_child.Show()
    #confirmacao de saida
    def sair(self, evt):
        dialogo = wx.MessageDialog(self, "Você tem certeza que deseja sair?", "Encerar o programa",
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dialogo.ShowModal() == wx.ID_YES:
            self.Destroy()  # Fecha a janela
        dialogo.Destroy()
    # Cria evento de informacao
    def sobre(self, evt):
        sobre_child_frame = SobreChildFrame(self)
        sobre_child_frame.Show()

    #variaveis de unidade de medidas
    def set_unit_lenght(self, unit, decimal):
        self.lenght_unit = unit
        self.decimal_lenght = decimal

    def get_unit_lenght(self):
        return self.lenght_unit , self.decimal_lenght

    def set_unit_area(self, unit, decimal):
        self.area_unit = unit
        self.decimal_area = decimal

    def get_unit_area(self):
        return self.area_unit , self.decimal_area

    def set_unit_volume(self, unit, decimal):
        self.volume_unit = unit
        self.decimal_volume = decimal

    def get_unit_volume(self):
        return self.volume_unit , self.decimal_volume

    def set_unit_inercia(self, unit, decimal):
        self.inercia_unit = unit
        self.decimal_inercia = decimal

    def get_unit_inercia(self):
        return self.inercia_unit , self.decimal_inercia

    def set_unit_six(self, unit, decimal):
        self.six_unit = unit
        self.decimal_six = decimal

    def get_unit_six(self):
        return self.six_unit , self.decimal_six

    def set_unit_force(self, unit, decimal):
        self.force_unit = unit
        self.decimal_force = decimal

    def get_unit_force(self):
        return self.force_unit, self.decimal_force

    def set_unit_moment(self, unit, decimal):
        self.moment_unit = unit
        self.decimal_moment = decimal

    def get_unit_moment(self):
        return self.moment_unit , self.decimal_moment

    def set_unit_press(self, unit, decimal):
        self.press_unit = unit
        self.decimal_press = decimal

    def get_unit_press(self):
        return self.press_unit , self.decimal_press

    def set_e_modulo(self, unit):
        self.e_modulo = unit

    def get_e_modulo(self):
        return self.e_modulo

    def set_g_modulo(self, unit):
        self.g_modulo = unit

    def get_g_modulo(self):
        return self.g_modulo

    def set_y_um(self, unit):
        self.y_um = unit

    def get_y_um(self):
        return self.y_um



# Cria aplicacao Wx
app = wx.App(False)

# Cria formulario
formulario = MDIFrame()
formulario.Show()

# Loop do programa
app.MainLoop()
