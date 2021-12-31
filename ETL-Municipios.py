# Tratamento de Dados (Indicadores Municipais do ES)
# --------------------------------------------------
#
# Dados obitidos através da API do IBGE, pelo link: https://servicodados.ibge.gov.br/
#

from requests import get
import pandas as pd
from unidecode import unidecode
from pymongo import MongoClient
from sys import argv

# 1. Carrega os Dados

# 1.1. Nomes e Códigos de Municípios

print('Carregando dados de Municípios...')

# URL para buscar nomes e dados de municípios do Espírito Santo
url_municipios = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/ES/municipios'

# Recebe como parâmetro um dicionário e o retorna em outro formato
def parse_municipio(m):
    return {
        'codarea': str(m['id']),
        'Municipio': m['nome'],
        'codarea_join': str(m['id'])[:-1],
        'Microrregiao_id': m['microrregiao']['id'],
        'Microrregiao': m['microrregiao']['nome'],
        'Mesorregiao_id': m['microrregiao']['mesorregiao']['id'],
        'Mesorregiao': m['microrregiao']['mesorregiao']['nome'],
    }

# Obtém o nome e o código de cada município
municipios = list(map(parse_municipio, get(url_municipios).json()))

# Gera um DataFrame dos nomes dos municípios e define o código como o índice
df_municipios = pd.DataFrame(municipios)
df_municipios.set_index('codarea_join', inplace=True)


# 1.2. Indicadores de Municípios

print('Carregando dados de Indicadores de Municípios...')

# O dicionário abaixo realiza uma associação entre o id e o nome do indicador
indicador_label = {
    '29167': 'Area', # Área Territorial - km²
    '29168': 'DensidadeDemografica', # Densidade Demográfica
    '29171': 'PopulacaoEstimada', # População Estimada
    '47001': 'PIBPerCapita', # PIB per Capita
    '28141': 'Receitas', # Total de Receitas Realizadas
    '29749': 'Despesas', # Total de Despesas Empenhadas
    '30255': 'IndiceDesenvolvimentoHumano', # IDHM
    '30279': 'MortalidadeInfantil', # Mortalidade Infantil
    '60045': 'Escolarizacao' # Taxa de escolarização de 6 a 14 anos
}

# Realiza uma junção dos ids dos indicadores separando por pipe
indicadores = '|'.join(indicador_label.keys())

# URL para obter os indicadores dos municípios
url_indicadores = f'https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/{indicadores}/resultados/32xxxxx'

# Obtem os dados dos indicadores a partir da URL
indicadores_results = get(url_indicadores).json()

# Recebe como parâmetro o id do indicador e os valores para diversos anos
# Retorna um dicionário contendo o código do município e o valor do indicador para o ano mais recente
def parse_result(indicador_id, l_res):
    codarea = l_res['localidade'] # id do município
    last_year = max(l_res['res'].keys()) # ano da última pesquisa realizada
    last_result = l_res['res'][last_year] # resultado da última pesquisa realizada
    label = indicador_label[indicador_id] # Label do indicador a partir do id
    
    return {
        'codarea_join': codarea,
        label: 0.0 if last_result == '-' else float(last_result)
    }

# Gera uma série para cada indicador e concatena ao DataFrame de municípios
for indicador_result in indicadores_results:
    indicador_id = str(indicador_result['id'])
    results = indicador_result['res']
    
    df_indicador_result = pd.DataFrame(map(lambda l_res: parse_result(indicador_id, l_res), results))
    df_indicador_result.set_index('codarea_join', inplace=True)
    
    df_municipios = pd.concat([df_municipios, df_indicador_result], axis=1)

df_municipios.reset_index(inplace=True)
df_municipios.drop(columns='codarea_join', inplace=True)


# 2. Padronização de Nomes

print('Padronizando nomes de Municípios, Microrregiões e Mesorregiões...')

# Para cada região (município, microrregião e mesorregião), coloca o nome em maiúsculo e remove acento.
padroniza_nome = lambda regiao: df_municipios[regiao].apply(lambda n: unidecode(n).upper())

df_municipios['Municipio'] = padroniza_nome('Municipio')
df_municipios['Microrregiao'] = padroniza_nome('Microrregiao')
df_municipios['Mesorregiao'] = padroniza_nome('Mesorregiao')


# 3. Salva os dados resultantes no banco de dados

print('Preparando para salvar o DataFrame resultante...')
# Persiste o DataFrame
str_conn = 'mongodb://localhost'

if len(argv) > 2:
    usr = argv[1]
    pwd = argv[2]
    str_conn = f'mongodb+srv://{usr}:{pwd}@es-covid-19.nuzlk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

client = MongoClient(str_conn)

dados_dict = df_municipios.to_dict(orient='records')

print('Deletando banco de dados existente...')
client.drop_database('db_municipios')

print('Inserindo novos dados...')
if len(dados_dict) > 0:
    client.db_municipios.dados.insert_many(dados_dict)

print('~~ Fim ~~')
