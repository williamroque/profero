import sys

import numpy

from spreadsheet_parser import Parser
from models import boletim_schema, saldo_schema

numpy.set_printoptions(threshold=sys.maxsize)

parser = Parser(boletim_schema)
data_column = parser.read('~/desktop/boletins/apr-20.csv')['root']['valores']
print(data_column, '\n\n')

parser = Parser(saldo_schema)
data_column = parser.read('~/desktop/saldos/Saldo 27a28as.xls')['root']

for cliente, atraso in zip(data_column['cliente'], data_column['atraso']):
    print(cliente, ' --- ', atraso)
