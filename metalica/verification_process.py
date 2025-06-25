import wx
import numpy as np


class VerificationProcess:
    def __init__(self, linear_mass_text, d_text, bf_text, tw_text, tf_text, h_text, d_l_text, area_text, i_x_text, w_x_text, r_x_text,
                 z_x_text, i_y_text, w_y_text, r_y_text, z_y_text, r_t_text, i_t_text, bf_two_text, d_tw_text, cw_text, u_text, fy, fu, lfx, lfy, lfz,
                 flb, fn, fcx,fcy, mfx, mfy, y_um, y_dois, g, e, cb):
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
        self.fn = fn
        self.fcx = fcx
        self.fcy = fcy
        self.mfx = mfx
        self.mfy = mfy
        self.y_um = y_um
        self.y_dois = y_dois
        self.e = e
        self.g = g
        self.cb = cb

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
# ************************************************************************************************************
            #verificacao da esbeltez local
            #elemento AA
            b_sobre_t_alma = self.d_l_text/self.tw_text
            b_sobre_t_limit_alma = 1.49*np.sqrt(self.e/self.fy)
            #elemento AL
            b_sobre_t_aba = (self.bf_text/2)/self.tf_text # bf/2 pega 1 aba da mesa
            b_sobre_t_limit_aba = 0.56*np.sqrt(self.e/self.fy)
            if b_sobre_t_alma <= b_sobre_t_limit_alma and b_sobre_t_aba <= b_sobre_t_limit_aba:
                #area vai ser a bruta
                area = self.area_text
                #pass
            else:
                print("teste 1 n passou")
                if b_sobre_t_alma <= b_sobre_t_limit_alma/np.sqrt(psi):
                    print("teste 2 passou")
                    area = self.area_text
                    # area_aa = self.d_l_text * self.tw_text
                    #b_efetivo = b real
                    pass
                else:
                    sigma_e_l = ((1.31*((1.49*np.sqrt(self.e/self.fy))/b_sobre_t_alma))**2)*self.fy
                    b_efetivo = self.d_l_text*(1-0.18*np.sqrt(sigma_e_l/(psi*self.fy)))*np.sqrt(sigma_e_l/(psi*self.fy))
                    # b = b_efetivo
                    area_aa = b_efetivo * self.tw_text
                if b_sobre_t_aba <= b_sobre_t_limit_aba/np.sqrt(psi):
                    area = self.area_text
                    # area_al = self.bf_text / 2 * self.tf_text
                    # b_efetivo = b real
                else:
                    sigma_e_l = ((1.49*((0.56*np.sqrt(self.e/self.fy))/(self.bf_text / 2 * self.tf_text)))**2)*self.fy
                    b_efetivo = (self.bf_text / 2) * (1 - 0.22 * np.sqrt(sigma_e_l / (psi * self.fy))) * np.sqrt(
                        sigma_e_l / (psi * self.fy))
                    # b = b_efetivo * 2???? ********************************************************************************************************************************
                    area_al = b_efetivo * self.tf_text
# ************************************************************************************************************
            area_efetiva_total = area_aa + area_al
            nrdc = psi*area_efetiva_total*self.fy/self.y_um
            if self.fn <= nrdc:
                #elemento passa
                return True , nrdc
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
                return True, ntrd

    def shear_force_x(self):
        #sf = shear force
        vrd = 0
        lambda_sf = self.h_text/self.tw_text
        lambda_p = 1.1*np.sqrt(5.34*self.e/self.fy)
        lambda_r = 1.37*np.sqrt(5.34*self.e/self.fy)
        aw = 2*self.bf_text*self.tf_text
        vpl = 0.6*aw*self.fy

        if lambda_sf <= lambda_p:
            vrd = vpl/self.y_um
        elif lambda_p < lambda_sf <= lambda_r:
            vrd = (lambda_p/lambda_sf)*(vpl/self.y_um)
        elif lambda_sf >= lambda_r:
            vrd = 1.24*((lambda_p/lambda_sf)**2)*(vpl/self.y_um)

        if self.fcx <= vrd:
            return True, vrd
        else:
            return False

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
        print(f"e = {self.e}")
        mrd_flt, mrd_flm, mrd_fla = 0, 0, 0 #inicializando para nao dar problema
        #flambagem lateral com torcao
        #*********************************************************************************************
        #considerando lfz como comprimento de flambagem
        lambda_flt = self.flb/self.r_y_text

        #Tabela D1 considerando 2 eixos de simetria
        lambda_flt_p = 1.76*np.sqrt(self.e/self.fy)
        #considerar 30% do fy para sigma
        beta = (self.fy-0.3*self.fy)*self.w_x_text/(self.e*self.i_t_text)
        lambda_flt_r = ((1.38*self.cb*np.sqrt(self.i_y_text*self.i_t_text)/(self.r_y_text*self.i_t_text*beta)))*np.sqrt(1+np.sqrt(1+(27*self.cw_text*beta**2)/((self.cb**2)*self.i_y_text)))
        mr_flt = (self.fy-0.3*self.fy)*self.w_x_text
        mpl_flt = self.z_x_text*self.fy
        print(f"lambda FLT {lambda_flt} lambdaP {lambda_flt_p} lambdaR {lambda_flt_r}")

        if lambda_flt <= lambda_flt_p:
            mrd_flt = mpl_flt/self.y_um
        elif lambda_flt_p < lambda_flt <= lambda_flt_r:
            mrd_flt = (1/self.y_um)*(mpl_flt-((mpl_flt-mr_flt)*((lambda_flt-lambda_flt_p)/(lambda_flt_r-lambda_flt_p))))
        elif lambda_flt > lambda_flt_r:
            mcr_flt = ((self.cb*(np.pi**2)*self.e*self.i_y_text)/(self.flb**2))*np.sqrt((self.cw_text/self.i_y_text)*(1+0.039*(self.i_t_text*(self.flb**2)/self.cw_text)))
            mrd_flt = mcr_flt/self.y_um

        # flambagem local da mesa comprimida
        # *********************************************************************************************
        lambda_flm = (self.bf_text/2)/self.tf_text
        lambda_flm_p = 0.38*np.sqrt(self.e/self.fy)
        lambda_flm_r = 0.83*np.sqrt(self.e/(self.fy-0.3*self.fy))

        print(f"lambda FLM {lambda_flm} lambdaP {lambda_flm_p} lambdaR {lambda_flm_r}")

        mr_flm = (self.fy-0.3*self.fy)*self.w_x_text

        mpl_flm = self.z_x_text*self.fy

        if lambda_flm <= lambda_flm_p:
            mrd_flm = mpl_flm/self.y_um
        elif lambda_flm_p < lambda_flm <= lambda_flm_r:
            mrd_flm = (1/self.y_um)*(mpl_flm-((mpl_flm-mr_flm)*((lambda_flm-lambda_flm_p)/(lambda_flm_r-lambda_flm_p))))
        elif lambda_flm > lambda_flm_r:
            mcr_flm = (0.69 * self.e) / (lambda_flm ** 2) * (self.i_x_text/(self.d_text/2)) # wc  = wx = ix/(d/2)
            mrd_flm = mcr_flm/self.y_um

        # flambagem local da alma
        # *********************************************************************************************
        lambda_fla = self.d_l_text/self.tw_text
        lambda_fla_p = 3.76*np.sqrt(self.e/self.fy)
        lambda_fla_r = 5.7*np.sqrt(self.e/self.fy)

        print(f"lambda FLA {lambda_fla} lambdaP {lambda_fla_p} lambdaR {lambda_fla_r}")

        mpl_fla = self.z_x_text*self.fy
        mr_fla = self.fy*self.w_x_text

        if lambda_fla <= lambda_fla_p:
            mrd_fla = mpl_fla / self.y_um
        elif lambda_fla_p < lambda_fla <= lambda_fla_r:
            mrd_fla = (1 / self.y_um) * (
                        mpl_fla - ((mpl_fla - mr_fla) * ((lambda_fla - lambda_fla_p) / (lambda_fla_r - lambda_fla_p))))
        elif lambda_fla > lambda_fla_r:
            mrd_fla = False # vai dar erro quando tentar achar o minimo usando numpy, logo retorna Falso
        try:
            mrd_calc = 1.5 * self.w_x_text * self.fy / self.y_um
            mrd_min = np.min([mrd_flt, mrd_flm, mrd_fla,mrd_calc ])
            print(f"mrd_flt = {mrd_flt}, mrd_flm {mrd_flm}, mrd_fla {mrd_fla}, mrd_calc {mrd_calc}")
            if mrd_min <= mrd_calc:
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


    def  combined_forces(self):
        #fazer a verificao aqui! ver na norma
        nrd = self.normal()
        vrd_x = self.shear_force_x()
        vrd_y = self.shear_force_y()
        mrdx = self.moment_force_x()
        mrdy = self.moment_force_y()
        print(f"nrd = {nrd}")
        print(f"vrdx = {vrd_x}")
        print(f"vrdy = {vrd_y}")
        print(f"mrdx = {mrdx}")
        print(f"mrdy = {mrdy}")

        nsd_nrd = self.fn/nrd[1]
        print(f"nsd/nrd = {nsd_nrd}")

        if nrd[0] == False or vrd_x[0] == False  or mrdx[0] == False or mrdy[0] == False :
            print("Nao passou!")
        else:
            if nsd_nrd >= 0.2:
                last_verif = nsd_nrd + (8 / 9) * ((self.mfx / mrdx[1]) + (self.mfy / mrdy[1]))
                if last_verif <= 1:
                    print("Passou")
                    return True
                else:
                    print("Nao passou!")
            else:
                last_verif = nsd_nrd * 0.5 + ((self.mfx / mrdx[1]) + (self.mfy / mrdy[1]))
                if last_verif <= 1:
                    print("Passou")
                    return True
                else:
                    print("Nao passou!")
            return None


    def calculate(self):
        self.combined_forces()
        print(f"self.linear_mass_text {self.linear_mass_text}, self.d_text {self.d_text},  self.bf_text {self.bf_text},self.tw_text {self.tw_text}, self.tf_text {self.tf_text} "
              f" self.h_text {self.h_text}, self.d_l_text {self.d_l_text}, self.d_l_text {self.d_l_text}, self.d_l_text {self.d_l_text}, self.d_l_text {self.d_l_text}"
              f" self.area_text {self.area_text}, self.i_x_text {self.i_x_text}, self.i_x_text {self.i_x_text}, self.w_x_text {self.w_x_text}, self.r_x_text {self.r_x_text}"
              f" self.z_x_text {self.z_x_text}, self.i_y_text {self.i_y_text}, self.w_y_text {self.w_y_text}, self.r_y_text {self.r_y_text}, self.z_y_text {self.z_y_text}"
              f" self.r_t_text {self.r_t_text}, self.i_t_text {self.i_t_text}, self.bf_two_text {self.bf_two_text}, self.d_tw_text {self.d_tw_text}, self.cw_text {self.cw_text}"
              f" self.u_text {self.u_text}, self.fy {self.fy}, self.fu {self.fu}, self.lfx {self.lfx}, self.lfy {self.lfy}, self.lfz {self.lfz}, self.flb {self.flb}"
              f" self.fn {self.fn}, self.fcx {self.fcx}, self.fcy {self.fcy}, self.mfx {self.mfx}, self.mfy {self.mfy}, self.y_um {self.y_um}, self.y_dois {self.y_dois},"
              f"self.e {self.e}, self.g {self.g}, self.cb {self.cb}")



