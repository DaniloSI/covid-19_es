import plotly.graph_objects as go
from components.database import DataBase

def get_label(variavel):
    return {
        'Confirmados': 'confirmados',
        'Obitos': 'óbitos',
        'Curas': 'curas',
    }[variavel]

def _make_treemap(df):
    return go.Treemap(
        labels = df['Label'].tolist(),
        parents = df['Parent'].tolist(),
        values = df['Value'].tolist(),
    )

def _treemap_municipios(top_n, variavel):
    df_treemap = DataBase.get_df()[['Municipio', variavel]]\
        .groupby('Municipio')\
        .sum()\
        .reset_index()\
        .sort_values(variavel, ascending=False)\
        .head(top_n)

    df_treemap.columns = ['Label', 'Value']
    df_treemap['Parent'] = ''
    
    return df_treemap

def _treemap_bairros(municipio, top_n, variavel):
    query = f'Municipio == "{municipio}"'
    df_treemap = DataBase.get_df().query(query)[['Municipio', 'Bairro', variavel]]\
        .groupby(['Municipio', 'Bairro'])\
        .sum()\
        .reset_index()\
        .sort_values(variavel, ascending=False)\
        .head(top_n)
    
    s_municipios = df_treemap['Municipio']

    df_treemap.columns = ['Parent', 'Label', 'Value']
    df_treemap['Parent'] = ''
    
    return df_treemap

def treemap(municipio=None, top_n=10, variavel='Confirmados'):
    label = get_label(variavel)
    title = lambda by: f'Top {top_n} {by} por {label}' if top_n is not None else f'{label} por {by}'
    figure = lambda t, by: go.Figure(t, layout = {
        'title': title(by),
        'title_x': 0.5,
        'margin': { 't': 25, 'r': 0, 'b': 0, 'l': 0 }
    })
    
    if municipio != None and municipio != '':
        df_treemap = _treemap_bairros(municipio, top_n, variavel)
        title_by = f'bairros do município {municipio}'
    else:
        df_treemap = _treemap_municipios(top_n, variavel)
        title_by = 'municipios'

    fig = figure(_make_treemap(df_treemap), title_by)
    fig.data[0].customdata = df_treemap['Value'].apply(lambda v: format(int(v), ',d').replace(',', '.'))
    fig.data[0].texttemplate = '%{label}<br>%{customdata} confirmados'
    fig.data[0].hovertemplate = '%{label}<br>%{customdata} confirmados<extra></extra>'

    return fig