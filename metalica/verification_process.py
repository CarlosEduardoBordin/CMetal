import wx
import numpy as np
from statistics import fmean
from OpenGL.raw.GLES2.NV.non_square_matrices import GL_FLOAT_MAT2x3_NV


class VerificationProcess:
    def __init__(self, linear_mass_text, d_text, bf_text, tw_text, tf_text, h_text, d_l_text, area_text, i_x_text, w_x_text, r_x_text,
                 z_x_text, i_y_text, w_y_text, r_y_text, z_y_text, r_t_text, i_t_text, bf_two_text, d_tw_text, cw_text, u_text, fy, fu, lfx, lfy, lfz,
                 fn, fc, mf, y_um, y_dois, e):
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
        self.fn = fn
        self.fc = fc
        self.mf = mf
        self.y_um = y_um
        self.y_dois = y_dois
        self.e = e

# para perfis laminados

    def normal(self):
        if self.fn < 0 :
            #compressao
            #indice de esbeltez da secao recomendado < 200
            ind_esblt_x = self.lfx/self.r_x_text
            ind_esblt_y = self.lfy / self.r_y_text
            if ind_esblt_x > 200 or ind_esblt_y > 200:
                pass #fazer uma verificao aqui
            #flambagem por flexao em x
            n_e_x = (np.pi**2)*self.e*self.i_x_text/(self.lfx**2)
            n_e_y = (np.pi**2)*self.e*self.i_y_text/(self.lfy**2)
            r_o = np.sqrt(self.r_x_text**2 + self.r_y_text**2 + 0 + 0) # considerando o perfil como simetrico
            n_e_z = (1/ (r_o**2))*(((np.pi**2)*self.e*self.cw_text/(self.lfz**2))+self.g * self.i_t_text) # J = it na tabela
            n_e = np.min([n_e_x, n_e_y, n_e_z])
            #lambda0 5.3.3.2
            lbd_zero = np.sqrt(self.area_text*self.fy/n_e)
            #fator de reducao 5.3.3.1
            if lbd_zero <= 1.5:
                psi = 0.658**(lbd_zero**2)
            else:
                psi = 0.877/(lbd_zero**2)
                
            #verificacao da esbeltez local
            #elemento AA
            b_sobre_t_alma = self.d_l_text/self.tw_text
            b_sobre_t_limit_alma = 1.49*np.sqrt(self.e/self.fy)
            #elemento AL
            b_sobre_t_aba = (self.bf_text/2)/self.tf_text # bf/2 pega 1 aba da mesa
            b_sobre_t_limit_aba = 0.56*np.sqrt(self.e/self.fy)
            if b_sobre_t_alma <= b_sobre_t_limit_alma:
                #area vai ser a bruta
                area_aa = self.d_l_text*self.tw_text
                #pass
            else:
                print("teste 1 n passou")
                if b_sobre_t_alma <= b_sobre_t_limit_alma/np.sqrt(psi):
                    print("teste 2 passou")
                    area_aa = self.d_l_text * self.tw_text
                    #b_efetivo = b real
                    pass
                else:
                    sigma_e_l = ((1.31*((1.49*np.sqrt(self.e/self.fy))/b_sobre_t_alma))**2)*self.fy
                    b_efetivo = self.d_l_text*(1-0.18*np.sqrt(sigma_e_l/(psi*self.fy)))*np.sqrt(sigma_e_l/(psi*self.fy))
                    # b = b_efetivo
                    area_aa = b_efetivo * self.tw_text
           #elemento al
            if  b_sobre_t_aba <= b_sobre_t_limit_aba:
                # area vai ser a bruta
                area_al = self.bf_text/2 * self.tf_text
            else:
                print("teste 1 n passou")
                if b_sobre_t_aba <= b_sobre_t_limit_aba/np.sqrt(psi):
                    area_al = self.bf_text / 2 * self.tf_text
                    # b_efetivo = b real
                else:
                    sigma_e_l = ((1.49*((0.56*np.sqrt(self.e/self.fy))/(self.bf_text / 2 * self.tf_text)))**2)*self.fy
                    b_efetivo = (self.bf_text / 2) * (1 - 0.22 * np.sqrt(sigma_e_l / (psi * self.fy))) * np.sqrt(
                        sigma_e_l / (psi * self.fy))
                    # b = b_efetivo * 4???? ********************************************************************************************************************************
                    area_al = b_efetivo * self.tf_text
            area_efetiva_total = area_aa + area_al
            nrdc = psi*area_efetiva_total*self.fy/self.y_um
            if self.fn <= nrdc:
                #elemento passa
                return True
            else:
                #elemento nao passa
                return False


#tracao
        else:
            #tracao
            #verificar o item 5.2.8 para barras !!
            #considerando a secao bruta da barra
            ntrd = self.area_text*self.fy/self.y_um
            ntsd = self.fn
            if ntsd > ntrd:
                #nao passa
                return False
            else:
                #passa
                return True

    
