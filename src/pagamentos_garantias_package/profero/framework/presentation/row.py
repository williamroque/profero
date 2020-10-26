class Row():
    def __init__(self, inputs, props, row_id, index, parent_slide):
        self.inputs = inputs

        self.height = props['height']
        self.y_offset = props['y_offset']
        self.row_id = row_id
        self.index = index

        self.parent_slide = parent_slide

        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def query(self, cell_id):
        search_generator = (cell for cell in self.cells if cell.id == cell_id)
        try:
            return next(search_generator)
        except StopIteration:
            return None

    def render(self, slide):
        for cell in self.cells:
            cell.render(slide)
