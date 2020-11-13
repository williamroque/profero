from pptx.util import Cm, Pt, Inches
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

from profero.framework.presentation.slide import Slide as FSlide
from profero.framework.presentation.row import Row
from profero.framework.presentation.cell import Cell
from profero.presentation.slides.common.header import HeaderRow
from profero.presentation.slides.common.note import NoteCell


NOTE = """
➢ Valores com base em {}
""".strip()


class TableCell(Cell):
    def __init__(self, inputs, slide_width, props, parent_row):
        super().__init__(
            inputs,
            {
                'width': slide_width,
                'x_offset': 0
            },
            'table', 0,
            parent_row
        )

        self.slide_width = slide_width
        self.props = props

    def render(self, slide):
        slide = self.parent_row.parent_slide
        slide.table_of_contents_slide.add_entry(
            slide.title, [slide.index + 1], slide
        )


class ChartCell(Cell):
    def __init__(self, inputs, slide_width, props, parent_row):
        super().__init__(
            inputs,
            {
                'width': slide_width,
                'x_offset': 0
            },
            'chart', 0,
            parent_row
        )

        self.slide_width = slide_width
        self.props = props

    def render(self, slide):
        pass


class Slide(FSlide):
    def __init__(self, inputs, index, props, table_of_contents_slide, parent_presentation):
        super().__init__(
            inputs,
            'direitos-creditorios-garantia', 6,
            index,
            None,
            parent_presentation
        )

        self.title = 'Direitos Creditórios em Garantia'

        self.props = props

        self.table_of_contents_slide = table_of_contents_slide

        slide_height = parent_presentation.presentation.slide_height
        slide_width = parent_presentation.presentation.slide_width

        note_height = Cm(2.04)

        header_row = HeaderRow(
            inputs,
            {
                'height': .25 * slide_height,
                'y_offset': Cm(0)
            }, 0,
            self.title,
            slide_width, slide_height,
            self
        )
        self.add_row(header_row)

        table_row = Row(
            inputs,
            {
                'height': .3 * slide_height - note_height / 2,
                'y_offset': header_row.y_offset + header_row.height
            },
            'table', 1,
            self
        )

        table_cell = TableCell(inputs, slide_width, self.props, table_row)
        table_row.add_cell(table_cell)

        self.add_row(table_row)

        chart_row = Row(
            inputs,
            {
                'height': .45 * slide_height - note_height / 2,
                'y_offset': table_row.y_offset + table_row.height
            },
            'chart', 2,
            self
        )

        chart_cell = ChartCell(inputs, slide_width, self.props, chart_row)
        chart_row.add_cell(chart_cell)

        self.add_row(chart_row)

        note_row = Row(
            inputs,
            {
                'height': note_height,
                'y_offset': chart_row.y_offset + chart_row.height
            },
            'note', 3,
            self
        )

        note_cell = NoteCell(
            inputs,
            slide_width,
            NOTE.format(
                inputs.get('date')
            ),
            note_row
        )
        note_row.add_cell(note_cell)

        self.add_row(note_row)
