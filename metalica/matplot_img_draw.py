import wx
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class DrawBeam(wx.Panel):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        #---------------------------- cfg plot canva -verificar a cor de fundo??
        self.fig, self.ax = plt.subplots(figsize=(2, 2))
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.fig.patch.set_facecolor((0.941, 0.941, 0.941)) # 240/255 -> cor do fundo

    def draw_w_hp(self, height, width, tw):
        self.ax.clear()
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        if not tw == 0:
            #---------------------------- desenha o perfil
            mesa_sup = patches.Rectangle((-width / 2, height / 2 - tw), width, tw, facecolor="steelblue")
            mesa_inf = patches.Rectangle((-width / 2, -height / 2), width, tw, facecolor="steelblue")
            alma = patches.Rectangle((-tw / 2, -height / 2 + tw), tw, height - 2 * tw,facecolor="steelblue")
            for parte in [mesa_sup, mesa_inf, alma]:
                self.ax.add_patch(parte)
            #---------------------------- desenha o perfil w e hp
            # Cota vertical (altura)
            x_cota_v = width / 2 + 15
            y1 = -height / 2
            y2 = height / 2

            self.ax.annotate("", xy=(x_cota_v, y1), xytext=(x_cota_v, y2),
                        arrowprops=dict(arrowstyle="<->"))
            self.ax.text(x_cota_v + 5, 0, f"{height} mm", ha="left", va="center", rotation=90)

            # Cota horizontal (largura)
            y_cota_h = -height / 2 - 20
            x1 = -width / 2
            x2 = width / 2

            self.ax.annotate("", xy=(x1, y_cota_h), xytext=(x2, y_cota_h),
                        arrowprops=dict(arrowstyle="<->"))
            self.ax.text(0, y_cota_h - 5, f"{width} mm", ha="center", va="top")

            # cota alma
            y_cota_a = 0
            x1a =  -tw/50
            x2a =  tw/50
            #o texto buga quando coloca exatamente no meio
            self.ax.annotate("", xy=(x1a, y_cota_a), xytext=(x2a , y_cota_a),
                             arrowprops=dict(arrowstyle="<->"))
            self.ax.text(0, y_cota_a -30, f"{tw} mm", ha="center", va="top")

            #escala
            self.ax.set_xlim(-width / 2 - 50, width / 2 + 50)
            self.ax.set_ylim(-height / 2 - 50, height / 2 + 50)
            return self.fig
