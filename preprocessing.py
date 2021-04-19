import pandas as pd
from unidecode import unidecode
from pymongo import MongoClient, ReplaceOne


print('Obtendo Microdados...')
url = 'https://bi.s3.es.gov.br/covid19/MICRODADOS.zip'
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
# Calcula o total diário de confirmados
df['Confirmados'] = df[['Municipio', 'Bairro', 'DataNotificacao']]\
    .groupby(['Municipio', 'Bairro', 'DataNotificacao'])\
    .cumcount() + 1

# Calcula o total diário de óbitos
df['Obitos'] = df['Evolucao'].apply(
    lambda evolucao: 1 if evolucao == 'Óbito pelo COVID-19' else 0)

df['Obitos'] = df[['Municipio', 'Bairro', 'DataNotificacao', 'Obitos']]\
    .groupby(['Municipio', 'Bairro', 'DataNotificacao'])\
    .cumsum()


# Calcula o total diário e acumulado de curas
df['Curas'] = df['Evolucao'].apply(
    lambda evolucao: 1 if evolucao == 'Cura' else 0)

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

columns_sum = ['Confirmados', 'Obitos', 'Curas']
df_counts_by_week = df_counts.groupby(['Municipio', 'Bairro', pd.Grouper(key='DataNotificacao', freq='W-MON')])[columns_sum]\
    .sum()\
    .reset_index()\
    .sort_values('DataNotificacao')

df_counts_by_week['ConfirmadosAcumulado'] = df_counts_by_week[['Municipio', 'Bairro', 'DataNotificacao', 'Confirmados']]\
    .groupby(['Municipio', 'Bairro'])\
    .cumsum()

df_counts_by_week['ObitosAcumulado'] = df_counts_by_week[['Municipio', 'Bairro', 'DataNotificacao', 'Obitos']]\
    .groupby(['Municipio', 'Bairro'])\
    .cumsum()

df_counts_by_week['CurasAcumulado'] = df_counts_by_week[['Municipio', 'Bairro', 'DataNotificacao', 'Curas']]\
    .groupby(['Municipio', 'Bairro'])\
    .cumsum()

print('Preparando para salvar o DataFrame resultante...')
# Persiste o DataFrame
usr = 'danilosi'
pwd = 'QRGrkX9BvrgRWi2O'
str_conn = f'mongodb+srv://{usr}:{pwd}@covid-19-es.nuzlk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(str_conn)

ids = list(map(lambda x_id: x_id['_id'], list(
    client.db.dados.find({}, {'_id': 1}))))

df_counts_by_week['_id'] = pd.Series(ids)
df_counts_by_week['_id'].fillna('', inplace=True)

df_counts_by_week_dict = df_counts_by_week.to_dict(orient='records')


def delete_ids_empty(item):
    if (item['_id'] == ''):
        del item['_id']
    return item


df_counts_by_week_dict = list(map(delete_ids_empty, df_counts_by_week_dict))

print('Fazendo replace dos dados existentes...')
to_replace = list(
    filter(lambda row: '_id' in row.keys(), df_counts_by_week_dict))
if len(to_replace) > 0:
    client.db.dados.bulk_write(
        list(map(lambda row: ReplaceOne(
            {'_id': row['_id']}, row, upsert=True), to_replace))
    )

print('Fazendo inserindo novos dados...')
to_insert = list(
    filter(lambda row: '_id' not in row.keys(), df_counts_by_week_dict))
if len(to_insert) > 0:
    client.db.dados.insert_many(to_insert)

print('Fim')
