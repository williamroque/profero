import pandas as pd


class Parser():
    def __init__(self, schema):
        self.schema = schema

    def read(self, path):
        if self.schema['file-type'] == 'xslx':
            df = pd.read_excel(path, header=None)
        else:
            df = pd.read_csv(path, header=None)

        result = {}

        for section_id, section in self.schema['sections'].items():
            df.columns = df.iloc[section['header-row']]

            result[section_id] = {}

            for group_id, group in section['groups'].items():
                if group['dtype'] == 'date':
                    df[group['query']] = pd.to_datetime(df[group['query']], errors='coerce')
                    df = df.dropna(subset=[group['query']])

                    result[section_id][group_id] = df[group['query']].to_numpy()
                elif group['dtype'] == 'float':
                    df[group['query']][df[group['query']].apply(lambda x: str(x).isnumeric())]
                    result[section_id][group_id] = df[group['query']].to_numpy()

        return result
