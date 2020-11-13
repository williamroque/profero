from pptx.util import Cm, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

from profero.framework.presentation.slide import Slide as FSlide
from profero.framework.presentation.row import Row
from profero.framework.presentation.cell import Cell
from profero.presentation.slides.common.header import HeaderRow


disclaimer_string = """
Esta apresentação não pode ser publicada, distribuída ou divulgada a qualquer terceiro.

As informações contidas nesta apresentação devem ser interpretadas somente em conjunto com a explicação oral feita pelos representantes da Logos Companhia Securitizadora (“LogosSec”).

As informações aqui contidas não podem ser divulgadas ou de qualquer forma distribuídas para terceiros, em sua totalidade ou parcialmente, ou utilizadas para qualquer outro propósito, sem a prévia e expressa autorização da LogosSec.

As informações contidas nesta apresentação refletem as condições existentes e nossa percepção do mercado e da operação até a presente data, estando, desta maneira, sujeitas a alterações.

Ao preparar esta apresentação, a LogosSec não realizou nenhuma verificação independente, entendendo que as informações disponíveis através de fontes públicas eram completas e verdadeiras com relação a todos os seus aspectos relevantes.
""".strip()


class DisclaimerCell(Cell):
    def __init__(self, inputs, slide_width, parent_row):
        super().__init__(
            inputs,
            {
                'width': slide_width,
                'x_offset': 0
            },
            'disclaimer', 0,
            parent_row
        )

    def render(self, slide):
        box_width = self.width * .87
        box_height = self.parent_row.height * .9

        disclaimer = self.create_rect(
            self.x_offset + self.width / 2 - box_width / 2,
            self.parent_row.y_offset + self.parent_row.height / 2 - box_height / 2,
            box_width, box_height
        )
        self.set_shape_transparency(disclaimer, 100)

        self.set_text(
            disclaimer,
            disclaimer_string,
            font_family='Calibri',
            font_size=Pt(14),
            color=RGBColor(0x16, 0x29, 0x4C),
            alignment=PP_ALIGN.JUSTIFY,
            vertical_anchor=MSO_ANCHOR.TOP
        )


class Slide(FSlide):
    def __init__(self, inputs, index, props, _, parent_presentation):
        super().__init__(
            inputs,
            'disclaimer', 6,
            index,
            None,
            parent_presentation
        )

        slide_height = parent_presentation.presentation.slide_height
        slide_width = parent_presentation.presentation.slide_width

        header_row = HeaderRow(
            inputs,
            {
                'height': .25 * slide_height,
                'y_offset': Cm(0)
            }, 0,
            'Disclaimer',
            slide_width, slide_height,
            self
        )
        self.add_row(header_row)

        disclaimer_row = Row(
            inputs,
            {
                'height': .75 * slide_height,
                'y_offset': header_row.y_offset + header_row.height
            },
            'disclaimer', 1,
            self
        )

        disclaimer_cell = DisclaimerCell(
            inputs,
            slide_width,
            disclaimer_row
        )
        disclaimer_row.add_cell(disclaimer_cell)

        self.add_row(disclaimer_row)
