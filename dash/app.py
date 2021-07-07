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
from components.mapas.Choropleth import Choropleth

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    'https://unpkg.com/@tabler/icons@latest/iconfont/tabler-icons.min.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


def data_update():
    DataBase.refresh()
    Dashboard.render()
    Choropleth.render()


schedule.every(20).minutes.do(data_update)


def schedule_update(trhead_name, delay):
    while True:
        schedule.run_pending()
        sleep(delay)


start_new_thread(schedule_update, ("Thread-Update", 1))

app.layout = Dashboard.get_dashboard


@app.callback(
    [
        Output("acumulados", "figure"),
        Output(component_id="radioitems-evolucao-variavel", component_property='style'),
    ],
    [
        Input("radioitems-evolucao-periodo", "value"),
        Input("radioitems-evolucao-variavel", "value"),
        Input("select-evolucao-municipios", "value"),
        Input("select-evolucao-bairros", "value"),
    ],
)
def on_evolucao_change(periodo, variavel, municipio, bairro):
    display = {'display': 'none'}

    if periodo == 'semanal':
        display = {'display': 'block'}

    return evolucao(periodo, variavel, municipio, bairro), display


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
        Input("slider_top_n", "value"),
    ],
    prevent_initial_call=True
)
def on_municipios_change(municipio, top_n):
    return treemap(municipio, top_n)


@app.callback(
    Output("scatter-municipios", "figure"),
    Input("radioitems-scatter", "value"),
    prevent_initial_call=True
)
def on_scatter_change(tipo):
    return get_figScatter(tipo)


@app.callback(
    Output("choropleth", "figure"),
    Input("radioitems-choropleth", "value"),
    prevent_initial_call=True
)
def on_choropleth_change(tipo):
    return Choropleth.get_figChoropleph(tipo)

# radioitems-choropleth


if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)
