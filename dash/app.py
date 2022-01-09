# -*- coding: utf-8 -*-

import dash
import schedule
from _thread import start_new_thread
from time import sleep
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from components.database import DataBase
from components.dashboard import Dashboard
from components.graficos.Evolucao import evolucao
from components.graficos.Scatter import get_fig_scatter
from components.graficos.TopRegioes import top_regioes
from components.graficos.Treemap import get_treemap
from components.graficos.Indicator import indicators
from components.mapas.Choropleth import get_fig_choropleph
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
    Output("acumulados", "figure"),
    [
        Input("radioitems-evolucao-periodo", "value"),
        Input("radioitems-evolucao-variavel", "value"),
        Input("select-evolucao-municipios", "value"),
        Input("select-evolucao-bairros", "value"),
    ],
)
def on_evolucao_change(periodo, variavel, municipio, bairro):
    return evolucao(periodo, variavel, municipio, bairro)


@app.callback(
    [
        Output("radioitems-evolucao-variavel", "value"),
        Output("radioitems-evolucao-variavel", "disabled")
    ],
    Input("radioitems-evolucao-periodo", "value"),
)
def on_periodo_change(periodo):
    if periodo != 'semanal':
        return '', True

    return 'confirmados', False

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
    if municipio is not None:
        bairros = DataBase.get_df()\
            .query(f'Municipio == "{municipio}"')\
            .sort_values('Bairro')\
            .drop_duplicates()['Bairro']\
            .tolist()

        if len(bairros) > 0:
            transform_label_value = lambda b: { "label": b, "value": b }
            options_bairros = list(map(transform_label_value, bairros))

            return options_bairros, False, None

    return [], True, None

@app.callback(
    Output("top_regioes", "figure"),
    [
        Input("input_top_n", "value"),
        Input("dropdown-top-regioes-variavel", "value"),
    ],
)
def on_top_regioes_change(top_n, variavel):
    return top_regioes(variavel, top_n)

@app.callback(
    Output("treemap", "figure"),
    [
        Input("niveis-treemap", "value"),
        Input("dropdown-treemap-variavel", "value"),
    ],
)
def on_treemap_change(regioes_filtro, variavel):
    return get_treemap(regioes_filtro, variavel)

@app.callback(
    Output("indicators", "figure"),
    Input("select-indicators-municipios", "value"),
)
def on_municipio_indicators_change(municipio):
    return indicators(municipio)

@app.callback(
    [
        Output("scatter-municipios", "figure"),
        Output("select-visualizacao", "disabled"),
    ],
    [
        Input("radioitems-scatter", "value"),
        Input("select-visualizacao", "value")
    ],
)
def on_scatter_change(tipo, tipo_visualizacao):
    return get_fig_scatter(tipo, tipo_visualizacao), tipo == 'casos-obitos'

@app.callback(
    Output("choropleth", "figure"),
    [
        Input("radioitems-choropleth", "value"),
        Input("switch-acumulado-mapa", "value"),
    ],
)
def on_choropleth_change(variavel, switch_acumulado):
    tipo = 'relativo' if len(switch_acumulado) == 0 else 'acumulado'
    return get_fig_choropleph(variavel, tipo)

if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)
