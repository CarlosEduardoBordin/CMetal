import wx
import os
#criando uma classe para os wx.StaticBox rotulo - orientacao do sizer
class StaticBox(wx.Panel):
    #criacao do box
    def __init__(self, parent, box_label, orientation):
        super().__init__(parent)
        self.box = wx.StaticBox(self, label = box_label) #cria o staticbox
        self.orientation = orientation
        if orientation == "vertical":
            self.sizer_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        elif orientation == "horizontal":
            self.sizer_box_sizer = wx.StaticBoxSizer(self.box, wx.HORIZONTAL)
        elif orientation == "grid":
            self.sizer_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
            self.grid_sizer = wx.FlexGridSizer(rows=0, cols=2, vgap=5, hgap=10)
            self.grid_sizer.AddGrowableCol(1, proportion=1)
            self.sizer_box_sizer.Add(self.grid_sizer, 1, wx.EXPAND | wx.ALL, 5)
        elif orientation == "grid_four":

            self.sizer_box_sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
            self.grid_sizer_four = wx.FlexGridSizer(rows=0, cols=4, vgap=5, hgap=10)
            self.grid_sizer_four.AddGrowableCol(0)
            self.grid_sizer_four.AddGrowableCol(1)
            self.grid_sizer_four.AddGrowableCol(2)
            self.grid_sizer_four.AddGrowableCol(3)
            self.sizer_box_sizer.Add(self.grid_sizer_four, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(self.sizer_box_sizer)

        # configuracao do widget interno
    def widgets_add(self, widget, cols, free_expansion):
        if self.orientation!= "grid" and self.orientation != "grid_four":
            if free_expansion:
                self.sizer_box_sizer.Add(widget, 1, flag =  wx.ALL | wx.EXPAND, border=5 )
            elif not free_expansion:
                self.sizer_box_sizer.Add(widget, 0, flag =  wx.ALL | wx.EXPAND, border=5)

        elif self.orientation == "grid": # verificar se deve ser livre
            if cols == 0:
                self.grid_sizer.Add(widget, 1, flag = wx.ALIGN_CENTER_VERTICAL , border=5)
            elif cols == 1:
                if self.grid_sizer.GetItemCount() % 2 == 0:
                    self.grid_sizer.Add((0, 0), 0)
                self.grid_sizer.Add(widget,  0, flag =  wx.ALIGN_CENTER_VERTICAL, border=5)
            self.Layout() #atualiza
        else:
            self.grid_sizer_four.Add(widget, 1, flag=wx.EXPAND | wx.ALL, border=5)


class TextBoxVrf(wx.TextCtrl):
    def __init__(self, parent, value, only_numeric=False, **kwargs):
        super().__init__(parent, value = value, style=wx.TE_PROCESS_ENTER, **kwargs)
        self.only_numeric = only_numeric

    def get_value(self):
        value = self.GetValue().replace(",", ".").strip()

        if self.only_numeric:
            try:
                value = float(value)
                self._set_background(wx.Colour(255, 255, 255))  # branco
                return value
            except ValueError:
                self._set_background(wx.Colour(255, 200, 200))  # vermelho claro
                wx.MessageBox(f"Valor inválido: {value}", "Erro", wx.OK | wx.ICON_ERROR)
                return None
        else:
            self._set_background(wx.Colour(255, 255, 255))  # branco
            return value

    def _set_background(self, color):
        self.SetBackgroundColour(color)
        self.Refresh()

    def set_value(self, value):
        self.SetValue(value)

class SaveBox(wx.FileDialog):
    def __init__(self, parent):
        super().__init__(
            parent = parent,  # 'parent' da janela, None para ser independente
            message = "Salvar o arquivo como: ",
            defaultDir=os.path.expanduser("~"),  #pega o caminha inicial
            defaultFile="",  # Nome de arquivo padrão (opcional)
            wildcard="Arquivo PDF (Todos os arquivos (*.*)|*.*", #aparece todos os arquivos na combobox de salvar
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT  #overwrite vai pedir para sobreescrever
        )
    def get_path(self):
        if self.ShowModal() == wx.ID_OK:
            return self.GetPath()
        return None
