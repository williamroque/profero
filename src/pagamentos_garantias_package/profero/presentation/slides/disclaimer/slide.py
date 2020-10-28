from pptx.util import Cm, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

from profero.framework.presentation.slide import Slide as FSlide
from profero.framework.presentation.row import Row
from profero.framework.presentation.cell import Cell
from profero.presentation.slides.common.header import *


disclaimer_string = """
Esta apresentação não pode ser publicada, distribuída ou divulgada a qualquer terceiro.

As informações contidas nesta apresentação devem ser interpretadas somente em conjunto com a explicação oral feita pelos representantes da Logos Companhia Securitizadora (“LogosSec”).

As informações aqui contidas não podem ser divulgadas ou de qualquer forma distribuídas para terceiros, em sua totalidade ou parcialmente, ou utilizadas para qualquer outro propósito, sem a prévia e expressa autorização da LogosSec.

As informações contidas nesta apresentação refletem as condições existentes e nossa percepção do mercado e da operação até a presente data, estando, desta maneira, sujeitas a alterações.

Ao preparar esta apresentação, a LogosSec não realizou nenhuma verificação independente, entendendo que as informações disponíveis através de fontes públicas eram completas e verdadeiras com relação a todos os seus aspectos relevantes.
""".strip()


class Slide(FSlide):
    def __init__(self, inputs, props, parent_presentation):
        super().__init__(
            inputs,
            'title', 6,
            None,
            parent_presentation
        )

        slide_height = parent_presentation.presentation.slide_height
        slide_width = parent_presentation.presentation.slide_width

        header_row = Row(
            inputs,
            {
                'height': .25 * slide_height,
                'y_offset': Cm(0)
            },
            'header', 0,
            self
        )

        client_logo_cell = ClientLogoCell(inputs, inputs.get('client-logo'), slide_width, header_row)
        header_row.add_cell(client_logo_cell)

        header_cell = HeaderCell(inputs, slide_width, client_logo_cell.x_offset + client_logo_cell.width, header_row)
        header_row.add_cell(header_cell)

        logo_cell = LogoCell(inputs, slide_width, header_cell.x_offset + header_cell.width, header_row)
        header_row.add_cell(logo_cell)

        self.add_row(header_row)
