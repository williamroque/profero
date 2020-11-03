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

        table_of_contents_slide = None

        for slide_i, slide in enumerate(inputs.get('slides')):
            module = importlib.import_module(
                'profero.presentation.slides.{}.slide'.format(slide['id'])
            )

            module_slide = module.Slide(
                inputs,
                slide_i,
                slide['inputs'],
                table_of_contents_slide,
                self
            )

            if module_slide.slide_id == 'table-of-contents':
                table_of_contents_slide = module_slide

            self.add_slide(module_slide)

