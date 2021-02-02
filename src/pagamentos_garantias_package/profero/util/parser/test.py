import sys

import numpy

from spreadsheet_parser import Parser

numpy.set_printoptions(threshold=sys.maxsize)

schema = {
    'file-type': 'csv',
    'sections': {
        'root': {
            'header-row': 7,
            'groups': {
                'valores': {
                    'query': 'Valor\nPago',
                    'subquery': ['Identificação', 'Total Geral:'],
                    'dtype': 'float',
                },
            }
        }
    }
}

parser = Parser(schema)
data_column = parser.read('~/desktop/boletins/jan-20.csv')['root']['valores']
print(data_column)
