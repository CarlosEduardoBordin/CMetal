import wx
import os
from widget_class import StaticBox
from widget_class import TextBoxVrf


class AefValuesConfiguration(wx.MDIChildFrame):
    def __init__(self, parent_mdi:  wx.MDIParentFrame, parent_child: wx.MDIChildFrame, frame_name):
        #nao colocar no init o parent child
        super().__init__(parent_mdi, id=wx.ID_ANY, title=frame_name,
                         pos=wx.DefaultPosition, size=(350, 300), style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)
        # self.parent = parent
        self.parent_mdi = parent_mdi
        self.parent_child = parent_child

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
                if self.checkbox_aef_ab.IsChecked():
                    self.set_aef(float(-1))
                else:
                    self.set_aef(float(self.aef_input.get_value()))
            except Exception as e:
                wx.MessageBox(f"{e}", "Erro", wx.OK)

        def on_visibilidade(event):
            try:
                #evento de mudar unidades
                self.an_text.SetLabel(f"Área líquida da barra ({self.parent_mdi.get_unit_area()[0]}) :")
                self.aef_text.SetLabel(f"Área efetiva ({self.parent_mdi.get_unit_area()[0]}) :")

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
        self.ct_text = wx.StaticText(self.aef_calc_box, id=wx.ID_ANY, label="Coeficiente Ct (ADM): ")
        self.ct_text.SetToolTip("(Ct) é um coeficiente de redução da área líquida. Ex: podendo (Ct = 1) para força de tração "
                                "transmitida diretamente para cada elemento da seção "
                                "transversal da barra, (Ct = Ac/Ag), quando a tração for "
                                "transmitida somente por soldas transversais (Ac)-seção transversal do "
                                "elemento conectado (Ag)- área bruta da seção, para demais valores de (Ct), a norma deve ser consultada!")
        self.aef_calc_box.widgets_add(self.ct_text, 0, False)
        self.ct_input = TextBoxVrf(self.aef_calc_box, value = "", only_numeric=True)
        self.aef_calc_box.widgets_add(self.ct_input, 0, False)

        self.an_text = wx.StaticText(self.aef_calc_box, id=wx.ID_ANY, label="Área líquida da barra  (): ")
        self.an_text.SetToolTip("(An) é a área líquida da barra, podendo ser igual a área bruta, ou em regiões com furos,"
                                " feitos para ligação ou outras finalidades deve ser calculada a parte")
        self.aef_calc_box.widgets_add(self.an_text, 0, False)
        self.an_input = TextBoxVrf(self.aef_calc_box, value = "", only_numeric=True)
        self.aef_calc_box.widgets_add(self.an_input, 0, False)

        self.aef_text = wx.StaticText(self.aef_calc_box, id=wx.ID_ANY, label="Área efetiva (): ")
        self.aef_calc_box.widgets_add(self.aef_text, 0, False)
        self.aef_input = TextBoxVrf(self.aef_calc_box, value = "", only_numeric=True)
        self.aef_calc_box.widgets_add(self.aef_input, 0, False)

        self.valores_text = wx.StaticText(self.aef_calc_box, id=wx.ID_ANY, label="Valores: ")
        self.aef_calc_box.widgets_add(self.valores_text, 0, False)

        self.btn_calc = wx.Button(self.aef_calc_box, label="Calcular")
        self.aef_calc_box.widgets_add(self.btn_calc, 1, False)
        self.btn_calc.Bind(wx.EVT_BUTTON, on_calculate)

        self.btn_apl = wx.Button(self.box_main, label="Aplicar")
        self.box_main.widgets_add(self.btn_apl, 1, False)
        self.btn_apl.Bind(wx.EVT_BUTTON, on_aplicar)

        self.main_sizer.Add(self.box_main,  proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5)

        self.window_main_panel.SetSizer(self.main_sizer)