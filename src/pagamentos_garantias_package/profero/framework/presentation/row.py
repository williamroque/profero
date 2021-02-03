"""
Esse módulo contém a classe `Row`.
"""


class Row():
    """
    Essa classe controla as instâncias da classe `Cell`; representa uma linha (fileira).
    """

    def __init__(self, inputs, props, row_id, index, parent_slide):
        """
        * `inputs (dict)` -- Valores de entrada.
        * `props (dict)` -- Propriedades da fileira.
        * `row_id (str)` -- ID da fileira.
        * `index (int)` -- Posição relativa da fileira.
        * `parent_slide (Slide)` -- Slide que contém essa fileira.
        """

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

    def add_cell(self, cell):
        """
        Adicionar uma instância de `Cell`.

        * `cell (Cell)` -- A instância a ser adicionada.
        """

        self.cells.append(cell)

    def query(self, cell_id):
        """
        Encontrar uma instância `Cell` que tenha o id especificado.

        * `cell_id (str)` -- O ID da célula a ser procurada.
        """

        # Usar um gerador para parar no primeiro valor válido
        search_generator = (cell for cell in self.cells if cell.cell_id == cell_id)
        try:
            return next(search_generator)
        except StopIteration:
            return None

    def render(self, slide):
        """
        Chamar método `render` em todas as instâncias `Cell`.

        * `slide (Slide)` -- A instância `Slide`.
        """

        for cell in self.cells:
            cell.render(slide)
