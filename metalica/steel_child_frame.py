import wx
import wx.adv
import re #biblioteca de expressoes
from metalica.edit_child_frame import EditChildFrame
from widget_class import StaticBox , TextBoxVrf, SaveBox
from metalica.table_manipulation import ReadExcelFile
from metalica.matplot_img_draw import DrawBeam
from metalica.verification_process import VerificationProcess
from metalica.help_steel_child_frame import ImgHelpButton
from metalica.values_config_child_frame import ValuesConfiguration
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


#() tupla [] lista {} dicionario
#criando o frame filho
class SteelChildFrame(wx.MDIChildFrame):
    def __init__(self, parent, frame_name):
        #parametros iniciais da janela
        super().__init__(parent, id=wx.ID_ANY, title = frame_name,
                         pos=(0,0), size = (800,740), style = wx.DEFAULT_FRAME_STYLE)
        self.parent = parent #atributo parente da janela
        #------------------------------------------------funcoes dos botoes
        self.data_steel_type = ReadExcelFile("steel.xlsx","tipo_de_aco")
        self.data_steel_lmn = ReadExcelFile("steel.xlsx","laminado")


        # **************************************************************************************** SUM sistema de unidade de medida
        #trabalhando em m, KN, Pa para realizar o calculo final!
        #evento de atualizacao das unidades de medidas dispostas na cfg
        self.factor_multiplier_lenght = { "mm": 0.001, "cm": 0.01, "m": 1.0}
        self.factor_multiplier_area = {"mm²" : 0.000001, "cm²" : 0.0001, "m²" : 1 }
        self.factor_multiplier_volume = {"mm³" : 0.000000001, "cm³" : 0.000001, "m³" : 1 }
        self.factor_multiplier_inertia = {"mm^4": 0.000000000001, "cm^4": 0.00000001, "m^4": 1}
        self.factor_multiplier_six_elevated = {"mm^6": 0.000000000000000001, "cm^6": 0.000000000001, "m^6": 1}
        self.factor_multiplier_force = {"N" : 1, "KN": 1000, "MN": 1000000}
        self.factor_multiplier_moment = {"Nm": 1, "KNm": 1000, "MNm":1000000}
        self.factor_multiplier_press = {"Pa" : 1, "KPa" : 1000, "MPa": 1000000, "GPa": 1000000000}

        # def unit_converter(value, origin_unit, conversion_factor_dict) -> float: #converter para float
        #     #converte usando um dicionario
        #     factor = conversion_factor_dict.get(origin_unit, 1.0)
        #     return value * factor

        def unit_converter(value: float, from_unit: str, to_unit: str, conversion_factor_dict: dict) -> float:
            if from_unit not in conversion_factor_dict:
                raise ValueError(f"Unidade de origem {from_unit} não reconhecida.")
            if to_unit not in conversion_factor_dict:
                raise ValueError(f"Unidade de destino {to_unit} não reconhecida.")

            # Converter para unidade base (multiplicador = 1), depois para unidade de destino
            value_in_base = value * conversion_factor_dict[from_unit]
            converted_value = value_in_base / conversion_factor_dict[to_unit]
            return converted_value


        def unit_extractor(text_for_extratiction):
            #acha a unidade de dentro do texto entre ()
            match = re.search(r"\((.*?)\)", text_for_extratiction)
            if match:
                return match.group(1)
           #se nao achar pega a ultima palavra - ver se funciona
            parts = text_for_extratiction.strip().split()
            if parts:
                return parts[-1]

            return None  # Retorna None se nenhuma unidade for encontrada

        # funcao para quando a janela estiver ativa ela atualizar automaticamente verificar como fazer para as unidades ja colocadas
        def on_activate_window(event):
            #quando o evento esta ativo
            if event.GetActive():
                self.text_lfx.SetLabel(f"Lfx ({self.parent.get_unit_lenght()[0]}) :")
                self.text_lfy.SetLabel(f"Lfy ({self.parent.get_unit_lenght()[0]}) :")
                self.text_lz.SetLabel(f"Lfz ({self.parent.get_unit_lenght()[0]}) :")
                self.text_lf.SetLabel(f"Lf ({self.parent.get_unit_lenght()[0]}) :")
                self.text_fnc.SetLabel(f"Normal compressão ({self.parent.get_unit_force()[0]}) :")
                self.text_fnt.SetLabel(f"Normal tração ({self.parent.get_unit_force()[0]}) :")
                self.text_fcx.SetLabel(f"Cortante X ({self.parent.get_unit_force()[0]}) :")
                self.text_fcy.SetLabel(f"Cortante Y ({self.parent.get_unit_force()[0]}) :")
                self.text_mx.SetLabel(f"Momento X ({self.parent.get_unit_moment()[0]}) :")
                self.text_my.SetLabel(f"Momento Y ({self.parent.get_unit_moment()[0]}) :")

            event.Skip()
        self.Bind(wx.EVT_ACTIVATE, on_activate_window)
        # ****************************************************************************************************************


        def load_values_fy_fu(event):
            selected_item = self.select_steel_type_menu.GetValue()
            fy_fu = self.data_steel_type.get_name_and_return_col_value("Tipo",f"{selected_item}",["fy", "fu"])
            fy, fu = float(fy_fu["fy"]), float(fy_fu["fu"]) #mudar aqui
            self.text_fy.SetValue(str(fy))
            self.text_fu.SetValue(str(fu))
        def load_edit_child_frame(event):
            edit_child = EditChildFrame(self.parent,"Editor")
            edit_child.Show()
            # lista de valores ja tirados do excel e ja definidos nos rotulos
        def on_select_perfil(event):
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
        def on_help_button_img(event):
            help_frame = ImgHelpButton(self.parent,"Ajuda")
            help_frame.Show()
        def on_values_cfg(event):
            values_cfg = ValuesConfiguration(self.parent,"Configurar as variáveis")
            values_cfg.Show()
        def on_calculate(event):
            # fy = self.text_fy.get_value()
            # fu = self.text_fu.get_value()
            # lfx_value = self.input_lfx.get_value()
            # lfy_value = self.input_lfy.get_value()
            # lfz_value = self.input_lfz.get_value()
            # lb_value = self.input_lfb.get_value()
            # fn_value = self.input_fn.get_value()
            # fc_value = self.input_fc.get_value()
            # mfx_value = self.input_mx.get_value()
            # mfy_value = self.input_my.get_value()
            fy = self.text_fy.get_value()
            fu = self.text_fu.get_value()
            lfx_value = unit_converter(self.input_lfx.get_value(), parent.get_unit_lenght(),"m" ,self.factor_multiplier_lenght)
            lfy_value = unit_converter(self.input_lfy.get_value(), parent.get_unit_lenght(), "m",self.factor_multiplier_lenght)
            lfz_value = unit_converter(self.input_lfz.get_value(), parent.get_unit_lenght(), "m",  self.factor_multiplier_lenght)
            lb_value = unit_converter(self.input_lfb.get_value(), parent.get_unit_lenght(), "m", self.factor_multiplier_lenght)
            fnt_value = unit_converter(self.input_fnt.get_value(), parent.get_unit_force(), "N", self.factor_multiplier_force)
            fnc_value = unit_converter(self.input_fnc.get_value(), parent.get_unit_force(), "N",
                                       self.factor_multiplier_force)
            fcx_value = unit_converter(self.input_fcx.get_value(), parent.get_unit_force(), "N", self.factor_multiplier_force)
            fcy_value = unit_converter(self.input_fcy.get_value(), parent.get_unit_force(), "N",
                                      self.factor_multiplier_force)
            mfx_value = unit_converter(self.input_mx.get_value(), parent.get_unit_moment(), "KNm", self.factor_multiplier_moment)
            mfy_value = unit_converter(self.input_my.get_value(), parent.get_unit_moment(), "KNm", self.factor_multiplier_moment)

            text_values = label_and_object.keys()
            option_selected = self.select_steel_perfil.GetStringSelection()

            return_values_dimension = self.data_steel_lmn.get_name_and_return_col_value("BITOLA mm x kg/mgraus",
                                                                                        f"{option_selected}",
                                                                                        text_values)
            value_list_perfil = list(return_values_dimension.values())

            transformed_list_perfil_data = []
            i = 0
            for unit, value_adress in label_and_object.items():
                search_unit = unit_extractor(unit)
                value_converted = 0
                if search_unit in self.factor_multiplier_lenght:
                    value_converted = unit_converter(value_list_perfil[i], search_unit, "m", self.factor_multiplier_lenght)
                elif search_unit in self.factor_multiplier_area:
                    value_converted = unit_converter(value_list_perfil[i], search_unit, "m²",
                                                     self.factor_multiplier_area)
                elif search_unit in self.factor_multiplier_volume:
                    value_converted = unit_converter(value_list_perfil[i], search_unit, "m³",
                                                     self.factor_multiplier_volume)
                elif search_unit in self.factor_multiplier_inertia:
                    value_converted = unit_converter(value_list_perfil[i], search_unit, "m^4",
                                                     self.factor_multiplier_inertia)
                elif search_unit in self.factor_multiplier_six_elevated:
                    value_converted = unit_converter(value_list_perfil[i], search_unit, "m^6",
                                                     self.factor_multiplier_six_elevated)
                elif search_unit in self.factor_multiplier_force:
                    value_converted = unit_converter(value_list_perfil[i], search_unit, "N",
                                                     self.factor_multiplier_force)
                elif search_unit in self.factor_multiplier_moment:
                    value_converted = unit_converter(value_list_perfil[i], search_unit, "Nm",
                                                     self.factor_multiplier_moment)
                elif search_unit in self.factor_multiplier_press:
                    value_converted = unit_converter(value_list_perfil[i], search_unit, "Pa",
                                                     self.factor_multiplier_press)
                else:
                    value_converted = value_list_perfil[i]
                value_converted = float(value_converted)
                transformed_list_perfil_data.extend([value_converted])
                i += 1
            print(transformed_list_perfil_data)
            values_to_append = [float(fy)*10**6, float(fu)*10**6, lfx_value, lfy_value, lfz_value, lb_value, fnt_value, fnc_value, fcx_value, fcy_value, mfx_value, mfy_value, 1.1, 1.1, 77000000000,200000000000,1]
            transformed_list_perfil_data.extend(values_to_append)


            self.save_dialog = SaveBox(self.parent) #abrir o dialogo de salvar
            path = self.save_dialog.get_path()
            self.save_dialog.Destroy()
            print(f"{path}")
            self.data = VerificationProcess(*transformed_list_perfil_data,frame_name, path)
            self.data.calculate()


        #------------------------------------------------
         # self.window_main_panel = wx.Panel(self) #cria o painel para por os objetos -> mudar para scroll notebook 720p nao aparece a janela inteira!
        self.window_main_panel = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.window_main_panel.SetScrollRate(0, 20)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL) #define a organizacao das formas no sizer principal


        self.box_steel_type = StaticBox(self.window_main_panel, "Tipo do aço",orientation = "vertical")
        self.box_steel_selection_select_menu = StaticBox(self.box_steel_type, box_label = "Selecione uma opção", orientation = "horizontal") # staticbox de selecao
        self.box_steel_type.widgets_add(self.box_steel_selection_select_menu,  0,False) # adiciona a static box de selecao ao sizer principal
        steel_type = self.data_steel_type.return_value_by_one_col("Tipo")
        #adiciona o select menu dentro do steel type
        self.select_steel_type_menu = wx.ComboBox(self.box_steel_selection_select_menu, id = wx.ID_ANY, style = wx.CB_READONLY,choices = steel_type, value = steel_type[1] )
        self.box_steel_selection_select_menu.widgets_add(self.select_steel_type_menu,0, False)
        self.btn_ok = wx.Button(self.box_steel_selection_select_menu, label="Ok")
        self.box_steel_selection_select_menu.widgets_add(self.btn_ok, 0, False)
        self.btn_ok.Bind(wx.EVT_BUTTON, load_values_fy_fu)
        self.btn_edit = wx.Button(self.box_steel_selection_select_menu, label="Editar")
        self.box_steel_selection_select_menu.widgets_add(self.btn_edit, 0, False)
        self.btn_edit.Bind(wx.EVT_BUTTON, load_edit_child_frame)
        self.label_fy = wx.StaticText(self.box_steel_selection_select_menu,id=wx.ID_ANY, label="fy (MPa)")
        self.box_steel_selection_select_menu.widgets_add(self.label_fy, 0, False)
        self.text_fy = TextBoxVrf(self.box_steel_selection_select_menu, value = "0", only_numeric=False)
        self.box_steel_selection_select_menu.widgets_add(self.text_fy, 0, False)
        #quebra de linha vertical
        self.box_steel_selection_select_menu.widgets_add(wx.StaticLine(self.box_steel_selection_select_menu, style=wx.LI_VERTICAL), 0,False)
        self.label_fu = wx.StaticText(self.box_steel_selection_select_menu,id=wx.ID_ANY, label="fu (MPa)")
        self.box_steel_selection_select_menu.widgets_add(self.label_fu, 0, False)
        self.text_fu = TextBoxVrf(self.box_steel_selection_select_menu, value = "0", only_numeric=False)
        self.box_steel_selection_select_menu.widgets_add(self.text_fu, 0,False)
        #------------------------------------------------- selecao do perfil
        self.box_perfil = StaticBox(self.window_main_panel, "Escolha do perfil", orientation="horizontal")
        self.box_perfil_selection = StaticBox(self.box_perfil, "Selecione um perfil", orientation= "vertical")
        self.box_perfil.widgets_add(self.box_perfil_selection, 0, False)
        # self.box_perfil_selection_size_fix = StaticBox(self.box_perfil, "Selecione um perfil", orientation= "vertical")
        # self.box_perfil.widgets_add(self.box_perfil_selection_size_fix, 0, "False")
        self.box_perfil_data = StaticBox(self.box_perfil, "Dados do perfil perfil", orientation="grid")
        self.box_perfil_data.SetMaxSize((800, -1))
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
        #btn ajuda
        self.button_help = wx.Button(self.box_perfil_selection, label = "Ajuda")
        self.box_perfil_selection.widgets_add(self.button_help, 0, True)
        self.button_help.Bind(wx.EVT_BUTTON, on_help_button_img)
        #coluna 1
        self.linear_mass_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Massa Linear (kg/m) :       ")
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
        self.z_x_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="zx (cm³) : ")
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
        self.u_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="u (m^2/m) : ")
        self.box_perfil_data.widgets_add(self.u_text , 0, False)
        #------------------------------------------------- box valores
        self.box_values_input = StaticBox(self.window_main_panel,"Verificação", orientation = "horizontal")
        #comprimentos de flambagem
        self.box_lengths = StaticBox(self.box_values_input, "Comprimentos do elemento", orientation= "grid")
        self.box_values_input.widgets_add(self.box_lengths,0, False)
        self.text_lfx = wx.StaticText(self.box_lengths,id = wx.ID_ANY, label = "Lx (m) :")
        self.box_lengths.widgets_add(self.text_lfx, 0, False)
        self.input_lfx = TextBoxVrf(self.box_lengths, value = "1", only_numeric=True)
        self.box_lengths.widgets_add(self.input_lfx, 1,False)
        self.text_lfy = wx.StaticText(self.box_lengths,id = wx.ID_ANY, label = "Ly (m) :")
        self.box_lengths.widgets_add(self.text_lfy, 0, False)
        self.input_lfy = TextBoxVrf(self.box_lengths, value = "1", only_numeric=True)
        self.box_lengths.widgets_add(self.input_lfy, 1,False)
        self.text_lz = wx.StaticText(self.box_lengths,id = wx.ID_ANY, label = "Lz (m) :")
        self.box_lengths.widgets_add(self.text_lz, 0, False)
        self.input_lfz = TextBoxVrf(self.box_lengths,  value = "1", only_numeric=True)
        self.box_lengths.widgets_add(self.input_lfz, 1,False)
        self.text_lf = wx.StaticText(self.box_lengths,id = wx.ID_ANY, label = "Lf (m) :")
        self.box_lengths.widgets_add(self.text_lf, 0, False)
        self.input_lfb = TextBoxVrf(self.box_lengths,  value = "1", only_numeric=True)
        self.box_lengths.widgets_add(self.input_lfb, 1,False)
        self.text_values_cfg = wx.StaticText(self.box_lengths,id = wx.ID_ANY, label = "Variáveis :")
        self.box_lengths.widgets_add(self.text_values_cfg, 0, False)
        self.button_cfg_values = wx.Button(self.box_lengths, label = "Configurar")
        self.box_lengths.widgets_add(self.button_cfg_values, 1,  False)
        self.button_cfg_values.Bind(wx.EVT_BUTTON, on_values_cfg)
        #valores dos esforcos
        self.box_load_solicitation = StaticBox(self.box_values_input, "Solicitações", orientation= "grid")
        self.box_values_input.widgets_add(self.box_load_solicitation, 0, False)
        self.text_fnt = wx.StaticText(self.box_load_solicitation, id=wx.ID_ANY, label="Normal tração (KN) :")
        self.box_load_solicitation.widgets_add(self.text_fnt, 0, False)
        self.input_fnt = TextBoxVrf(self.box_load_solicitation, value = "1", only_numeric=True)
        self.box_load_solicitation.widgets_add(self.input_fnt, 1, False)
        self.text_fnc = wx.StaticText(self.box_load_solicitation, id=wx.ID_ANY, label="Normal compressão (KN) :")
        self.box_load_solicitation.widgets_add(self.text_fnc, 0, False)
        self.input_fnc = TextBoxVrf(self.box_load_solicitation, value = "1", only_numeric=True)
        self.box_load_solicitation.widgets_add(self.input_fnc, 1, False)
        self.text_fcx = wx.StaticText(self.box_load_solicitation, id=wx.ID_ANY, label="Cortante X (KN) :")
        self.box_load_solicitation.widgets_add(self.text_fcx, 0, False)
        self.input_fcx = TextBoxVrf(self.box_load_solicitation, value = "1", only_numeric=True)
        self.box_load_solicitation.widgets_add(self.input_fcx, 1, False)
        self.text_fcy = wx.StaticText(self.box_load_solicitation, id=wx.ID_ANY, label="Cortante Y (KN) :")
        self.box_load_solicitation.widgets_add(self.text_fcy, 0,  False)
        self.input_fcy = TextBoxVrf(self.box_load_solicitation, value = "1",only_numeric=True)
        self.box_load_solicitation.widgets_add(self.input_fcy, 1, False)
        self.text_mx = wx.StaticText(self.box_load_solicitation, id=wx.ID_ANY, label="Momento X (Kn*m) :")
        self.box_load_solicitation.widgets_add(self.text_mx, 0, False)
        self.input_mx = TextBoxVrf(self.box_load_solicitation, value = "1",only_numeric=True)
        self.box_load_solicitation.widgets_add(self.input_mx, 1, False)
        self.text_my = wx.StaticText(self.box_load_solicitation, id=wx.ID_ANY, label="Momento Y (Kn*m) :")
        self.box_load_solicitation.widgets_add(self.text_my, 0, False)
        self.input_my = TextBoxVrf(self.box_load_solicitation, value = "1",only_numeric=True)
        self.box_load_solicitation.widgets_add(self.input_my, 1, False)
        #------------------------------------------------- #dicionario de variaveis
        label_and_object = {"Massa Linear kg/m": self.linear_mass_text, "d (mm) : ": self.d_text,
                            "bf (mm) : ": self.bf_text, "tw (mm) : ": self.tw_text, "tf (mm) : ": self.tf_text,
                            "h (mm) : ": self.h_text, "d' (mm) : ": self.d_l_text, "Área (cm²) : ": self.area_text,
                            "Ix (cm^4) : ": self.i_x_text, "Wx (cm³) : ": self.w_x_text,
                            "rx (cm) : ": self.r_x_text, "zx (cm³) : ": self.z_x_text, "Iy (cm^4) : ": self.i_y_text,
                            "Wy (cm³) : ": self.w_y_text, "ry (cm) : ": self.r_y_text,
                            "zy (cm³) : ": self.z_y_text, "rt (cm) : ": self.r_t_text,
                            "It (cm^4) : ": self.i_t_text, "Mesa bf/2.tf : ": self.bf_two_text,
                            "Alma d'/tw : ": self.d_tw_text, "Cw (cm^6) : ": self.cw_text,
                            "u (m²/m) : ": self.u_text}

        #         label_and_object = {"Massa Linear kg/m": self.linear_mass_text, "d (mm) : ": self.d_text,
        #                             "bf (mm) : ": self.bf_text, "tw (mm) : ": self.tw_text, "tf (mm) : ": self.tf_text,
        #                             "h (mm) : ": self.h_text, "d' (mm) : ": self.d_l_text, "Área (cm²) : ": self.area_text,
        #                             "Ix (cm^4) : ": self.i_x_text, "Wx (cm³) : ": self.w_x_text,
        #                             "rx (cm) : ": self.r_x_text, "zx (cm) : ": self.z_x_text, "Iy (cm^4) : ": self.i_y_text,
        #                             "Wy (cm³) : ": self.w_y_text, "ry (cm) : ": self.r_y_text,
        #                             "zy (cm³) : ": self.z_y_text, "rt (cm) : ": self.r_t_text,
        #                             "It (cm^4) : ": self.i_t_text, "Mesa bf/2.tf : ": self.bf_two_text,
        #                             "Alma d'/tw : ": self.d_tw_text, "Cw (cm^6) : ": self.cw_text,
        #                             "u (m²/m) : ": self.u_text}

        #------------------------------------------------- box resultados - verificar como vai ser gerado o relatorio
        self.box_results = StaticBox(self.box_values_input, "Resultados", orientation= "vertical")
        self.box_values_input.widgets_add(self.box_results, 0, True)
        self.calculate =  wx.Button(self.box_results, label = "Calcular")
        self.box_results.widgets_add(self.calculate, 0, False)
        self.calculate.Bind(wx.EVT_BUTTON, on_calculate)
        self.box_status = StaticBox(self.box_results, "Situação:", orientation = "vertical")
        self.box_results.widgets_add(self.box_status, 0,False)

        self.status_label = wx.StaticText(self.box_status, id=wx.ID_ANY, label="STATUS", style=wx.ALIGN_CENTER_HORIZONTAL) #style=wx.ALIGN_CENTER_HORIZONTAL centralizar o texto na box

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.status_label.SetFont(font)

        self.box_status.widgets_add(self.status_label, 0, False)

        self.main_sizer.Add(self.box_steel_type,proportion =  0, flag = wx.ALL | wx.EXPAND, border = 5) #adiciona o primeiro staticbox ao sizer principal da janela
        self.main_sizer.Add(self.box_perfil, proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5) # adiciona o escolha do perfil
        self.main_sizer.Add(self.box_values_input, proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5) #adiciona o insercao de valores


        self.window_main_panel.SetSizer(self.main_sizer)
