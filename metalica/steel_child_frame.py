import os

import wx
import wx.adv
import re
from pint import UnitRegistry
from metalica.edit_child_frame import EditChildFrame
from widget_class import StaticBox , TextBoxVrf, SaveBox, StaticTextTune
from table_manipulation import ReadExcelFile
from metalica.matplot_img_draw import DrawBeam
from metalica.help_steel_child_frame import ImgHelpButton
from metalica.cb_child_frame import CBValuesConfiguration
from metalica.aef_child_frame import AefValuesConfiguration
from metalica.verification_process import VerificationProcess
from metalica.child_frame_list import PerfilList
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


#() tupla [] lista {} dicionario
#criando o frame filho
class SteelChildFrame(wx.MDIChildFrame):

    def __init__(self, parent, frame_name):
        #parametros iniciais da janela
        super().__init__(parent, id=wx.ID_ANY, title = frame_name,
                         pos=(0,0), size = (800,775), style = wx.DEFAULT_FRAME_STYLE)
        self.perfil_list = []
        self.parent = self.GetParent() #atributo parente da janela
        self.SetIcon(icon = wx.Icon("icones/if.png", wx.BITMAP_TYPE_PNG))  # Definindo o ícone para o MDIFrame

        # self.SetIcon(wx.Icon("icones/perfil.bmp"))
        #------------------------------------------------funcoes dos botoes
        self.data_steel_type = ReadExcelFile("steel.xlsx","tipo_de_aco")

        self.cb = 1
        self.aef = -1

        # **************************************************************************************** SUM sistema de unidade de medida
        #trabalhando em m, KN, Pa para realizar o calculo final!
        #evento de atualizacao das unidades de medidas dispostas na cfg
        self.factor_multiplier_lenght = { "mm", "cm", "m"}
        self.factor_multiplier_area = {"mm^2" , "cm^2", "m^2"}
        self.factor_multiplier_volume = {"mm^3", "cm^3", "m^3"}
        self.factor_multiplier_inertia = {"mm^4", "cm^4", "m^4"}
        self.factor_multiplier_six_elevated = {"mm^6", "cm^6", "m^6"}
        self.factor_multiplier_force = {"N", "kN", "MN"}
        self.factor_multiplier_moment = {"N*m", "KN*m", "MN*m"}
        self.factor_multiplier_press = {"N/m^2", "kN/m^2", "MN/m^2", "GN/m^2"}


        # self.Bind(wx.EVT_CLOSE, self.on_close_steel_child)

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

        ureg = UnitRegistry()

        def unit_converter_dois(value: float, from_unit: str, to_unit: str) -> float:
            try:
                quantidade = value * ureg(from_unit)
                return quantidade.to(to_unit).magnitude
            #                return quantidade.to(to_unit).magnitude
            except Exception as e:
                raise ValueError(f"Erro na conversão de {from_unit} para {to_unit}: {e}")


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
          try:
              # #quando o evento esta ativo
              self.label_name = self.label_fu.GetLabel()
              if event.GetActive():
                  self.label_fu.SetLabel(f"fu ({self.parent.get_unit_press()[0]}) :")
                  self.label_fy.SetLabel(f"fy ({self.parent.get_unit_press()[0]}) :")
                  if self.label_fu.GetLabel() != self.label_name:
                      self.text_fu.SetValue("")
                      self.text_fy.SetValue("")
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
          except RuntimeError:
              pass
        self.Bind(wx.EVT_ACTIVATE, on_activate_window)
        # ****************************************************************************************************************


        def load_values_fy_fu(event):
            selected_item = self.select_steel_type_menu.GetValue()
            fy_fu = self.data_steel_type.get_name_and_return_col_value("Tipo",f"{selected_item}",["fy", "fu"])
            fy, fu = float(fy_fu["fy"]), float(fy_fu["fu"]) #mudar aqui

            fy = fy * ureg.MPa
            fy_convertido = fy.to(parent.get_unit_press()[0]).magnitude
            fu = fu * ureg.MPa
            fu_convertido = fu.to(parent.get_unit_press()[0]).magnitude

            self.text_fy.SetValue(str(fy_convertido))
            self.text_fu.SetValue(str(fu_convertido))
        def load_edit_child_frame(event):
            edit_child = EditChildFrame(self.parent,"Editor")
            edit_child.Show()
            # lista de valores ja tirados do excel e ja definidos nos rotulos
        def on_select_tipo(event):
            if self.select_type.GetValue() == "Soldado":
                self.data_steel_lmn = ReadExcelFile("steel.xlsx", "soldado")
            elif self.select_type.GetValue() == "Laminado":

                self.data_steel_lmn = ReadExcelFile("steel.xlsx", "laminado")
            perfil_type = self.data_steel_lmn.return_value_by_one_col("BITOLA mm x kg/mgraus")
            self.select_steel_perfil.Clear()
            self.select_steel_perfil.AppendItems(perfil_type)

        def on_select_perfil(event):
            text_values = label_and_object.keys()
            option_selected = self.select_steel_perfil.GetStringSelection()
            return_values_dimension = self.data_steel_lmn.get_name_and_return_col_value("BITOLA mm x kg/mgraus",f"{option_selected}",text_values)
            for name_col, value  in return_values_dimension.items():
                value = round(value,2)
                label = str(name_col) + " " + str(value)
                if name_col in label_and_object.keys():
                    label = label_and_object[name_col]
                    novo_texto = f"{label.GetLabel().split(":")[0]}: {value}"
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
        def on_cb(event):
            cb = CBValuesConfiguration(self,f"Fator de modificação para diagrama de momento fletor não uniforme Cb - {frame_name}")
            cb.Show()
        def on_aef(event):
            aef = AefValuesConfiguration(parent,self,f"Área líquida efetiva Aef - {frame_name}")#
            aef.Show()

        def get_info(option_selected, aef):
            try:
                fy = float(self.text_fy.get_value())
                fu = float(self.text_fu.get_value())

                e = unit_converter_dois(float(parent.get_e_modulo()), "N/m^2",
                                                parent.get_unit_press()[0])

                g = unit_converter_dois(float(parent.get_g_modulo()), "N/m^2",
                                                parent.get_unit_press()[0])

                y_um = float(parent.get_y_um())
                cb = float(self.get_cb()) #adm
                lfx_value = unit_converter_dois(self.input_lfx.get_value(), parent.get_unit_lenght()[0],
                                                parent.get_unit_lenght()[0])
                lfy_value = unit_converter_dois(self.input_lfy.get_value(), parent.get_unit_lenght()[0],
                                                parent.get_unit_lenght()[0])
                lfz_value = unit_converter_dois(self.input_lfz.get_value(), parent.get_unit_lenght()[0],
                                                parent.get_unit_lenght()[0])
                lb_value = unit_converter_dois(self.input_lfb.get_value(), parent.get_unit_lenght()[0],
                                               parent.get_unit_lenght()[0])
                fnt_value = unit_converter_dois(self.input_fnt.get_value(), parent.get_unit_force()[0],
                                                parent.get_unit_force()[0])
                fnc_value = unit_converter_dois(self.input_fnc.get_value(), parent.get_unit_force()[0],
                                                parent.get_unit_force()[0])
                fcx_value = unit_converter_dois(self.input_fcx.get_value(), parent.get_unit_force()[0],
                                                parent.get_unit_force()[0])
                fcy_value = unit_converter_dois(self.input_fcy.get_value(), parent.get_unit_force()[0],
                                                parent.get_unit_force()[0])
                mfx_value = unit_converter_dois(self.input_mx.get_value(), parent.get_unit_moment()[0],
                                                parent.get_unit_moment()[0])
                mfy_value = unit_converter_dois(self.input_my.get_value(), parent.get_unit_moment()[0],
                                                parent.get_unit_moment()[0])
                # pegando dados do perfil
                text_values = label_and_object.keys()
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
                        value_converted = unit_converter_dois(value_list_perfil[i], search_unit,
                                                              parent.get_unit_lenght()[0])  # ok
                    elif search_unit in self.factor_multiplier_area:
                        value_converted = unit_converter_dois(value_list_perfil[i], search_unit, parent.get_unit_area()[0])
                    elif search_unit in self.factor_multiplier_volume:
                        value_converted = unit_converter_dois(value_list_perfil[i], search_unit,
                                                              parent.get_unit_volume()[0])
                    elif search_unit in self.factor_multiplier_inertia:
                        value_converted = unit_converter_dois(value_list_perfil[i], search_unit,
                                                              parent.get_unit_inercia()[0])
                    elif search_unit in self.factor_multiplier_six_elevated:
                        value_converted = unit_converter_dois(value_list_perfil[i], search_unit, parent.get_unit_six()[0])
                    else:
                        value_converted = value_list_perfil[i]
                    value_converted = float(value_converted)
                    transformed_list_perfil_data.extend([value_converted])
                    i += 1
                    # print(f"Unidade : {unit} , valor: {value_adress} , para  {value_converted}")

                # print(transformed_list_perfil_data)
                values_to_append = [aef, fy, fu, lfx_value, lfy_value, lfz_value, lb_value, fnt_value,
                                    fnc_value, fcx_value, fcy_value, mfx_value, mfy_value,
                                    y_um, g, e, cb]
                transformed_list_perfil_data.extend(values_to_append)
                # print(transformed_list_perfil_data)
                return transformed_list_perfil_data
            except Exception as e:
                wx.MessageBox(f"Erro : {e}", "Erro", wx.OK | wx.ICON_ERROR)

        def return_aef():
            if self.get_aef() > 0:
                aef = float(self.get_aef())
                return aef
            else:
                aef = -1
                wx.MessageBox(f"A área utilizada no calculo será considerada igual a área bruta", "Alerta",
                              wx.OK | wx.ICON_EXCLAMATION)
                return aef

        # ureg = UnitRegistry()

        def on_calculate(event):
            try:
                aef = return_aef()
                option_selected = self.select_steel_perfil.GetStringSelection()
                a = get_info(option_selected, aef)
                transformed_list_perfil_data = ((a[0]),((a[1]) * ureg(parent.get_unit_lenght()[0])) , (a[2]) * ureg(parent.get_unit_lenght()[0]), (a[3]) * ureg(parent.get_unit_lenght()[0]), (a[4]) * ureg(parent.get_unit_lenght()[0]),
                                                (a[5]) * ureg(parent.get_unit_lenght()[0]), (a[6]) * ureg(parent.get_unit_lenght()[0]), (a[7]) * ureg(parent.get_unit_area()[0]), (a[8]) * ureg(parent.get_unit_inercia()[0]),
                                                (a[9]) * ureg(parent.get_unit_volume()[0]), (a[10]) * ureg(parent.get_unit_lenght()[0]) , (a[11]) * ureg(parent.get_unit_volume()[0]), (a[12]) * ureg(parent.get_unit_inercia()[0]),
                                                (a[13]) * ureg(parent.get_unit_volume()[0]), (a[14]) * ureg(parent.get_unit_lenght()[0]), (a[15]) * ureg(parent.get_unit_volume()[0]), (a[16]) * ureg(parent.get_unit_lenght()[0]),
                                                (a[17]) * ureg(parent.get_unit_inercia()[0]), (a[18]), (a[19]) , (a[20]) * ureg(parent.get_unit_six()[0]), (a[21]), (a[22]), (a[23]) * ureg(parent.get_unit_press()[0]), (a[24]) * ureg(parent.get_unit_press()[0]),
                                                (a[25]) * ureg(parent.get_unit_lenght()[0]) , (a[26]) * ureg(parent.get_unit_lenght()[0]), (a[27]) * ureg(parent.get_unit_lenght()[0]), (a[28]) * ureg(parent.get_unit_lenght()[0]),
                                                (a[29]) * ureg(parent.get_unit_force()[0]), (a[30]) * ureg(parent.get_unit_force()[0]), (a[31]) * ureg(parent.get_unit_force()[0]), (a[32]) * ureg(parent.get_unit_force()[0]),
                                                (a[33]) * ureg(parent.get_unit_moment()[0]), (a[34]) * ureg(parent.get_unit_moment()[0]), (a[35]), (a[36]) * ureg(parent.get_unit_press()[0]),
                                                (a[37]) * ureg(parent.get_unit_press()[0]) , (a[38])
                )
                print(transformed_list_perfil_data)
                self.save_dialog = SaveBox(self.parent) #abrir o dialogo de salvar
                path = self.save_dialog.get_path()
                self.save_dialog.Destroy()
                print(f"{path}")
                print(self.select_type.GetValue())
                self.data = VerificationProcess(parent, *transformed_list_perfil_data, option_selected,self.select_type.GetValue(),frame_name, path)


                resultado = self.data.calculate()
                if resultado:
                    self.status_label.SetLabel("APROVADO!")
                    self.status_label.SetForegroundColour(wx.Colour(20, 200, 20))
                    # self.status_label.set_valueand_color("APROVADO!", 20, 200, 20)#Alinhamento de centro nao esta funcionando !
                else:
                    self.status_label.SetLabel("REPROVADO!")
                    self.status_label.SetForegroundColour(wx.Colour(200, 20, 20))
                    # self.status_label.set_valueand_color("REPROVADO!",200, 20, 20)
                self.box_status.Update()
                self.box_status.Layout()
                
                if parent.get_open_file():
                    caminho_arquivo = f"{path}.pdf"
                    os.startfile(caminho_arquivo)

            except Exception as e:
                wx.MessageBox(f"Erro : {e}", "Erro", wx.OK | wx.ICON_ERROR)


        def on_calculate_all(event):
            # try:
                self.clear_perfil_list()
                steel_perfil_list = self.data_steel_lmn.return_value_by_one_col("BITOLA mm x kg/mgraus")

                print(steel_perfil_list)
                aef = return_aef()

                for perfil in steel_perfil_list:
                    a = get_info(perfil, aef)
                    print(f"////////////////////////////////////////// {perfil}")
                    print(type((a[0])))

                    transformed_list_perfil_data = ((a[0]), ((a[1]) * ureg(parent.get_unit_lenght()[0])),
                                                    (a[2]) * ureg(parent.get_unit_lenght()[0]),
                                                    (a[3]) * ureg(parent.get_unit_lenght()[0]),
                                                    (a[4]) * ureg(parent.get_unit_lenght()[0]),
                                                    (a[5]) * ureg(parent.get_unit_lenght()[0]),
                                                    (a[6]) * ureg(parent.get_unit_lenght()[0]),
                                                    (a[7]) * ureg(parent.get_unit_area()[0]),
                                                    (a[8]) * ureg(parent.get_unit_inercia()[0]),
                                                    (a[9]) * ureg(parent.get_unit_volume()[0]),
                                                    (a[10]) * ureg(parent.get_unit_lenght()[0]),
                                                    (a[11]) * ureg(parent.get_unit_volume()[0]),
                                                    (a[12]) * ureg(parent.get_unit_inercia()[0]),
                                                    (a[13]) * ureg(parent.get_unit_volume()[0]),
                                                    (a[14]) * ureg(parent.get_unit_lenght()[0]),
                                                    (a[15]) * ureg(parent.get_unit_volume()[0]),
                                                    (a[16]) * ureg(parent.get_unit_lenght()[0]),
                                                    (a[17]) * ureg(parent.get_unit_inercia()[0]), (a[18]), (a[19]),
                                                    (a[20]) * ureg(parent.get_unit_six()[0]), (a[21]), (a[22]),
                                                    (a[23]) * ureg(parent.get_unit_press()[0]),
                                                    (a[24]) * ureg(parent.get_unit_press()[0]),
                                                    (a[25]) * ureg(parent.get_unit_lenght()[0]),
                                                    (a[26]) * ureg(parent.get_unit_lenght()[0]),
                                                    (a[27]) * ureg(parent.get_unit_lenght()[0]),
                                                    (a[28]) * ureg(parent.get_unit_lenght()[0]),
                                                    (a[29]) * ureg(parent.get_unit_force()[0]),
                                                    (a[30]) * ureg(parent.get_unit_force()[0]),
                                                    (a[31]) * ureg(parent.get_unit_force()[0]),
                                                    (a[32]) * ureg(parent.get_unit_force()[0]),
                                                    (a[33]) * ureg(parent.get_unit_moment()[0]),
                                                    (a[34]) * ureg(parent.get_unit_moment()[0]), (a[35]),
                                                    (a[36]) * ureg(parent.get_unit_press()[0]),
                                                    (a[37]) * ureg(parent.get_unit_press()[0]), (a[38])
                                                    )
                    if self.select_type.GetValue() == "Soldado":
                        self.data = VerificationProcess(parent, *transformed_list_perfil_data, "","Soldado", frame_name, frame_name)
                    elif self.select_type.GetValue() == "Laminado":
                        self.data = VerificationProcess(parent, *transformed_list_perfil_data,"", "Laminado", frame_name, frame_name)

                    self.data.calculate_all()

                    resultado = [perfil, self.data.calculate_all()]
                    self.append_perfil_list(resultado)
                    print(transformed_list_perfil_data)

                lista_aprovados_reprovados = PerfilList(parent, self, f"Lista de perfis - {frame_name}")
                lista_aprovados_reprovados.Show()
            # except Exception as e:
            #     wx.MessageBox(f"Erro : {e}", "Erro", wx.OK | wx.ICON_ERROR)


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
        self.label_fy = wx.StaticText(self.box_steel_selection_select_menu,id=wx.ID_ANY, label="fy (MN/m^2)")
        self.box_steel_selection_select_menu.widgets_add(self.label_fy, 0, False)
        self.text_fy = TextBoxVrf(self.box_steel_selection_select_menu, value = "0", only_numeric=True)
        self.box_steel_selection_select_menu.widgets_add(self.text_fy, 0, False)
        #quebra de linha vertical
        self.box_steel_selection_select_menu.widgets_add(wx.StaticLine(self.box_steel_selection_select_menu, style=wx.LI_VERTICAL), 0,False)
        self.label_fu = wx.StaticText(self.box_steel_selection_select_menu,id=wx.ID_ANY, label="fu (MN/m^2)")
        self.box_steel_selection_select_menu.widgets_add(self.label_fu, 0, False)
        self.text_fu = TextBoxVrf(self.box_steel_selection_select_menu, value = "0", only_numeric=True)
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
        tipo = ["Soldado", "Laminado"]
        self.select_type = wx.ComboBox(self.box_perfil_selection, id = wx.ID_ANY, style = wx.CB_READONLY,choices = tipo) #VERIFICAR pq ele fica grande mesmo nao expandindo
        self.select_type.Bind(wx.EVT_COMBOBOX, on_select_tipo)
        # self.select_type.SetMaxSize(wx.Size(-1, 20))
        self.box_perfil_selection.widgets_add(self.select_type, 0, "False")
        self.select_steel_perfil = wx.ComboBox(self.box_perfil_selection, id = wx.ID_ANY, style = wx.CB_READONLY, choices=[]) #VERIFICAR pq ele fica grande mesmo nao expandindo
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
        self.area_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Área (cm^2) : ")
        self.box_perfil_data.widgets_add(self.area_text, 0, False)
        self.i_x_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Ix (cm^4) : ")
        self.box_perfil_data.widgets_add(self.i_x_text, 0, False)
        self.w_x_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Wx (cm^3) : ")
        self.box_perfil_data.widgets_add(self.w_x_text, 0, False)
        self.r_x_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="rx (cm) : ")
        self.box_perfil_data.widgets_add(self.r_x_text, 0, False)
        self.z_x_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="zx (cm^3) : ")
        self.box_perfil_data.widgets_add(self.z_x_text, 0, False)
        self.i_y_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Iy (cm^4) : ")
        self.box_perfil_data.widgets_add(self.i_y_text, 0, False)
        self.w_y_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="Wy (cm^3) : ")
        self.box_perfil_data.widgets_add(self.w_y_text , 0, False)
        self.r_y_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="ry (cm) : ")
        self.box_perfil_data.widgets_add(self.r_y_text , 0, False)
        self.z_y_text = wx.StaticText(self.box_perfil_data, id=wx.ID_ANY, label="zy (cm^3) : ")
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
        self.box_lengths = StaticBox(self.box_values_input, "Informações do elemento", orientation= "grid")
        self.box_values_input.widgets_add(self.box_lengths,0, False)
        self.text_lfx = wx.StaticText(self.box_lengths,id = wx.ID_ANY, label = "Lx (m) :")
        self.text_lfx.SetToolTip("(Lx) comprimento destravado do elemento paralelo ao eixo X")
        self.box_lengths.widgets_add(self.text_lfx, 0, False)
        self.input_lfx = TextBoxVrf(self.box_lengths, value = "1", only_numeric=True)
        self.box_lengths.widgets_add(self.input_lfx, 1,False)
        self.text_lfy = wx.StaticText(self.box_lengths,id = wx.ID_ANY, label = "Ly (m) :")
        self.text_lfy.SetToolTip("(Ly) comprimento destravado do elemento paralelo ao eixo Y")
        self.box_lengths.widgets_add(self.text_lfy, 0, False)
        self.input_lfy = TextBoxVrf(self.box_lengths, value = "1", only_numeric=True)
        self.box_lengths.widgets_add(self.input_lfy, 1,False)
        self.text_lz = wx.StaticText(self.box_lengths,id = wx.ID_ANY, label = "Lz (m) :")
        self.text_lz.SetToolTip("(Lz) comprimento destravado do elemento associado a sua torção")
        self.box_lengths.widgets_add(self.text_lz, 0, False)
        self.input_lfz = TextBoxVrf(self.box_lengths,  value = "1", only_numeric=True)
        self.box_lengths.widgets_add(self.input_lfz, 1,False)
        self.text_lf = wx.StaticText(self.box_lengths,id = wx.ID_ANY, label = "Lf (m) :")
        self.text_lf.SetToolTip("(Lf) ou (Lb) Distância entre as contenções de flambagem lateral com torção")
        self.box_lengths.widgets_add(self.text_lf, 0, False)
        self.input_lfb = TextBoxVrf(self.box_lengths,  value = "1", only_numeric=True)
        self.box_lengths.widgets_add(self.input_lfb, 1,False)
        self.text_values_cfg_cb = wx.StaticText(self.box_lengths,id = wx.ID_ANY, label = "Coeficiente :")
        self.box_lengths.widgets_add(self.text_values_cfg_cb, 0, False)
        self.button_cb = wx.Button(self.box_lengths, label = "Cb")
        self.box_lengths.widgets_add(self.button_cb, 1,  False)
        self.button_cb.Bind(wx.EVT_BUTTON, on_cb)
        self.text_values_cfg_aef = wx.StaticText(self.box_lengths,id = wx.ID_ANY, label = "Área efetiva :")
        self.box_lengths.widgets_add(self.text_values_cfg_aef, 0, False)
        self.button_aef = wx.Button(self.box_lengths, label = "Aef")
        self.box_lengths.widgets_add(self.button_aef, 1,  False)
        self.button_aef.Bind(wx.EVT_BUTTON, on_aef)
        #teste
        # self.awdawd = wx.StaticText(self.box_lengths,id = wx.ID_ANY, label = "Área efetiva :")
        # self.box_lengths.widgets_add(self.awdawd, 0, False)
        # self.button_teste = wx.Button(self.box_lengths, label = "Aef")
        # self.box_lengths.widgets_add(self.button_teste, 1,  False)
        # self.button_teste.Bind(wx.EVT_BUTTON, on_teste)
        #valores dos esforcos
        self.box_load_solicitation = StaticBox(self.box_values_input, "Solicitações", orientation= "grid")
        self.box_values_input.widgets_add(self.box_load_solicitation, 0, False)
        self.text_fnt = wx.StaticText(self.box_load_solicitation, id=wx.ID_ANY, label="Normal tração (KN) :")
        self.text_fnt.SetToolTip("Valor de cálculo referente a força de tração que o elemento está submetido")
        self.box_load_solicitation.widgets_add(self.text_fnt, 0, False)
        self.input_fnt = TextBoxVrf(self.box_load_solicitation, value = "1", only_numeric=True)
        self.box_load_solicitation.widgets_add(self.input_fnt, 1, False)
        self.text_fnc = wx.StaticText(self.box_load_solicitation, id=wx.ID_ANY, label="Normal compressão (KN) :")
        self.text_fnc.SetToolTip("Valor de cálculo referente a força de compressão que o elemento está submetido (o valor será calculado em módulo!)")
        self.box_load_solicitation.widgets_add(self.text_fnc, 0, False)
        self.input_fnc = TextBoxVrf(self.box_load_solicitation, value = "1", only_numeric=True)
        self.box_load_solicitation.widgets_add(self.input_fnc, 1, False)
        self.text_fcx = wx.StaticText(self.box_load_solicitation, id=wx.ID_ANY, label="Cortante X (KN) :")
        self.text_fcx.SetToolTip("Valor de cálculo referente a força cortante perpendicular ao eixo X do elemento")
        self.box_load_solicitation.widgets_add(self.text_fcx, 0, False)
        self.input_fcx = TextBoxVrf(self.box_load_solicitation, value = "1", only_numeric=True)
        self.box_load_solicitation.widgets_add(self.input_fcx, 1, False)
        self.text_fcy = wx.StaticText(self.box_load_solicitation, id=wx.ID_ANY, label="Cortante Y (KN) :")
        self.text_fcy.SetToolTip("Valor de cálculo referente a força cortante perpendicular ao eixo Y do elemento")
        self.box_load_solicitation.widgets_add(self.text_fcy, 0,  False)
        self.input_fcy = TextBoxVrf(self.box_load_solicitation, value = "1",only_numeric=True)
        self.box_load_solicitation.widgets_add(self.input_fcy, 1, False)
        self.text_mx = wx.StaticText(self.box_load_solicitation, id=wx.ID_ANY, label="Momento X (Kn*m) :")
        self.text_fcy.SetToolTip("Valor de cálculo referente a momento fletor em relação ao eixo X do elemento")
        self.box_load_solicitation.widgets_add(self.text_mx, 0, False)
        self.input_mx = TextBoxVrf(self.box_load_solicitation, value = "1",only_numeric=True)
        self.box_load_solicitation.widgets_add(self.input_mx, 1, False)
        self.text_my = wx.StaticText(self.box_load_solicitation, id=wx.ID_ANY, label="Momento Y (Kn*m) :")
        self.text_fcy.SetToolTip("Valor de cálculo referente a momento fletor em relação ao eixo Y do elemento")
        self.box_load_solicitation.widgets_add(self.text_my, 0, False)
        self.input_my = TextBoxVrf(self.box_load_solicitation, value = "1",only_numeric=True)
        self.box_load_solicitation.widgets_add(self.input_my, 1, False)
        #------------------------------------------------- #dicionario de variaveis
        label_and_object = {"Massa Linear kg/m": self.linear_mass_text, "d (mm) : ": self.d_text,
                            "bf (mm) : ": self.bf_text, "tw (mm) : ": self.tw_text, "tf (mm) : ": self.tf_text,
                            "h (mm) : ": self.h_text, "d' (mm) : ": self.d_l_text, "Área (cm^2) : ": self.area_text,
                            "Ix (cm^4) : ": self.i_x_text, "Wx (cm^3) : ": self.w_x_text,
                            "rx (cm) : ": self.r_x_text, "zx (cm^3) : ": self.z_x_text, "Iy (cm^4) : ": self.i_y_text,
                            "Wy (cm^3) : ": self.w_y_text, "ry (cm) : ": self.r_y_text,
                            "zy (cm^3) : ": self.z_y_text, "rt (cm) : ": self.r_t_text,
                            "It (cm^4) : ": self.i_t_text, "Mesa bf/2.tf : ": self.bf_two_text,
                            "Alma d'/tw : ": self.d_tw_text, "Cw (cm^6) : ": self.cw_text,
                            "u (m²/m) : ": self.u_text}

        #------------------------------------------------- box resultados - verificar como vai ser gerado o relatorio
        self.box_results = StaticBox(self.box_values_input, "Resultados", orientation= "vertical")
        self.box_values_input.widgets_add(self.box_results, 0, True)
        self.calculate =  wx.Button(self.box_results, label = "Calcular")
        self.calculate.SetToolTip("Calcular para o elemento selecionado")

        self.box_results.widgets_add(self.calculate, 0, False)
        self.calculate.Bind(wx.EVT_BUTTON, on_calculate)
        self.box_status = StaticBox(self.box_results, "Situação:", orientation = "vertical")
        self.box_results.widgets_add(self.box_status, 0,False)

        self.box_todos = StaticBox(self.box_results, "Todos os perfis", orientation="vertical")
        self.box_results.widgets_add(self.box_todos, 0, True)
        self.calculate_all = wx.Button(self.box_todos, label="Calcular")
        self.calculate_all.SetToolTip("Calcular para todos os elementos")
        self.box_todos.widgets_add(self.calculate_all, 0, False)
        self.calculate_all.Bind(wx.EVT_BUTTON, on_calculate_all)



        # self.status_label = StaticTextTune(self.box_status, "STATUS",wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL, 0,0,0, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.status_label = wx.StaticText(self.box_status, id=wx.ID_ANY, label="STATUS", style=wx.ALIGN_CENTER_HORIZONTAL) #style=wx.ALIGN_CENTER_HORIZONTAL centralizar o texto na box
        self.status_label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.box_status.widgets_add(self.status_label, 0, False)

        self.main_sizer.Add(self.box_steel_type,proportion =  0, flag = wx.ALL | wx.EXPAND, border = 5) #adiciona o primeiro staticbox ao sizer principal da janela
        self.main_sizer.Add(self.box_perfil, proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5) # adiciona o escolha do perfil
        self.main_sizer.Add(self.box_values_input, proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5) #adiciona o insercao de valores
        self.window_main_panel.SetSizer(self.main_sizer)

    def set_cb(self, unit):
        self.cb = unit

    def get_cb(self):
        return self.cb

    def set_aef(self, unit):
        self.aef = unit

    def get_aef(self):
        return self.aef

    def append_perfil_list(self, perfis):
        self.perfil_list.append(perfis)

    def clear_perfil_list(self):
        self.perfil_list.clear()

    def get_perfil_list(self):
        return self.perfil_list

