from spreadsheet_parser import Parser

schema = {
    'file-type': 'csv',
    'sections': {
        'root': {
            'header-row': 4,
            'groups': {
                'data': {
                    'query': 'DATA',
                    'dtype': 'date'
                },
                'vn': {
                    'query': 'VN',
                    'dtype': 'float'
                },
                'juros': {
                    'query': ' JUROS (R$) ',
                    'dtype': 'float'
                }
            }
        }
    }
}

parser = Parser(schema)
data_column = parser.read('~/desktop/18_pu.csv')['root']['juros']
print(data_column)
