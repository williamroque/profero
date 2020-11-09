from pptx.util import Cm, Pt, Inches
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.path
import matplotlib.patches as patches

from profero.framework.presentation.slide import Slide as FSlide
from profero.framework.presentation.row import Row
from profero.framework.presentation.cell import Cell
from profero.presentation.slides.common.header import HeaderRow
from profero.presentation.slides.common.note import NoteCell

import re
import io


NOTE = """
➢ Valores com base em {}
➢ O Gatilho de Sobregarantia é calculado a partir da razão entre o saldo dos Direitos Creditórios Adimplidos e o saldo devedor dos CRI
➢ Direitos Creditórios Inadimplidos são os recebíveis cujas prestações não tenham sido pagas a partir do 91º dia a contar do respectivo vencimento
➢ Limíte de Garantia Mínima: {:.0%}
""".strip()


class ChartCell(Cell):
    def __init__(self, inputs, slide_width, props, parent_row):
        super().__init__(
            inputs,
            {
                'width': slide_width,
                'x_offset': 0
            },
            'table', 0,
            parent_row
        )

        self.slide_width = slide_width
        self.props = props

    def render(self, slide):
        slide = self.parent_row.parent_slide

        values = np.array([
            self.props['direitos-creditorios-adimplidos'],
            self.props['direitos-creditorios-inadimplidos'],
            self.props['estoque'],
            self.props['fundo-reserva']
        ])

        labels = (
            'Direitos Creditórios Adimplidos',
            'Direitos Creditórios Inadimplidos',
            'Estoque',
            'Fundo de Reserva'
        )

        annotations = [
            (
                'Saldo do CRI – R$ {:.2f} MM'.format(
                    self.inputs.get('saldo-cri') / 1e+6
                ),
                self.inputs.get('saldo-cri')
            ),
            (
                'Limite de Garantia Mínima – {:.0%} – R$ {:.2f} MM'.format(
                    self.props['garantia-minima'] / self.inputs.get('saldo-cri'),
                    self.props['garantia-minima'] / 1e+6
                ).replace('.', ','),
                self.props['garantia-minima']
            ),
            (
                'Gatilho de Sobregarantia – {:.0%} – R$ {:.2f} MM'.format(
                    self.props['gatilho-sobregarantia'] / self.inputs.get('saldo-cri'),
                    self.props['gatilho-sobregarantia'] / 1e+6
                ).replace('.', ','),
                self.props['gatilho-sobregarantia']
            ),
            (
                'Garantia Total da Operação – {:.0%} – R$ {:.2f} MM'.format(
                    values.sum() / self.inputs.get('saldo-cri'),
                    values.sum() / 1e+6
                ).replace('.', ','),
                values.sum()
            )
        ]

        chart_width = 11.24
        chart_height = 4.52

        plot_width = .4
        plot_x = 1/2 - plot_width/2 + .1

        fig = plt.figure(figsize=(chart_width, chart_height))
        ax = fig.add_axes([plot_x, .05, plot_width, .9])

        ax.tick_params(
            axis='x',
            which='both',
            bottom=False,
            top=False,
            labelbottom=False
        )

        ax.tick_params(
            axis='y',
            colors='#0F3B5E',
            labelsize=8
        )

        ax.ticklabel_format(useOffset=False, style='plain')
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:,.2f}'.format(x) if x != 0 else '-'))

        ax.spines['bottom'].set_color('#ddd')
        ax.spines['top'].set_color('#ddd')
        ax.spines['left'].set_color('#666')
        ax.spines['right'].set_color('#fff')

        ticks = np.arange(10) * 10 ** (len(str(int(sum(values)))) - 1)
        plt.yticks(ticks=ticks)

        ax.grid(
            axis='y',
            color='#eee'
        )
        ax.set_axisbelow(True)

        ax.set_xlim(-.5, .5)

        bar_width = .4

        colors = ['#222A35', '#333F50', '#8497B0', '#ADB9CA']
        font_colors = ['#fff', '#ddd', '#222', '#000']

        bars = []
        for (i, value), csum in zip(enumerate(values), values.cumsum()):
            bottom = csum - value

            bars.append(
                ax.bar(
                    0, value,
                    bar_width, bottom=bottom,
                    color=colors[i]
                )[0]
            )
            plt.text(
                0, bottom + value / 2,
                'R$ {:.2f} MM'.format(
                    value / 1e+6
                ).replace('.', ','),
                ha='center', va='center',
                color=font_colors[i],
                fontsize=9,
                fontweight='bold'
            )

        for note, value in annotations:
            arrow = patches.FancyArrowPatch(
                (-.3, value),
                (.3, value),
                arrowstyle='Simple,head_width=5,head_length=10'
            )

            ax.add_patch(arrow)

            v1 = arrow.get_path().vertices[0:3, :]
            c1 = arrow.get_path().codes[0:3]
            p1 = matplotlib.path.Path(v1, c1)
            pp1 = patches.PathPatch(p1, color='#000', linestyle='--', fill=False, lw=.8)
            arrow.axes.add_patch(pp1)

            v2 = arrow.get_path().vertices[3:8, :]
            c2 = arrow.get_path().codes[3:8]
            c2[0] = 1
            p2 = matplotlib.path.Path(v2,c2)
            pp2 = patches.PathPatch(p2, color='#000', lw=1.5, linestyle='-')
            arrow.axes.add_patch(pp2)
            arrow.remove()

            ax.text(
                .31,
                (value / values.sum() - .01) * values.sum(), note,
                fontsize=7
            )

        ax.legend(
            bars,
            labels,
            bbox_to_anchor=(-.3, .5),
            frameon=False
        )

        image_stream = io.BytesIO()
        fig.savefig(image_stream, format='png')

        chart_width = Inches(chart_width)
        chart_height = Inches(chart_height)

        slide.slide.shapes.add_picture(
            image_stream,
            self.slide_width / 2 - chart_width / 2,
            self.parent_row.y_offset + self.parent_row.height / 2 - chart_height / 2,
            chart_width,
            chart_height
        )

        slide.table_of_contents_slide.add_entry(
            slide.title, [slide.index + 1], self.parent_row.parent_slide
        )


class Slide(FSlide):
    def __init__(self, inputs, index, props, table_of_contents_slide, parent_presentation):
        super().__init__(
            inputs,
            'garantia', 6,
            index,
            None,
            parent_presentation
        )

        self.title = 'Garantia'

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
            NOTE.format(
                inputs.get('date'),
                props['garantia-minima'] / inputs.get('saldo-cri')
            ),
            note_row
        )
        note_row.add_cell(note_cell)

        self.add_row(note_row)
