# Esse slide representa o índice

from pptx.util import Cm, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

from profero.framework.presentation.slide import Slide as FSlide
from profero.framework.presentation.row import Row
from profero.framework.presentation.cell import Cell
from profero.presentation.slides.common.header import HeaderRow

import re


# Essa classe representa a caixa de texto do índice
class EntryCell(Cell):
    def __init__(self, inputs, slide_width, parent_row):
        super().__init__(
            inputs,
            {
                'width': slide_width,
                'x_offset': 0
            },
            'entry', 0,
            parent_row
        )

        # O texto da tabela
        self.text = ''

    def render(self, slide):
        # Dimensões da caixa
        box_width = self.width * .87
        box_height = self.parent_row.height * .9

        # A caixa de texto em si
        self.entry_box = self.create_rect(
            self.x_offset + self.width / 2 - box_width / 2,
            self.parent_row.y_offset + self.parent_row.height / 2 - box_height / 2,
            box_width, box_height
        )
        self.set_shape_transparency(self.entry_box, 100)

    # Adicionar um elemento individual no índice. Uma entrada pode representar um
    # slide ou uma coleção de slides. O `title` deve ser o texto a ser mostrado na
    # entrada; o parâmetro `pages` representa a lista (`list`) de páginas a serem
    # mostradas; o `linked_slide` representa o slide alvo do link.
    def add_entry(self, title, pages, linked_slide):
        # Representa o número de caracteres por linha (com essa largura especifica
        # da caixa, a fonte 'Courier' e o tamanho 12 pt)
        CHARS_PER_ROW = 113

        # Remover marcas de substituições (ver `header.py`)
        title = re.sub(r'_(.+)_', r'\1', title) + ' '

        pages.sort()

        # Para dois elementos consecutivos $a$ e $b$ dentro da lista `pages` e
        # $a < b$, se $b - a = 1$, usar 'a-b'; caso contrário, usar 'a,b'.
        page_str = ''
        for i in range(len(pages)):
            if i > 0:
                page_str += (',' if pages[i] - pages[i-1] > 1 else '-') + str(pages[i])
            else:
                page_str += str(pages[i])

        # Quando houver 'a_1-a_2...-a_n', substituir por 'a_1-a_n'
        page_str = re.sub(r'(\d+-)(\d+-)+', r'\1', page_str)

        # Começar entrada em uma nova linha e encher com caracteres '.' à esquerda do
        # Texto com os números das paginas
        self.text += '\n{}{}'.format(
            title,
            '.' * (CHARS_PER_ROW - len(title) - len(page_str) - 1) + ' ' + page_str
        )

        self.set_text(
            self.entry_box,
            self.text,
            font_family='Input',
            font_size=Pt(12),
            color=RGBColor(0x20, 0x38, 0x64),
            alignment=PP_ALIGN.JUSTIFY,
            vertical_anchor=MSO_ANCHOR.TOP,
            slide_link=linked_slide
        )


class Slide(FSlide):
    def __init__(self, inputs, index, props, _, parent_presentation):
        super().__init__(
            inputs,
            'table-of-contents', 6,
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
            'Temas a serem abordados',
            slide_width, slide_height,
            self
        )
        self.add_row(header_row)

        entry_row = Row(
            inputs,
            {
                'height': .75 * slide_height,
                'y_offset': header_row.y_offset + header_row.height
            },
            'entry', 1,
            self
        )

        self.entry_cell = EntryCell(inputs, slide_width, entry_row)

        entry_row.add_cell(self.entry_cell)

        self.add_row(entry_row)

    # Propagar chamada ao `add_entry`
    def add_entry(self, *args):
        self.entry_cell.add_entry(*args)
