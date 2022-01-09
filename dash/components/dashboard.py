# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_bootstrap_components as dbc


from components.filtros.Select import dropdown_municipios
from components.navbar import navbar

from components.observer import Subscriber

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
                                # Indicadores
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            dbc.Row(
                                                dbc.Col(dropdown_municipios('select-indicators-municipios'), width=6)
                                            )
                                        ),
                                        dbc.CardBody(
                                            dbc.Row(
                                                dbc.Col(
                                                    dcc.Loading(
                                                        dcc.Graph(id='indicators'),
                                                        type='dot'
                                                    )
                                                )
                                            )
                                        )
                                    ],
                                    className="mb-2"
                                ),
                                # Top Regiões
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                dbc.Row(
                                                    [
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
                                                                id="dropdown-top-regioes-variavel",
                                                                options=[
                                                                    {"label": "Confirmados",
                                                                        "value": 'Confirmados'},
                                                                    {"label": "Óbitos",
                                                                        "value": 'Obitos'},
                                                                    {"label": "Recuperados",
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
                                                dcc.Graph(id='top_regioes'),
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
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.Select(
                                                            id="radioitems-choropleth",
                                                            options=[
                                                                {'label': 'Incidência',
                                                                    'value': 'Incidencia'},
                                                                {'label': 'Letalidade',
                                                                    'value': 'Letalidade'},
                                                            ],
                                                            value='Incidencia',
                                                        )
                                                    ),
                                                    dbc.Col(
                                                        dbc.Checklist(
                                                            options=[
                                                                {"label": "Acumulado", "value": 1},
                                                            ],
                                                            value=[],
                                                            id="switch-acumulado-mapa",
                                                            switch=True,
                                                        ),
                                                    ),
                                                ],
                                                style={'alignItems': 'center'}
                                            )
                                        ),
                                        dbc.CardBody(
                                            dcc.Loading(
                                                dcc.Graph(id='choropleth'),
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
                                                            value='semanal',
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
                                                                {"label": "Recuperados",
                                                                    "value": 'curas'},
                                                            ],
                                                            value='',
                                                            clearable=False,
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
                                                dcc.Graph(id='acumulados'),
                                                type='dot'
                                            )
                                        ),
                                    ],
                                    className="mb-2"
                                ),
                                # Treemap
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dcc.Dropdown(
                                                                id='niveis-treemap',
                                                                options=[
                                                                    {'label': 'Mesorregião', 'value': 'Mesorregiao'},
                                                                    {'label': 'Microrregião', 'value': 'Microrregiao'}
                                                                ],
                                                                value=['Mesorregiao', 'Microrregiao'],
                                                                multi=True,
                                                                placeholder='Selecione os níveis de região...'
                                                            )
                                                        ),
                                                        dbc.Col(
                                                            dcc.Dropdown(
                                                                id="dropdown-treemap-variavel",
                                                                options=[
                                                                    {"label": "Confirmados",
                                                                        "value": 'Confirmados'},
                                                                    {"label": "Óbitos",
                                                                        "value": 'Obitos'},
                                                                    {"label": "Recuperados",
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
                                                dcc.Graph(id='treemap'),
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
                                                                {"label": "Casos x Óbitos (Acumulado)",
                                                                    "value": 'casos-obitos'},
                                                                {"label": "Incidência x Letalidade",
                                                                    "value": 'incidencia-letalidade'},
                                                            ],
                                                            value='casos-obitos',
                                                            inline=True
                                                        ),
                                                    ),
                                                    dbc.Col(
                                                        dbc.Select(
                                                            id="select-visualizacao",
                                                            options=[
                                                                {"label": "Últimas 2 semanas",
                                                                    "value": 'last-two-weeks'},
                                                                {"label": "Animação mês a mês",
                                                                    "value": 'time-elapse'},
                                                            ],
                                                            value='time-elapse',
                                                        ),
                                                    ),
                                                ],
                                                align="center"
                                            )
                                        ]),
                                        dbc.CardBody(
                                            dcc.Loading(
                                                dcc.Graph(id='scatter-municipios'),
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
