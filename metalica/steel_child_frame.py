import os.path
import wx
import wx.adv
from metalica.edit_child_frame import EditChildFrame
from metalica.widget_class import StaticBox
from metalica.table_manipulation import ReadExcelFile
from metalica.matplot_img_draw import DrawBeam
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from typing import Dict, Any # para mudar os valores da selecao

#() tupla [] lista {} dicionario
#criando o frame filho
class SteelChildFrame(wx.MDIChildFrame):
    def __init__(self, parent, frame_name):
        #parametros iniciais da janela
        super().__init__(parent, id=wx.ID_ANY, title = frame_name,
                         pos=(0,0), size = (800,600), style = wx.DEFAULT_FRAME_STYLE)
        self.parent = parent #atributo parente da janela
        #------------------------------------------------funcoes dos botoes
        self.data_steel_type = ReadExcelFile("steel.xlsx","tipo_de_aco")
        self.data_steel_lmn = ReadExcelFile("steel.xlsx","laminado")

        def load_values_fy_fu(event):
            selected_item = self.select_steel_type_menu.GetValue()
            fy_fu = self.data_steel_type.get_name_and_return_col_value("Tipo",f"{selected_item}",["fy", "fu"])
            fy, fu = float(fy_fu["fy"]), float(fy_fu["fu"]) #mudar aqui
            self.text_fy.SetValue(str(fy))
            self.text_fu.SetValue(str(fu))
        def load_edit_child_frame(event):
            edit_child = EditChildFrame(self.parent,"Editor")
            edit_child.Show()
        def on_select_perfil(event):
            #lista de valores ja tirados do excel e ja definidos nos rotulos
            label_and_object = {"Massa Linear kg/m" : self.linear_mass_text, "d (mm) : " : self.d_text, "bf (mm) : ": self.bf_text, "tw (mm) : ": self.tw_text, "tf (mm) : " : self.tf_text,
                                "h (mm) : " : self.h_text, "d' (mm) : ": self.d_l_text, "Área (cm²) : ": self.area_text, "Ix (cm^4) : " : self.i_x_text, "Wx (cm³) : ": self.w_x_text,
                                "rx (cm) : " :  self.r_x_text, "zx (cm) : ": self.z_x_text, "Iy (cm^4) : " :  self.i_y_text, "Wy (cm³) : " :  self.w_y_text, "ry (cm) : " : self.r_y_text,
                                "zy (cm³) : ": self.z_y_text, "rt (cm) : " : self.r_t_text ,"It (cm^4) : " : self.i_t_text, "Mesa bf/2.tf : " :  self.bf_two_text,
                                "Alma d'/tw : " : self.d_tw_text, "Cw (cm^6) : " : self.cw_text, "u (m²/m) : " : self.u_text}
            text_values = label_and_object.keys()
            option_selected = self.select_steel_perfil.GetStringSelection()
            return_values_dimension = self.data_steel_lmn.get_name_and_return_col_value("BITOLA mm x kg/mgraus",f"{option_selected}",text_values)

            for name_col, value  in return_values_dimension.items():
                label = str(name_col) + " " + str(value)
                if name_col in label_and_object.keys():
                    label = label_and_object[name_col]
                    novo_texto = f"{label.GetLabel().split(':')[0]}: {value}"
                    if label.GetLabel() != novo_texto:
                        label.SetLabel(novo_texto)
                self.Layout()
            self.box_desenho.draw_w_hp(return_values_dimension["d (mm) : "], return_values_dimension["bf (mm) : "], return_values_dimension["tw (mm) : "])
            self.canvas.draw()
            #fazer as variacoes para os tipos de perfis 
            # path = os.path.join(os.getcwd(), "icones", "whp.bmp")
            # self.img_crtl_perfil.SetBitmap(wx.Bitmap(path))
            # self.img_crtl_perfil.GetParent().Layout() #atualiza a imagem

        #------------------------------------------------
        self.window_main_panel = wx.Panel(self) #cria o painel para por os objetos
        self.main_sizer = wx.BoxSizer(wx.VERTICAL) #define a organizacao das formas no sizer principal
        #------------------------------------------------- selecao do aco
        self.box_steel_type = StaticBox(self.window_main_panel, "Tipo do aço",orientation = "vertical")
        self.box_steel_selection_select_menu = StaticBox(self.box_steel_type, box_label = "Selecione uma opção", orientation = "horizontal") # staticbox de selecao
        self.box_steel_type.widgets_add(self.box_steel_selection_select_menu,  0,True) # adiciona a static box de selecao ao sizer principal
        steel_type = self.data_steel_type.return_value_by_one_col("Tipo")
        #adiciona o select menu dentro do steel type
        self.select_steel_type_menu = wx.ComboBox(self.box_steel_selection_select_menu, id = wx.ID_ANY, style = wx.CB_READONLY,choices = steel_type, value = steel_type[0] )
        self.box_steel_selection_select_menu.widgets_add(self.select_steel_type_menu,0, True)
        self.btn_ok = wx.Button(self.box_steel_selection_select_menu, label="Ok")
        self.box_steel_selection_select_menu.widgets_add(self.btn_ok, 0, True)
        self.btn_ok.Bind(wx.EVT_BUTTON, load_values_fy_fu)
        self.btn_edit = wx.Button(self.box_steel_selection_select_menu, label="Editar")
        self.box_steel_selection_select_menu.widgets_add(self.btn_edit, 0, True)
        self.btn_edit.Bind(wx.EVT_BUTTON, load_edit_child_frame)
        self.label_fy = wx.StaticText(self.box_steel_selection_select_menu,id=wx.ID_ANY, label="fy (Mpa)")
        self.box_steel_selection_select_menu.widgets_add(self.label_fy, 0, True)
        self.text_fy = wx.TextCtrl(self.box_steel_selection_select_menu, id=wx.ID_ANY, value = "", size=(10,10))
        self.box_steel_selection_select_menu.widgets_add(self.text_fy, 0, True)
        #quebra de linha vertical
        self.box_steel_selection_select_menu.widgets_add(wx.StaticLine(self.box_steel_selection_select_menu, style=wx.LI_VERTICAL), 0,False)
        self.label_fu = wx.StaticText(self.box_steel_selection_select_menu,id=wx.ID_ANY, label="fu (Mpa)")
        self.box_steel_selection_select_menu.widgets_add(self.label_fu, 0, True)
        self.text_fu = wx.TextCtrl(self.box_steel_selection_select_menu, id=wx.ID_ANY, value = "", size = (10,10))
        self.box_steel_selection_select_menu.widgets_add(self.text_fu, 0,True)
        #------------------------------------------------- selecao do perfil
        self.box_perfil = StaticBox(self.window_main_panel, "Escolha do perfil", orientation="horizontal")
        self.box_perfil_selection = StaticBox(self.box_perfil, "Selecione um perfil", orientation= "vertical")
        self.box_perfil.widgets_add(self.box_perfil_selection, 0, "False")
        # self.box_perfil_selection_size_fix = StaticBox(self.box_perfil, "Selecione um perfil", orientation= "vertical")
        # self.box_perfil.widgets_add(self.box_perfil_selection_size_fix, 0, "False")
        self.box_perfil_data = StaticBox(self.box_perfil, "Dados do perfil perfil", orientation="grid")
        self.box_perfil.widgets_add(self.box_perfil_data, 0, True)
        perfil_type = self.data_steel_lmn.return_value_by_one_col("BITOLA mm x kg/mgraus")
        self.select_steel_perfil = wx.ComboBox(self.box_perfil_selection, id = wx.ID_ANY, style = wx.CB_READONLY,choices = perfil_type) #VERIFICAR pq ele fica grande mesmo nao expandindo
        self.select_steel_perfil.SetMaxSize(wx.Size(-1, 20))
        self.select_steel_perfil.Bind(wx.EVT_COMBOBOX, on_select_perfil)
        self.box_perfil_selection.widgets_add(self.select_steel_perfil, 0, "False")
        self.box_perfil_selection.widgets_add(wx.StaticLine(self.box_perfil_selection, style=wx.LI_HORIZONTAL), 0,False) #linha horizontal separar caixa de selecao e imagem
        #------------------------------------------------- imagem do perfil
        self.box_desenho = DrawBeam()
        self.canvas = FigureCanvas(self.box_perfil_selection, -1, self.box_desenho.fig)
        self.box_perfil_selection.widgets_add(self.canvas, 0, False)
        #coluna 1
        self.linear_mass_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Massa Linear (kg/m) : ")
        self.box_perfil_data.widgets_add(self.linear_mass_text, 0, False)
        self.d_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="d (mm) : ")
        self.box_perfil_data.widgets_add(self.d_text, 0, False)
        self.bf_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="bf (mm) : ")
        self.box_perfil_data.widgets_add(self.bf_text, 0, False)
        self.tw_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="tw (mm) : ")
        self.box_perfil_data.widgets_add(self.tw_text, 0, False)
        self.tf_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="tf (mm) : ")
        self.box_perfil_data.widgets_add(self.tf_text, 0, False)
        self.h_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="h (mm) : ")
        self.box_perfil_data.widgets_add(self.h_text, 0, False)
        self.d_l_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="d' (mm) : ")
        self.box_perfil_data.widgets_add(self.d_l_text, 0, False)
        self.area_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Área (cm²) : ")
        self.box_perfil_data.widgets_add(self.area_text, 0, False)
        self.i_x_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Ix (cm^4) : ")
        self.box_perfil_data.widgets_add(self.i_x_text, 0, False)
        self.w_x_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Wx (cm³) : ")
        self.box_perfil_data.widgets_add(self.w_x_text, 0, False)
        self.r_x_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="rx (cm) : ")
        self.box_perfil_data.widgets_add(self.r_x_text, 0, False)
        self.z_x_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="zx (cm) : ")
        self.box_perfil_data.widgets_add(self.z_x_text, 0, False)
        self.i_y_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Iy (cm^4) : ")
        self.box_perfil_data.widgets_add(self.i_y_text, 0, False)
        self.w_y_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Wy (cm³) : ")
        self.box_perfil_data.widgets_add(self.w_y_text , 0, False)
        self.r_y_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="ry (cm) : ")
        self.box_perfil_data.widgets_add(self.r_y_text , 0, False)
        self.z_y_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="zy (cm³) : ")
        self.box_perfil_data.widgets_add(self.z_y_text , 0, False)
        self.r_t_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="rt (cm) : ")
        self.box_perfil_data.widgets_add(self.r_t_text , 0, False)
        self.i_t_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="It (cm^4) : ")
        self.box_perfil_data.widgets_add(self.i_t_text , 0, False)
        self.bf_two_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Mesa bf/2.tf : ")
        self.box_perfil_data.widgets_add(self.bf_two_text , 0, False)
        self.d_tw_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Alma d'/tw : ")
        self.box_perfil_data.widgets_add(self.d_tw_text , 0, False)
        self.cw_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Cw (cm^6) : ")
        self.box_perfil_data.widgets_add(self.cw_text , 0, False)
        self.u_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="u (m²/m) : ")
        self.box_perfil_data.widgets_add(self.u_text , 0, False)
        # #coluna 2
        # self.linear_mass_text_result = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="linear_mass_text_result")
        # self.box_perfil_data.widgets_add(self.linear_mass_text_result, 1, False)
        # self.d_text_result = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="gfhfghfghfghfgh")
        # self.box_perfil_data.widgets_add(self.d_text_result, 1, False)
        # # self.box_perfil_data.add_to_grid(self.linear_mass_text, col=0)
        # # self.box_perfil_data.add_to_grid(self.linear_mass_text2, col=1)


        self.main_sizer.Add(self.box_steel_type,proportion =  0, flag = wx.ALL | wx.EXPAND, border = 5) #adiciona o primeiro staticbox ao sizer principal da janela
        self.main_sizer.Add(self.box_perfil, proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5)
        self.window_main_panel.SetSizer(self.main_sizer)
