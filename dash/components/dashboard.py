# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime
import plotly.graph_objects as go

from components.filtros.Select import dropdown_municipios
from components.graficos.Evolucao import evolucao
from components.graficos.Scatter import get_figScatter
from components.graficos.Treemap import treemap
from components.mapas.Choropleth import Choropleth

from components.database import DataBase

import urllib
import json
from datetime import datetime, timedelta


def date_interval_text():
    url = 'https://api.github.com/repos/danilosi/covid-19_es/actions/runs?page=0&per_page=1&status=success'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    datetime_utc = data['workflow_runs'][0]['updated_at']

    data_ultima_atualizacao = (datetime.fromisoformat(
        datetime_utc.replace('Z', '')) - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M')

    return f'Última atualização: {data_ultima_atualizacao}'


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
                html.Div(html.A(html.Img(src='assets/img/GitHub-Mark-32px.png'),
                                href="https://github.com/DaniloSI/covid-19_es", target="_blank", style={'marginRight': 10}), style={'display': 'flex', 'justify-content': 'flex-end'}),
                html.H3('Covid-19 no Espírito Santo',
                        style={'textAlign': "center", 'fontWeight': 400}),
                html.H6(date_interval_text(),
                        style={'textAlign': "center", 'fontWeight': 200, 'margin': '10px 0px 25px 0px'}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dropdown_municipios('select-treemap-municipios'),
                                                            xs=True
                                                        ),
                                                        dbc.Col(
                                                            dcc.Slider(
                                                                id='slider_top_n',
                                                                min=0,
                                                                max=30,
                                                                step=1,
                                                                marks={
                                                                    10: {'label': 'Top 10 bairros'},
                                                                    20: {'label': 'Top 20 bairros'},
                                                                },
                                                                tooltip={
                                                                    'placement': 'top'
                                                                },
                                                                value=10,
                                                            ),
                                                            width=7
                                                        )
                                                    ],
                                                    align="center"
                                                )
                                            ]
                                        ),
                                        dbc.CardBody(
                                            dcc.Loading(
                                                dcc.Graph(
                                                    id='treemap',
                                                    figure=treemap()
                                                ),
                                                type='dot'
                                            )
                                        ),
                                    ],
                                    className="mb-2"
                                ),
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            dbc.RadioItems(
                                                id="radioitems-choropleth",
                                                options=[
                                                    {'label': 'Incidência',
                                                        'value': 'Incidencia'},
                                                    {'label': 'Letalidade',
                                                        'value': 'Letalidade'},
                                                    {'label': 'Confirmados',
                                                        'value': 'ConfirmadosAcumulado'},
                                                    {'label': 'Óbitos',
                                                        'value': 'ObitosAcumulado'},
                                                ],
                                                value='Incidencia',
                                                inline=True,
                                            )
                                        ),
                                        dbc.CardBody(
                                            dcc.Loading(
                                                dcc.Graph(
                                                    id='choropleth',
                                                    figure=Choropleth.get_figChoropleph(
                                                        'Incidencia')
                                                ),
                                                type='dot'
                                            )
                                        ),
                                    ],
                                    className="mb-2"
                                )
                            ],
                            className="pr-lg-1",
                            md=12,
                            lg=5
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader([
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dropdown_municipios('select-evolucao-municipios'),
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
                                                    ),
                                                    dbc.Col(
                                                        dbc.RadioItems(
                                                            id="radioitems-evolucao-periodo",
                                                            options=[
                                                                {"label": "Acumulado",
                                                                    "value": 'acumulado'},
                                                                {"label": "Semanal",
                                                                    "value": 'semanal'},
                                                            ],
                                                            value='acumulado',
                                                            inline=True
                                                        ),
                                                        width=2
                                                    ),
                                                    dbc.Col(
                                                        dbc.RadioItems(
                                                            id="radioitems-evolucao-variavel",
                                                            options=[
                                                                {"label": "Confirmados",
                                                                    "value": 'confirmados'},
                                                                {"label": "Óbitos",
                                                                    "value": 'obitos'},
                                                                {"label": "Curas",
                                                                    "value": 'curas'},
                                                            ],
                                                            value='confirmados',
                                                            inline=True
                                                        ),
                                                        width=2
                                                    ),
                                                ],
                                                align="center"
                                            )
                                        ]),
                                        dbc.CardBody(
                                            dcc.Loading(
                                                dcc.Graph(
                                                    id='acumulados',
                                                    figure=evolucao()
                                                ),
                                                type='dot'
                                            )
                                        ),
                                    ],
                                    className="mb-2"
                                ),
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
                                            dcc.Loading(
                                                dcc.Graph(
                                                    id='scatter-municipios',
                                                    figure=get_figScatter()
                                                ),
                                                type='dot'
                                            )
                                        ),
                                    ],
                                    className="mb-2"
                                )
                            ],
                            className="pl-lg-1",
                            md=12,
                            lg=7
                        )
                    ],
                    className="no-gutters"
                ),
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
