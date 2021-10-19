from .dao import DAO

class CovidDAO(DAO):

    def __init__(self):
        super().__init__('db')