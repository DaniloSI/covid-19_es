# Tratamento de Dados (Indicadores Municipais do ES)
# --------------------------------------------------
#
# Dados obitidos através do site IBGE Cidades, pelo link: https://www.ibge.gov.br/cidades-e-estados/es/
# 
# Para obter os dados e torná-los prontos para o processamento, siga o passo-a-passo abaixo:
# 1. Acesse o link mencionado e clique em "exportar";
# 2. Selecione "Todos os Municípios - ES", clique em "XLS" e faça o download;
# 3. Após realizar o download da planilha, renomeie-a para "municipios.xls" e coloque na mesma pasta do presente notebook.
#

import pandas as pd
import xlrd
import numpy as np
from unidecode import unidecode
from pymongo import MongoClient, ReplaceOne
from sys import argv


# ---
# Carrega os dados
workbook = xlrd.open_workbook_xls('municipios.xls', ignore_workbook_corruption=True)
dados = pd.read_excel(workbook, skiprows=[0,1], skipfooter=15)

# Remove as colunas "Gentílico" e "Prefeito"
dados.drop(list(dados.columns[2:4]), axis=1, inplace=True)


# ---
# Renomeia as Colunas
map_columns = {
    'município': 'Municipio',
    'código': 'codarea',
    'área territorial': 'Area',
    'população estimada': 'PopulacaoEstimada',
    'densidade demográfica': 'DensidadeDemografica',
    'escolarização': 'Escolarizacao',
    'idhm': 'IndiceDesenvolvimentoHumano',
    'mortalidade infantil': 'MortalidadeInfantil',
    'receitas': 'Receitas',
    'despesas': 'Despesas',
    'pib': 'PIBPerCapita',
}

def mapper(column):
    try:
        column_key = list(filter(lambda c: c in column.lower(), map_columns.keys()))[0]
        return map_columns[column_key]
    except IndexError:
        return column

dados.rename(mapper, axis='columns', inplace=True)


# ---
# Padroniza e Converte os Dados

dados['Municipio'] = dados['Municipio'].apply(lambda n: unidecode(n).upper())

def convert(data):
    if (type(data) in [float, int]):
        return data

    if (data.strip() == '-'):
        return np.nan
    
    if (',' in data):
        return float(data.replace(',', '.'))
    
    return int(data)

columns_convert = [
    'Area',
    'DensidadeDemografica',
    'Escolarizacao',
    'IndiceDesenvolvimentoHumano',
    'MortalidadeInfantil',
    'Receitas',
    'Despesas',
    'PIBPerCapita'
]

for column in columns_convert:
    dados[column] = dados[column].apply(convert)


# ---
# Salva os Dados no Banco de Dados
print('Preparando para salvar o DataFrame resultante...')
# Persiste o DataFrame
str_conn = 'mongodb://localhost'

if len(argv) > 2:
    usr = argv[1]
    pwd = argv[2]
    str_conn = f'mongodb+srv://{usr}:{pwd}@covid-19-es.nuzlk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

client = MongoClient(str_conn)

dados_dict = dados.to_dict(orient='records')

print('Deletando banco de dados existente...')
client.drop_database('db_municipios')

print('Inserindo novos dados...')
if len(dados_dict) > 0:
    client.db_municipios.dados.insert_many(dados_dict)

print('~~ Fim ~~')

