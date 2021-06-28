import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timedelta
import os


def get_str_conn():
    if 'MODE' in os.environ and os.environ['MODE'] == 'development':
        return 'mongodb://localhost'

    usr = os.environ['MONGODB_USR']
    pwd = os.environ['MONGODB_PWD']

    return f'mongodb+srv://{usr}:{pwd}@covid-19-es.nuzlk.mongodb.net/db?retryWrites=true&w=majority'

class DataBase():
    _executed_first = False
    _df = None
    _str_conn = get_str_conn()

    @staticmethod
    def fech():
        # from_date = datetime.now() - timedelta(30 * 4)
        # query_filter = {'DataNotificacao': {"$gte": from_date}}
        print('----- # -----')
        print('Carregando dados...')
        with MongoClient(DataBase._str_conn) as client:
            collection = client.db.dados
            print(f'Carregando um total de {collection.count_documents({})} registros')
            DataBase._df = pd.DataFrame(list(collection.find({}, {'_id': 0})))
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
