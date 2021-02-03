"""Esse módulo contém a subclasse `Slideshow`."""

import importlib
from pptx.util import Cm

from profero.framework.presentation.presentation import Presentation


class Slideshow(Presentation):
    """
    Subclasse do `Presentation` para uso como singleton.
    """

    def __init__(self, inputs):
        super().__init__(
            inputs,
            {
                'width': Cm(33.87),
                'height': Cm(19.05),
                'output_path': inputs.get('output-path')
            }
        )

        # Usar primeiro slide com o ID 'table-of-contents' (temas a serem abordados) como
        # o índice
        table_of_contents_slide = None

        for slide_i, slide in enumerate(inputs.get('slides')):
            # Importar módulo com o nome especificado pelo `manifest.json`
            module = importlib.import_module(
                'profero.presentation.slides.{}.slide'.format(slide['id'])
            )

            # Construir classe `Slide` do módulo
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
