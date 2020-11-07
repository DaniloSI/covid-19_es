# -*- coding: utf-8 -*-

import pandas as pd
import json

# Carrega Data Frames
with open('../data/ES_MALHA_MUNICIPIOS.geojson') as json_file:
    municipios = json.load(json_file)

df = pd.read_csv('../notebooks_output/microdados_pre-processed.csv', sep=',', encoding='UTF-8')

df_municipios = pd.read_csv('../data/municipios.csv')