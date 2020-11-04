from profero.framework.presentation.cell import Cell
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor


class NoteCell(Cell):
    def __init__(self, inputs, slide_width, note, parent_row):
        super().__init__(
            inputs,
            {
                'width': slide_width,
                'x_offset': 0
            },
            'note', 0,
            parent_row
        )

        self.note = note

    def render(self, slide):
        card = self.create_rect(
            0, self.parent_row.y_offset,
            self.width, self.parent_row.height
        )

        self.set_shape_transparency(card, 100)

        self.set_text(
            card,
            self.note,
            font_family='Helvetica',
            font_size=Pt(8),
            color=RGBColor(0x0F, 0x3B, 0x5E),
            margin_left=Cm(1.3)
        )
