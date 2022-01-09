import dash_core_components as dcc
from components.database import DataBase

def dropdown_municipios(id):
    transform_label_value = lambda m: {"label": m, "value": m}

    municipios = DataBase.get_df_municipios()['Municipio'].tolist()

    return dcc.Dropdown(
        id=id,
        options=list(map(transform_label_value, municipios)),
        value=None,
        placeholder='Selecione um município',
    )