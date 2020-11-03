# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('../notebooks_output/microdados_pre-processed.csv', sep=',', encoding='UTF-8')

figLineConfirmadosAcumulado = px.line(
    df.groupby(['DataNotificacao', 'Municipio'])
        .sum()
        .reset_index(),
        # .query('Municipio == "VITORIA" | Municipio == "SERRA"'),
    x="DataNotificacao",
    y="ConfirmadosAcumulado",
    color="Municipio",
    hover_name="Municipio",
    labels={
        'DataNotificacao': 'Data',
        'ConfirmadosAcumulado': 'Casos Acumulados',
        'Municipio': 'Município'
    }
)

figLineObitosAcumulado = px.line(
    df.groupby(['DataNotificacao', 'Municipio'])
        .sum()
        .reset_index(),
    x="DataNotificacao",
    y="ObitosAcumulado",
    color="Municipio",
    hover_name="Municipio",
    labels={
        'DataNotificacao': 'Data',
        'ObitosAcumulado': 'Óbitos Acumulados',
        'Municipio': 'Município'
    }
)

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

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Acumulado de Casos', style={'textAlign': 'center'}),
                            dbc.CardBody(
                                dcc.Graph(
                                    id='casos-acumulados',
                                    figure=figLineConfirmadosAcumulado
                                ),
                            ),
                        ]
                    ),
                    md=6
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Acumulado de Óbitos', style={'textAlign': 'center'}),
                            dbc.CardBody(
                                dcc.Graph(
                                    id='obitos-acumulados',
                                    figure=figLineObitosAcumulado
                                ),
                            ),
                        ]
                    ),
                    md=6
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Acumulado de Casos vs Acumulado de Óbitos', style={'textAlign': 'center'}),
                            dbc.CardBody(
                                dcc.Graph(
                                    id='casos-obitos-acumulados',
                                    figure=figScatterCasosObitosAcumulado
                                ),
                            ),
                        ]
                    ),
                    md=6
                ),
            ]
        )
    ],
    fluid=True,
    className='p-2'
)

if __name__ == '__main__':
    app.run_server(debug=True)