# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime

from components.graficos.Evolucao import get_figAreaAcumulados
from components.graficos.ScatterMunicipio import get_figScatterCasosObitosAcumulado, get_figScatterIncidenciaLetalidade
from components.mapas.ChoroplethIncidenciaLetalidade import get_rowChoropleph

from components.database import DataBase


def last_date_text():
    str_format = '%d/%m/%Y'
    data_notificacao = DataBase.get_df()['DataNotificacao']
    data_primeira_notificacao = data_notificacao.min().strftime(str_format)
    data_ultima_notificacao = data_notificacao.max().strftime(str_format)
    return f'{data_primeira_notificacao} - {data_ultima_notificacao}'


def total_casos_es():
    total_confirmados = int(DataBase.get_df()['Confirmados'].sum())
    return '{:,}'.format(total_confirmados).replace(',', '.')


def total_obitos_es():
    total_obitos = int(DataBase.get_df()['Obitos'].sum())
    return '{:,}'.format(total_obitos).replace(',', '.')


def total_curas_es():
    total_curas = int(DataBase.get_df()['Curas'].sum())
    return '{:,}'.format(total_curas).replace(',', '.')


class Dashboard():
    _dashboard = None

    @staticmethod
    def render():
        print('----- # -----')
        print('Renderizando o Dashboard...')
        Dashboard._dashboard = dbc.Container(
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
                                                        html.P('Intervalo de datas que compreendem os dados:', style={
                                                            'textAlign': 'center'}),
                                                        html.H5(last_date_text(), style={
                                                            'textAlign': 'center'})
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
                                                        html.P('Total de Casos Confirmados no Estado:', style={
                                                            'textAlign': 'center'}),
                                                        html.H5(total_casos_es(), style={
                                                            'textAlign': 'center'})
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
                                                        html.P('Total de Óbitos no Estado:', style={
                                                            'textAlign': 'center'}),
                                                        html.H5(total_obitos_es(), style={
                                                            'textAlign': 'center'})
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
                                                        html.P('Total de Curados no Estado:', style={
                                                            'textAlign': 'center'}),
                                                        html.H5(total_curas_es(), style={
                                                            'textAlign': 'center'})
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
                                            figure=get_figAreaAcumulados()
                                        ),
                                    ),
                                ],
                                className="m-1"
                            ),
                            className="pr-0"
                        ),
                        dbc.Col(
                            get_rowChoropleph(),
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
                                            figure=get_figScatterCasosObitosAcumulado()
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
                                                figure=get_figScatterIncidenciaLetalidade()
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
        print('Dashboard renderizado.')
        print('----- # -----')

    @staticmethod
    def get_dashboard():
        if Dashboard._dashboard == None:
            Dashboard.render()

        return Dashboard._dashboard
