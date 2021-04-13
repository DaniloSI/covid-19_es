import pandas as pd
from unidecode import unidecode
from pymongo import MongoClient, ReplaceOne


print('Obtendo Microdados...')
url = 'https://bi.static.es.gov.br/covid19/MICRODADOS.csv'
df = pd.read_csv(url, sep=';', encoding='cp1252')


print('Realizando a conversão de data e selecionando os casos confirmados...')
# Converte a data e seleciona os casos confirmados
df['DataNotificacao'] = pd.to_datetime(df['DataNotificacao'])
df.sort_values('DataNotificacao', inplace=True)
df = df.query('Classificacao == "Confirmados"').reset_index(drop=True)


print('Padronizando nomes de municípios e bairros...')
# Padroniza nome de municípios e bairros
df['Municipio'] = df['Municipio'].apply(lambda x: unidecode(str(x)).upper())
df['Bairro'] = df['Bairro'].apply(lambda x: unidecode(str(x)).upper())


print('Calculando casos, óbitos e curas...')
# Calcula o total diário e acumulado de confirmados
df['ConfirmadosAcumulado'] = df[['Municipio', 'Bairro', 'DataNotificacao']]\
    .groupby(['Municipio', 'Bairro'])\
    .cumcount() + 1

df['Confirmados'] = df[['Municipio', 'Bairro', 'DataNotificacao']]\
    .groupby(['Municipio', 'Bairro', 'DataNotificacao'])\
    .cumcount() + 1


# Calcula o total diário e acumulado de óbitos
df['Obitos'] = df['Evolucao'].apply(
    lambda evolucao: 1 if evolucao == 'Óbito pelo COVID-19' else 0)

df['ObitosAcumulado'] = df[['Municipio', 'Bairro', 'DataNotificacao', 'Obitos']]\
    .groupby(['Municipio', 'Bairro'])\
    .cumsum()

df['Obitos'] = df[['Municipio', 'Bairro', 'DataNotificacao', 'Obitos']]\
    .groupby(['Municipio', 'Bairro', 'DataNotificacao'])\
    .cumsum()


# Calcula o total diário e acumulado de curas
df['Curas'] = df['Evolucao'].apply(
    lambda evolucao: 1 if evolucao == 'Cura' else 0)

df['CurasAcumulado'] = df[['Municipio', 'Bairro', 'DataNotificacao', 'Curas']]\
    .groupby(['Municipio', 'Bairro'])\
    .cumsum()

df['Curas'] = df[['Municipio', 'Bairro', 'DataNotificacao', 'Curas']]\
    .groupby(['Municipio', 'Bairro', 'DataNotificacao'])\
    .cumsum()


# Contagem de Casos, Óbitos e Curas
grupo_base = ['DataNotificacao', 'Municipio', 'Bairro']

datas = df[['DataNotificacao']].drop_duplicates().reset_index(drop=True)
municipios_bairros = df[['Municipio', 'Bairro']
                        ].drop_duplicates().reset_index(drop=True)

datas['key'] = 0
municipios_bairros['key'] = 0

df_counts = pd.merge(datas, municipios_bairros, how='outer')[grupo_base]

df_counts = df_counts.merge(
    df[[
        'Municipio',
        'Bairro',
        'DataNotificacao',
        'Confirmados',
        'Obitos',
        'Curas',
        'ConfirmadosAcumulado',
        'ObitosAcumulado',
        'CurasAcumulado'
    ]].drop_duplicates(grupo_base, keep='last')
    .dropna(),
    on=grupo_base,
    how='left'
)

df_counts.fillna(
    {
        'Confirmados': 0,
        'Obitos': 0,
        'Curas': 0,
    },
    inplace=True
)

columns_ffill = ['ConfirmadosAcumulado', 'ObitosAcumulado', 'CurasAcumulado']

df_counts[columns_ffill] = df_counts.groupby(['Municipio', 'Bairro'])\
    .fillna(method='ffill')\
    .fillna(0)[columns_ffill]


print('Preparando para salvar o DataFrame resultante...')
# Persiste o DataFrame
usr = 'danilosi'
pwd = 'QRGrkX9BvrgRWi2O'
str_conn = f'mongodb+srv://{usr}:{pwd}@sandbox.nuzlk.mongodb.net/covid-19-es?retryWrites=true&w=majority'
client = MongoClient(str_conn)

df_counts['_id'] = pd.Series(
    list(map(lambda x_id: x_id['_id'], list(client.db.dados.find({}, {'_id': 1})))))
df_counts['_id'].fillna('', inplace=True)

df_counts_dict = df_counts.to_dict(orient='records')

print('Inserindo novos registros...')
client.db.dados.bulk_write(
    list(map(lambda row: ReplaceOne(
        {'_id': row['_id']}, row, upsert=True), df_counts_dict))
)

print('Fim')
