import wx
import os
from widget_class import StaticBox
from widget_class import TextBoxVrf


class AefValuesConfiguration(wx.MDIChildFrame):
    def __init__(self, parent, frame_name ):
        super().__init__(parent=parent.GetParent(), id=wx.ID_ANY, title=frame_name,
                         pos=wx.DefaultPosition, size=(350, 300))
        self.parent = parent
        self.window_main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        def on_calculate(event):
           try:
                ct = float(self.ct_input.get_value())
                an = float(self.an_input.get_value())
                aef= ct*an
                self.aef_input.set_value(str(round(aef, 4)))

           except Exception as e:
               wx.MessageBox(f"{e}", "Erro", wx.OK )

        def on_aplicar(event):
            try:
                self.cb_value.set_value(str(self.aef_input.get_value()))
            except Exception as e:
                wx.MessageBox(f"{e}", "Erro", wx.OK)

        def on_visibilidade(event):
            try:
                verificar_check_box = self.checkbox_aef_ab.IsChecked()
                if verificar_check_box:
                    self.aef_calc_box.Show(False)
                else:
                    self.aef_calc_box.Show(True)
                self.window_main_panel.Layout()
                self.window_main_panel.Refresh()
            except RuntimeError:
                pass

        self.box_main = StaticBox(self.window_main_panel, "Aef",orientation = "vertical")

        self.utilizar_ab = StaticBox(self.box_main, "", orientation="vertical")
        self.box_main.widgets_add(self.utilizar_ab, 0, "False")

        self.checkbox_aef_ab = wx.CheckBox(self.utilizar_ab, label="Utilizar a área efetiva (Aef) igual a área bruta (Ag)")
        self.checkbox_aef_ab.SetValue(True)
        self.utilizar_ab.widgets_add(self.checkbox_aef_ab, 0, "False")
        #bindando o envento para quando estiver checkada nao editar
        self.Bind(wx.EVT_CHECKBOX, on_visibilidade)
        self.Bind(wx.EVT_ACTIVATE, on_visibilidade)

        self.aef_calc_box = StaticBox(self.box_main, "Calculo da área",orientation = "grid")
        self.box_main.widgets_add(self.aef_calc_box,0,"False")


        self.ct_text = wx.StaticText(self.aef_calc_box, id=wx.ID_ANY, label="Coeficiente (Ct): ")
        self.ct_text.SetToolTip("(Ct) é um coeficiente de redução da área líquida. Ex: podendo (Ct = 1) para força de tração "
                                "transmitida diretamente para cada elemento da seção "
                                "transversal da barra, (Ct = Ac/Ag), quando a tração for "
                                "transmitida somente por soldas transversais (Ac)-seção transversal do "
                                "elemento conectado (Ag)- área bruta da seção, para demais valores de (Ct), a norma deve ser consultada!")
        self.aef_calc_box.widgets_add(self.ct_text, 0, False)
        self.ct_input = TextBoxVrf(self.aef_calc_box, value = "", only_numeric=True)
        self.aef_calc_box.widgets_add(self.ct_input, 0, False)

        self.an_text = wx.StaticText(self.aef_calc_box, id=wx.ID_ANY, label="Área líquida da barra  (An): ")
        self.an_text.SetToolTip("(An) é a área líquida da barra, podendo ser igual a área bruta, ou em regiões com furos,"
                                " feitos para ligação ou outras finalidades deve ser calculada a parte")
        self.aef_calc_box.widgets_add(self.an_text, 0, False)
        self.an_input = TextBoxVrf(self.aef_calc_box, value = "", only_numeric=True)
        self.aef_calc_box.widgets_add(self.an_input, 0, False)

        self.aef_text = wx.StaticText(self.aef_calc_box, id=wx.ID_ANY, label="Área efetiva (Aef): ")
        self.aef_calc_box.widgets_add(self.aef_text, 0, False)
        self.aef_input = TextBoxVrf(self.aef_calc_box, value = "", only_numeric=True)
        self.aef_calc_box.widgets_add(self.aef_input, 0, False)

        self.aef_text = wx.StaticText(self.aef_calc_box, id=wx.ID_ANY, label="Valores: ")
        self.aef_calc_box.widgets_add(self.aef_text, 0, False)

        self.btn_calc = wx.Button(self.aef_calc_box, label="Calcular")
        self.aef_calc_box.widgets_add(self.btn_calc, 1, False)
        self.btn_calc.Bind(wx.EVT_BUTTON, on_calculate)

        self.btn_apl = wx.Button(self.box_main, label="Aplicar")
        self.box_main.widgets_add(self.btn_apl, 1, False)
        self.btn_apl.Bind(wx.EVT_BUTTON, on_aplicar)


        #
        # self.img = wx.StaticBitmap(self.box_img,bitmap = wx.Bitmap(os.path.join(os.getcwd(), "icones", "desenho_viga.bmp")))
        # self.box_img.widgets_add(self.img, 0, True)
        # self.box_input_values = StaticBox(self.window_main_panel, "", orientation = "vertical")
        # self.box_values_cfg = StaticBox(self.box_input_values, "", orientation = "grid")
        # self.box_input_values.widgets_add(self.box_values_cfg, 0, False)
        # self.momento_max_text = wx.StaticText(self.box_values_cfg, id=wx.ID_ANY, label="Valor do momento máximo: ")
        # self.box_values_cfg.widgets_add(self.momento_max_text, 0, False)
        # self.momento_max_input = TextBoxVrf(self.box_values_cfg, value = "", only_numeric=True)
        # self.box_values_cfg.widgets_add(self.momento_max_input, 0, False)
        # self.momento_ma_text = wx.StaticText(self.box_values_cfg, id=wx.ID_ANY, label="Valor do momento A: ")
        # self.momento_ma_text.SetToolTip("Valor do momento fletor em módulo situado a 1/4 do comprimento destravado (Lb)")
        # self.box_values_cfg.widgets_add(self.momento_ma_text, 0, False)
        # self.momento_ma_input = TextBoxVrf(self.box_values_cfg, value = "", only_numeric=True)
        # self.box_values_cfg.widgets_add(self.momento_ma_input, 0, False)
        # self.momento_mb_text = wx.StaticText(self.box_values_cfg, id=wx.ID_ANY, label="Valor do momento B: ")
        # self.momento_mb_text.SetToolTip("Valor do momento fletor em módulo situado a 1/2 do comprimento destravado (Lb)")
        # self.box_values_cfg.widgets_add(self.momento_mb_text, 0, False)
        # self.momento_mb_input = TextBoxVrf(self.box_values_cfg, value = "", only_numeric=True)
        # self.box_values_cfg.widgets_add(self.momento_mb_input, 0, False)
        # self.momento_mc_text = wx.StaticText(self.box_values_cfg, id=wx.ID_ANY, label="Valor do momento C: ")
        # self.momento_mc_text.SetToolTip("Valor do momento fletor em módulo situado a 3/4 do comprimento destravado (Lb)")
        # self.box_values_cfg.widgets_add(self.momento_mc_text, 0, False)
        # self.momento_mc_input = TextBoxVrf(self.box_values_cfg, value = "", only_numeric=True)
        # self.box_values_cfg.widgets_add(self.momento_mc_input, 0, False)
        # self.momento_rm_text = wx.StaticText(self.box_values_cfg, id=wx.ID_ANY, label="Rm : ")
        # self.momento_rm_text.SetToolTip("Parâmetro de monosimetria da seção transversal (1 para duplamente simétricas, "
        #                                 "demais variações é necessário consultar a norma!)")
        # self.box_values_cfg.widgets_add(self.momento_rm_text, 0, False)
        # self.momento_rm_input = TextBoxVrf(self.box_values_cfg, value = "1", only_numeric=True)
        # self.box_values_cfg.widgets_add(self.momento_rm_input, 0, False)
        # #calcular
        # self.box_calculate = StaticBox(self.box_input_values, "", orientation = "vertical")
        # self.box_input_values.widgets_add(self.box_calculate, 0, False)
        #
        # self.box_input_cb = StaticBox(self.box_input_values, "", orientation = "grid")
        # self.cb_text = wx.StaticText(self.box_input_cb, id=wx.ID_ANY, label="Valor calculado do Cb :  ")
        # self.box_input_cb.widgets_add(self.cb_text, 0, False)
        # self.cb_value = TextBoxVrf(self.box_input_cb, value="1", only_numeric=True)
        # self.box_input_cb.widgets_add(self.cb_value, 0, False)
        # self.box_input_values.widgets_add(self.box_input_cb, 0, False)
        #
        # self.btn_calc = wx.Button(self.box_calculate, label="Calcular")
        # self.box_calculate.widgets_add(self.btn_calc, 1, True)
        # self.btn_calc.Bind(wx.EVT_BUTTON, on_calculate_cb)
        #
        # self.btn_aplicar = wx.Button(self.box_calculate, label="Aplicar")
        # self.box_calculate.widgets_add(self.btn_aplicar, 1, True)
        # self.btn_aplicar.Bind(wx.EVT_BUTTON, on_aplicar)
        #
        # info_text = "Para a verificação da flambagem local com torção, pode ser necessário utilizar o coeficiente (Cb)" \
        #             "que é um fator de correção aplicado em casos de diagrama de momento fletor não uniforme ao longo " \
        #             "do comprimento destravado (Lb) caso não se tenha informações sobre diagrama recomenda-se utilizar " \
        #             "o valor de (Cb) = 1, pois quanto mais proximo de 1 for o valor mais conservador será o cálculo. "
        #
        #
        #
        # # self.info_text = wx.StaticText(self.box_input_values, id=wx.ID_ANY, label=info_text)
        # self.info_text = wx.TextCtrl(self.box_input_values, value=info_text, style=wx.TE_MULTILINE | wx.TE_READONLY)
        # self.box_input_values.widgets_add(self.info_text, 0, False)

        self.main_sizer.Add(self.box_main,  proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5)

        self.window_main_panel.SetSizer(self.main_sizer)