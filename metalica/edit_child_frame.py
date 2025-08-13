import wx
import wx.grid
import os
from itertools import product # para 2 for dentro de 1 linha
from widget_class import StaticBox
from table_manipulation import ReadExcelFile
from table_manipulation import WriteExcelFile

class EditChildFrame(wx.MDIChildFrame):
    def __init__(self, parent, frame_name):
        super().__init__(parent, id=wx.ID_ANY, title = frame_name,
                         pos=wx.DefaultPosition, size = (400,670), style = wx.DEFAULT_FRAME_STYLE)

        def add_line(event):
            self.grid.AppendRows(1)
        def rmv_line(event):
            line_numbers = self.grid.GetNumberRows()
            if line_numbers > 0:
                self.grid.DeleteRows(line_numbers -1,1)
        def save_table(event):
            num_lines = self.grid.GetNumberRows()
            num_cols = self.grid.GetNumberCols()
            data = []
            for ln in range(num_lines):
                line_data = []
                for cls in range(num_cols):
                    line_data.append(self.grid.GetCellValue(ln, cls))  # Capturar valor da célula
                data.append(line_data)
            print(data)
            file_save_name = WriteExcelFile("steel.xlsx")
            file_save_name.save_data_to_file("tipo_de_aco", data, num_cols, ["Tipo", "fy","fu"])

        #----------------------------------------------------- sizer principal
        self.window_main_panel = wx.Panel(self) #cria o painel para por os objetos
        self.main_sizer = wx.BoxSizer(wx.VERTICAL) #define a organizacao das formas no sizer principal
        # ----------------------------------------------------- box
        self.edit_box = StaticBox(self.window_main_panel, "Editar",orientation = "vertical")
        self.img_box = StaticBox(self.edit_box,"Tensão deformação fy - fu", orientation = "vertical")
        self.edit_box.widgets_add(self.img_box, 0,False)
        path = os.path.join(os.getcwd(), "icones", "fyfu.bmp") #----------------------------------------------------------------------
        self.img_crtl = wx.StaticBitmap(self.img_box, bitmap = wx.Bitmap(path))
        self.img_box.widgets_add(self.img_crtl, 0,False)
        self.img_box.widgets_add(wx.StaticText(self.img_box, id = wx.ID_ANY, label = "fy - Resistência ao escoamento do aço",style = wx.ALIGN_CENTER),0,False)
        self.img_box.widgets_add(wx.StaticText(self.img_box, id=wx.ID_ANY, label = "fu - Resistência a ruptura do aço", style = wx.ALIGN_CENTER), 0,False)
        self.table_box = StaticBox(self.edit_box,"Tabela", orientation = "vertical")
        self.edit_box.widgets_add(self.table_box, 0,True)
        self.table_box_value_cel = StaticBox(self.table_box,"Valores", orientation = "vertical")
        self.table_box.widgets_add(self.table_box_value_cel, 0, False)
        self.table_box_value_cel.SetMaxSize((wx.DefaultCoord,200))
        #------------------------------------------------------ table box
        self.grid = wx.grid.Grid(self.table_box_value_cel)
        self.table_box_value_cel.widgets_add(self.grid, 0,True)
        self.data = ReadExcelFile("steel.xlsx", "tipo_de_aco") #read file
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
        self.table_box.widgets_add(self.table_box_file, 0,True)
        self.btn_add = wx.Button(self.table_box_file, label="Adicionar")
        self.btn_add.SetBitmapPosition(wx.LEFT)
        self.btn_add.SetBitmap(wx.Bitmap("icones/mais.png", wx.BITMAP_TYPE_PNG))
        self.table_box_file.widgets_add(self.btn_add, 0,True)
        self.btn_add.Bind(wx.EVT_BUTTON, add_line)
        self.btn_rmv = wx.Button(self.table_box_file, label="Remover")
        self.btn_rmv.SetBitmapPosition(wx.LEFT)
        self.btn_rmv.SetBitmap(wx.Bitmap("icones/menos.png", wx.BITMAP_TYPE_PNG))
        self.table_box_file.widgets_add(self.btn_rmv, 0,True)
        self.btn_rmv.Bind(wx.EVT_BUTTON, rmv_line)
        self.btn_save= wx.Button(self.table_box_file, label="Salvar")
        self.btn_save.SetBitmapPosition(wx.LEFT)
        self.btn_save.SetBitmap(wx.Bitmap("icones/disquete.png", wx.BITMAP_TYPE_PNG))
        self.table_box_file.widgets_add(self.btn_save, 0,True)
        self.btn_save.Bind(wx.EVT_BUTTON, save_table)


        self.main_sizer.Add(self.edit_box,proportion =  0, flag = wx.ALL | wx.EXPAND, border = 5) #adiciona o primeiro staticbox ao sizer principal da janela
        self.window_main_panel.SetSizer(self.main_sizer)
