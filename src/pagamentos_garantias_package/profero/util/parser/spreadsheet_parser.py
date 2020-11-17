import pandas as pd


# Essa classe lê e processa planilhas `.xlsx` e `.csv`
class Parser():
    # O dicionário schema descreve o modelo da planilha
    def __init__(self, schema):
        self.schema = schema

    # Ler e processar planilha
    def read(self, path):
        # O modelo deve especificar se o formato do arquivo é `.xlsx` ou `.csv`.
        # Tive problemas com o `.xlsx` quando o arquivo foi gerado pelo MEGA
        # (provavelmente alguma inconsistência com as fórmulas ou metadados).
        # Converta em `.csv` e revise os valores quando for o caso.
        # Confira o arquivo `test.py` para ver um exemplo de modelo.
        if self.schema['file-type'] == 'xslx':
            df = pd.read_excel(path, header=None)
        else:
            df = pd.read_csv(path, header=None)

        result = {}

        # O modelo é divido em seções e as seções em grupos. Em geral,
        # as seções devem ser divisões lógicas com títulos na mesma linha.
        # Os grupos devem ser todos os valores de um só tipo embaixo do mesmo
        # título.
        for section_id, section in self.schema['sections'].items():
            # Configurar a linha especificada pelo modelo como o cabeçalho
            df.columns = df.iloc[section['header-row']]

            result[section_id] = {}

            # Iterar sobre grupos do modelo e adaptar valores da coluna de
            # acordo com o tipo dos dados
            for group_id, group in section['groups'].items():
                if group['dtype'] == 'date':
                    # Já que o tipo é data (ver ^), forçar a coluna a adotar
                    # o tipo `datetime64[ns]` do `pandas`
                    df[group['query']] = pd.to_datetime(df[group['query']], errors='coerce')

                    # Remover todos os valores `NaN` criados acima e por
                    # células em branco
                    df = df.dropna(subset=[group['query']])

                    # Converter a coluna em uma matriz `numpy` unidimensional
                    result[section_id][group_id] = df[group['query']].to_numpy()
                elif group['dtype'] == 'float':
                    # Já que o tipo é decimal/numérico (ver ^), filtrar a coluna por valores
                    # numéricos
                    df[group['query']][df[group['query']].apply(lambda x: str(x).isnumeric())]

                    # Converter a coluna em uma matriz `numpy` unidimensional
                    result[section_id][group_id] = df[group['query']].to_numpy()

        return result
