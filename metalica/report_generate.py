import wx
import os
from pylatex import Document, Section, Math
from pylatex.utils import NoEscape

class ReportGenerator:
    def __init__(self, file_name):
        self.file_name = file_name
        geometria = {
            "tmargin": "2cm",
            "lmargin": "2cm"
        }
        self.doc = Document(self.file_name, geometry_options=geometria)
        self.doc.preamble.append(NoEscape(r'\usepackage[dvipsnames]{xcolor}'))# tem que colocar isso para gerar o texto com cor !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.doc.preamble.append(NoEscape(r'\date{\today}'))# pega a data da geracao
        self.doc.preamble.append(NoEscape(r'\onehalfspacing'))
        self.doc.append(NoEscape(r'\maketitle')) #cria o titulo



    def add_section(self, title):
        #adicionar titulo a secao
        self.doc.append(NoEscape(r'\section*{' + title + '}'))

    def add_paragraph(self, text):
        #adicionar titulo a secao
        self.doc.append(text)

    def add_formula(self, formula_text):
        formula_formatada = NoEscape(r'\hspace{' + "1em" + r'} $' + formula_text + r'$ \\')
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
            self.doc.generate_pdf(compiler='pdflatex', clean_tex=False)
            print(f"PDF '{self.file_name}.pdf' gerado com sucesso!")
        except Exception as e:
            print(
                f"Ocorreu um erro ao gerar o PDF. Verifique se sua instalação do LaTeX (MiKTeX, etc.) está funcionando corretamente.")
            print(f"Erro: {e}")



