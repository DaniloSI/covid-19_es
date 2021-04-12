import pandas as pd
from pymongo import MongoClient
from datetime import datetime


class DataBase():
    _usr = 'danilosi'
    _pwd = 'QRGrkX9BvrgRWi2O'
    _str_conn = f'mongodb+srv://{_usr}:{_pwd}@covid-19-es.nuzlk.mongodb.net/covid-19-es?retryWrites=true&w=majority'
    _client = MongoClient(_str_conn)
    _executed_first = False
    _df = None

    @staticmethod
    def fech():
        print('----- # -----')
        print('Carregando dados...')
        DataBase._df = pd.DataFrame(
            list(DataBase._client.db.dados.find({}, {'_id': 0}).limit(1000)))
        print('Dados carregados.')
        print('----- # -----')

    @staticmethod
    def refresh():
        DataBase.fech()
        now = datetime.now()
        print("Dados atualizados em: ", now.ctime())
        print('----- # -----')

    @staticmethod
    def get_df():
        if (not DataBase._executed_first):
            DataBase.fech()
            DataBase._executed_first = True

        return DataBase._df
