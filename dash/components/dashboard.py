# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime

from components.graficos.Evolucao import get_figAreaAcumulados
from components.graficos.ScatterMunicipio import get_figScatter
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
        municipios_options = list(map(lambda m: {"label": m, "value": m}, DataBase.get_df()[[
            'Municipio']].sort_values('Municipio').drop_duplicates()['Municipio'].tolist()))
        print('----- # -----')
        print('Renderizando o Dashboard...')
        Dashboard._dashboard = dbc.Container(
            [
                html.Div(html.A(html.Img(src='assets/img/GitHub-Mark-32px.png'),
                                href="https://github.com/DaniloSI/covid-19_es", target="_blank", style={'marginRight': 10}), style={'position': 'absolute', 'right': 0, 'top': 30}),
                html.H3('Covid-19 no Espírito Santo',
                        style={'textAlign': "center", 'fontWeight': 400, 'margin': '25px 0px'}),
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
                                    dbc.CardHeader([
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.RadioItems(
                                                        id="radioitems-evolucao",
                                                        options=[
                                                            {"label": "Semanal",
                                                                "value": 'semanal'},
                                                            {"label": "Acumulado",
                                                                "value": 'acumulado'},
                                                        ],
                                                        value='semanal',
                                                        inline=True
                                                    ),
                                                    width=3
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id="select-evolucao-municipios",
                                                        options=municipios_options,
                                                        value=None,
                                                        placeholder="Selecione um município",
                                                    ),
                                                    xs=True
                                                ),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id="select-evolucao-bairros",
                                                        options=[],
                                                        value=None,
                                                        placeholder="Selecione um bairro",
                                                        disabled=True
                                                    ),
                                                    xs=True
                                                )
                                            ],
                                            align="center"
                                        )
                                    ]),
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
                                    dbc.CardHeader([
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.RadioItems(
                                                        id="radioitems-scatter",
                                                        options=[
                                                            {"label": "Casos x Óbitos",
                                                                "value": 'casos-obitos'},
                                                            {"label": "Incidência x Letalidade",
                                                                "value": 'incidencia-letalidade'},
                                                        ],
                                                        value='casos-obitos',
                                                        inline=True
                                                    ),
                                                ),
                                            ],
                                            align="center"
                                        )
                                    ]),
                                    dbc.CardBody(
                                        dcc.Graph(
                                            id='scatter-municipios',
                                            figure=get_figScatter()
                                        ),
                                    ),
                                ],
                                className="m-1"
                            ),
                            className="pr-0"
                        ),
                        dbc.Col(
                            [],
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
