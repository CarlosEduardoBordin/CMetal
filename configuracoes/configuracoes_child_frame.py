import wx
from metalica.widget_class import StaticBox


class ConfiguracoesChildFrame(wx.MDIChildFrame):
    def __init__(self, parent):
        # Inicializa a janela filha com o título nome_formulario
        super().__init__(parent, -1, "Configurações", size=(300, 220), style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)
        self.parent = parent
        self.SetMinSize((300, 200))
        self.SetIcon( wx.Icon('icones/cfg.png', wx.BITMAP_TYPE_PNG))  # Definindo o ícone para o MDIFrame

        self.window_main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        def on_btn_apl(event):
            lenght_unit_selected = self.combo_box_si_lenght.GetValue()
            force_unit_selected = self.combo_box_si_force.GetValue()
            moment_unit_selected = self.combo_box_si_moment.GetValue()
            press_unit_selected = self.combo_box_si_press.GetValue()
            self.parent.set_unit_lenght(lenght_unit_selected)
            self.parent.set_unit_force(force_unit_selected)
            self.parent.set_unit_moment(moment_unit_selected)
            self.parent.set_unit_press(press_unit_selected)

        self.box_si = StaticBox(self.window_main_panel, "Sistema de unidades", orientation="grid")
        #comprimento
        self.lenght_text = wx.StaticText(self.box_si, id=wx.ID_ANY, label="Unidade de comprimento: ")
        self.box_si.widgets_add(self.lenght_text, 0, False)
        si_values_lenght = ["mm", "cm", "m"]
        self.combo_box_si_lenght = wx.ComboBox(self.box_si, id = wx.ID_ANY, style = wx.CB_READONLY,choices = si_values_lenght, value = si_values_lenght[2])
        self.box_si.widgets_add(self.combo_box_si_lenght, 1, False)
        #forca
        self.force_text = wx.StaticText(self.box_si, id=wx.ID_ANY, label="Unidade de força: ")
        self.box_si.widgets_add(self.force_text, 0, False)
        si_values_force = ["N", "KN", "MN"]
        self.combo_box_si_force= wx.ComboBox(self.box_si, id = wx.ID_ANY, style = wx.CB_READONLY,choices = si_values_force, value = si_values_force[1])
        self.box_si.widgets_add(self.combo_box_si_force, 1, False)
        #momento
        self.moment_text = wx.StaticText(self.box_si, id=wx.ID_ANY, label="Unidade de momento: ")
        self.box_si.widgets_add(self.moment_text, 0, False)
        si_values_momento = ["Nm", "KNm", "MNm"]
        self.combo_box_si_moment = wx.ComboBox(self.box_si, id = wx.ID_ANY, style = wx.CB_READONLY,choices = si_values_momento, value = si_values_momento[1])
        self.box_si.widgets_add(self.combo_box_si_moment, 1, False)
        #p/a
        self.press_text = wx.StaticText(self.box_si, id=wx.ID_ANY, label="Unidade de pressão: ")
        self.box_si.widgets_add(self.press_text, 0, False)
        si_values_press = ["Pa", "KPa", "MPa", "GPa"]
        self.combo_box_si_press= wx.ComboBox(self.box_si, id = wx.ID_ANY, style = wx.CB_READONLY,choices = si_values_press, value = si_values_press[2])
        self.box_si.widgets_add(self.combo_box_si_press, 1, False)
        #botao salvar
        self.aplicar_text = wx.StaticText(self.box_si, id=wx.ID_ANY, label="Configurações de unidades: ")
        self.box_si.widgets_add(self.aplicar_text, 0, False)

        self.btn_apl = wx.Button(self.box_si, label="Aplicar")
        self.box_si.widgets_add(self.btn_apl, 1, False)
        self.btn_apl.Bind(wx.EVT_BUTTON, on_btn_apl)

        self.main_sizer.Add(self.box_si,  proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5)
        self.window_main_panel.SetSizer(self.main_sizer)

