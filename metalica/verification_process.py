import wx
import numpy as np
from metalica.report_generate import ReportGenerator


class VerificationProcess:
    def __init__(self, linear_mass_text, d_text, bf_text, tw_text, tf_text, h_text, d_l_text, area_text, i_x_text, w_x_text, r_x_text,
                 z_x_text, i_y_text, w_y_text, r_y_text, z_y_text, r_t_text, i_t_text, bf_two_text, d_tw_text, cw_text, u_text, fy, fu, lfx, lfy, lfz,
                 flb, fnt, fnc,  fcx,fcy, mfx, mfy, y_um, y_dois, g, e, cb):
        self.report_logs = []
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
        self.y_dois = y_dois
        self.e = e
        self.g = g
        self.cb = cb
        #precisao colocar em cfg

        self.casa_decimal_comprimento = 2
        self.casa_decimal_area = 2
        self.casa_decimal_volume = 2
        self.casa_decimal_inercia = 2
        self.casa_decimal_six = 2
        self.casa_decimal_forca = 2
        self.casa_decimal_momento = 2
        self.casa_decimal_pressao = 2


# para perfis laminados

    area_precision = 10
    def normal_traction(self):
        ntrd = self.area_text*self.fy/self.y_um
        ntsd = self.fnt
        passou = ntsd <= ntrd #verificando
        status_texto =  r" \textcolor{ForestGreen}{Aprovado}" if passou else r"\textcolor{red}{Reprovado}"
        ############################################memoria
        memoria_calculo_nomal = {
            "titulo_da_secao": "Verificação a força normal de tração ",
            "corpo": [
                {"tipo": "paragrafo","conteudo": "ELU para escoamento da seção bruta: \n"},
                {
                    "tipo": "formula","conteudo": (
                            r"N_{trd} = \frac{A_g * f_y}{\gamma_{a1}} \Rightarrow \frac{"
                            + f"{self.area_text:.{self.casa_decimal_area}f} * " + f"{self.fy:.{self.casa_decimal_pressao}f}"+ r"}{"+
                            f"{self.y_um:.{self.casa_decimal_pressao}f}" + r"} = "+ f"{ntrd:.{self.casa_decimal_forca}f}"
                )},
                {"tipo": "paragrafo", "conteudo": "\n Verificando: "},
                {
                    "tipo": "formula",
                    "conteudo": (r"N_{tsd} \le  N_{trd} \Rightarrow " + f"{ntsd:.{self.casa_decimal_forca}f}" +r"\le" +f"{ntrd:.{self.casa_decimal_forca}f}"
                            + r"\quad " + status_texto)
                }
            ]
        }
        if passou:
            return False, memoria_calculo_nomal #nao passa
        else:
            return True, memoria_calculo_nomal #passa


    def normal_compression(self):
        # compressao
        # indice de esbeltez da secao recomendado < 200
        ind_esblt_x = self.lfx / self.r_x_text
        ind_esblt_y = self.lfy / self.r_y_text
        # flambagem por flexao em x
        n_e_x = (np.pi ** 2) * self.e * self.i_x_text / (self.lfx ** 2)
        n_e_y = (np.pi ** 2) * self.e * self.i_y_text / (self.lfy ** 2)
        r_o = np.sqrt(self.r_x_text ** 2 + self.r_y_text ** 2 + 0 + 0)  # considerando o perfil como simetrico
        print(f"nex = {n_e_x}")
        print(f"ney = {n_e_y}")
        n_e_z = (1 / (r_o ** 2)) * (((np.pi ** 2) * self.e * self.cw_text / (
                    self.lfz ** 2)) + self.g * self.i_t_text)  # J = it na tabela
        print(f"nez = {n_e_z}")

        n_e = np.min([n_e_x, n_e_y, n_e_z])
        # lambda0 5.3.3.2
        lbd_zero = np.sqrt(self.area_text * self.fy / n_e)
        # fator de reducao 5.3.3.1
        if lbd_zero <= 1.5:
            psi = 0.658 ** (lbd_zero ** 2)
        else:
            psi = 0.877 / (lbd_zero ** 2)
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
        passou = self.fnc <= nrdc # verificando
        status_texto = r" \textcolor{ForestGreen}{Aprovado}" if passou else r"\textcolor{red}{Reprovado}"

        memoria_calculo_normal_c = {
            "titulo_da_secao": "Verificação da força normal de Compressão",
            "corpo": [
                {"tipo": "paragrafo", "conteudo": "Índice de esbeltez da barra comprimida: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"\lambda_x = \frac{L_x}{r_x} \Rightarrow = \frac{" + f"{self.lfx:.{self.casa_decimal_comprimento}f}" + r"}{" + f"{self.r_x_text:.{self.casa_decimal_comprimento}f}" + r"} = " + f"{ind_esblt_x:.2f}"
                            + r", \quad \lambda_y = \frac{L_y}{r_y} \Rightarrow \lambda_y = \frac{" + f"{self.lfy:.{self.casa_decimal_comprimento}f}" + r"}{" + f"{self.r_y_text:.{self.casa_decimal_comprimento}f}" + r"} = " + f"{ind_esblt_y:.2f} \n"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Flambagem por flexão em relação ao eixo x da seção transversal: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"N_{ex} = \frac{\pi^2 * E * I_x}{L_x^2} \Rightarrow \frac{\pi^2 * " + f"{self.e:.{self.casa_decimal_pressao}f}" + r" * " + f"{self.i_x_text:.{self.casa_decimal_inercia}f}" + r"}{" + f"{self.lfx:.{self.casa_decimal_comprimento}f}" + r"^2} = " + f"{n_e_x:.{self.casa_decimal_forca}f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Flambagem por flexão em relação ao eixo y da seção transversal: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"N_{ey} = \frac{\pi^2 * E * I_y}{L_y^2} \Rightarrow \frac{\pi^2 * " + f"{self.e:.{self.casa_decimal_pressao}f}" + r" * " + f"{self.i_y_text:.{self.casa_decimal_inercia}f}" + r"}{" + f"{self.lfy:.{self.casa_decimal_comprimento}f}" + r"^2} = " + f"{n_e_y:.{self.casa_decimal_forca}f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Raio de giração polar da seção bruta: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"R_0 = \sqrt{r_x^2 + r_y^2 + x_0^2 + y_0^2} \Rightarrow \sqrt{" + f"{self.r_x_text}" + r"^2 + " + f"{self.r_y_text}" + r"^2 + 0^2 + 0^2} = " + f"{r_o:.{self.casa_decimal_comprimento}f}" + f" \n"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n Flambagem por torção em relação ao eixo longitudinal z: \n"},
                {
                    "tipo": "formula",
                    "conteudo": (
                           f"\n" + r"N_{ez} = \frac{1}{r_0} \left( \frac{\pi * E * C_w}{L_z^2} + G * J \right) \Rightarrow \frac{1}{" + f"{r_o:.{self.casa_decimal_comprimento}f}" + r"} \left( \frac{\pi * " + f"{self.e:.{self.casa_decimal_pressao}f}" + r" * " + f"{self.cw_text:.{self.casa_decimal_six}f}" + r"}{" + f"{self.lfz:.{self.casa_decimal_comprimento}f}" + r"^2} + " + f"{self.g:.{self.casa_decimal_pressao}f}" + r" + " + f"{self.i_t_text:.{self.casa_decimal_inercia}f}" + r" \right) = " + f"{n_e_z:.{self.casa_decimal_forca}f}"
                    )
                },
                {"tipo": "paragrafo", "conteudo": "\n"}, #quebra linha
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
                            r"\lambda_0 = \sqrt{\frac{A_g * f_y}{N_e}} \Rightarrow \sqrt{\frac{" + f"{self.area_text:.{self.casa_decimal_area}f}" + r" * " + f"{self.fy:.{self.casa_decimal_pressao}f}" + r"}{" + f"{n_e:.{self.casa_decimal_forca}f}" + r"}} = " + f"{lbd_zero:.2f}"
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
                            r"\n A_{ef} =" + f"{area_efetiva:.{self.casa_decimal_area}f} \n")
                },
                {"tipo": "paragrafo", "conteudo": "\n Força axial de compressão resistente de cálculo: \n "},
                {
                    "tipo": "formula",
                    "conteudo": (
                            r"N_{crd} = \frac{\chi * A_{ef} * f_y}{\gamma_1} \Rightarrow \frac{" + f"{psi:.3f}" + r" * " + f"{area_efetiva:.{self.casa_decimal_area}f}" + r" * " + f"{self.fy:.{self.casa_decimal_pressao}f}" + r"}{" + f"{self.y_um}" + r"} = " + f"{nrdc:.{self.casa_decimal_pressao}f}")
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

        if passou:
            # elemento passa
            return True, memoria_calculo_normal_c
        else:
            # elemento nao passa
            return False, memoria_calculo_normal_c

    def shear_force_x(self):
        #sf = shear force
        vrd = 0
        lambda_sf = self.h_text/self.tw_text
        lambda_p = 1.1*np.sqrt(5.34*self.e/self.fy)
        lambda_r = 1.37*np.sqrt(5.34*self.e/self.fy)
        aw = 2*self.bf_text*self.tf_text
        vpl = 0.6*aw*self.fy

        status_lambda, lambda_texto = 0, 0
        if lambda_sf <= lambda_p:
            vrd = vpl/self.y_um
            status_lambda = r"\lambda \le \lambda_{p} "
            lambda_texto = r"V_{rd} = \frac{V_{pl}}{\gamma_1} \Rightarrow \frac{" + f"{vpl:.{self.casa_decimal_forca}f}" + r"}{" + f"{self.y_um}" + r"} = " + f"{vrd:.{self.casa_decimal_forca}f}"

        elif lambda_p < lambda_sf <= lambda_r:
            vrd = (lambda_p/lambda_sf)*(vpl/self.y_um)
            status_lambda = r"\lambda_{p} \le \lambda_{} \le \lambda_{r}  "
            lambda_texto = r"V_{rd} = \frac{\lambda_{p} \cdot V_{pl}}{\lambda \cdot \gamma_1} \Rightarrow " + r"\frac{" + f"{lambda_p:.2f} \cdot {vpl:.{self.casa_decimal_forca}f}" + r"}{" + f"{lambda_sf:.2f} \cdot {self.y_um}" + r"} = " + f"{vrd:.{self.casa_decimal_forca}f}"

        elif lambda_sf >= lambda_r:
            vrd = 1.24*((lambda_p/lambda_sf)**2)*(vpl/self.y_um)
            status_lambda = r"\lambda_{} \ge \lambda_{r} "
            lambda_texto = r"V_{rd} = 1{,}24 \cdot \left( \frac{\lambda_{p}}{\lambda} \right)^2 \cdot \frac{V_{pl}}{\gamma_1} \Rightarrow " + f"1.24 \\cdot \\left( \\frac{{{lambda_p}}}{{{lambda_sf}}} \\right)^2 \\cdot " + f"\\frac{{{vpl:.{self.casa_decimal_forca}f}}}{{{self.y_um}}} = {vrd:.{self.casa_decimal_forca}f}"

        passou = self.fcx <= vrd  # verificando
        status_texto = r" \textcolor{ForestGreen}{Aprovado}" if passou else r"\textcolor{red}{Reprovado}"

        memoria_calculo_shear_x = {
            "titulo_da_secao": "Verificação da cortante em relalção ao eixo X do perfil",
            "corpo": [
                    {"tipo": "paragrafo", "conteudo": "\n Verificação da flambagem da alma pela cortante: \n "},
                    {
                        "tipo": "formula",
                        "conteudo": (
                            r"\lambda = \frac{h}{t_w} \Rightarrow \frac{" +
                            f"{self.h_text:.{self.casa_decimal_comprimento}f}" + r"}{" + f"{self.tw_text:.{self.casa_decimal_comprimento}f}" + r"} = " +f"{lambda_sf:.2f}"
                        )
                    },
                    {
                        "tipo": "formula",
                        "conteudo": (
                            r"\lambda_p = 1.1 * \sqrt{\frac{k_v * E}{f_y}} \Rightarrow "
                            r"1.1 * \sqrt{\frac{5.34 * " + f"{self.e:.{self.casa_decimal_pressao}f}" + r"}{" + f"{self.fy:.{self.casa_decimal_pressao}f}" + r"}} = " + f"{lambda_p:.2f}"
                        )
                    },
                    {
                        "tipo": "formula",
                        "conteudo": (
                            r"\lambda_r = 1.37 * \sqrt{\frac{k_v * E}{f_y}} \Rightarrow "
                            r"1.37 * \sqrt{\frac{5.34 * " + f"{self.e:.{self.casa_decimal_pressao}f}" + r"}{" + f"{self.fy:.{self.casa_decimal_pressao}f}" + r"}} = " + f"{lambda_r:.2f}"
                        )
                    },
                     {"tipo": "paragrafo", "conteudo": "\n Área efetiva do cisalhamento: \n "},
                    {
                        "tipo": "formula",
                        "conteudo": (
                            r"A_w = 2 * b_f * t_f \Rightarrow 2 * " + f"{self.bf_text:.{self.casa_decimal_comprimento}f} * {self.tf_text:.{self.casa_decimal_comprimento}f} = {aw:.2f}"
                        )
                    },
                    {"tipo": "paragrafo", "conteudo": "\n Força cortante correspondente a plastificação da alma: \n "},
                    {
                        "tipo": "formula",
                        "conteudo": (
                            r"V_{pl} = 0.6 * A_w * f_y \Rightarrow 0.6 * " +
                            f"{aw:.2f} * {self.fy:.{self.casa_decimal_pressao}f} = {vpl:.{self.casa_decimal_forca}f}"
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

        if passou:
            return True, memoria_calculo_shear_x
        else:
            return False, memoria_calculo_shear_x


    def shear_force_y(self):
        vrd = 0
        #sf = shear force
        lambda_sf = (self.bf_text/2)/self.tf_text
        #kv = 1.2 item 5.4.3.3
        lambda_p = 1.1*np.sqrt((1.2*self.e)/self.fy)
        lambda_r = 1.37*np.sqrt(1.2*self.e/self.fy)
        aw = 2*self.bf_text*self.tf_text
        vpl = 0.6*aw*self.fy

        if lambda_sf <= lambda_p:
            vrd = vpl/self.y_um
        elif lambda_p < lambda_sf <= lambda_r:
            vrd = (lambda_p/lambda_sf)*(vpl/self.y_um)
        elif lambda_sf >= lambda_r:
            vrd = 1.24*((lambda_p/lambda_sf)**2)*(vpl/self.y_um)

        if self.fcy <= vrd:
            return True, vrd
        else:
            return False

    def moment_force_x(self):
        mrd_flt, mrd_flm, mrd_fla = 0, 0, 0 #inicializando para nao dar problema
        #flambagem lateral com torcao
        #*********************************************************************************************
        #considerando lfb como comprimento de flambagem
        lambda_flt = self.flb/self.r_y_text
        #Tabela D1 considerando 2 eixos de simetria
        lambda_flt_p = 1.76*np.sqrt(self.e/self.fy)
        #considerar 30% do fy para sigma
        beta = (self.fy-0.3*self.fy)*self.w_x_text/(self.e*self.i_t_text)
        print(f"beta = {beta}")
        lambda_flt_r = (((1.38*self.cb*np.sqrt(self.i_y_text*self.i_t_text)/(self.r_y_text*self.i_t_text*beta)))*
                        np.sqrt(1+np.sqrt(1+(27*self.cw_text*beta**2)/((self.cb**2)*self.i_y_text))))
        mr_flt = (self.fy-0.3*self.fy)*self.w_x_text
        mpl_flt = self.z_x_text*self.fy
        print("###########################################################################")
        print(f" lambda_flt {lambda_flt}, lambda_flt_p {lambda_flt_p}, lambda_flt_r {lambda_flt_r}, mr = {mr_flt}, mpl_flt {mpl_flt}")

        if lambda_flt <= lambda_flt_p:
            print("a")
            print(f"z_x = {self.z_x_text}, fy = {self.fy}")
            mrd_flt = mpl_flt/self.y_um
        elif lambda_flt_p < lambda_flt <= lambda_flt_r:
            print("b")
            mrd_flt = (1/self.y_um)*(mpl_flt-((mpl_flt-mr_flt)*((lambda_flt-lambda_flt_p)/(lambda_flt_r-lambda_flt_p))))
        elif lambda_flt > lambda_flt_r:
            print("c")
            mcr_flt = ((self.cb*(np.pi**2)*self.e*self.i_y_text)/(self.flb**2))*np.sqrt((self.cw_text/self.i_y_text)*(1+0.039*(self.i_t_text*(self.flb**2)/self.cw_text)))
            mrd_flt = mcr_flt/self.y_um
        print(f"mrd_flt = {mrd_flt}")

        # flambagem local da mesa comprimida
        # *********************************************************************************************
        lambda_flm = (self.bf_text/2)/self.tf_text
        lambda_flm_p = 0.38*np.sqrt(self.e/self.fy)
        lambda_flm_r = 0.83*np.sqrt(self.e/(self.fy-0.3*self.fy))
        mr_flm = (self.fy-0.3*self.fy)*self.w_x_text
        mpl_flm = self.z_x_text*self.fy
        print("###########################################################################")
        print(f" lambda_flm {lambda_flm}, lambda_flm_p {lambda_flm_p}, lambda_flm_r {lambda_flm_r}, mr = {mr_flm}, mpl_flt {mpl_flm}")

        if lambda_flm <= lambda_flm_p:
            mrd_flm = mpl_flm/self.y_um
        elif lambda_flm_p < lambda_flm <= lambda_flm_r:
            mrd_flm = (1/self.y_um)*(mpl_flm-((mpl_flm-mr_flm)*((lambda_flm-lambda_flm_p)/(lambda_flm_r-lambda_flm_p))))
        elif lambda_flm > lambda_flm_r:
            mcr_flm = (0.69 * self.e) / (lambda_flm ** 2) * (self.i_x_text/(self.d_text/2)) # wc  = wx = ix/(d/2)
            mrd_flm = mcr_flm/self.y_um
        print(f"mrd_flm = {mrd_flm}")

        # flambagem local da alma
        # *********************************************************************************************
        lambda_fla = self.d_l_text/self.tw_text
        lambda_fla_p = 3.76*np.sqrt(self.e/self.fy)
        lambda_fla_r = 5.7*np.sqrt(self.e/self.fy)
        mpl_fla = self.z_x_text*self.fy
        mr_fla = self.fy*self.w_x_text
        print("###########################################################################")
        print(f" lambda_fla {lambda_fla}, lambda_fla_p {lambda_fla_p}, lambda_fla_r {lambda_fla_r}, mr = {mr_fla}, mpl_fla {mpl_fla}")

        if lambda_fla <= lambda_fla_p:
            mrd_fla = mpl_fla / self.y_um
        elif lambda_fla_p < lambda_fla <= lambda_fla_r:
            mrd_fla = (1 / self.y_um) * (
                        mpl_fla - ((mpl_fla - mr_fla) * ((lambda_fla - lambda_fla_p) / (lambda_fla_r - lambda_fla_p))))
        elif lambda_fla > lambda_fla_r:
            mrd_fla = False # vai dar erro quando tentar achar o minimo usando numpy, logo retorna Falso
        print(f"mrd_fla {mrd_fla}")
        try:
            mfrc = 1.5 * self.w_x_text * self.fy / self.y_um

            print(f"mrd_calculado = {mfrc}")
            mrd_min = np.min([mrd_flt, mrd_flm, mrd_fla,mfrc])
            print(f"mrd_flt = {mrd_flt}, mrd_flm {mrd_flm}, mrd_fla {mrd_fla}, mrd_calc {mfrc}")
            if mrd_min <= mfrc:
                if self.mfx <= mrd_min:
                    return True, mrd_min
                else:
                    return False
            else:
                return False

        except :
            return False


    def moment_force_y(self):
        mrd_flt, mrd_flm, mrd_fla = 0, 0, 0 #inicializando para nao dar problema
        #flambagem lateral com torcao
        #*********************************************************************************************
        #nao se aplica segundo a norma para momento no menor eixo de inercia
        #verificar o item novamente para ver!

        # flambagem local da mesa comprimida
        # *********************************************************************************************
        lambda_flm = self.bf_text/(2*self.tf_text)
        lambda_flm_p = 0.38*np.sqrt(self.e/self.fy)
        lambda_flm_r = 0.83*np.sqrt(self.e/(self.fy-0.3*self.fy))


        ############################################ **********************
        mr_flm = (self.fy-0.3*self.fy)*self.w_y_text

        mpl_flm = self.z_y_text*self.fy

        if lambda_flm <= lambda_flm_p:
            mrd_flm = mpl_flm/self.y_um
        elif lambda_flm_p < lambda_flm <= lambda_flm_r:
            mrd_flm = (1/self.y_um)*(mpl_flm-((mpl_flm-mr_flm)*((lambda_flm-lambda_flm_p)/(lambda_flm_r-lambda_flm_p))))
        elif lambda_flm > lambda_flm_r:

            #verificar se fica ix ou iy
            mcr_flm = (0.69 * self.e) / (lambda_flm ** 2) * (self.w_y_text)
            mrd_flm = mcr_flm/self.y_um

        # flambagem local da alma
        # *********************************************************************************************


        try:
            mrd_calc = 1.5*self.w_y_text*self.fy/self.y_um
            mrd_min = np.min([mrd_calc, mrd_flm ])
            print(f"Y mrd_min =  {mrd_min} , Y mrd_calc = {mrd_calc}")
            if mrd_min <= mrd_calc:
                if self.mfy <= mrd_min:
                    return True, mrd_min
                else:
                    return False
            else:
                return False

        except :
            return False


    # def  combined_forces(self):
    #     #fazer a verificao aqui! ver na norma
    #     nrd = self.normal_traction()
    #     print(nrd)
    #
    #     vrd_x = self.shear_force_x()
    #     vrd_y = self.shear_force_y()
    #     mrdx = self.moment_force_x()
    #     mrdy = self.moment_force_y()
    #     print(f"nrd = {nrd}")
    #     print(f"vrdx = {vrd_x}")
    #     print(f"vrdy = {vrd_y}")
    #     print(f"mrdx = {mrdx}")
    #     print(f"mrdy = {mrdy}")
    #
    #     nsd_nrd = self.fn/nrd[1]
    #     print(f"nsd/nrd = {nsd_nrd}")
    #
    #     if nrd[0] == False or vrd_x[0] == False  or mrdx[0] == False or mrdy[0] == False :
    #         print("Nao passou!")
    #     else:
    #         if nsd_nrd >= 0.2:
    #             last_verif = nsd_nrd + (8 / 9) * ((self.mfx / mrdx[1]) + (self.mfy / mrdy[1]))
    #             if last_verif <= 1:
    #                 print("Passou")
    #                 return True
    #             else:
    #                 print("Nao passou!")
    #         else:
    #             last_verif = nsd_nrd * 0.5 + ((self.mfx / mrdx[1]) + (self.mfy / mrdy[1]))
    #             if last_verif <= 1:
    #                 print("Passou")
    #                 return True
    #             else:
    #                 print("Nao passou!")
    #         return None



    def calculate(self):
        meu_relatorio = ReportGenerator('relatorio_completo_viga')

        nrdt = self.normal_traction()
        nrdc = self.normal_compression()
        vrdx = self.shear_force_x()

        meu_relatorio.add_calculo(nrdt[1])
        meu_relatorio.add_calculo(nrdc[1])
        meu_relatorio.add_calculo(vrdx[1])

        meu_relatorio.gerar_pdf()

        # self.combined_forces()
        #
        # nrd = self.normal()
        # print(f"nrd {nrd}")
        # mrdx = self.moment_force_x()
        # print(f"mrdx = {mrdx}")
        #

######

        # # gerar memoria de calculo
        # pdf = ReportGenerator( title="Relatório de Cálculo Estrutural")
        # pdf.add_results(self.report_logs)
        # pdf.save_file_as()


        # print(f"self.linear_mass_text {self.linear_mass_text}, self.d_text {self.d_text},  self.bf_text {self.bf_text},self.tw_text {self.tw_text}, self.tf_text {self.tf_text} "
        #       f" self.h_text {self.h_text}, self.d_l_text {self.d_l_text}, self.d_l_text {self.d_l_text}, self.d_l_text {self.d_l_text}, self.d_l_text {self.d_l_text}"
        #       f" self.area_text {self.area_text}, self.i_x_text {self.i_x_text}, self.i_x_text {self.i_x_text}, self.w_x_text {self.w_x_text}, self.r_x_text {self.r_x_text}"
        #       f" self.z_x_text {self.z_x_text}, self.i_y_text {self.i_y_text}, self.w_y_text {self.w_y_text}, self.r_y_text {self.r_y_text}, self.z_y_text {self.z_y_text}"
        #       f" self.r_t_text {self.r_t_text}, self.i_t_text {self.i_t_text}, self.bf_two_text {self.bf_two_text}, self.d_tw_text {self.d_tw_text}, self.cw_text {self.cw_text}"
        #       f" self.u_text {self.u_text}, self.fy {self.fy}, self.fu {self.fu}, self.lfx {self.lfx}, self.lfy {self.lfy}, self.lfz {self.lfz}, self.flb {self.flb}"
        #       f" self.fn {self.fn}, self.fcx {self.fcx}, self.fcy {self.fcy}, self.mfx {self.mfx}, self.mfy {self.mfy}, self.y_um {self.y_um}, self.y_dois {self.y_dois},"
        #       f"self.e {self.e}, self.g {self.g}, self.cb {self.cb}")



