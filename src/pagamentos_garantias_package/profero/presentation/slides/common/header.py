from pptx.util import Cm, Pt

from profero.framework.presentation.cell import Cell

import importlib.resources
import profero.assets


class ClientLogoCell(Cell):
    def __init__(self, inputs, client_logo_path, slide_width, parent_row):
        super().__init__(
            inputs,
            {
                'width': slide_width * .15,
                'x_offset': 0
            },
            'client-logo', 0,
            parent_row
        )

        self.client_logo_path = client_logo_path

        self.picture_width = Cm(3.3)
        self.picture_height = Cm(2.55)

    def render(self, slide):
        slide.shapes.add_picture(
            self.client_logo_path,
            self.width / 2 - self.picture_width / 2,
            self.parent_row.height / 2 - self.picture_height / 2,
            self.picture_width, self.picture_height
        )


class HeaderCell(Cell):
    def __init__(self, inputs, slide_width, x_offset, parent_row):
        super().__init__(
            inputs,
            {
                'width': slide_width * .7,
                'x_offset': x_offset
            },
            'header', 1,
            parent_row
        )

    def render(self, slide):
        pass


class LogoCell(Cell):
    def __init__(self, inputs, slide_width, x_offset, parent_row):
        margin = Cm(.5)

        super().__init__(
            inputs,
            {
                'width': slide_width * .15,
                'x_offset': x_offset - margin
            },
            'logo', 2,
            parent_row
        )

        self.picture_width = Cm(5.57)
        self.picture_height = Cm(2.67)

    def render(self, slide):
        with importlib.resources.path(profero.assets, 'logo.png') as p:
            logo_path = str(p)
        slide.shapes.add_picture(
            logo_path,
            self.x_offset + self.width / 2 - self.picture_width / 2,
            self.parent_row.y_offset + self.parent_row.height / 2 - self.picture_height / 2,
            self.picture_width, self.picture_height
        )
