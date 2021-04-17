# -*- coding: utf-8 -*-

import dash
import os
import schedule
from _thread import start_new_thread
from time import sleep
from components.database import DataBase
from components.dashboard import Dashboard
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from components.graficos.Evolucao import get_figAreaAcumulados

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server


def data_update():
    DataBase.refresh()
    Dashboard.render()


schedule.every(20).minutes.do(data_update)


def schedule_update(trhead_name, delay):
    while True:
        schedule.run_pending()
        sleep(delay)


start_new_thread(schedule_update, ("Thread-Update", 1))

app.layout = Dashboard.get_dashboard


@app.callback(
    Output("acumulados", "figure"),
    Input("radioitems-evolucao", "value"),
)
def on_form_change(radioitems_evolucao_value):
    return get_figAreaAcumulados(radioitems_evolucao_value)


if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)
