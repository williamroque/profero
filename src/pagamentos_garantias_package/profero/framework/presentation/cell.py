from pptx.oxml.xmlchemy import OxmlElement


class Cell():
    def __init__(self, inputs, props, cell_id, index, parent_row):
        self.inputs = inputs

        self.width = props['width']
        self.x_offset = props['x_offset']
        self.cell_id = cell_id
        self.index = index

        self.parent_row = parent_row

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
