from pptx.util import Cm, Pt, Inches
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

from profero.framework.presentation.slide import Slide as FSlide
from profero.framework.presentation.row import Row
from profero.framework.presentation.cell import Cell
from profero.presentation.slides.common.header import HeaderRow
from profero.presentation.slides.common.note import NoteCell

import matplotlib.pyplot as plt
import numpy as np

import io

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR')


NOTE = """
➢ Curva: pagamentos previstos na curva de amortização original dos CRI
➢ Pagamentos: valores efetivamente pagos a título de amortização e juros dos CRI seniores e subordinado
➢ Valores em reais
""".strip()


class ChartCell(Cell):
    def __init__(self, inputs, slide_width, props, parent_row):
        super().__init__(
            inputs,
            {
                'width': slide_width,
                'x_offset': 0
            },
            'chart', 0,
            parent_row
        )

        self.slide_width = slide_width
        self.props = props

    def render(self, slide):
        primeira_serie = str(self.inputs.get('primeira-serie'))
        segunda_serie = str(self.inputs.get('primeira-serie') + 1)

        atual_inputs = zip(
            self.props[primeira_serie],
            self.props[segunda_serie]
        )

        months = []
        curva = []
        pagamento = []
        juros_sen = []
        amort_sen = []
        amex_sen = []
        juros_sub = []
        amort_sub = []
        amex_sub = []

        for sen, sub in atual_inputs:
            months.append(sen[0])

            curva.append(
                sen[1] + sen[2] +\
                sub[1] + sub[2]
            )
            pagamento.append(
                sen[1] + sen[2] + sen[3] +\
                sub[1] + sub[2] + sub[3]
            )

            juros_sen.append(sen[1])
            juros_sub.append(sub[1])

            amort_sen.append(sen[2])
            amort_sub.append(sub[2])

            amex_sen.append(sen[3])
            amex_sub.append(sub[3])

        labels = [
            'Curva',
            'Amortização Seniores',
            'Juros Seniores',
            'AMEX Seniores',
            'Amortização Subordinada',
            'Juros Subordinada',
            'AMEX Subordinada',
            'Pagamento',
            'Recebimento'
        ]
        values = np.array(list(zip(
            curva,
            amort_sen,
            juros_sen,
            amex_sen,
            amort_sub,
            juros_sub,
            amex_sub,
            pagamento,
            self.props['recebimento']
        ))).T

        chart_width = 11.24
        chart_height = 4.52

        plot_width = .7
        plot_x = 1/2 - plot_width/2 + .1

        plot_height = .5
        plot_y = .47 # unintuitive, but positive values offset upwards (positive Cartesian coordinates)

        fig = plt.figure(figsize=(chart_width, chart_height))
        ax = fig.add_axes([plot_x, plot_y, plot_width, plot_height])

        ax.plot(values)
        plt.xticks([])

        ax.table(cellText=values,
                  rowLabels=labels,
                  #rowColours=,
                  colLabels=months,
                  loc='bottom')

        image_stream = io.BytesIO()
        fig.savefig(image_stream, format='png', dpi=300)

        chart_width = Inches(chart_width)
        chart_height = Inches(chart_height)

        slide.shapes.add_picture(
            image_stream,
            self.slide_width / 2 - chart_width / 2,
            self.parent_row.y_offset + self.parent_row.height / 2 - chart_height / 2,
            chart_width,
            chart_height
        )

        slide = self.parent_row.parent_slide
        slide.table_of_contents_slide.add_entry(
            slide.title, [slide.index + 1], slide
        )


class Slide(FSlide):
    def __init__(self, inputs, index, props, table_of_contents_slide, parent_presentation):
        super().__init__(
            inputs,
            'pagamentos-x-curva', 6,
            index,
            None,
            parent_presentation
        )

        self.title = 'Pagamentos _x_ Curva'

        self.props = props

        self.table_of_contents_slide = table_of_contents_slide

        slide_height = parent_presentation.presentation.slide_height
        slide_width = parent_presentation.presentation.slide_width

        note_height = Cm(2.04)

        header_row = HeaderRow(
            inputs,
            {
                'height': .25 * slide_height,
                'y_offset': Cm(0)
            }, 0,
            self.title,
            slide_width, slide_height,
            self
        )
        self.add_row(header_row)

        chart_row = Row(
            inputs,
            {
                'height': .75 * slide_height - note_height,
                'y_offset': header_row.y_offset + header_row.height
            },
            'chart', 1,
            self
        )

        chart_cell = ChartCell(inputs, slide_width, self.props, chart_row)
        chart_row.add_cell(chart_cell)

        self.add_row(chart_row)

        note_row = Row(
            inputs,
            {
                'height': note_height,
                'y_offset': chart_row.y_offset + chart_row.height
            },
            'note', 2,
            self
        )

        note_cell = NoteCell(
            inputs,
            slide_width,
            NOTE,
            note_row
        )
        note_row.add_cell(note_cell)

        self.add_row(note_row)
