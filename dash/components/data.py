# -*- coding: utf-8 -*-

import pandas as pd
import json
from components.database import DataBase
import schedule
from _thread import start_new_thread
from time import sleep

from datetime import datetime

# Carrega Data Frames
with open('../data/ES_MALHA_MUNICIPIOS.geojson') as json_file:
    municipios = json.load(json_file)

df = DataBase.get_df()


schedule.every(30).seconds.do(DataBase.refresh)


def schedule_update(trhead_name, delay):
    while True:
        schedule.run_pending()
        sleep(delay)


start_new_thread(schedule_update, ("Thread-Update", 1))

df_municipios = pd.read_csv('../data/municipios.csv')
