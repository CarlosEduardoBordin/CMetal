import wx
import numpy as np
from pint import UnitRegistry
from metalica.report_generate import ReportGenerator


class VerificationProcess:
    def __init__(self, parent_mdi : wx.MDIParentFrame, linear_mass_text, d_text, bf_text, tw_text, tf_text, h_text, d_l_text, area_text, i_x_text,
                 w_x_text, r_x_text,
                 z_x_text, i_y_text, w_y_text, r_y_text, z_y_text, r_t_text, i_t_text, bf_two_text, d_tw_text, cw_text,
                 u_text, aef, fy, fu, lfx, lfy, lfz,
                 flb, fnt, fnc, fcx, fcy, mfx, mfy, y_um, g, e, cb, frame_name, save_path):
        self.parent_mdi = parent_mdi
        self.linear_mass_text = linear_mass_text
        self.d_text = d_text
        self.bf_text = bf_text
        self.tw_text = tw_text
        self.tf_text = tf_text
        self.h_text = h_text
        self.d_l_text = d_l_text
        self.area_text = area_text
        self.i_x_text = i_x_text
        self.w_x_text = w_x_text
        self.r_x_text = r_x_text
        self.z_x_text = z_x_text
        self.i_y_text = i_y_text
        self.w_y_text = w_y_text
        self.r_y_text = r_y_text
        self.z_y_text = z_y_text
        self.r_t_text = r_t_text
        self.i_t_text = i_t_text
        self.bf_two_text = bf_two_text
        self.d_tw_text = d_tw_text
        self.cw_text = cw_text
        self.u_text = u_text
        self.aef = aef
        self.fy = fy
        self.fu = fu
        self.lfx = lfx
        self.lfy = lfy
        self.lfz = lfz
        self.flb = flb
        self.fnt = fnt
        self.fnc = fnc
        self.fcx = fcx
        self.fcy = fcy
        self.mfx = mfx
        self.mfy = mfy
        self.y_um = y_um
        self.e = e
        self.g = g
        self.cb = cb
        self.save_path = save_path
        self.frame_name = frame_name
        #precisao colocar em cfg
        self.ureg = UnitRegistry()
        self.unidade_comprimento = (self.parent_mdi.get_unit_press()[0])
        self.unidade_area = (self.parent_mdi.get_unit_area()[0])
        self.unidade_volume = (self.parent_mdi.get_unit_volume()[0])
        self.unidade_inercia = (self.parent_mdi.get_unit_inercia()[0])
        self.unidade_six = (self.parent_mdi.get_unit_six()[0])
        self.unidade_forca = (self.parent_mdi.get_unit_force()[0])
        self.unidade_momento = (self.parent_mdi.get_unit_moment()[0])
        self.unidade_pressao = (self.parent_mdi.get_unit_press()[0])
        #casas decimais !
        self.casa_decimal_comprimento = int(float(self.parent_mdi.get_unit_press()[1]))
        self.casa_decimal_area = int(float(self.parent_mdi.get_unit_area()[1]))
        self.casa_decimal_volume = int(float(self.parent_mdi.get_unit_volume()[1]))
        self.casa_decimal_inercia = int(float(self.parent_mdi.get_unit_inercia()[1]))
        self.casa_decimal_six = int(float(self.parent_mdi.get_unit_six()[1]))
        self.casa_decimal_forca = int(float(self.parent_mdi.get_unit_force()[1]))
        self.casa_decimal_momento = int(float(self.parent_mdi.get_unit_moment()[1]))
        self.casa_decimal_pressao = int(float(self.parent_mdi.get_unit_press()[1]))
        # self.casa_decimal_comprimento = self.parent.get_unit_press()[0]
        # self.casa_decimal_area = 5
        # self.casa_decimal_volume = 5
        # self.casa_decimal_inercia = 5
        # self.casa_decimal_six = 2
        # self.casa_decimal_forca = 2
        # self.casa_decimal_momento = 2
        # self.casa_decimal_pressao = 2



    # para perfis laminados
    def normal_traction(self):

        if self.aef <= 0: aef = self.area_text # verificacao da area efetiva !
        else: aef = self.aef
        ntrd = aef * self.fy / self.y_um
        ntsd = self.fnt

        passou = ntsd <= ntrd

        # print(f"nts {ntrd} nrd {self.fnt}")
        status_texto = r" \textcolor{ForestGreen}{Aprovado}" if passou else r"\textcolor{red}{Reprovado}"
        ############################################memoria
        memoria_calculo_nomal = {
            "titulo_da_secao": "Verificação a força normal de tração ",
            "corpo": [
                {"tipo": "paragrafo", "conteudo": "ELU para escoamento da seção bruta: \n"},
                {
                    "tipo": "formula", "conteudo": (
                        r"N_{trd} = \frac{A_g * f_y}{\gamma_{a1}} \Rightarrow \frac{"
                        + f"{aef.magnitude:.{self.casa_decimal_area}f} * " + f"{self.fy.magnitude:.{self.casa_decimal_pressao}f}" + r"}{" +
                        f"{self.y_um:.2f}" + r"} = " + f"{ntrd:.{self.casa_decimal_forca}f}"
                )},
                {"tipo": "paragrafo", "conteudo": "\n Verificando: "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"N_{tsd} \le  N_{trd} \Rightarrow " + f"{ntsd:.{self.casa_decimal_forca}f}"  + r"\le" + f"{ntrd:.{self.casa_decimal_forca}f}"
                            + r"\quad " + status_texto)
                }
            ]
        }
        utilization_t = ntsd / ntrd
        if passou:
            return False, memoria_calculo_nomal, utilization_t  #nao passa
        else:
            return True, memoria_calculo_nomal, utilization_t  #passa

    def normal_compression(self):
        # compressao
        # indice de esbeltez da secao recomendado < 200
        ind_esblt_x = self.lfx / self.r_x_text
        ind_esblt_y = self.lfy / self.r_y_text
        # flambagem por flexao em x
        n_e_x = (np.pi ** 2) * self.e * self.i_x_text / (self.lfx ** 2)
        n_e_y = (np.pi ** 2) * self.e * self.i_y_text / (self.lfy ** 2)
        r_o = np.sqrt(self.r_x_text ** 2 + self.r_y_text ** 2 + 0 + 0)  # considerando o perfil como simetrico
        # print(f"nex = {n_e_x}")
        # print(f"ney = {n_e_y}")
        n_e_z = (1 / (r_o ** 2)) * (((np.pi ** 2) * self.e * self.cw_text / (
                self.lfz ** 2)) + self.g * self.i_t_text)  # J = it na tabela
        # n_e_x = n_e_x.to(self.unidade_forca)
        # n_e_y = n_e_y.to(self.unidade_forca)
        # n_e_z = n_e_z.to(self.unidade_forca)

        print(n_e_x)
        print(n_e_y)
        print(n_e_z)
        n_e = np.min([n_e_x.magnitude, n_e_y.magnitude, n_e_z.magnitude])
        # lambda0 5.3.3.2
        lbd_zero = np.sqrt(self.area_text * self.fy / n_e)
        # fator de reducao 5.3.3.1
        if lbd_zero.magnitude <= 1.5:
            psi = 0.658 ** (lbd_zero.magnitude ** 2)
        else:
            psi = 0.877 / (lbd_zero.magnitude ** 2)
        # ************************************************************************************************************
        # verificacao da esbeltez local
        # elemento AA
        b_sobre_t_alma = self.d_l_text / self.tw_text
        b_sobre_t_limit_alma = 1.49 * np.sqrt(self.e / self.fy)
        # elemento AL
        b_sobre_t_aba = (self.bf_text / 2) / self.tf_text  # bf/2 pega 1 aba da mesa
        b_sobre_t_limit_aba = 0.56 * np.sqrt(self.e / self.fy)

        area_efetiva_alma, area_efetiva_aba, b_efetivo_alma, b_efetivo_aba = 0, 0, 0, 0

        if b_sobre_t_alma <= b_sobre_t_limit_alma and b_sobre_t_aba <= b_sobre_t_limit_aba:
            # area vai ser a bruta
            area_efetiva = self.area_text
            # pass
        else:
            # alma
            if b_sobre_t_alma <= b_sobre_t_limit_alma / np.sqrt(psi):
                area_efetiva_alma = 0
                # area_efetiva_alma =  self.d_l_text * self.tw_text
            else:
                sigma_e_l = ((1.31 * ((1.49 * np.sqrt(self.e / self.fy)) / b_sobre_t_alma)) ** 2) * self.fy
                b_efetivo_alma = self.d_l_text * (1 - 0.18 * np.sqrt(sigma_e_l / (psi * self.fy))) * np.sqrt(
                    sigma_e_l / (psi * self.fy))
                # area_efetiva_alma = (self.d_l_text * self.tw_text) - b_efetivo
            if b_sobre_t_aba <= b_sobre_t_aba <= b_sobre_t_limit_aba / np.sqrt(psi):
                area_efetiva_aba = 0
                # area_efetiva_aba = (self.bf_text/2) * self.tf_text
            else:
                sigma_e_l = ((1.49 * (
                        (0.56 * np.sqrt(self.e / self.fy)) / (self.bf_text / 2 * self.tf_text))) ** 2) * self.fy
                b_efetivo_aba = (self.bf_text / 2) * (1 - 0.22 * np.sqrt(sigma_e_l / (psi * self.fy))) * np.sqrt(
                    sigma_e_l / (psi * self.fy))
                # area_efetiva_aba = ((self.bf_text/2) * self.tf_text)- b_efetivo
            area_efetiva = self.area_text - area_efetiva_alma - area_efetiva_aba - b_efetivo_alma - b_efetivo_aba * 4
        nrdc = psi * area_efetiva * self.fy / self.y_um
        passou = self.fnc <= nrdc  # verificando
        status_texto = r" \textcolor{ForestGreen}{Aprovado}" if passou else r"\textcolor{red}{Reprovado}"

        memoria_calculo_normal_c = {
            "titulo_da_secao": "Verificação da força normal de compressão",
            "corpo": [
                {"tipo": "paragrafo", "conteudo": "Índice de esbeltez da barra comprimida: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"\lambda_x = \frac{L_x}{r_x} \Rightarrow = \frac{" + f"{self.lfx.magnitude:.{self.casa_decimal_comprimento}f}" + r"}{" +
                            f"{self.r_x_text.magnitude:.{self.casa_decimal_comprimento}f}" + r"} = " + f"{ind_esblt_x:.2f}"
                            + r", \quad \lambda_y = \frac{L_y}{r_y} \Rightarrow \lambda_y = \frac{" + f"{self.lfy.magnitude:.{self.casa_decimal_comprimento}f}" +
                            r"}{" + f"{self.r_y_text.magnitude:.{self.casa_decimal_comprimento}f}" + r"} = " + f"{ind_esblt_y:.2f} \n"
                    )
                },
                {"tipo": "paragrafo",
                 "conteudo": "\n Flambagem por flexão em relação ao eixo x da seção transversal: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"N_{ex} = \frac{\pi^2 * E * I_x}{L_x^2} \Rightarrow \frac{\pi^2 * " + f"{self.e.magnitude:.{self.casa_decimal_pressao}f}" +
                            r" * " + f"{self.i_x_text.magnitude:.{self.casa_decimal_inercia}f}" + r"}{" + f"{self.lfx.magnitude:.{self.casa_decimal_comprimento}f}" +
                            r"^2} = " + f"{n_e_x:.{self.casa_decimal_forca}f}"
                    )
                },
                {"tipo": "paragrafo",
                 "conteudo": "\n Flambagem por flexão em relação ao eixo y da seção transversal: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"N_{ey} = \frac{\pi^2 * E * I_y}{L_y^2} \Rightarrow \frac{\pi^2 * " +
                            f"{self.e.magnitude:.{self.casa_decimal_pressao}f}" + r" * " + f"{self.i_y_text.magnitude:.{self.casa_decimal_inercia}f}" +
                            r"}{" + f"{self.lfy.magnitude:.{self.casa_decimal_comprimento}f}" + r"^2} = " + f"{n_e_y:.{self.casa_decimal_forca}f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Raio de giração polar da seção bruta: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"R_0 = \sqrt{r_x^2 + r_y^2 + x_0^2 + y_0^2} \Rightarrow \sqrt{" + f"{self.r_x_text}" + r"^2 + " +
                            f"{self.r_y_text.magnitude}" + r"^2 + 0^2 + 0^2} = " + f"{r_o.magnitude:.{self.casa_decimal_comprimento}f}" + f" \n"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Flambagem por torção em relação ao eixo longitudinal z: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                            f"\n" + r"N_{ez} = \frac{1}{r_0} \left( \frac{\pi * E * C_w}{L_z^2} + G * J \right) \Rightarrow \frac{1}{" +
                            f"{r_o:.{self.casa_decimal_comprimento}f}" + r"} \left( \frac{\pi * " + f"{self.e.magnitude:.{self.casa_decimal_pressao}f}" +
                            r" * " + f"{self.cw_text.magnitude:.{self.casa_decimal_six}f}" + r"}{" + f"{self.lfz.magnitude:.{self.casa_decimal_comprimento}f}" + r"^2} + " +
                            f"{self.g.magnitude:.{self.casa_decimal_pressao}f}" + r" + " + f"{self.i_t_text.magnitude:.{self.casa_decimal_inercia}f}" + r" \right) = " +
                            f"{n_e_z:.{self.casa_decimal_forca}f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n"},  #quebra linha
                {
                    "tipo": "formula",
                    "conteudo": (
                            "\n" + r"N_e = \min(N_{ex}, N_{ey}, N_{ez}) = " + f"{n_e:.{self.casa_decimal_forca}f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Índice de esbeltez reduzido: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"\lambda_0 = \sqrt{\frac{A_g * f_y}{N_e}} \Rightarrow \sqrt{\frac{" +
                            f"{self.area_text.magnitude:.{self.casa_decimal_area}f}" + r" * " + f"{self.fy.magnitude:.{self.casa_decimal_pressao}f}" +
                            r"}{" + f"{n_e:.{self.casa_decimal_forca}f}" + r"}} = " + f"{lbd_zero:.2f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Fator de redução: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"\chi = " + f"{psi:.3f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Area efetiva: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r" A_{ef} =" + f"{area_efetiva:.{self.casa_decimal_area}f} \n")
                },
                {"tipo": "paragrafo", "conteudo": "\n Força axial de compressão resistente de cálculo: \n "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"N_{crd} = \frac{\chi * A_{ef} * f_y}{\gamma_1} \Rightarrow \frac{" +
                            f"{psi:.3f}" + r" * " + f"{area_efetiva.magnitude:.{self.casa_decimal_area}f}" + r" * " +
                            f"{self.fy.magnitude:.{self.casa_decimal_pressao}f}" + r"}{" + f"{self.y_um}" + r"} = " + f"{nrdc:.{self.casa_decimal_pressao}f}")
                },
                {"tipo": "paragrafo", "conteudo": "\n Verificando: "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"N_{tsd} \le  N_{trd} \Rightarrow " + f"{self.fnc:.{self.casa_decimal_forca}f}" + r"\le" + f"{nrdc:.{self.casa_decimal_forca}f}"
                            + r"\quad" + status_texto)
                },
            ]
        }

        utilization_c = self.fnc / nrdc
        if passou:
            # elemento passa
            return True, memoria_calculo_normal_c, utilization_c
        else:
            # elemento nao passa
            return False, memoria_calculo_normal_c, utilization_c

    def shear_force_x(self):
        #sf = shear force
        vrd = 0
        lambda_sf = self.h_text / self.tw_text
        lambda_p = 1.1 * np.sqrt(5.34 * self.e / self.fy)
        lambda_r = 1.37 * np.sqrt(5.34 * self.e / self.fy)
        aw = 2 * self.d_text * self.tw_text
        vpl = 0.6 * aw * self.fy

        status_lambda, lambda_texto = "", ""
        if lambda_sf <= lambda_p:
            vrd = vpl / self.y_um
            status_lambda = r"\lambda \le \lambda_{p} "
            lambda_texto = (r"V_{rd} = \frac{V_{pl}}{\gamma_1} \Rightarrow \frac{" +
                            f"{vpl:.{self.casa_decimal_forca}f}" + r"}{" + f"{self.y_um}" + r"} = " + f"{vrd:.{self.casa_decimal_forca}f}")
        elif lambda_p < lambda_sf <= lambda_r:
            vrd = (lambda_p / lambda_sf) * (vpl / self.y_um)
            status_lambda = r"\lambda_{p} \le \lambda_{} \le \lambda_{r}  "
            lambda_texto = (r"V_{rd} = \frac{\lambda_{p} * V_{pl}}{\lambda * \gamma_1} \Rightarrow " + r"\frac{" +
                            f"{lambda_p:.2f} * {vpl:.{self.casa_decimal_forca}f}" + r"}{" + f"{lambda_sf:.2f} * {self.y_um}" + r"} = " +
                            f"{vrd:.{self.casa_decimal_forca}f}")
        elif lambda_sf >= lambda_r:
            vrd = 1.24 * ((lambda_p / lambda_sf) ** 2) * (vpl / self.y_um)
            status_lambda = r"\lambda_{} \ge \lambda_{r} "
            lambda_texto = (
                    r"V_{rd} = 1.24 * \left( \frac{\lambda_{p}}{\lambda} \right)^2 * \frac{V_{pl}}{\gamma_1} \Rightarrow " +
                    f"1.24 * \\left( \\frac{{{lambda_p}}}{{{lambda_sf}}} \\right)^2 * " +
                    f"\\frac{{{vpl:.{self.casa_decimal_forca}f}}}{{{self.y_um}}} = {vrd:.{self.casa_decimal_forca}f}")

        passou = self.fcx <= vrd  # verificando
        status_texto = r" \textcolor{ForestGreen}{Aprovado}" if passou else r"\textcolor{red}{Reprovado}"

        memoria_calculo_shear_x = {
            "titulo_da_secao": "Verificação da cortante em relalção ao eixo X do perfil",
            "corpo": [
                {"tipo": "paragrafo", "conteudo": "\n Verificação da flambagem da alma pela cortante: \n "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r" \lambda = \frac{h}{t_w} \Rightarrow \frac{" +
                            f"{self.h_text.magnitude:.{self.casa_decimal_comprimento}f}" + r"}{" + f"{self.tw_text.magnitude:.{self.casa_decimal_comprimento}f}" + r"} = " + f"{lambda_sf:.2f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                            r" \lambda_p = 1.1 * \sqrt{\frac{k_v * E}{f_y}} \Rightarrow "
                            r"1.1 * \sqrt{\frac{5.34 * " + f"{self.e.magnitude:.{self.casa_decimal_pressao}f}" + r"}{" + f"{self.fy.magnitude:.{self.casa_decimal_pressao}f}" + r"}} = " + f"{lambda_p:.2f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"\lambda_r = 1.37 * \sqrt{\frac{k_v * E}{f_y}} \Rightarrow "
                            r"1.37 * \sqrt{\frac{5.34 * " + f"{self.e.magnitude:.{self.casa_decimal_pressao}f}" + r"}{" + f"{self.fy.magnitude:.{self.casa_decimal_pressao}f}" + r"}} = " + f"{lambda_r:.2f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Área efetiva do cisalhamento: \n "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"A_w = 2 * d * t_w \Rightarrow 2 * " + f"{self.d_text.magnitude:.{self.casa_decimal_comprimento}f} * {self.tw_text.magnitude:.{self.casa_decimal_comprimento}f} = {aw:.2f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Força cortante correspondente a plastificação da alma: \n "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"V_{pl} = 0.6 * A_w * f_y \Rightarrow 0.6 * " +
                            f"{aw:.2f} * {self.fy.magnitude:.{self.casa_decimal_pressao}f} = {vpl:.{self.casa_decimal_forca}f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n  Verificando a condição: \n "},
                {
                    "tipo": "formula",
                    "conteudo": status_lambda
                },
                {"tipo": "paragrafo", "conteudo": "\n  Força cortante resistente de cálculo: \n "},

                {
                    "tipo": "formula",
                    "conteudo": lambda_texto
                },
                {"tipo": "paragrafo", "conteudo": "\n Verificando: "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"V_{sd} \le  V_{rd} \Rightarrow " + f"{self.fcx:.{self.casa_decimal_pressao}f}" + r"\le" + f"{vrd:.{self.casa_decimal_forca}f}"
                            + r"\quad" + status_texto)
                },
            ]
        }

        utilization_s_x = self.fcx / vrd
        if passou:
            return True, memoria_calculo_shear_x, utilization_s_x
        else:
            return False, memoria_calculo_shear_x, utilization_s_x

    def shear_force_y(self):
        vrd = 0
        #sf = shear force
        lambda_sf = (self.bf_text / 2) / self.tf_text
        #kv = 1.2 item 5.4.3.3
        lambda_p = 1.1 * np.sqrt((1.2 * self.e) / self.fy)
        lambda_r = 1.37 * np.sqrt(1.2 * self.e / self.fy)
        aw = 2 * self.bf_text * self.tf_text
        vpl = 0.6 * aw * self.fy

        status_lambda, lambda_texto = "", ""
        if lambda_sf <= lambda_p:
            vrd = vpl / self.y_um
            status_lambda = r"\lambda \le \lambda_{p} "
            lambda_texto = r"V_{rd} = \frac{V_{pl}}{\gamma_1} \Rightarrow \frac{" + f"{vpl:.{self.casa_decimal_forca}f}" + r"}{" + f"{self.y_um}" + r"} = " + f"{vrd:.{self.casa_decimal_forca}f}"

        elif lambda_p < lambda_sf <= lambda_r:
            vrd = (lambda_p / lambda_sf) * (vpl / self.y_um)
            status_lambda = r"\lambda_{p} \le \lambda_{} \le \lambda_{r}  "
            lambda_texto = r"V_{rd} = \frac{\lambda_{p} * V_{pl}}{\lambda * \gamma_1} \Rightarrow " + r"\frac{" + f"{lambda_p:.2f} * {vpl:.{self.casa_decimal_forca}f}" + r"}{" + f"{lambda_sf:.2f} * {self.y_um}" + r"} = " + f"{vrd:.{self.casa_decimal_forca}f}"

        elif lambda_sf >= lambda_r:
            vrd = 1.24 * ((lambda_p / lambda_sf) ** 2) * (vpl / self.y_um)
            status_lambda = r"\lambda_{} \ge \lambda_{r} "
            lambda_texto = r"V_{rd} = 1.24 * \left( \frac{\lambda_{p}}{\lambda} \right)^2 * \frac{V_{pl}}{\gamma_1} \Rightarrow " + f"1.24 * \\left( \\frac{{{lambda_p}}}{{{lambda_sf}}} \\right)^2 * " + f"\\frac{{{vpl:.{self.casa_decimal_forca}f}}}{{{self.y_um}}} = {vrd:.{self.casa_decimal_forca}f}"

        passou = self.fcy <= vrd  # verificando
        status_texto = r" \textcolor{ForestGreen}{Aprovado}" if passou else r"\textcolor{red}{Reprovado}"

        memoria_calculo_shear_y = {
            "titulo_da_secao": "Verificação da cortante em relalção ao eixo Y do perfil",
            "corpo": [
                {"tipo": "paragrafo", "conteudo": "\n Verificação da flambagem da mesa pela cortante: \n "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"\lambda = \frac{bf*0.5}{tf} \Rightarrow \frac{" +
                            f"{self.bf_text.magnitude:.{self.casa_decimal_comprimento}f} * 0.5" + r"}{" + f"{self.tf_text.magnitude:.{self.casa_decimal_comprimento}f}" + r"} = " + f"{lambda_sf:.2f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"\lambda_p = 1.1 * \sqrt{\frac{k_v * E}{f_y}} \Rightarrow "
                            r"1.1 * \sqrt{\frac{5.34 * " + f"{self.e.magnitude:.{self.casa_decimal_pressao}f}" + r"}{" + f"{self.fy.magnitude:.{self.casa_decimal_pressao}f}" + r"}} = " + f"{lambda_p:.2f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"\lambda_r = 1.37 * \sqrt{\frac{k_v * E}{f_y}} \Rightarrow "
                            r"1.37 * \sqrt{\frac{5.34 * " + f"{self.e.magnitude:.{self.casa_decimal_pressao}f}" + r"}{" + f"{self.fy.magnitude:.{self.casa_decimal_pressao}f}" + r"}} = " + f"{lambda_r:.2f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Área efetiva do cisalhamento: \n "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"A_w = 2 * b_f * t_f \Rightarrow 2 * " + f"{self.bf_text.magnitude:.{self.casa_decimal_comprimento}f} * {self.tf_text.magnitude:.{self.casa_decimal_comprimento}f} = {aw:.2f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Força cortante correspondente a plastificação da mesa: \n "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"V_{pl} = 0.6 * A_w * f_y \Rightarrow 0.6 * " +
                            f"{aw:.2f} * {self.fy.magnitude:.{self.casa_decimal_pressao}f} = {vpl:.{self.casa_decimal_forca}f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n  Verificando a condição: \n "},
                {
                    "tipo": "formula",
                    "conteudo": status_lambda
                },
                {"tipo": "paragrafo", "conteudo": "\n  Força cortante resistente de cálculo: \n "},
                {
                    "tipo": "formula",
                    "conteudo": lambda_texto
                },
                {"tipo": "paragrafo", "conteudo": "\n Verificando: "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            rf"V_{{sd}} \le  V_{{rd}} \Rightarrow " + f"{self.fcx:.{self.casa_decimal_forca}f}" + r"\le" + f"{vrd:.{self.casa_decimal_forca}f}"
                            + r"\quad" + status_texto)
                },
            ]
        }

        utilization_s_y = self.fcy / vrd
        if passou:
            return True, memoria_calculo_shear_y, utilization_s_y
        else:
            return False, memoria_calculo_shear_y, utilization_s_y

    def moment_force_x(self):
        mrd_flt, mrd_flm, mrd_fla = 0, 0, 0  #inicializando para nao dar problema
        #flambagem lateral com torcao
        #*********************************************************************************************
        lambda_flt = self.flb / self.r_y_text  #considerando lfb como comprimento de flambagem
        lambda_flt_p = 1.76 * np.sqrt(self.e / self.fy)  #Tabela D1 considerando 2 eixos de simetria
        beta = (self.fy - 0.3 * self.fy) * self.w_x_text / (self.e * self.i_t_text)  #considerar 30% do fy para sigma
        lambda_flt_r = (
                (1.38 * self.cb * np.sqrt(self.i_y_text * self.i_t_text) / (self.r_y_text * self.i_t_text * beta)) *
                np.sqrt(1 + np.sqrt(1 + (27 * self.cw_text * beta ** 2) / ((self.cb ** 2) * self.i_y_text))))
        mr_flt = (self.fy - 0.3 * self.fy) * self.w_x_text
        mpl_flt = self.z_x_text * self.fy
        #fazendo um lambda separado para cada, para nao ficar ruim de passar na memoria !
        status_lambda_flt, lambda_flt_text, status_mcr_flt = "", "", ""
        if lambda_flt <= lambda_flt_p:
            mrd_flt = mpl_flt / self.y_um
            status_lambda_flt = r"\lambda \le \lambda_{flt} "
            lambda_flt_text = r"M_{rd} = \frac{M_{pl}}{\gamma_1} \Rightarrow \frac{" + f"{mpl_flt:.{self.casa_decimal_momento}f}" + r"}{" + f"{self.y_um}" + r"} = " + f"{mrd_flt:.{self.casa_decimal_momento}f}"
        elif lambda_flt_p < lambda_flt <= lambda_flt_r:
            mrd_flt = (1 / self.y_um) * (
                    mpl_flt - ((mpl_flt - mr_flt) * ((lambda_flt - lambda_flt_p) / (lambda_flt_r - lambda_flt_p))))
            status_lambda_flt = r"\lambda_{p} \le \lambda_{flt} \le \lambda_{r}  "
            lambda_flt_text = (
                rf"M_{{rd}} = \frac{{1}}{{\gamma_1}} * \left[M_{{pl}} - \left(M_{{pl}} - M_{{r}}\right)"
                rf" * \left(\frac{{\lambda_{{LT}} - \lambda_{{p}}}}{{\lambda_{{r}} - \lambda_{{p}}}}\right)\right]"
                rf" \Rightarrow \frac{{1}}{{{self.y_um}}} * \left[{mpl_flt.magnitude:.{self.casa_decimal_momento}f} - "
                rf"\left({mpl_flt.magnitude:.{self.casa_decimal_momento}f} - {mr_flt.magnitude:.{self.casa_decimal_momento}f}\right) * "
                rf"\left(\frac{{{lambda_flt.magnitude:.2f} - {lambda_flt_p.magnitude:.2f}}}{{{lambda_flt_r.magnitude:.2f} - {lambda_flt_p.magnitude:.2f}}}\right)\right] = "
                rf"{mrd_flt:.{self.casa_decimal_momento}f}"
            )
        elif lambda_flt > lambda_flt_r:
            mcr_flt = ((self.cb * (np.pi ** 2) * self.e * self.i_y_text) / (self.flb ** 2)) * np.sqrt(
                (self.cw_text / self.i_y_text) * (1 + 0.039 * (self.i_t_text * (self.flb ** 2) / self.cw_text)))
            mrd_flt = mcr_flt / self.y_um
            status_lambda_flt = r"\lambda_{flt} \ge \lambda_{r} "
            #deu problema no miktex essa aqui
            status_mcr_flt = (
                rf"M_{{cr}} = \frac{{C_b * \pi^2 * E * I_y}}{{L_b^2}} * \sqrt{{\frac{{C_w}}{{I_y}}"
                rf" * \left(1 + 0.039 * \frac{{I_t * L_b^2}}{{C_w}}\right)}} \Rightarrow "
                rf"\frac{{{self.cb} * \pi^2 * {self.e:.{self.casa_decimal_pressao}f} * {self.i_y_text:.{self.casa_decimal_inercia}f}}}"
                rf"{{{self.flb.magnitude:.{self.casa_decimal_comprimento}f}^2}} * \sqrt{{\frac{{{self.cw_text.magnitude:.{self.casa_decimal_six}f}}}{{{self.i_y_text.magnitude:.{self.casa_decimal_inercia}f}}}"
                rf" * \left(1 + 0.039 * \frac{{{self.i_t_text.magnitude:.{self.casa_decimal_inercia}f} * {self.flb.magnitude:.{self.casa_decimal_comprimento}f}^2}}"
                rf"{{{self.cw_text.magnitude:.{self.casa_decimal_six}f}}}\right)}} = {mcr_flt:.{self.casa_decimal_momento}f}")
            lambda_flt_text = (r"M_{rd} = \frac{M_{cr}}{\gamma_1} \Rightarrow \frac{" +
                               f"{mcr_flt.magnitude:.{self.casa_decimal_momento}f}" + r"}{" +
                               f"{self.y_um}" + r"} = " + f"{mrd_flt:.{self.casa_decimal_momento}f}")
        # flambagem local da mesa comprimida
        # *********************************************************************************************
        lambda_flm = (self.bf_text / 2) / self.tf_text
        lambda_flm_p = 0.38 * np.sqrt(self.e / self.fy)
        lambda_flm_r = 0.83 * np.sqrt(self.e / (self.fy - 0.3 * self.fy))
        mr_flm = (self.fy - 0.3 * self.fy) * self.w_x_text
        mpl_flm = self.z_x_text * self.fy

        status_lambda_flm, status_mcr_flm, lambda_flm_text = "", "", ""
        if lambda_flm <= lambda_flm_p:
            mrd_flm = mpl_flm / self.y_um
            status_lambda_flm = r"\lambda \le \lambda_{flm} "
            lambda_flm_text = r"M_{rd} = \frac{M_{pl}}{\gamma_1} \Rightarrow \frac{" + f"{mpl_flm.magnitude:.{self.casa_decimal_momento}f}" + r"}{" + f"{self.y_um}" + r"} = " + f"{mrd_flm:.{self.casa_decimal_momento}f}"
        elif lambda_flm_p < lambda_flm <= lambda_flm_r:
            mrd_flm = (1 / self.y_um) * (
                    mpl_flm - ((mpl_flm - mr_flm) * ((lambda_flm - lambda_flm_p) / (lambda_flm_r - lambda_flm_p))))
            status_lambda_flm = r"\lambda_{p} \le \lambda_{flm} \le \lambda_{r}  "
            lambda_flm_text = (
                rf"M_{{rd}} = \frac{{1}}{{\gamma_1}} * \left[M_{{pl}} - \left(M_{{pl}} - M_{{r}}\right)"
                rf" * \left(\frac{{\lambda_{{lm}} - \lambda_{{p}}}}{{\lambda_{{r}} - \lambda_{{p}}}}\right)\right]"
                rf" \Rightarrow \frac{{1}}{{{self.y_um}}} * \left[{mpl_flm.magnitude:.{self.casa_decimal_momento}f} - "
                rf"\left({mpl_flm.magnitude:.{self.casa_decimal_momento}f} - {mr_flm.magnitude:.{self.casa_decimal_momento}f}\right) * "
                rf"\left(\frac{{{lambda_flm.magnitude:.2f} - {lambda_flm_p.magnitude:.2f}}}{{{lambda_flm_r.magnitude:.2f} - {lambda_flm_p.magnitude:.2f}}}\right)\right] = "
                rf"{mrd_flm:.{self.casa_decimal_momento}f}"
            )
        elif lambda_flm > lambda_flm_r:
            mcr_flm = (0.69 * self.e) / (lambda_flm ** 2) * (self.i_x_text / (self.d_text / 2))  # wc  = wx = ix/(d/2)
            mrd_flm = mcr_flm / self.y_um
            status_lambda_flm = r"\lambda_{flm} \ge \lambda_{r} "
            status_mcr_flm = (
                rf"M_{{cr}} = \frac{{0.69 * E}}{{\lambda_{{f}}^2}} * \frac{{I_x}}{{d/2}}"
                rf" \Rightarrow \frac{{0.69 * {self.e.magnitude:.{self.casa_decimal_pressao}f}}}{{{lambda_flm.magnitude:.2f}^2}} * "
                rf"\frac{{{self.i_x_text.magnitude:.{self.casa_decimal_inercia}f}}}{{{self.d_text.magnitude:.{self.casa_decimal_comprimento}f}/2}} = "
                rf"{mcr_flm:.{self.casa_decimal_momento}f}"
            )
            lambda_flm_text = (
                rf"M_{{rd}} = \frac{{M_{{cr}}}}{{\gamma_1}} \Rightarrow \frac{{{mcr_flm.magnitude:.{self.casa_decimal_momento}f}}}{{{self.y_um}}} = "
                rf"{mrd_flm:.{self.casa_decimal_momento}f}"
            )
        # flambagem local da alma
        # *********************************************************************************************
        lambda_fla = self.d_l_text / self.tw_text
        lambda_fla_p = 3.76 * np.sqrt(self.e / self.fy)
        lambda_fla_r = 5.7 * np.sqrt(self.e / self.fy)
        mpl_fla = self.z_x_text * self.fy
        mr_fla = self.fy * self.w_x_text

        status_lambda_fla, status_mcr_fla, lambda_fla_text = "", "", ""
        if lambda_fla <= lambda_fla_p:
            mrd_fla = mpl_fla / self.y_um
            status_lambda_fla = r"\lambda \le \lambda_{fla} "
            lambda_fla_text = r"M_{rd} = \frac{M_{pl}}{\gamma_1} \Rightarrow \frac{" + f"{mpl_fla.magnitude:.{self.casa_decimal_momento}f}" + r"}{" + f"{self.y_um}" + r"} = " + f"{mrd_fla:.{self.casa_decimal_momento}f}"
        elif lambda_fla_p < lambda_fla <= lambda_fla_r:
            mrd_fla = (1 / self.y_um) * (
                    mpl_fla - ((mpl_fla - mr_fla) * ((lambda_fla - lambda_fla_p) / (lambda_fla_r - lambda_fla_p))))
            status_lambda_fla = r"\lambda_{p} \le \lambda_{flm} \le \lambda_{r} "
            lambda_fla_text = (
                rf"M_{{rd}} = \frac{{1}}{{\gamma_1}} * \left[M_{{pl}} - \left(M_{{pl}} - M_{{r}}\right)"
                rf" * \left(\frac{{\lambda_{{la}} - \lambda_{{p}}}}{{\lambda_{{r}} - \lambda_{{p}}}}\right)\right]"
                rf" \Rightarrow \frac{{1}}{{{self.y_um}}} * \left[{mpl_fla.magnitude:.{self.casa_decimal_momento}f} - "
                rf"\left({mpl_fla.magnitude:.{self.casa_decimal_momento}f} - {mr_fla.magnitude:.{self.casa_decimal_momento}f}\right) * "
                rf"\left(\frac{{{lambda_fla.magnitude:.2f} - {lambda_fla_p.magnitude:.2f}}}{{{lambda_fla_r.magnitude:.2f} - {lambda_fla_p.magnitude:.2f}}}\right)\right] = "
                rf"{mrd_fla:.{self.casa_decimal_momento}f}"
            )
        elif lambda_fla > lambda_fla_r:
            status_lambda_fla = r" \textcolor{red}{Viga de alma esbelta - verificar Anexo E}"
            mrd_fla = False  # vai dar erro quando tentar achar o minimo usando numpy, logo retorna Falso

        mfrc = 1.5 * self.w_x_text * self.fy / self.y_um
        mrd_min = min([mrd_flt, mrd_flm, mrd_fla, mfrc])


        passou = self.mfx <= mrd_min  # verificando
        status_texto = r" \textcolor{ForestGreen}{Aprovado}" if passou else r"\textcolor{red}{Reprovado}"

        # memoria de calculo
        # *********************************************************************************************
        memoria_calculo_moment_x = {
            "titulo_da_secao": "Verificação do momento em relalção ao eixo X do perfil",
            "corpo": [
                {"tipo": "paragrafo", "conteudo": "Flambagem local com torção: \n "},
                ################################################################################################ FLT
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"\lambda_{LT} = \frac{L_b}{r_y} \Rightarrow \frac{" + f"{self.flb:.{self.casa_decimal_comprimento}f}" + r"}{" +
                            f"{self.r_y_text:.{self.casa_decimal_comprimento}f}" + r"} = " + f"{lambda_flt:.2f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"\lambda_{p} = 1.76 * \sqrt{\frac{E}{f_y}} \Rightarrow 1.76 * \sqrt{\frac{" +
                            f"{self.e.magnitude:.{self.casa_decimal_pressao}f}" + r"}{" +
                            f"{self.fy.magnitude:.{self.casa_decimal_pressao}f}" + r"}} = " +
                            f"{lambda_flt_p:.2f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"\beta = \frac{(f_y - 0.3 * f_y) * W_x}{E * I_t} \Rightarrow \frac{(" +
                            f"{self.fy.magnitude:.{self.casa_decimal_pressao}f} - 0.3 * {self.fy.magnitude:.{self.casa_decimal_pressao}f}) * " +
                            f"{self.w_x_text.magnitude:.{self.casa_decimal_volume}f}" + r"}{" +
                            f"{self.e.magnitude:.{self.casa_decimal_pressao}f} * {self.i_t_text.magnitude:.{self.casa_decimal_momento}f}" + r"} = " +
                            f"{beta:.2f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"\lambda_{r} = 1.38 * C_b * \sqrt{\frac{I_y * I_t}{r_y * I_t * \beta}}"
                            r" * \sqrt{1 + \sqrt{1 + \frac{27 * C_w * \beta^2}{C_b^2 * I_y}}}"
                            r" \Rightarrow " +
                            f"{lambda_flt_r:.2f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"M_{rd} = (f_y - 0.3 * f_y) * W_x \Rightarrow (" +
                            f"{self.fy.magnitude:.{self.casa_decimal_pressao}f} - 0.3 * {self.fy.magnitude:.{self.casa_decimal_pressao}f}) * " +
                            f"{self.w_x_text.magnitude:.{self.casa_decimal_volume}f} = {mr_flt:.{self.casa_decimal_momento}f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"M_{pl} = Z_x * f_y \Rightarrow " +
                            f"{self.z_x_text.magnitude:.{self.casa_decimal_volume}f} * {self.fy.magnitude:.{self.casa_decimal_pressao}f} = " +
                            f"{mpl_flt:.{self.casa_decimal_momento}f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n  Verificando a condição: \n "},
                {
                    "tipo": "formula",
                    "conteudo": status_lambda_flt
                },
                {"tipo": "paragrafo", "conteudo": "\n Momento fletor resistente  de cálculo do elemento \n "},
                {
                    "tipo": "formula",
                    "conteudo": lambda_flt_text
                },
                {"tipo": "paragrafo", "conteudo": " \n"},
                {
                    "tipo": "formula",
                    "conteudo": status_mcr_flt + " "
                },
                ################################################################################################ FLM
                {"tipo": "paragrafo", "conteudo": "\n  Flambagem local da mesa comprida: \n "},
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"\lambda = \frac{{b_f/2}}{{t_f}} \Rightarrow \frac{{{self.bf_text.magnitude:.{self.casa_decimal_comprimento}f}/2}}{{{self.tf_text.magnitude:.{self.casa_decimal_comprimento}f}}} = "
                        rf"{lambda_flm:.{self.casa_decimal_momento}f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"\lambda_p = 0.38 * \sqrt{{\frac{{E}}{{f_y}}}} \Rightarrow 0.38 * \sqrt{{\frac{{{self.e.magnitude:.{self.casa_decimal_pressao}f}}}{{{self.fy.magnitude:.{self.casa_decimal_pressao}f}}}}} = "
                        rf"{lambda_flm_p:.{self.casa_decimal_momento}f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"\lambda_r = 0.83 * \sqrt{{\frac{{E}}{{f_y - 0.3 f_y}}}} \Rightarrow 0.83 * \sqrt{{\frac{{{self.e.magnitude:.{self.casa_decimal_pressao}f}}}{{{self.fy.magnitude:.{self.casa_decimal_pressao}f} - 0.3 * {self.fy.magnitude:.{self.casa_decimal_pressao}f}}}}} = "
                        rf"{lambda_flm_r:.{self.casa_decimal_momento}f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"M_r = (f_y - 0.3 * f_y) * W_x \Rightarrow ({self.fy.magnitude:.{self.casa_decimal_pressao}f} - 0.3 * {self.fy.magnitude:.{self.casa_decimal_pressao}f}) * "
                        rf"{self.w_x_text.magnitude:.{self.casa_decimal_volume}f} = {mr_flm:.{self.casa_decimal_momento}f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"M_{{pl}} = Z_x * f_y \Rightarrow {self.z_x_text.magnitude:.{self.casa_decimal_momento}f} * {self.fy.magnitude:.{self.casa_decimal_pressao}f} = "
                        rf"{mpl_flm:.{self.casa_decimal_momento}f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n  Verificando a condição: \n "},
                {
                    "tipo": "formula",
                    "conteudo": status_lambda_flm
                },
                {"tipo": "paragrafo", "conteudo": "\n Momento fletor resistente  de cálculo do elemento \n "},
                {
                    "tipo": "formula",
                    "conteudo": lambda_flm_text
                },
                {"tipo": "paragrafo", "conteudo": " \n"},
                {
                    "tipo": "formula",
                    "conteudo": status_mcr_flm + " "
                },
                ################################################################################################ FLA
                {"tipo": "paragrafo", "conteudo": "Flambagem local da Alma: \n "},
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"\lambda_w = \frac{{d}}{{t_w}} \Rightarrow \frac{{{self.d_l_text.magnitude:.{self.casa_decimal_comprimento}f}}}{{{self.tw_text.magnitude:.{self.casa_decimal_comprimento}f}}} = "
                        rf"{lambda_fla:.{self.casa_decimal_momento}f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"\lambda_p = 3.76 * \sqrt{{\frac{{E}}{{f_y}}}} \Rightarrow 3.76 * \sqrt{{\frac{{{self.e.magnitude:.{self.casa_decimal_pressao}f}}}{{{self.fy.magnitude:.{self.casa_decimal_pressao}f}}}}} = "
                        rf"{lambda_fla_p:.{self.casa_decimal_momento}f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"\lambda_r = 5.7 * \sqrt{{\frac{{E}}{{f_y}}}} \Rightarrow 5.7 * \sqrt{{\frac{{{self.e.magnitude:.{self.casa_decimal_pressao}f}}}{{{self.fy.magnitude:.{self.casa_decimal_pressao}f}}}}} = "
                        rf"{lambda_fla_r:.{self.casa_decimal_momento}f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"M_{{pl}} = Z_x * f_y \Rightarrow {self.z_x_text.magnitude:.{self.casa_decimal_momento}f} * {self.fy.magnitude:.{self.casa_decimal_pressao}f} = "
                        rf"{mpl_fla:.{self.casa_decimal_momento}f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"M_r = W_x * f_y \Rightarrow {self.w_x_text.magnitude:.{self.casa_decimal_momento}f} * {self.fy.magnitude:.{self.casa_decimal_pressao}f} = "
                        rf"{mr_fla:.{self.casa_decimal_momento}f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Verificando a condição: \n "},
                {
                    "tipo": "formula",
                    "conteudo": status_lambda_fla
                },
                {"tipo": "paragrafo", "conteudo": "\n Momento fletor resistente  de cálculo do elemento \n "},
                {
                    "tipo": "formula",
                    "conteudo": lambda_fla_text
                },
                {"tipo": "paragrafo", "conteudo": "\n"},
                {
                    "tipo": "formula",
                    "conteudo": status_mcr_fla + " "
                },
                {"tipo": "paragrafo", "conteudo": " Verificando \n"},
                {
                    "tipo": "formula",
                    "conteudo": rf"M_{{rd,calc}} = \frac{{1.5 * W_x * f_y}}{{\gamma_1}} \Rightarrow "
                                rf"\frac{{1.5 * {self.w_x_text.magnitude:.{self.casa_decimal_momento}f} * {self.fy.magnitude:.{self.casa_decimal_pressao}f}}}{{{self.y_um}}} = "
                                rf"{mfrc.magnitude:.{self.casa_decimal_momento}f}"
                },
                {
                    "tipo": "formula",
                    "conteudo": rf"M_{{rd}} = \min \left( M_{{rd,flt}},\ M_{{rd,flm}},\ M_{{rd,fla}},\ M_{{frc}} \right) \Rightarrow "
                                rf"\min \left( {mrd_flt.magnitude:.{self.casa_decimal_momento}f},\ "
                                rf"{mrd_flm.magnitude:.{self.casa_decimal_momento}f},\ "
                                rf"{mrd_fla.magnitude:.{self.casa_decimal_momento}f},\ "
                                rf"{mfrc.magnitude:.{self.casa_decimal_momento}f} \right) = "
                                rf"{mrd_min:.{self.casa_decimal_momento}f}"
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"M_{sdx} \le  M_{rdx} \Rightarrow " + f"{self.mfx:.{self.casa_decimal_momento}f}" + r"\le" + f"{mrd_min:.{self.casa_decimal_momento}f}"
                            + r"\quad" + status_texto)
                }
            ]
        }

        utilization_m_x = self.mfx / mrd_min
        if passou:
            return True, memoria_calculo_moment_x, utilization_m_x
        else:
            return False, memoria_calculo_moment_x, utilization_m_x

    def moment_force_y(self):
        mrd_flt, mrd_flm, mrd_fla = 0, 0, 0  #inicializando para nao dar problema
        #flambagem lateral com torcao
        #*********************************************************************************************
        #nao se aplica segundo a norma para momento no menor eixo de inercia
        #verificar o item novamente para ver!
        # flambagem local da mesa comprimida
        # *********************************************************************************************
        lambda_flm = self.bf_text / (2 * self.tf_text)
        lambda_flm_p = 0.38 * np.sqrt(self.e / self.fy)
        lambda_flm_r = 0.83 * np.sqrt(self.e / (self.fy - 0.3 * self.fy))
        mr_flm = (self.fy - 0.3 * self.fy) * self.w_y_text
        mpl_flm = self.z_y_text * self.fy

        status_lambda_flm, status_mcr_flm, lambda_flm_text = "", "", ""
        if lambda_flm <= lambda_flm_p:
            mrd_flm = mpl_flm / self.y_um
            status_lambda_flm = r"\lambda_{flm} \le \lambda_{p} "
            lambda_flm_text = (
                    r"M_{rd} = \frac{M_{pl}}{\gamma_1} \Rightarrow \frac{" + f"{mpl_flm.magnitude:.{self.casa_decimal_momento}f}" + r"}{" + f"{self.y_um}" + r"} = "
                    + f"{mrd_flm:.{self.casa_decimal_momento}f}")
        elif lambda_flm_p < lambda_flm <= lambda_flm_r:
            mrd_flm = (1 / self.y_um) * (
                    mpl_flm - ((mpl_flm - mr_flm) * ((lambda_flm - lambda_flm_p) / (lambda_flm_r - lambda_flm_p))))
            status_lambda_flm = r"\lambda_{p} \le \lambda_{flm} \le \lambda_{r} "
            lambda_flm_text = (
                rf"M_{{rd,\lambda_{{flm}}}} = \frac{{1}}{{\gamma_1}} * \left[M_{{pl}} - \left(M_{{pl}} - M_r\right)"
                rf" * \left(\frac{{\lambda_{{flm}} - \lambda_p}}{{\lambda_r - \lambda_p}}\right)\right] \Rightarrow "
                rf"\frac{{1}}{{{self.y_um}}} * \left[{mpl_flm.magnitude:.{self.casa_decimal_momento}f} - \left({mpl_flm.magnitude:.{self.casa_decimal_momento}f} - {mr_flm.magnitude:.{self.casa_decimal_momento}f}\right)"
                rf" * \left(\frac{{{lambda_flm.magnitude:.2f} - {lambda_flm_p.magnitude:.2f}}}{{{lambda_flm_r.magnitude:.2f} - {lambda_flm_p.magnitude:.2f}}}\right)\right] = "
                rf"{mrd_flm:.{self.casa_decimal_momento}f}"
            )
        elif lambda_flm > lambda_flm_r:
            #verificar se fica ix ou iy
            mcr_flm = (0.69 * self.e) / (lambda_flm ** 2) * self.w_y_text
            mrd_flm = mcr_flm / self.y_um
            status_lambda_flm = r"\lambda_{flm} \ge \lambda_{r} "
            status_mcr_flm = (
                rf"M_{{cr,\lambda_{{flm}}}} = \frac{{0.69 * E}}{{\lambda^2}} * W_y \Rightarrow "
                rf"\frac{{0.69 * {self.e.magnitude:.{self.casa_decimal_pressao}f}}}{{{lambda_flm.magnitude:.2f}^2}} * "
                rf"{self.w_y_text.magnitude:.{self.casa_decimal_momento}f} = {mcr_flm:.{self.casa_decimal_momento}f}"
            )
            lambda_flm_text = (
                rf"M_{{rd,\lambda_{{flm}}}} = \frac{{M_{{cr}}}}{{\gamma_1}} \Rightarrow \frac{{{mcr_flm.magnitude:.{self.casa_decimal_momento}f}}}{{{self.y_um}}} = "
                rf"{mrd_flm:.{self.casa_decimal_momento}f}"
            )
        mrd_calc = 1.5 * self.w_y_text * self.fy / self.y_um
        mrd_min = min([mrd_calc, mrd_flm])

        passou = self.mfy <= mrd_min  # verificando
        status_texto = r" \textcolor{ForestGreen}{Aprovado}" if passou else r"\textcolor{red}{Reprovado}"

        memoria_calculo_moment_y = {
            "titulo_da_secao": "Verificação do momento em relalção ao eixo Y do perfil",
            "corpo": [

                {"tipo": "paragrafo", "conteudo": "Flambagem local da mesa comprida: \n "},
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"\lambda = \frac{{b_f}} {{2 t_f}} \Rightarrow \frac{{{self.bf_text.magnitude:.{self.casa_decimal_comprimento}f}}}{{2 * {self.tf_text.magnitude:.{self.casa_decimal_comprimento}f}}} = "
                        rf"{lambda_flm:.2f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"\lambda_p = 0.38 * \sqrt{{\frac{{E}}{{f_y}}}} \Rightarrow 0.38 * \sqrt{{\frac{{{self.e.magnitude:.{self.casa_decimal_pressao}f}}}{{{self.fy.magnitude:.{self.casa_decimal_pressao}f}}}}} = "
                        rf"{lambda_flm_p:.2f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"\lambda_r = 0.83 * \sqrt{{\frac{{E}}{{f_y - 0.3 f_y}}}} \Rightarrow 0.83 * \sqrt{{\frac{{{self.e.magnitude:.{self.casa_decimal_pressao}f}}}{{{(self.fy.magnitude - 0.3 * self.fy.magnitude):.{self.casa_decimal_pressao}f}}}}} = "
                        rf"{lambda_flm_r:.2f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"M_r = (f_y - 0.3 f_y) * W_y \Rightarrow ({self.fy.magnitude:.{self.casa_decimal_pressao}f} - 0.3 * {self.fy.magnitude:.{self.casa_decimal_pressao}f})"
                        rf" * {self.w_y_text.magnitude:.{self.casa_decimal_momento}f} = {mr_flm:.{self.casa_decimal_momento}f}"
                    )
                },
                {
                    "tipo": "formula",
                    "conteudo": (
                        rf"M_{{pl}} = Z_y * f_y \Rightarrow {self.z_y_text.magnitude:.{self.casa_decimal_momento}f} * {self.fy.magnitude:.{self.casa_decimal_pressao}f} = {mpl_flm:.{self.casa_decimal_momento}f}"
                    )
                },
                ################################################################################################ FLM
                {"tipo": "paragrafo", "conteudo": "\n  Verificando a condição: \n "},
                {
                    "tipo": "formula",
                    "conteudo": status_lambda_flm
                },
                {"tipo": "paragrafo", "conteudo": "\n Momento fletor resistente  de cálculo do elemento \n "},
                {
                    "tipo": "formula",
                    "conteudo": lambda_flm_text
                },
                {"tipo": "paragrafo", "conteudo": " \n"},
                {
                    "tipo": "formula",
                    "conteudo": status_mcr_flm + " "
                },

                {"tipo": "paragrafo", "conteudo": " Verificando \n"},
                {
                    "tipo": "formula",
                    "conteudo": rf"M_{{rd,calc}} = \frac{{1.5 * W_y * f_y}}{{\gamma_1}} \Rightarrow "
                                rf"\frac{{1.5 * {self.w_y_text.magnitude:.{self.casa_decimal_momento}f} * {self.fy.magnitude:.{self.casa_decimal_pressao}f}}}{{{self.y_um}}} = "
                                rf"{mrd_calc.magnitude:.{self.casa_decimal_momento}f}"
                },
                {
                    "tipo": "formula",
                    "conteudo": rf"M_{{rd}} = \min \left( M_{{rd,calc}},\ M_{{rd,flm}} \right) \Rightarrow \min \left( "
                                rf"{mrd_calc.magnitude:.{self.casa_decimal_momento}f},\ {mrd_flm.magnitude:.{self.casa_decimal_momento}f} \right) = "
                                rf"{mrd_min:.{self.casa_decimal_momento}f}"
                },
                {"tipo": "paragrafo", "conteudo": "\n "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"M_{sdx} \le  M_{rdy} \Rightarrow " + f"{self.mfy:.{self.casa_decimal_momento}f}" + r"\le" + f"{mrd_min:.{self.casa_decimal_momento}f}"
                            + r"\quad" + status_texto)
                }
            ]
        }

        utilization_m_x = y = self.mfy / mrd_min
        if passou:
            return True, memoria_calculo_moment_y, utilization_m_x
        else:
            return False, memoria_calculo_moment_y, utilization_m_x

    def combined_forces(self):
        #fazer a verificao aqui! ver na norma
        nrdt = self.normal_traction()
        nrdc = self.normal_compression()
        vrd_x = self.shear_force_x()
        vrd_y = self.shear_force_y()
        mrdx = self.moment_force_x()
        mrdy = self.moment_force_y()
        utilization = [nrdt[2], nrdc[2]]
        result_list = []
        memoria_calculo_forcas_combinadas = {
            "titulo_da_secao": "Verificação dos esforços combinados: ",
            "corpo": [
                {"tipo": "paragrafo", "conteudo": "Verificando as codições:\n "},
            ]
        }
        for value in utilization:
            if value >= 0.2:
                last_verif = value + (8 / 9) * (mrdx[2] + mrdy[2])
                trecho_memorioa = {
                    "tipo": "formula",
                    "conteudo": (
                            r" \frac{N_{sd}}{N_{rd}} \ge 0.2 \Rightarrow \frac{N_{sdt}}{N_{rdt}}+\frac{8}{9}({\frac{M_{sdx}}{M_{rdx}}+\frac{M_{sdy}}{M_{rdy}}})  \Rightarrow " +
                            rf"{value.magnitude:.5f} + \frac{{8}}{{9}} * \left({mrdx[2].magnitude:.5f} + {mrdy[2].magnitude:.5f}\right) = "
                            rf"{last_verif.magnitude:.2f}"
                    )
                }
                memoria_calculo_forcas_combinadas["corpo"].append(trecho_memorioa)
            else:
                last_verif = value * 0.5 + (mrdx[2] + mrdy[2])
                trecho_memorioa = {
                    "tipo": "formula",
                    "conteudo": (
                            r"\frac{N_{sd}}{N_{rd}} \le 0.2 \Rightarrow \frac{N_{sd}}{N_{rd}*2}+{\frac{M_{sdx}}{M_{rdx}}+\frac{M_{sdy}}{M_{rdy}}}  \Rightarrow " +
                            rf"{value.magnitude:.5f} + \frac{{1}}{{2}} + \left({mrdx[2].magnitude:.5f} + {mrdy[2].magnitude:.5f}\right) = "
                            rf"{last_verif.magnitude:.5f}"
                    )
                }
                memoria_calculo_forcas_combinadas["corpo"].append(trecho_memorioa)

            passou = last_verif <= 1
            status_texto = r" \textcolor{ForestGreen}{Aprovado}" if passou else r"\textcolor{red}{Reprovado}"
            texto_conferencia = {
                "tipo": "formula",
                "conteudo": (
                        r"Status : " + status_texto)
            }
            memoria_calculo_forcas_combinadas["corpo"].append(texto_conferencia)
            result_list.append(passou)
        return all(result_list), memoria_calculo_forcas_combinadas

    def calculate(self):


        nrdt = self.normal_traction()
        nrdc = self.normal_compression()
        vrdx = self.shear_force_x()
        vrdy = self.shear_force_y()
        mrdx = self.moment_force_x()
        mrdy = self.moment_force_y()
        ec = self.combined_forces()
        try:
            meu_relatorio = ReportGenerator(self.frame_name, self.save_path)
            meu_relatorio.make_title() #gera o titulo
            meu_relatorio.add_calculo(nrdt[1])
            meu_relatorio.add_calculo(nrdc[1])
            meu_relatorio.add_calculo(vrdx[1])
            meu_relatorio.add_calculo(vrdy[1])
            meu_relatorio.add_calculo(mrdx[1])
            meu_relatorio.add_calculo(mrdy[1])
            meu_relatorio.add_calculo(ec[1])
            meu_relatorio.gerar_pdf()
            wx.MessageBox("Calculado com sucesso!", "Sucesso",wx.OK | wx.ICON_INFORMATION )
            # print(ec[0])
            return ec[0]
            # return True
        except Exception as error:
            wx.MessageBox(f"{error}", "Erro",wx.OK | wx.ICON_ERROR)
            return False
            # return ec[0]

    def calculate_all(self):
        ec = self.combined_forces()
        return ec[0]



# print(f"self.linear_mass_text {self.linear_mass_text}, self.d_text {self.d_text}, self.bf_text {self.bf_text},self.tw_text {self.tw_text}, self.tf_text {self.tf_text} "
#       f" self.h_text {self.h_text}, self.d_l_text {self.d_l_text}, self.d_l_text {self.d_l_text}, self.d_l_text {self.d_l_text}, self.d_l_text {self.d_l_text}"
#       f" self.area_text {self.area_text}, self.i_x_text {self.i_x_text}, self.i_x_text {self.i_x_text}, self.w_x_text {self.w_x_text}, self.r_x_text {self.r_x_text}"
#       f" self.z_x_text {self.z_x_text}, self.i_y_text {self.i_y_text}, self.w_y_text {self.w_y_text}, self.r_y_text {self.r_y_text}, self.z_y_text {self.z_y_text}"
#       f" self.r_t_text {self.r_t_text}, self.i_t_text {self.i_t_text}, self.bf_two_text {self.bf_two_text}, self.d_tw_text {self.d_tw_text}, self.cw_text {self.cw_text}"
#       f" self.u_text {self.u_text}, self.fy {self.fy}, self.fu {self.fu}, self.lfx {self.lfx}, self.lfy {self.lfy}, self.lfz {self.lfz}, self.flb {self.flb}"
#       f" self.fn {self.fn}, self.fcx {self.fcx}, self.fcy {self.fcy}, self.mfx {self.mfx}, self.mfy {self.mfy}, self.y_um {self.y_um}, self.y_dois {self.y_dois},"
#       f"self.e {self.e}, self.g {self.g}, self.cb {self.cb}")
