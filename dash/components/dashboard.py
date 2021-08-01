# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from components.filtros.Select import dropdown_municipios
from components.graficos.Evolucao import evolucao
from components.graficos.Scatter import get_figScatter
from components.graficos.Treemap import treemap
from components.graficos.Indicator import indicators
from components.mapas.Choropleth import Choropleth
from components.navbar import navbar

from components.database import DataBase
from components.observer import Subscriber


def total_casos_es():
    total_confirmados = int(DataBase.get_df()['Confirmados'].sum())
    return '{:,}'.format(total_confirmados).replace(',', '.')


def total_obitos_es():
    total_obitos = int(DataBase.get_df()['Obitos'].sum())
    return '{:,}'.format(total_obitos).replace(',', '.')


def total_curas_es():
    total_curas = int(DataBase.get_df()['Curas'].sum())
    return '{:,}'.format(total_curas).replace(',', '.')


class Dashboard(Subscriber):
    _dashboard = None

    @staticmethod
    def update():
        print('----- # -----')
        print('Renderizando o Dashboard...')
        Dashboard._dashboard = dbc.Container(
            [
                navbar(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                # Treemap
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dropdown_municipios('select-treemap-municipios', True),
                                                            xs=True
                                                        ),
                                                        dbc.Col(
                                                            dbc.InputGroup(
                                                                [
                                                                    dbc.InputGroupAddon("Top", addon_type="prepend"),
                                                                    dbc.Input(
                                                                        id='input_top_n',
                                                                        type="number",
                                                                        min=0,
                                                                        step=1,
                                                                        value=10
                                                                    ),
                                                                ],
                                                            ),
                                                            width=3,
                                                            style={
                                                                'padding-left': '10px'
                                                            }
                                                        ),
                                                        dbc.Col(
                                                            dcc.Dropdown(
                                                                id="dropdown-treemap-variavel",
                                                                options=[
                                                                    {"label": "Confirmados",
                                                                        "value": 'Confirmados'},
                                                                    {"label": "Óbitos",
                                                                        "value": 'Obitos'},
                                                                    {"label": "Curas",
                                                                        "value": 'Curas'},
                                                                ],
                                                                value='Confirmados',
                                                                clearable=False
                                                            ),
                                                            width=4,
                                                            style={
                                                                'padding-left': '10px'
                                                            }
                                                        )
                                                    ],
                                                    align="center",
                                                    no_gutters=True
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
                                # Mapa Coroplético
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
                                # Indicadores
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            dbc.Row(
                                                dbc.Col(dropdown_municipios('select-indicators-municipios', True), width=6)
                                            )
                                        ),
                                        dbc.CardBody(
                                            dbc.Row(
                                                dbc.Col(
                                                    dcc.Loading(
                                                        dcc.Graph(
                                                            id='indicators',
                                                            figure=indicators()
                                                        ),
                                                        type='dot'
                                                    )
                                                )
                                            )
                                        )
                                    ],
                                    className="mb-2"
                                ),
                                # Evolução
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
                                                        xs=True,
                                                        style={
                                                            'padding-left': '10px'
                                                        }
                                                    ),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            id="radioitems-evolucao-periodo",
                                                            options=[
                                                                {"label": "Acumulado",
                                                                    "value": 'acumulado'},
                                                                {"label": "Semanal",
                                                                    "value": 'semanal'},
                                                            ],
                                                            value='acumulado',
                                                            clearable=False,
                                                        ),
                                                        width=2,
                                                        style={
                                                            'padding-left': '10px'
                                                        }
                                                    ),
                                                    dbc.Col(
                                                        dcc.Dropdown(
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
                                                            clearable=False,
                                                            disabled=True
                                                        ),
                                                        width=4,
                                                        style={
                                                            'padding-left': '10px'
                                                        }
                                                    )
                                                ],
                                                align="center",
                                                no_gutters=True
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
                                # Pairplot
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
            Dashboard.update()

        return Dashboard._dashboard
