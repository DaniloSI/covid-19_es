# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Carrega Data Frames
with open('../notebooks_source/ES_MALHA_MUNICIPIOS.geojson') as json_file:
    municipios = json.load(json_file)

df = pd.read_csv('../notebooks_output/microdados_pre-processed.csv', sep=',', encoding='UTF-8')

df_municipios = pd.read_csv('../notebooks_source/municipios.csv')

df_choropleph = df.groupby(['DataNotificacao', 'Municipio'])\
    .sum()\
    .reset_index()\
    .drop_duplicates('Municipio', keep='last')\
    .merge(df_municipios, on='Municipio', how='left')
df_choropleph['Incidencia'] = round(df_choropleph['ConfirmadosAcumulado'] * 10000 / df_choropleph['PopulacaoEstimada'], 1)

figChoroplethIncidencia = px.choropleth(
    df_choropleph,
    geojson=municipios,
    locations='codarea',
    featureidkey="properties.codarea",
    color='Incidencia',
    color_continuous_scale="Viridis",
    hover_name='Municipio',
    hover_data={
        'ConfirmadosAcumulado': True,
        'Incidencia': ':.1f',
        'codarea': False},
    labels={
        'codarea': 'Código do Município',
        'ConfirmadosAcumulado': 'Casos',
        'Incidencia': 'Incidência',
    },
    title='Incidência (Total a Cada 10 Mil Habitantes)',
)

figChoroplethIncidencia.update_geos(fitbounds="geojson", visible=False, lataxis_range=[0,500], lonaxis_range=[0, 100])
figChoroplethIncidencia.update_layout(autosize=True, margin={'t': 50, 'r': 0, 'b': 0, 'l': 0})


df_choropleph_letalidade = df.groupby(['DataNotificacao', 'Municipio'])\
    .sum()\
    .reset_index()\
    .drop_duplicates('Municipio', keep='last')\
    .merge(df_municipios, on='Municipio', how='left')

df_choropleph_letalidade['Letalidade'] = round(df_choropleph_letalidade['ObitosAcumulado'] * 100.0 / df_choropleph_letalidade['ConfirmadosAcumulado'], 2)

df_choropleph_letalidade.dropna(inplace=True)

figChoroplethLetalidade = px.choropleth(
    df_choropleph_letalidade,
    geojson=municipios,
    locations='codarea',
    featureidkey="properties.codarea",
    color='Letalidade',
    color_continuous_scale="Magma",
    hover_name='Municipio',
    hover_data={
        'ObitosAcumulado': True,
        'Letalidade': ':.1f',
        'codarea': False},
    labels={
        'codarea': 'Código do Município',
        'ObitosAcumulado': 'Óbitos',
        'Letalidade': 'Letalidade',
    },
    title='Letalidade (%)',
)

figChoroplethLetalidade.update_geos(fitbounds="geojson", visible=False, lataxis_range=[0,500], lonaxis_range=[0, 100])
figChoroplethLetalidade.update_layout(autosize=True, margin={'t': 50, 'r': 0, 'b': 0, 'l': 0})



# Gera Elementos Visuais
figAreaAcumulados = go.Figure()

df_acumulados = df[['DataNotificacao', 'ConfirmadosAcumulado', 'ObitosAcumulado', 'CurasAcumulado']]\
    .groupby(['DataNotificacao'])\
    .sum()\
    .reset_index()\
    .rename({'ConfirmadosAcumulado': 'Casos', 'ObitosAcumulado': 'Óbitos', 'CurasAcumulado': 'Curas'}, axis=1)

figAreaAcumulados.add_trace(
    go.Scatter(
        x=df_acumulados['DataNotificacao'],
        y=df_acumulados['Casos'],
        fill='tozeroy',
        fillcolor=f'rgba{(99, 100, 250, 0.3)}',
        line_color='#636EFA',
        name='Casos',
    )
)

figAreaAcumulados.add_trace(
    go.Scatter(
        x=df_acumulados['DataNotificacao'],
        y=df_acumulados['Curas'],
        fill='tozeroy',
        fillcolor=f'rgba{(114, 219, 197, 0.6)}',
        line_color='#00CC96',
        name='Curas',
    )
)

figAreaAcumulados.add_trace(
    go.Scatter(
        x=df_acumulados['DataNotificacao'],
        y=df_acumulados['Óbitos'],
        fill='tozeroy',
        fillcolor=f'rgba{(239, 85, 59, 0.6)}',
        line_color='#EF553B',
        name='Óbitos',
    )
)

figAreaAcumulados.update_layout(title="Evolução Total do Espírito Santo", autosize=True, margin={'t': 50, 'r': 0, 'b': 50, 'l': 50})


figScatterCasosObitosAcumulado = px.scatter(
    df.groupby(['DataNotificacao', 'Municipio'])
        .sum()
        .reset_index()
        .drop_duplicates('Municipio', keep='last')
        .sort_values('ConfirmadosAcumulado')
        .tail(30),
    x='ObitosAcumulado',
    y='ConfirmadosAcumulado',
    color='Municipio',
    size='ConfirmadosAcumulado',
    hover_data=['Municipio'],
    labels={
        'ObitosAcumulado': 'Óbitos Acumulados',
        'ConfirmadosAcumulado': 'Casos Acumulados',
        'Municipio': 'Município',
    },
    title='Top 30 Municípios'
)

figScatterCasosObitosAcumulado.update_layout(autosize=True, margin={'t': 50, 'r': 0, 'b': 50, 'l': 50})

# Renderiza componentes
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                dcc.Graph(
                                    id='acumulados',
                                    figure=figAreaAcumulados
                                ),
                            ),
                        ],
                        className="m-1"
                    ),
                    className="pr-0"
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                dcc.Graph(
                                    id='casos-obitos-acumulados',
                                    figure=figScatterCasosObitosAcumulado
                                ),
                            ),
                        ],
                        className="m-1"
                    ),
                    className="pl-0"
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                dcc.Graph(
                                                    id='incidencia',
                                                    figure=figChoroplethIncidencia
                                                ),
                                            ),
                                        ],
                                        className="m-1"
                                    ),
                                    md=6,
                                    className="pr-0"
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                dcc.Graph(
                                                    id='letalidade',
                                                    figure=figChoroplethLetalidade
                                                ),
                                            ),
                                        ],
                                        className="m-1"
                                    ),
                                    md=6,
                                    className="pl-0"
                                ),
                            ]
                        ),
                    ],
                    md=6,
                    className="pr-0"
                )
            ]
        )
    ],
    fluid=True,
    className='p-2'
)

if __name__ == '__main__':
    app.run_server(debug=True)