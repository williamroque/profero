import time
import locale

import os
import json

import numpy as np

from profero.util.input import Input
from profero.presentation.slideshow import Slideshow


locale.setlocale(locale.LC_TIME, 'pt_BR')


def main():
    print('Processing inputs.', flush=True)

    inputs = Input()

    print('Inputs processed.\n', flush=True)

    print('Rendering presentation.', flush=True)

    slideshow = Slideshow(inputs)
    slideshow.render()

    print('Presentation rendered.\n', flush=True)

