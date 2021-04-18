# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime
import plotly.graph_objects as go

from components.graficos.Evolucao import get_figAreaAcumulados
from components.graficos.ScatterMunicipio import get_figScatter
from components.mapas.ChoroplethIncidenciaLetalidade import get_rowChoropleph

from components.database import DataBase


def get_indicator(title, value, reference, subtitle='', subsubtitle='', maior_melhor=False):
    fig = go.Figure()

    colors = {
        'red': '#FF4136',
        'green': '#3D9970',
    }

    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=value,
            title={"text": f"{title}<br><span style='font-size:0.8em;color:gray'>{subtitle}</span><br><span style='font-size:0.8em;color:gray'>{subsubtitle}</span>"},
            delta={
                'reference': reference,
                'relative': True,
                'increasing': {
                    'color': colors['red' if not maior_melhor else 'green']
                },
                'decreasing': {
                    'color': colors['red' if maior_melhor else 'green']
                }
            },
        )
    )

    fig.update_layout(height=170, margin={'t': 80, 'l': 10, 'b': 10, 'r': 10})

    return fig


def get_figIndicator(propriedade, label, maior_melhor=False):
    df = DataBase.get_df()
    atual = int(df[propriedade].sum())
    ultima_data = df['DataNotificacao'].max()
    anterior = int(df.query(
        f'DataNotificacao != "{ultima_data}"')[propriedade].sum())

    return get_indicator(label, atual, anterior, 'Em todo o estado', maior_melhor=maior_melhor)


def date_interval_text():
    str_format = '%d/%m/%Y'
    data_notificacao = DataBase.get_df()['DataNotificacao']

    if type(data_notificacao.min()) != str:
        data_primeira_notificacao = data_notificacao.min().strftime(str_format)
        data_ultima_notificacao = data_notificacao.max().strftime(str_format)
    else:
        data_primeira_notificacao = datetime.fromisoformat(
            data_notificacao.min()).strftime(str_format)
        data_ultima_notificacao = datetime.fromisoformat(
            data_notificacao.max()).strftime(str_format)

    return f'De {data_primeira_notificacao} até {data_ultima_notificacao}'


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
                        style={'textAlign': "center", 'fontWeight': 400, 'margin': '25px 0px 0px 0px'}),
                html.H6(date_interval_text(),
                        style={'textAlign': "center", 'fontWeight': 200, 'margin': '10px 0px 25px 0px'}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
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
                                )
                            ],
                            className="pr-0",
                            width=6
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    dbc.CardBody(
                                        dbc.Row([
                                            dbc.Col(
                                                dcc.Graph(
                                                    id="indicador-confirmados",
                                                    figure=get_figIndicator(
                                                        'Confirmados', 'Casos')
                                                ),
                                                style={'padding': 0}
                                            ),
                                            dbc.Col(
                                                dcc.Graph(
                                                    id="indicador-obitos",
                                                    figure=get_figIndicator(
                                                        'Obitos', 'Óbitos')
                                                ),
                                                style={'padding': 0}
                                            ),
                                            dbc.Col(
                                                dcc.Graph(
                                                    id="indicador-curas",
                                                    figure=get_figIndicator(
                                                        'Curas', 'Curas', maior_melhor=True)
                                                ),
                                                style={'padding': 0}
                                            ),
                                        ])
                                    ),
                                    className="m-1"
                                ),
                                get_rowChoropleph()
                            ],
                            className="pl-0",
                            width=6
                        )
                    ]
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
