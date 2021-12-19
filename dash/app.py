# -*- coding: utf-8 -*-

import dash
import os
import schedule
from _thread import start_new_thread
from time import sleep
from components.database import DataBase
from components.dashboard import Dashboard
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from components.graficos.Evolucao import evolucao
from components.graficos.Scatter import get_figScatter
from components.graficos.Treemap import treemap
from components.graficos.Indicator import indicators
from components.mapas.Choropleth import Choropleth
from components.observer import Publisher

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    'https://unpkg.com/@tabler/icons@latest/iconfont/tabler-icons.min.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# Padrão Observer para atualizar os dados e o Dashboard de modo geral.
publisher = Publisher()

publisher.subscribe(DataBase)
publisher.subscribe(Dashboard)
publisher.subscribe(Choropleth)
# end

# Instancia a Thread para executar a atualização do Dashboard periodicamente
schedule.every(20)\
    .minutes\
    .do(publisher.notify_subscribers)

def schedule_update(trhead_name, delay):
    while True:
        schedule.run_pending()
        sleep(delay)

start_new_thread(
    schedule_update,
    ("Thread-Update", 1)
)
# end

app.layout = Dashboard.get_dashboard

@app.callback(
    [
        Output("acumulados", "figure"),
        Output(component_id="radioitems-evolucao-variavel", component_property='disabled'),
    ],
    [
        Input("radioitems-evolucao-periodo", "value"),
        Input("radioitems-evolucao-variavel", "value"),
        Input("select-evolucao-municipios", "value"),
        Input("select-evolucao-bairros", "value"),
    ],
)
def on_evolucao_change(periodo, variavel, municipio, bairro):
    return evolucao(periodo, variavel, municipio, bairro), periodo != 'semanal'

@app.callback(
    [
        Output("select-evolucao-bairros", "options"),
        Output("select-evolucao-bairros", "disabled"),
        Output("select-evolucao-bairros", "value"),
    ],
    Input("select-evolucao-municipios", "value"),
    prevent_initial_call=True
)
def on_municipio_change(municipio):
    if municipio != None:
        query_municipio = f'Municipio == "{municipio}"'
        bairros = DataBase.get_df()[['Municipio', 'Bairro']].query(
            query_municipio).sort_values('Bairro').drop_duplicates()['Bairro'].tolist()

        if len(bairros) > 0:
            options_bairros = list(
                map(lambda b: {"label": b, "value": b}, bairros))
            return options_bairros, False, None

    return [], True, None

@app.callback(
    Output("treemap", "figure"),
    [
        Input("select-treemap-municipios", "value"),
        Input("input_top_n", "value"),
        Input("dropdown-treemap-variavel", "value"),
    ],
    prevent_initial_call=True
)
def on_municipio_treemap_change(municipio, top_n, variavel):
    return treemap(municipio, top_n, variavel)

@app.callback(
    Output("indicators", "figure"),
    Input("select-indicators-municipios", "value"),
    prevent_initial_call=True
)
def on_municipio_indicators_change(municipio):
    return indicators(municipio)

@app.callback(
    Output("scatter-municipios", "figure"),
    [
        Input("radioitems-scatter", "value"),
        Input("select-visualizacao", "value")
    ],
    prevent_initial_call=True
)
def on_scatter_change(tipo, tipo_visualizacao):
    return get_figScatter(tipo, tipo_visualizacao)

@app.callback(
    Output("choropleth", "figure"),
    Input("radioitems-choropleth", "value"),
    prevent_initial_call=True
)
def on_choropleth_change(tipo):
    return Choropleth.get_figChoropleph(tipo)

if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)
