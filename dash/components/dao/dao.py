from abc import ABC
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import os
from components.observer import Subscriber


class DAO(ABC, Subscriber):
    df = None

    def __init__(self, collection_name):
        self.collection_name = collection_name
        self._fetch()

    def _get_str_conn(self):
        if 'MODE' in os.environ and os.environ['MODE'] == 'development':
            return 'mongodb://localhost'

        usr = os.environ['MONGODB_USR']
        pwd = os.environ['MONGODB_PWD']

        return f'mongodb+srv://{usr}:{pwd}@covid-19-es.nuzlk.mongodb.net/db?retryWrites=true&w=majority'

    def _fetch(self):
        print('----- # -----')
        print(f'Carregando dados de {self.collection_name}...')
        with MongoClient(self._get_str_conn()) as client:
            collection = client[self.collection_name].dados
            print(f'Carregando um total de {collection.count_documents({})} registros')
            self.df = pd.DataFrame(list(collection.find({}, {'_id': 0})))
        print('Dados carregados.')
        print('----- # -----')

    def update(self):
        self._fetch()
        now = datetime.now()
        print("Dados atualizados em: ", now.ctime())
        print('----- # -----')
    
    def get_df(self):
        return self.df
