from pptx.util import Cm

from profero.framework.presentation.slide import Slide as FSlide
from profero.framework.presentation.row import Row
from profero.presentation.slides.common.header import HeaderRow


class Slide(FSlide):
    def __init__(self, inputs, index, props, parent_presentation):
        super().__init__(
            inputs,
            'title', 6,
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
