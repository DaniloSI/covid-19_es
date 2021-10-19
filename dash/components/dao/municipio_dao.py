from .dao import DAO

class MunicipioDAO(DAO):

    def __init__(self):
        super().__init__('db_municipios')