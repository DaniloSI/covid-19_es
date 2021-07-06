import plotly.graph_objects as go
from components.database import DataBase

def _make_treemap(df):
    return go.Treemap(
        labels = df['Label'].tolist(),
        parents = df['Parent'].tolist(),
        values = df['Value'].tolist(),
        textinfo = 'label+value',
    )

def _treemap_municipios(top_n):
    df_treemap = DataBase.get_df()[['Municipio', 'Confirmados']]\
        .groupby('Municipio')\
        .sum()\
        .reset_index()\
        .sort_values('Confirmados', ascending=False)\
        .head(top_n)

    df_treemap.columns = ['Label', 'Value']
    df_treemap['Parent'] = ''
    
    return _make_treemap(df_treemap)

def _treemap_bairros(municipio, top_n):
    query = f'Municipio == "{municipio}"'
    df_treemap = DataBase.get_df().query(query)[['Municipio', 'Bairro', 'Confirmados']]\
        .groupby(['Municipio', 'Bairro'])\
        .sum()\
        .reset_index()\
        .sort_values('Confirmados', ascending=False)\
        .head(top_n)
    
    s_municipios = df_treemap['Municipio']

    df_treemap.columns = ['Parent', 'Label', 'Value']
    df_treemap['Parent'] = ''
    
    return _make_treemap(df_treemap)

def treemap(municipio=None, top_n=10):
    figure = lambda t, by: go.Figure(t, layout = {
        'title': f'Top {top_n} confirmados por {by}',
        'title_x': 0.5,
        'margin': { 't': 25, 'r': 0, 'b': 0, 'l': 0 }
    })
    
    if municipio != None and municipio != '':
        return figure(_treemap_bairros(municipio, top_n), f'bairros do município {municipio}')
    
    return figure(_treemap_municipios(top_n), 'municipios')