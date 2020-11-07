# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import os

from components.graficos.Evolucao import figAreaAcumulados
from components.graficos.ScatterMunicipio import figScatterCasosObitosAcumulado, figScatterIncidenciaLetalidade
from components.mapas.ChoroplethIncidenciaLetalidade import rowChoropleph

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

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