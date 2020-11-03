from pptx.util import Cm, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

from profero.framework.presentation.slide import Slide as FSlide
from profero.framework.presentation.row import Row
from profero.framework.presentation.cell import Cell
from profero.presentation.slides.common.header import HeaderRow

import re


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

        self.text = ''

    def render(self, slide):
        box_width = self.width * .87
        box_height = self.parent_row.height * .9

        self.entry_box = self.create_rect(
            self.x_offset + self.width / 2 - box_width / 2,
            self.parent_row.y_offset + self.parent_row.height / 2 - box_height / 2,
            box_width, box_height
        )
        self.set_shape_transparency(self.entry_box, 100)

    def add_entry(self, title, pages, linked_slide):
        CHARS_PER_ROW = 113

        pages.sort()

        page_str = ''
        for i in range(len(pages)):
            if i > 0:
                page_str += (',' if pages[i] - pages[i-1] > 1 else '-') + str(pages[i])
            else:
                page_str += str(pages[i])

        page_str = re.sub(r'(\d+-)(\d+-)+', r'\1', page_str)

        self.text += '\n{}{}'.format(
            title,
            page_str.rjust(CHARS_PER_ROW - len(title), '.')
        )

        self.set_text(
            self.entry_box,
            self.text,
            font_family='Courier',
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

    def add_entry(self, *args):
        self.entry_cell.add_entry(*args)
