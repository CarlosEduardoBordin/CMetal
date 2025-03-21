from cProfile import label
from sys import flags

import wx
import wx.adv
from numpy.random import choice
from wx.lib.sized_controls import border


#criando uma classe para os wx.StaticBox rotulo - orientacao do sizer
class StaticBox(wx.Panel):
    #criacao do box
    def __init__(self, parent, box_label, orientation):
        super().__init__(parent)
        self.box = wx.StaticBox(self, label = box_label)
        self.sizer_box = wx.StaticBoxSizer(self.box, orientation)
        self.SetSizer(self.sizer_box)
    # configuracao do widget interno
    def widgets_add(self, widget):
        self.sizer_box.Add(widget, flag=wx.ALL, border=5)
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
        self.box_steel_selection = StaticBox(self.window_main_panel, "Tipo do aço",orientation = wx.VERTICAL)
        self.box_steel_selection.widgets_add(wx.StaticText(self.box_steel_selection, label="Selecione uma opção"))
        languages = ['C', 'C++', 'Python', 'Java', 'Perl']
        self.box_steel_selection.widgets_add(wx.ComboBox(self.box_steel_selection, id = wx.ID_ANY, style = wx.CB_READONLY,choices = languages))
        #-------------cria a static box para dar ok ou alterar o tipo do material
        self.box_steel_selection_edit = StaticBox(self.box_steel_selection, box_label = "Editar", orientation = wx.HORIZONTAL)

        self.btn_ok_selection_steel = wx.Button(self.box_steel_selection_edit, label="OK!")
        self.box_steel_selection_edit.widgets_add(self.btn_ok_selection_steel)

        self.btn_edit_selection_steel = wx.Button(self.box_steel_selection_edit, label="Editar")
        self.box_steel_selection_edit.widgets_add(self.btn_edit_selection_steel)
        #adiciona a box editar dentro da box steel selection
        self.box_steel_selection.widgets_add(self.box_steel_selection_edit)
        #-------------------------------------------------
        self.main_sizer.Add(self.box_steel_selection,proportion =  0, flag = wx.ALL | wx.EXPAND, border = 5)
        self.window_main_panel.SetSizer(self.main_sizer)
