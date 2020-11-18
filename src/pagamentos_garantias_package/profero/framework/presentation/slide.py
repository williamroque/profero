from pptx.util import Pt


# Essa classe controla todas as instâncias da classe `Row` e representa o slide
class Slide():
    def __init__(self, inputs, slide_id, slide_type, index, background, parent_presentation):
        self.inputs = inputs

        # O id do slide para usar com o método `query` da classe `Presentation`
        self.slide_id = slide_id

        # O tipo do slide de acordo com o PowerPoint; o tipo 6 é o em branco
        self.slide_type = slide_type

        # A posição relativa do slide
        self.index = index

        # A classe `Presentation` que controla esse slide 
        self.parent_presentation = parent_presentation

        # Criar um slide novo pelo `python-pptx` de acordo com o tipo de
        # layout definido acima e salvar a instância criada da classe
        # `pptx.Slide`
        self.slide = parent_presentation.presentation.slides.add_slide(
            parent_presentation.presentation.slide_layouts[self.slide_type]
        )

        # O fundo a ser usado
        self.background = background

        if self.background != None:
            # Criar um `Shape` de imagem usando o `self.background` e ajustar
            # para cobrir todo o slide
            background_image = self.slide.shapes.add_picture(
                self.background,
                Pt(-1), Pt(-1),
                width=parent_presentation.presentation.slide_width + Pt(2),
                height=parent_presentation.presentation.slide_height + Pt(3)
            )

            # Forma não muito intuitiva de colocar a imagem no segundo plano
            self.slide.shapes._spTree.remove(background_image._element)
            self.slide.shapes._spTree.insert(2, background_image._element)

        # Armazena todas as instâncias da classe `Row`
        self.rows = []

    # Adicionar uma instância `Row`
    def add_row(self, row):
        self.rows.append(row)

    # Encontrar uma instância `Row` que tenha o id especificado
    def query(self, row_id):
        # Usar um gerador para parar no primeiro valor válido
        search_generator = (row for row in self.rows if row.id == row_id)
        try:
            return next(search_generator)
        except StopIteration:
            return None

    # Chamar o método `render` de todas as instâncias `Row`
    def render(self, presentation):
        for row in self.rows:
            row.render(self.slide)
