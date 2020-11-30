# Essa classe controla as instâncias da classe `Cell`; representa uma linha (fileira)
class Row():
    def __init__(self, inputs, props, row_id, index, parent_slide):
        self.inputs = inputs

        # A altura da linha
        self.height = props['height']

        # A posição vertical da linha
        self.y_offset = props['y_offset']

        # O id da linha para uso com `query`
        self.row_id = row_id

        # A posição relativa da linha
        self.index = index

        # O slide que controla essa instância
        self.parent_slide = parent_slide

        # As instâncias da classe `Cell` que essa instância controla
        self.cells = []

    # Adicionar uma instância de `Cell`
    def add_cell(self, cell):
        self.cells.append(cell)

    # Procurar por uma instância `Cell`; ver comentário em `slide.py`
    def query(self, cell_id):
        search_generator = (cell for cell in self.cells if cell.cell_id == cell_id)
        try:
            return next(search_generator)
        except StopIteration:
            return None

    # Chamar método `render` em todas as instâncias `Cell`
    def render(self, slide):
        for cell in self.cells:
            cell.render(slide)
