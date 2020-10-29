from pptx.util import Cm, Pt
from pptx.oxml.xmlchemy import OxmlElement
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor


class Cell():
    def __init__(self, inputs, props, cell_id, index, parent_row):
        self.inputs = inputs

        self.width = props['width']
        self.x_offset = props['x_offset']
        self.cell_id = cell_id
        self.index = index

        self.parent_row = parent_row

    def create_rect(self, x, y, rect_width, rect_height, fill_color=RGBColor(0xB, 0x5D, 0x77), inherit_shadow=False, show_border=False):
        shape = self.parent_row.parent_slide.slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            x, y,
            rect_width, rect_height
        )

        shape.shadow.inherit = inherit_shadow

        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color

        if not show_border:
            shape.line.fill.background()

        return shape


    def set_text(self, shape, text, alignment=PP_ALIGN.LEFT, font_family='Calibri', font_size=Pt(18), bold=False, italic=None, color=RGBColor(0xFF, 0xFF, 0xFF), link_address=None, vertical_anchor=MSO_ANCHOR.MIDDLE, margin_left=Cm(.25), margin_top=Cm(.25), margin_right=Cm(.25), margin_bottom=Cm(.25)):
        text_frame = shape.text_frame
        text_frame.clear()

        text_frame.vertical_anchor = vertical_anchor
        text_frame.margin_left = margin_left
        text_frame.margin_top = margin_top
        text_frame.margin_right = margin_right
        text_frame.margin_bottom = margin_bottom

        p = text_frame.paragraphs[0]
        p.alignment = alignment
        run = p.add_run()
        run.text = text
        run.hyperlink.address = link_address

        font = run.font
        font.name = font_family
        font.size = font_size
        font.bold = bold
        font.italic = italic
        font.color.rgb = color

    def sub_element(self, parent, tagname, **kwargs):
            element = OxmlElement(tagname)
            element.attrib.update(kwargs)
            parent.append(element)
            return element

    def set_shape_transparency(self, shape, alpha):
        ts = shape.fill._xPr.solidFill
        sF = ts.get_or_change_to_srgbClr()
        sE = self.sub_element(sF, 'a:alpha', val=str((100 - alpha) * 1000))

    def render(self, slide):
        pass
