import io
import matplotlib.pyplot as plt

from viktor import ViktorController
from viktor.parametrization import ViktorParametrization, Text, NumberField, LineBreak
from viktor.views import ImageView, ImageResult


class Parametrization(ViktorParametrization):
    introduction = Text(
        """
        📊 I-Beam Section Visualization App  
        使用 Matplotlib 绘制工字钢截面
        """
    )

    height = NumberField('截面高度 H (mm)', default=300)
    width = NumberField('截面宽度 B (mm)', default=150)
    lb1 = LineBreak()

    flange_thickness = NumberField('翼缘厚度 tf (mm)', default=20)
    web_thickness = NumberField('腹板厚度 tw (mm)', default=10)


class Controller(ViktorController):
    label = 'I-Beam Section App (Matplotlib)'
    parametrization = Parametrization

    @ImageView("工字钢截面图", duration_guess=1)
    def get_image_view(self, params, **kwargs):

        H = params.height
        B = params.width
        tf = params.flange_thickness
        tw = params.web_thickness

        fig, ax = plt.subplots()

        # 上翼缘
        ax.add_patch(
            plt.Rectangle((-B/2, H/2 - tf), B, tf, color='lightblue', ec='black')
        )

        # 下翼缘
        ax.add_patch(
            plt.Rectangle((-B/2, -H/2), B, tf, color='lightblue', ec='black')
        )

        # 腹板
        ax.add_patch(
            plt.Rectangle((-tw/2, -H/2 + tf), tw, H - 2*tf, color='lightblue', ec='black')
        )

        # 等比例显示
        ax.set_aspect('equal', adjustable='box')

        # 设置边界
        ax.set_xlim(-B/1.2, B/1.2)
        ax.set_ylim(-H/1.2, H/1.2)

        ax.set_xlabel("Width (mm)")
        ax.set_ylabel("Height (mm)")
        ax.set_title("I-Beam Cross Section")

        ax.grid(True)

        # 保存为内存图片
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)

        return ImageResult(buf)