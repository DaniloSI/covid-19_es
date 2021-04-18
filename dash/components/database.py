import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timedelta


class DataBase():
    _usr = 'danilosi'
    _pwd = 'QRGrkX9BvrgRWi2O'
    _str_conn = f'mongodb+srv://{_usr}:{_pwd}@covid-19-es.nuzlk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    _client = MongoClient(_str_conn)
    _executed_first = False
    _df = None

    @staticmethod
    def fech():
        # from_date = datetime.now() - timedelta(30 * 4)
        # query_filter = {'DataNotificacao': {"$gte": from_date}}
        print('----- # -----')
        print('Carregando dados...')
        DataBase._df = pd.DataFrame(
            list(DataBase._client.db.dados.find({}, {'_id': 0})))
        # DataBase._df = pd.read_csv(
        #     '../notebooks/microdados_pre-processed.csv', sep=',', encoding='UTF-8')
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
