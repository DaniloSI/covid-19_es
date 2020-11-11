# -*- coding: utf-8 -*-

import pandas as pd
import json

# Carrega Data Frames
with open('../data/ES_MALHA_MUNICIPIOS.geojson') as json_file:
    municipios = json.load(json_file)

df = pd.read_csv('../notebooks_output/microdados_pre-processed.csv', sep=',', encoding='UTF-8')

df_municipios = pd.read_csv('../data/municipios.csv')

data_ultima_notificacao = df['DataNotificacao'].max()
data_primeira_notificacao = df['DataNotificacao'].min()
total_casos_es = '{:,}'.format(int(df['Confirmados'].sum())).replace(',', '.')
total_obitos_es = '{:,}'.format(int(df['Obitos'].sum())).replace(',', '.')
total_curas_es = '{:,}'.format(int(df['Curas'].sum())).replace(',', '.')