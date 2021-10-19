from components.observer import Subscriber
from components.dao.covid_dao import CovidDAO
from components.dao.municipio_dao import MunicipioDAO

class DataBase(Subscriber):
    covid = CovidDAO()
    municipio = MunicipioDAO()

    @staticmethod
    def update():
        DataBase.covid.update()
        DataBase.municipio.update()

    @staticmethod
    def get_df():
        return DataBase.covid.get_df()
    
    @staticmethod
    def get_df_municipios():
        return DataBase.municipio.get_df()
