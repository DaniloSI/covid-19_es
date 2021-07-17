import dash_core_components as dcc
from components.database import DataBase

def dropdown_municipios(id, com_bairros=False):
    transform_label_value = lambda m: {"label": m, "value": m}

    df = DataBase.get_df().query('Bairro != "NAN"')[['Municipio']]\
        .sort_values('Municipio')\
        .drop_duplicates()['Municipio']\
        .tolist()

    municipios_options = list(map(transform_label_value, df))

    return dcc.Dropdown(
        id=id,
        options=municipios_options,
        value=None,
        placeholder='Selecione um município',
    )