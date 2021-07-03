import plotly.graph_objects as go
from components.database import DataBase

def _treemap_municipios(top_n):
    df_treemap = DataBase.get_df()[['Municipio', 'Confirmados']]\
        .groupby('Municipio')\
        .sum()\
        .reset_index()
    df_treemap.columns = ['Label', 'Value']
    df_treemap['Parent'] = ''
    
    df_treemap = df_treemap.sort_values('Value', ascending=False)\
        .head(top_n)
    
    return go.Treemap(
        labels = df_treemap['Label'].tolist(),
        parents = df_treemap['Parent'].tolist(),
        values = df_treemap['Value'].tolist(),
        texttemplate = '%{label}<br>%{value:d} confirmados',
        hovertemplate = '%{label}<br>%{value:d} confirmados<extra></extra>'
    )

def _treemap_bairros(municipio, top_n):
    query = f'Municipio == "{municipio}"'
    # Gera dataframe para dados de municípios
    df_treemap = DataBase.get_df().query(query)[['Municipio', 'Bairro', 'Confirmados']]\
        .groupby(['Municipio', 'Bairro'])\
        .sum()\
        .reset_index()\
        .sort_values('Confirmados', ascending=False)\
        .head(top_n)
    
    s_municipios = df_treemap['Municipio']

    df_treemap.columns = ['Parent', 'Label', 'Value']
    df_treemap['Parent'] = ''
    
    return go.Treemap(
        labels = df_treemap['Label'].tolist(),
        parents = df_treemap['Parent'].tolist(),
        values = df_treemap['Value'].tolist(),
        textinfo = 'label+value'
    )

def treemap(municipio=None, top_n=20):
    figure = lambda t, by: go.Figure(t, layout = {
        'title': f'Top {top_n} confirmados por {by}',
        'title_x': 0.5,
        'margin_t': 50,
    })
    
    if municipio != None and municipio != '':
        return figure(_treemap_bairros(municipio, top_n), f'bairros do município {municipio}')
    
    return figure(_treemap_municipios(top_n), 'municipios')