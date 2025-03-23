import wx
import wx.adv
import pandas as pd
from metalica.edit_child_frame import EditChildFrame
from metalica.widget_class import StaticBox
from metalica.table_manipulation import ReadExcelFile

#criando o frame filho
class SteelChildFrame(wx.MDIChildFrame):
    def __init__(self, parent, frame_name):
        #parametros iniciais da janela
        super().__init__(parent, id=wx.ID_ANY, title = frame_name,
                         pos=(0,0), size = (800,600), style = wx.DEFAULT_FRAME_STYLE)
        self.parent = parent #atributo parente da janela
        #------------------------------------------------funcoes dos botoes
        self.data = ReadExcelFile("tipo_aco.xlsx")
        def load_values_fy_fu(event):
            selected_item = self.select_steel_type_menu.GetValue()
            fy_fu = self.data.get_name_and_return_col_value("Tipo",f"{selected_item}",["fy", "fu"])
            fy, fu = float(fy_fu["fy"]), float(fy_fu["fu"])
            self.text_fy.SetValue(str(fy))
            self.text_fu.SetValue(str(fu))
        def load_edit_child_frame(event):
            edit_child = EditChildFrame(self.parent,"Editor")
            edit_child.Show()
        #------------------------------------------------
        self.window_main_panel = wx.Panel(self) #cria o painel para por os objetos
        self.main_sizer = wx.BoxSizer(wx.VERTICAL) #define a organizacao das formas no sizer principal
        #------------------------------------------------- selecao do aco
        self.box_steel_type = StaticBox(self.window_main_panel, "Tipo do aço",orientation = "vertical")
        self.box_steel_selection_select_menu = StaticBox(self.box_steel_type, box_label = "Selecione uma opção", orientation = "horizontal") # staticbox de selecao
        self.box_steel_type.widgets_add(self.box_steel_selection_select_menu) # adiciona a static box de selecao ao sizer principal
        steel_type = self.data.return_value_by_one_col("Tipo")
        #adiciona o select menu dentro do steel type
        self.select_steel_type_menu = wx.ComboBox(self.box_steel_selection_select_menu, id = wx.ID_ANY, style = wx.CB_READONLY,choices = steel_type, value = steel_type[0] )
        self.box_steel_selection_select_menu.widgets_add(self.select_steel_type_menu)
        self.btn_ok = wx.Button(self.box_steel_selection_select_menu, label="Ok!")
        self.box_steel_selection_select_menu.widgets_add(self.btn_ok)
        self.btn_ok.Bind(wx.EVT_BUTTON, load_values_fy_fu)
        self.btn_edit = wx.Button(self.box_steel_selection_select_menu, label="Adicionar")
        self.box_steel_selection_select_menu.widgets_add(self.btn_edit)
        self.btn_edit.Bind(wx.EVT_BUTTON, load_edit_child_frame)
        self.label_fy = wx.StaticText(self.box_steel_selection_select_menu,id=wx.ID_ANY, label="fy (Mpa)")
        self.box_steel_selection_select_menu.widgets_add(self.label_fy)
        self.text_fy = wx.TextCtrl(self.box_steel_selection_select_menu, id=wx.ID_ANY, value = "")
        self.box_steel_selection_select_menu.widgets_add(self.text_fy)
        #quebra de linha vertical
        self.box_steel_selection_select_menu.widgets_add(wx.StaticLine(self.box_steel_selection_select_menu, style=wx.LI_VERTICAL))
        self.label_fu = wx.StaticText(self.box_steel_selection_select_menu,id=wx.ID_ANY, label="fu (Mpa)")
        self.box_steel_selection_select_menu.widgets_add(self.label_fu)
        self.text_fu = wx.TextCtrl(self.box_steel_selection_select_menu, id=wx.ID_ANY, value = "")
        self.box_steel_selection_select_menu.widgets_add(self.text_fu)

        self.main_sizer.Add(self.box_steel_type,proportion =  0, flag = wx.ALL | wx.EXPAND, border = 5) #adiciona o primeiro staticbox ao sizer principal da janela
        self.window_main_panel.SetSizer(self.main_sizer)
