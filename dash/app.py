# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import os
from datetime import datetime

from components.graficos.Evolucao import figAreaAcumulados
from components.graficos.ScatterMunicipio import figScatterCasosObitosAcumulado, figScatterIncidenciaLetalidade
from components.mapas.ChoroplethIncidenciaLetalidade import rowChoropleph

from components.data import data_ultima_notificacao
from components.data import data_primeira_notificacao
from components.data import total_casos_es
from components.data import total_obitos_es
from components.data import total_curas_es

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

def format_date(date):
    return datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')

last_date_text = '{} - {}'.format(format_date(data_primeira_notificacao), format_date(data_ultima_notificacao))

# Renderiza componentes
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardBody([
                                                html.P('Intervalo de datas que compreendem os dados:', style={'textAlign': 'center'}),
                                                html.H5(last_date_text, style={'textAlign': 'center'})
                                            ])
                                        ],
                                        className="m-1"
                                    ),
                                ],
                                className="pr-0"
                            ),
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardBody([
                                                html.P('Total de Casos Confirmados no Estado:', style={'textAlign': 'center'}),
                                                html.H5(total_casos_es, style={'textAlign': 'center'})
                                            ])
                                        ],
                                        className="m-1"
                                    ),
                                ],
                                className="pl-0"
                            )
                        ]
                    ),
                    className="col-6 pr-0"
                ),
                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardBody([
                                                html.P('Total de Óbitos no Estado:', style={'textAlign': 'center'}),
                                                html.H5(total_obitos_es, style={'textAlign': 'center'})
                                            ])
                                        ],
                                        className="m-1"
                                    ),
                                ],
                                className="pr-0"
                            ),
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardBody([
                                                html.P('Total de Curados no Estado:', style={'textAlign': 'center'}),
                                                html.H5(total_curas_es, style={'textAlign': 'center'})
                                            ])
                                        ],
                                        className="m-1"
                                    ),
                                ],
                                className="pl-0"
                            )
                        ]
                    ),
                    className="col-6 pl-0"
                ),
            ]
        ),
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
                    rowChoropleph,
                    className="pl-0"
                ),
            ]
        ),
        dbc.Row(
            [
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
                    className="pr-0"
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    dcc.Graph(
                                        id='incidencia-letalidade',
                                        figure=figScatterIncidenciaLetalidade
                                    ),
                                ),
                            ],
                            className="m-1"
                        ),
                    ],
                    className="pl-0"
                )
            ]
        )
    ],
    fluid=True,
    className='p-2'
)

if __name__ == '__main__':
    app.run_server(debug=True)