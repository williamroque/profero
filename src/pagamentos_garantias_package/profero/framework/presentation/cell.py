class Cell():
    def __init__(self, inputs, props, cell_id, index, parent_row):
        self.inputs = inputs

        self.width = props['width']
        self.x_offset = props['x_offset']
        self.cell_id = cell_id
        self.index = index

        self.parent_row = parent_row

    def render(self, slide):
        pass
