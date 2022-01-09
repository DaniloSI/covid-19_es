from components.observer import Subscriber
from components.dao.covid_dao import CovidDAO
from components.dao.municipio_dao import MunicipioDAO

class DataBase(Subscriber):
    covid = CovidDAO()
    municipio = MunicipioDAO()
    df_full = None

    @staticmethod
    def _update_df_full():
        df_covid = DataBase.covid.get_df()
        df_municipios = DataBase.municipio.get_df()

        df_result = df_covid.set_index('Municipio').join(df_municipios.set_index('Municipio'))
        df_result = df_result[df_result['codarea'].notna()].reset_index()

        DataBase.df_full = df_result

    @staticmethod
    def update():
        DataBase.covid.update()
        DataBase.municipio.update()

        DataBase._update_df_full()

    @staticmethod
    def get_df():
        return DataBase.covid.get_df()
    
    @staticmethod
    def get_df_municipios():
        return DataBase.municipio.get_df()

    @staticmethod
    def get_df_full():
        if DataBase.df_full is None:
            DataBase._update_df_full()

        return DataBase.df_full
