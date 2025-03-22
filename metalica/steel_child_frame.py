import wx
import wx.adv
import pandas as pd
from numpy.random import choice

#"tipo_aco.xlsx"
class ReadExcelFile:
    def __init__(self, path):
        self.path = path
        #verifica a se tem o arquivo !!
        try:
            self.data = pd.read_excel(path)
        except Exception as exception_code:
            wx.MessageBox(f"Erro: {exception_code}", "Erro",style = wx.OK | wx.ICON_ERROR)

    def return_value_by_one_col(self, col_name):
        return_list = self.data[col_name].tolist()
        return return_list

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
        self.Layout()

#criando o frame filho
class SteelChildFrame(wx.MDIChildFrame):
    def __init__(self, parent, frame_name):
        #parametros iniciais da janela
        super().__init__(parent, id=wx.ID_ANY, title = frame_name,
                         pos=(0,0), size = (600,600), style = wx.DEFAULT_FRAME_STYLE)
        #------------------------------------------------
        self.window_main_panel = wx.Panel(self) #cria o painel para por os objetos
        self.main_sizer = wx.BoxSizer(wx.VERTICAL) #define a organizacao das formas no sizer principal
        #------------------------------------------------- selecao do aco
        self.box_steel_type = StaticBox(self.window_main_panel, "Tipo do aço",orientation = "vertical")
        self.box_steel_selection_select_menu = StaticBox(self.box_steel_type, box_label = "Selecione uma opção", orientation = "horizontal") # staticbox de selecao
        self.box_steel_type.widgets_add(self.box_steel_selection_select_menu) # adiciona a static box de selecao ao sizer principal
        self.list_name = ReadExcelFile("tipo_aco.xlsx") # abre o arquivo do excel
        steel_type = self.list_name.return_value_by_one_col("Tipo")
        steel_degree = self.list_name.return_value_by_one_col("Grau")
        choice_value = [f"{a}" + " GRAU " +f"{b}" for a, b in zip(steel_type, steel_degree)] #gambiarra pra unir as 2 colunas
        #adiciona o select menu dentro do steel type
        self.box_steel_selection_select_menu.widgets_add(wx.ComboBox(self.box_steel_selection_select_menu, id = wx.ID_ANY, style = wx.CB_READONLY,choices = choice_value))
        self.btn_ok = wx.Button(self.box_steel_selection_select_menu, label="Ok!")
        self.box_steel_selection_select_menu.widgets_add(self.btn_ok)
        self.btn_edit = wx.Button(self.box_steel_selection_select_menu, label="Editar")
        self.box_steel_selection_select_menu.widgets_add(self.btn_edit)
        
        self.label_fy = wx.StaticText(self.box_steel_selection_select_menu,id=wx.ID_ANY, label="fy")
        self.box_steel_selection_select_menu.widgets_add(self.label_fy)
        #quebra de linha vertical
        self.box_steel_selection_select_menu.widgets_add(wx.StaticLine(self.box_steel_selection_select_menu, style=wx.LI_VERTICAL))
        self.label_fu = wx.StaticText(self.box_steel_selection_select_menu,id=wx.ID_ANY, label="fu")
        self.box_steel_selection_select_menu.widgets_add(self.label_fu)
        # #-------------cria a static box para dar ok ou alterar o tipo do material
        # self.box_steel_selection_edit = StaticBox(self.box_steel_type, box_label = "Editar", orientation = "horizontal")
        # self.btn_ok_selection_steel = wx.Button(self.box_steel_selection_edit, label="Ok!")
        # self.box_steel_selection_edit.widgets_add(self.btn_ok_selection_steel)
        # self.btn_edit_selection_steel = wx.Button(self.box_steel_selection_edit, label="Editar")
        # self.box_steel_selection_edit.widgets_add(self.btn_edit_selection_steel)
        # self.box_steel_type.widgets_add(self.box_steel_selection_edit) #adiciona o editar dentro do selecionar
        #-------------------------------------------------
        self.main_sizer.Add(self.box_steel_type,proportion =  0, flag = wx.ALL | wx.EXPAND, border = 5) #adiciona o primeiro staticbox ao sizer principal da janela
        self.window_main_panel.SetSizer(self.main_sizer)
