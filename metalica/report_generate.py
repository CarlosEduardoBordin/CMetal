import wx
import platform
import uuid
from datetime import datetime
from pylatex import Document, Command, Table,  Tabular
from pylatex.utils import NoEscape, bold


class ReportGenerator:
    def __init__(self,  parent_mdi : wx.MDIParentFrame , file_name, path):
        # self.frame_name = frame_name
        self.file_name = file_name
        self.path = path

        papel = parent_mdi.get_papel()
        orientacao = parent_mdi.get_orientacao()
        if orientacao: value = True
        else: value = False

        geometria = {
            "paper": papel,
            "landscape": value,
            "tmargin": "2cm",
            "lmargin": "2cm"
        }

        self.doc = Document(self.file_name, geometry_options=geometria)
        self.doc.preamble.append(NoEscape(r"\usepackage[dvipsnames]{xcolor}"))
        self.doc.preamble.append(NoEscape(r"\usepackage{parskip}"))  # Pacote para espaço sem indentação
        apend_titulo = self.file_name # colocar o titulo ou pedir ele?
        self.doc.preamble.append(Command("title", "Memória de cálculo - " + apend_titulo))
        system_name, system_version, hwid = platform.system(), platform.version(), str(uuid.getnode()) #str(uuid.getnode()) pega o MAC
        self.doc.preamble.append(Command("author", f"Sistema: {system_name}, versão: {system_version}, ID: {hwid}")) # Opcional, mas bom ter
        data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.doc.preamble.append(Command("date", NoEscape(fr"Data de geração: {data_geracao}")))

    def make_title(self):
        self.doc.append(NoEscape(r"\maketitle"))

    def add_section(self, title):
        #adicionar titulo a secao
        self.doc.append(NoEscape(r"\section*{" + title + "}"))

    def add_paragraph(self, text):
        self.doc.append(NoEscape(r"\noindent " + text + r" \par"))

    def add_formula(self, formula_text):
        formula_formatada = NoEscape(
            r"\begin{flushleft}" +
            r"$$" + formula_text + r"$$" +
            r"\end{flushleft}"
        )
        self.doc.append(formula_formatada)

    def add_calculo(self, dicionario_de_informacoes):
        self.add_section(dicionario_de_informacoes["titulo_da_secao"])
        for item in dicionario_de_informacoes["corpo"]: # pega os items do corpo do texto
            if item["tipo"] == "paragrafo":
                self.add_paragraph(item["conteudo"])
            elif item["tipo"] == "formula":
                self.add_formula(item["conteudo"])

    def gerar_pdf(self):
        try:
            self.doc.generate_pdf(self.path, clean_tex=False, compiler="pdflatex")
            # self.doc.generate_pdf(self.path, compiler="pdflatex", clean_tex=True)
        except Exception as e:
            wx.MessageBox(f"Ocorreu um erro ao salvar {e}", "Erro", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_ERROR)




