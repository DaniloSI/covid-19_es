# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv('../notebooks_output/microdados_pre-processed.csv', sep=',', encoding='UTF-8')

fig = px.line(
    df.groupby(['DataNotificacao', 'Municipio'])
        .sum()
        .reset_index()
        .query('Municipio == "VITORIA" | Municipio == "SERRA"'),
    x="DataNotificacao",
    y="Obitos",
    color="Municipio",
    hover_name="Municipio",
    labels={
        'DataNotificacao': 'Data',
        'Obitos': 'Óbitos',
        'Municipio': 'Município'
    }
)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)