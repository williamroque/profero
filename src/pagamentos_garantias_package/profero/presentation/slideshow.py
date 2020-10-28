import importlib
from pptx.util import Cm

from profero.framework.presentation.presentation import Presentation


class Slideshow(Presentation):
    def __init__(self, inputs):
        super().__init__(
            inputs,
            {
                'width': Cm(33.87),
                'height': Cm(19.05),
                'output_path': inputs.get('output-path')
            }
        )

        for slide in inputs.get('slides'):
            module = importlib.import_module(
                'profero.presentation.slides.{}.slide'.format(slide['id'])
            )
            self.add_slide(module.Slide(inputs, slide['inputs'], self))

