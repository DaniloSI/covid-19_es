# -*- coding: utf-8 -*-

import pandas as pd
import json
from components.database import DataBase

from datetime import datetime

# Carrega Data Frames
with open('../data/ES_MALHA_MUNICIPIOS.geojson') as json_file:
    municipios = json.load(json_file)

df = DataBase.get_df()

df_municipios = pd.read_csv('../data/municipios.csv')
