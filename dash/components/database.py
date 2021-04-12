import pandas as pd
from pymongo import MongoClient
from datetime import datetime


class DataBase():
    _usr = 'danilosi'
    _pwd = 'QRGrkX9BvrgRWi2O'
    _str_conn = f'mongodb+srv://{_usr}:{_pwd}@covid-19-es.nuzlk.mongodb.net/covid-19-es?retryWrites=true&w=majority'
    _executed_first = False
    _df = None
    _i = 1000

    @staticmethod
    def initialize():
        print('----- # -----')
        print('Carregando dados...')
        client = MongoClient(DataBase._str_conn)
        DataBase._df = pd.DataFrame(
            list(client.db.dados.find({}, {'_id': 0}).limit(DataBase._i)))
        print('Dados carregados.')
        print('----- # -----')

    @staticmethod
    def refresh():
        DataBase._i += 30000
        DataBase.initialize()
        now = datetime.now()
        print("Dados atualizados em: ", now.ctime())
        print('----- # -----')

    @staticmethod
    def get_df():
        if (not DataBase._executed_first):
            DataBase.initialize()
            DataBase._executed_first = True

        return DataBase._df
