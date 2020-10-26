class Slide():
    def __init__(self, inputs, slide_id, slide_type, background, parent_presentation):
        self.inputs = inputs

        self.slide_id = slide_id
        self.slide_type = slide_type

        self.parent_presentation = parent_presentation

        self.slide = parent_presentation.slides.add_slide(
            parent_presentation.slide_layouts[self.slide_type]
        )

        self.background = background

        if self.background != None:
            background_image = self.slide.shapes.add_picture(
                self.background,
                0, 0,
                width=parent_presentation.slide_width,
                height=parent_presentation.slide_height
            )

            self.slide.shapes._spTree.remove(background_image._element)
            self.slide.shapes._spTree.insert(2, background_image._element)

        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def query(self, row_id):
        search_generator = (row for row in self.rows if row.id == row_id)
        try:
            return next(search_generator)
        except StopIteration:
            return None

    def render(self, presentation):
        for row in self.rows:
            row.render(self.slide)
