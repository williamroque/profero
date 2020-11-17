import sys
import json
import copy


# Essa classe puxa os dados de entrada do stdin e processa eles
class Input():
    def __init__(self):
        self.inputs = json.loads(sys.stdin.readlines()[0])

    # Mapear valor de uma entrada (fonte) a outra (alvo) com uma função
    def apply_map(self, source, target, callback):
        self.inputs[target] = {} # Criar alvo

        # Se a fonte for uma lista, iterar sobre fonte, aplicando a função
        # Senão, aplicar função no valor escalar
        for key, value in self.inputs[source].items():
            if type(value) == list:
                self.inputs[target][key] = []
                for x in value:
                    self.inputs[target][key].append(callback(x))
            else:
                self.inputs[target][key] = callback(value)

    # Puxar valor
    def get(self, key):
        return self.inputs[key]

    # Atualizar valor
    def update(self, key, value):
        self.inputs[key] = value
