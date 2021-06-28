import dash_core_components as dcc
from components.database import DataBase

def dropdown_municipios(id, multi=False):
    transform_label_value = lambda m: {"label": m, "value": m}
    df = DataBase.get_df()[['Municipio']].sort_values('Municipio').drop_duplicates()['Municipio'].tolist()
    municipios_options = list(map(transform_label_value, df))

    placeholder = 'Selecione municípios' if multi else 'Selecione um município'

    return dcc.Dropdown(
        id=id,
        options=municipios_options,
        value=None,
        placeholder=placeholder,
        multi=multi
    )