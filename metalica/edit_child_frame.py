import wx
import wx.grid
import os
from itertools import product # para 2 for dentro de 1 linha

from wx.lib.sized_controls import border
from metalica.widget_class import StaticBox
from metalica.table_manipulation import ReadExcelFile

class EditChildFrame(wx.MDIChildFrame):
    def __init__(self, parent, frame_name):
        super().__init__(parent, id=wx.ID_ANY, title = frame_name,
                         pos=wx.DefaultPosition, size = (400,800), style = wx.DEFAULT_FRAME_STYLE)
        #----------------------------------------------------- sizer principal
        self.window_main_panel = wx.Panel(self) #cria o painel para por os objetos
        self.main_sizer = wx.BoxSizer(wx.VERTICAL) #define a organizacao das formas no sizer principal
        # ----------------------------------------------------- box
        self.edit_box = StaticBox(self.window_main_panel, "Editar",orientation = "vertical")
        self.img_box = StaticBox(self.edit_box,"Tensão deformação fy - fu", orientation = "vertical")
        self.edit_box.widgets_add(self.img_box)
        path = os.path.join(os.getcwd(), "icones", "fyfu.bmp") #----------------------------------------------------------------------
        self.img_crtl = wx.StaticBitmap(self.img_box, bitmap = wx.Bitmap(path))
        self.img_box.widgets_add(self.img_crtl)
        self.img_box.widgets_add(wx.StaticText(self.img_box, id = wx.ID_ANY, label = "fy - Resistência ao escoamento do aço",style = wx.ALIGN_CENTER))
        self.img_box.widgets_add(wx.StaticText(self.img_box, id=wx.ID_ANY, label = "fu - Resistência a ruptura do aço", style = wx.ALIGN_CENTER))
        self.table_box = StaticBox(self.edit_box,"Tabela", orientation = "vertical")
        self.edit_box.widgets_add(self.table_box)
        self.table_box_value_cel = StaticBox(self.table_box,"Valores", orientation = "vertical")
        self.table_box.widgets_add(self.table_box_value_cel)
        self.table_box_value_cel.SetMaxSize((wx.DefaultCoord,300))
        #------------------------------------------------------ table box
        self.grid = wx.grid.Grid(self.table_box_value_cel)
        self.table_box_value_cel.widgets_add(self.grid)
        self.data = ReadExcelFile("tipo_aco.xlsx") #read file
        line, col = self.data.read_number_of_coluns_and_lines()
        self.grid.CreateGrid(line, col)
        self.grid.SetColLabelValue(0,"Tipo")
        self.grid.SetColLabelValue(1, "fy")
        self.grid.SetColLabelValue(2,"fu")
        i = 0
        for l, c  in product(range(line), range(col)):
            values_table = self.data.read_values()
            cel_value = list(values_table.values())
            self.grid.SetCellValue(int(l),int(c),str(cel_value[i]))
            i+=1
        self.table_box_file = StaticBox(self.table_box,"Arquivo", orientation = "horizontal")
        self.table_box.widgets_add(self.table_box_file)
        self.btn_add = wx.Button(self.table_box_file, label="Adicionar")
        self.table_box_file.widgets_add(self.btn_add)
        self.btn_rmv = wx.Button(self.table_box_file, label="Remover")
        self.table_box_file.widgets_add(self.btn_rmv)
        self.btn_save= wx.Button(self.table_box_file, label="Salvar")
        self.table_box_file.widgets_add(self.btn_save)


        self.main_sizer.Add(self.edit_box,proportion =  0, flag = wx.ALL | wx.EXPAND, border = 5) #adiciona o primeiro staticbox ao sizer principal da janela
        self.window_main_panel.SetSizer(self.main_sizer)
