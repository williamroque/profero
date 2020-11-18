import pptx


# Essa clase controla todas as instâncias `Slide` e representa a apresentação
# enteira
class Presentation():
    def __init__(self, inputs, props):
        self.inputs = inputs

        # Armazena todos as instâncias `Slide`
        self.slides = []

        # Inicializar uma instância da classe `pptx.Presentation` do `python-pptx`
        self.presentation = pptx.Presentation()
        self.presentation.slide_width = props['width']
        self.presentation.slide_height = props['height']

        # O caminho do arquivo de saída
        self.output_path = props['output_path']

    # Adicionar uma instância `Slide`
    def add_slide(self, slide):
        self.slides.append(slide)

    # Ver comentário no arquivo `slide.py`
    def query(self, slide_id):
        search_generator = (slide for slide in self.slides if slide.id == slide_id)
        try:
            return next(search_generator)
        except StopIteration:
            return None

    # Chamar o método `render` em todas as instâncias `Slide` e salvar a
    # apresentação no arquivo de saída
    def render(self):
        for slide in self.slides:
            slide.render(self.presentation)
        self.presentation.save(self.output_path)
