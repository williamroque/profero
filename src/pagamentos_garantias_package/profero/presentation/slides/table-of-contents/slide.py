from pptx.util import Cm

from profero.framework.presentation.slide import Slide as FSlide
from profero.framework.presentation.row import Row

import importlib.resources
import profero.assets


class Slide(FSlide):
    def __init__(self, inputs, props, parent_presentation):
        with importlib.resources.path(profero.assets, 'background.png') as p:
            background_path = str(p)

        super().__init__(
            inputs,
            'table-of-contents', 6,
            background_path,
            parent_presentation
        )


