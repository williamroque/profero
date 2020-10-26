import pptx

class Presentation():
    def __init__(self, inputs, props):
        self.inputs = inputs

        self.slides = []

        self.presentation = pptx.Presentation()
        self.presentation.slide_width = props['width']
        self.presentation.slide_height = props['height']

        self.output_path = props['output_path']

    def add_slide(self, slide):
        self.slides.append(slide)

    def query(self, slide_id):
        search_generator = (slide for slide in self.slides if slide.id == slide_id)
        try:
            return next(search_generator)
        except StopIteration:
            return None

    def render(self):
        for slide in self.slides:
            slide.render(self.presentation)
        self.presentation.save(self.output_path)
