import sys

import numpy

from spreadsheet_parser import Parser
from models import *

numpy.set_printoptions(threshold=sys.maxsize)

parser = Parser(boletim_schema)
data = parser.read('~/desktop/boletins/apr-20.csv')['root']['valores']
print(data, '\n\n')

parser = Parser(saldo_schema)
data = parser.read('~/desktop/saldos/Saldo 27a28as.xls')['root']

for cliente, atraso in zip(data['cliente'], data['atraso']):
    print(cliente, ' --- ', atraso)

parser = Parser(estoque_schema)
data = parser.read('~/desktop/estoque/ESTOQUE LONDRINA - BASE JAN.2021.xlsx')
print(data)
