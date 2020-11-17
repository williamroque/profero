from profero.util.input import Input
from profero.presentation.slideshow import Slideshow


def main():
    print('Processing inputs.', flush=True)

    # Processar stdin
    inputs = Input()

    print('Inputs processed.\n', flush=True)

    print('Rendering presentation.', flush=True)

    # Construir e renderizar apresentação
    slideshow = Slideshow(inputs)
    slideshow.render()

    print('Presentation rendered.\n', flush=True)

