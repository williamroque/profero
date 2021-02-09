"""Esse módulo contém os modelos dos diferentes tipos de planilha."""

boletim_schema = {
    'file-type': 'csv',
    'sections': {
        'root': {
            'header-query': [0, 'Identificação'],
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

saldo_schema = {
    'file-type': 'xslx',
    'sections': {
        'root': {
            'header-query': [0, 'Filial'],
            'groups': {
                'cliente': {
                    'query': 'Cliente',
                    'subquery': ['Estado', 'SC'],
                    'dtype': 'string'
                },
                'atraso': {
                    'query': 'Valor Atraso',
                    'subquery': ['Estado', 'SC'],
                    'dtype': 'float'
                }
            }
        }
    }
}
