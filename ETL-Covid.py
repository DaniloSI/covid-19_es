import pandas as pd
from unidecode import unidecode
from pymongo import MongoClient
from sys import argv
import os
from datetime import date


production = not ('MODE' in os.environ and os.environ['MODE'] == 'development')

mode = 'Production' if production else 'Development'
print(f'Executando no modo "{mode}"')

print('Obtendo Microdados...')
url = 'MICRODADOS.zip'

if production:
    url = 'https://bi.s3.es.gov.br/covid19/MICRODADOS.zip'

df = pd.read_csv(url, sep=';', encoding='cp1252')\
    .query('Classificacao == "Confirmados"')\
    .reset_index(drop=True)


print('Realizando a conversão de data e selecionando os casos confirmados...')

# Obtém a data de confirmação do caso, seguindo o mesmo critério do Painel da Covid-19 (data da coleta do exame ou do encerramento do caso)
df['DataConfirmado'] = df['DataColeta_RT_PCR'].combine_first(df['DataColetaTesteRapido'])\
    .combine_first(df['DataColetaSorologia'])\
    .combine_first(df['DataColetaSorologiaIGG'])\
    .combine_first(df['DataEncerramento'])

# Deleta os dados que não possuem data de confirmação.
df = df[df['DataConfirmado'].notna()]

# Deleta os dados que possuem datas antes da pandemia e depois de hoje.
df = df.query(f'DataConfirmado >= "2020-01-01" & DataConfirmado <= "{date.today().isoformat()}"')

# Converte a data e seleciona os casos confirmados
df['DataNotificacao'] = pd.to_datetime(df['DataConfirmado'])
df['DataObito'] = pd.to_datetime(df['DataObito'])
df.sort_values('DataNotificacao', inplace=True)


print('Padronizando nomes de municípios e bairros...')
# Padroniza nome de municípios e bairros
converte_nome = lambda tipo_regiao: df[tipo_regiao].apply(lambda x: unidecode(str(x)).upper())

df['Municipio'] = converte_nome('Municipio')
df['Bairro'] = converte_nome('Bairro')


print('Calculando casos, óbitos e curas...')
grupo_base = ['DataNotificacao', 'Municipio', 'Bairro']

datas = pd.concat([df['DataNotificacao'], df[df['DataObito'].notna()]['DataObito']])\
    .drop_duplicates()\
    .reset_index()\
    .rename({0: 'DataNotificacao'}, axis=1)\
    .drop('index', axis=1)

municipios_bairros = df[['Municipio', 'Bairro']].drop_duplicates().reset_index(drop=True)
    
datas['key'] = 0
municipios_bairros['key'] = 0

# Calcula o total diário de confirmados
df['Confirmados'] = 1
df['Curas'] = df['Evolucao'].apply(lambda e: 1 if e == 'Cura' else 0)
df['Obitos'] = df['Evolucao'].apply(lambda e: 1 if e == 'Óbito pelo COVID-19' else 0)

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
    how='outer'
).fillna(0)

df_datas_municipios = pd.merge(datas, municipios_bairros, how='outer')[grupo_base]

df_counts = df_datas_municipios.merge(
    df_counts,
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
df_counts_by_week = df_counts.groupby(['Municipio', 'Bairro', pd.Grouper(key='DataNotificacao', freq='W', label='left', closed='left')])[columns_sum]\
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
str_conn = 'mongodb://localhost'

if production:
    usr = argv[1]
    pwd = argv[2]
    str_conn = f'mongodb+srv://{usr}:{pwd}@es-covid-19.nuzlk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

client = MongoClient(str_conn)

df_counts_by_week_dict = df_counts_by_week.to_dict(orient='records')

print('Deletando banco de dados existente...')
client.drop_database('db')

print(f'Inserindo {len(df_counts_by_week_dict)} dados...')
if len(df_counts_by_week_dict) > 0:
    client.db.dados.insert_many(df_counts_by_week_dict)

print('Fim')
