import wx
import os
from widget_class import StaticBox
from widget_class import TextBoxVrf


class PerfilList(wx.MDIChildFrame):
    def __init__(self, parent_mdi:  wx.MDIParentFrame, parent_child: wx.MDIChildFrame, frame_name):
        super().__init__(parent_mdi, id=wx.ID_ANY, title=frame_name,
                         pos=wx.DefaultPosition, size=(430, 400), style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX)
        # self.parent = parent
        self.parent_mdi = parent_mdi
        self.parent_child = parent_child

        self.window_main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        def update_list(lista):
            self.list_ctrl.DeleteAllItems()
            print(lista)
            for perfil, status in lista:
                indice = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(perfil))
                if status:
                    self.list_ctrl.SetItem(indice, 1, "Aprovado! ")
                    self.list_ctrl.SetItemTextColour(indice, wx.Colour(0, 128, 0))
                else:
                    self.list_ctrl.SetItem(indice, 1, "Reprovado ")
                    self.list_ctrl.SetItemTextColour(indice, wx.Colour(200, 0, 0))

        def filter_list():
            # inicia deletando os items
            dados_filtrados_verdadeiro = []
            dados_filtrados_falso = []
            for perfilstatus in self.parent_child.get_perfil_list():
                if perfilstatus[1]:
                    dados_filtrados_verdadeiro.append(perfilstatus)
                else:
                    dados_filtrados_falso.append(perfilstatus)
            return dados_filtrados_verdadeiro, dados_filtrados_falso

        def on_activate_checkbox(event):
            lista_aprovados, lista_reprovados = filter_list()
            aprovados = self.checkbox_aprovado.IsChecked()
            reprovados = self.checkbox_reprovado.IsChecked()
            if aprovados and reprovados:
                update_list(self.parent_child.get_perfil_list())
            elif aprovados:
                update_list(lista_aprovados)
            elif reprovados:
                update_list(lista_reprovados)
            else:
                update_list([])
            # update_list(dados_filtrados_verdadeiro)
        def on_mais_leve(event):
            lista_aprovados, lista_reprovados = filter_list()
            menor_massa = min(lista_aprovados, key=lambda massa: float(massa[1])) #pega o segundo valor que e massa linear
            update_list([menor_massa])

        self.box_main = StaticBox(self.window_main_panel, "Lista",orientation = "vertical")
        #list crtl
        self.list_ctrl = wx.ListCtrl(self.box_main, style=wx.LC_REPORT)
        self.box_main.widgets_add(self.list_ctrl,0,True)
        self.list_ctrl.InsertColumn(0, "Perfil")
        self.list_ctrl.InsertColumn(1, "Status")
        update_list(self.parent_child.get_perfil_list())

        self.box_manipulate = StaticBox(self.window_main_panel, "Manipular",orientation = "vertical")
        self.filtrar = StaticBox(self.box_manipulate, "Filtrar",orientation = "horizontal")
        self.box_manipulate.widgets_add(self.filtrar,0,False)
        self.checkbox_aprovado = wx.CheckBox(self.filtrar, label="Aprovados")
        self.checkbox_aprovado.SetValue(True)
        self.filtrar.widgets_add(self.checkbox_aprovado,0,False)
        self.Bind(wx.EVT_CHECKBOX, on_activate_checkbox, self.checkbox_aprovado)
        self.checkbox_reprovado = wx.CheckBox(self.filtrar, label="Reprovados")
        self.checkbox_reprovado.SetValue(True)
        self.filtrar.widgets_add(self.checkbox_reprovado,0,False)
        self.Bind(wx.EVT_CHECKBOX, on_activate_checkbox, self.checkbox_reprovado)
        self.box_mais_leve = StaticBox(self.box_manipulate, "Procurar", orientation="vertical")
        self.box_manipulate.widgets_add(self.box_mais_leve, 0, False)
        self.btn_procurar = wx.Button(self.box_mais_leve, label="Procurar o mais leve")
        self.box_mais_leve.widgets_add(self.btn_procurar, 0, False)
        self.btn_procurar.Bind(wx.EVT_BUTTON, on_mais_leve)


        self.main_sizer.Add(self.box_main,  proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5)
        self.main_sizer.Add(self.box_manipulate,  proportion = 0, flag = wx.ALL | wx.EXPAND, border = 5)


        self.window_main_panel.SetSizer(self.main_sizer)