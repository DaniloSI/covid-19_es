import pandas as pd
from unidecode import unidecode
from pymongo import MongoClient, ReplaceOne
from sys import argv

print('Obtendo Microdados...')
# url = 'https://bi.s3.es.gov.br/covid19/MICRODADOS.zip'
url = 'MICRODADOS.zip'
df = pd.read_csv(url, sep=';', encoding='cp1252')


print('Realizando a conversão de data e selecionando os casos confirmados...')
# Converte a data e seleciona os casos confirmados
df['DataNotificacao'] = pd.to_datetime(df['DataNotificacao'])
df['DataObito'] = pd.to_datetime(df['DataObito'])
df.sort_values('DataNotificacao', inplace=True)
df = df.query('Classificacao == "Confirmados"').reset_index(drop=True)


print('Padronizando nomes de municípios e bairros...')
# Padroniza nome de municípios e bairros
df['Municipio'] = df['Municipio'].apply(lambda x: unidecode(str(x)).upper())
df['Bairro'] = df['Bairro'].apply(lambda x: unidecode(str(x)).upper())


print('Calculando casos, óbitos e curas...')
grupo_base = ['DataNotificacao', 'Municipio', 'Bairro']

datas = df[['DataNotificacao']].drop_duplicates().reset_index(drop=True)
municipios_bairros = df[['Municipio', 'Bairro']
                        ].drop_duplicates().reset_index(drop=True)

datas['key'] = 0
municipios_bairros['key'] = 0

# Calcula o total diário de confirmados
df['Confirmados'] = 1
df['Curas'] = df['Evolucao'].apply(lambda e: 1 if e == 'Cura' else 0)
df['Obitos'] = df['Evolucao'].apply(
    lambda e: 1 if e == 'Óbito pelo COVID-19' else 0)

df_confirmados_curas = df[['Municipio', 'Bairro', 'DataNotificacao', 'Confirmados', 'Curas']]\
    .groupby(['Municipio', 'Bairro', 'DataNotificacao'])\
    .sum()\
    .reset_index()

df_obitos = df[['Municipio', 'Bairro', 'DataObito', 'Obitos']]\
    .groupby(['Municipio', 'Bairro', 'DataObito'])\
    .sum()\
    .reset_index()\
    .rename({'DataObito': 'DataNotificacao'}, axis=1)

df_counts = df_confirmados_curas.merge(
    df_obitos,
    on=grupo_base,
    how='left'
).fillna(0)

columns_sum = ['Confirmados', 'Obitos', 'Curas']
df_counts_by_week = df_counts.groupby(['Municipio', 'Bairro', pd.Grouper(key='DataNotificacao', freq='7D')])[columns_sum]\
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
usr = argv[1]
pwd = argv[2]
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
