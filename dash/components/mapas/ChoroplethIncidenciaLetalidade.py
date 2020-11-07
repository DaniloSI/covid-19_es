# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from ..data import df, df_municipios, municipios

df_choropleph = df.groupby(['DataNotificacao', 'Municipio'])\
    .sum()\
    .reset_index()\
    .drop_duplicates('Municipio', keep='last')\
    .merge(df_municipios, on='Municipio', how='left')
df_choropleph['Incidencia'] = round(df_choropleph['ConfirmadosAcumulado'] * 10000 / df_choropleph['PopulacaoEstimada'], 1)

figChoroplethIncidencia = px.choropleth(
    df_choropleph,
    geojson=municipios,
    locations='codarea',
    featureidkey="properties.codarea",
    color='Incidencia',
    color_continuous_scale="Viridis",
    hover_name='Municipio',
    hover_data={
        'ConfirmadosAcumulado': True,
        'Incidencia': ':.1f',
        'codarea': False},
    labels={
        'codarea': 'Código do Município',
        'ConfirmadosAcumulado': 'Casos',
        'Incidencia': 'Incidência',
    },
    title='Incidência (Total a Cada 10 Mil Habitantes)',
)

figChoroplethIncidencia.update_geos(fitbounds="geojson", visible=False, lataxis_range=[0,500], lonaxis_range=[0, 100])
figChoroplethIncidencia.update_layout(autosize=True, margin={'t': 50, 'r': 0, 'b': 0, 'l': 0}, coloraxis_colorbar_title='')

df_choropleph_letalidade = df.groupby(['DataNotificacao', 'Municipio'])\
    .sum()\
    .reset_index()\
    .drop_duplicates('Municipio', keep='last')\
    .merge(df_municipios, on='Municipio', how='left')

df_choropleph_letalidade['Letalidade'] = round(df_choropleph_letalidade['ObitosAcumulado'] * 100.0 / df_choropleph_letalidade['ConfirmadosAcumulado'], 2)

df_choropleph_letalidade.dropna(inplace=True)

figChoroplethLetalidade = px.choropleth(
    df_choropleph_letalidade,
    geojson=municipios,
    locations='codarea',
    featureidkey="properties.codarea",
    color='Letalidade',
    color_continuous_scale="Magma",
    hover_name='Municipio',
    hover_data={
        'ObitosAcumulado': True,
        'Letalidade': ':.1f',
        'codarea': False},
    labels={
        'codarea': 'Código do Município',
        'ObitosAcumulado': 'Óbitos',
        'Letalidade': 'Letalidade',
    },
    title='Letalidade (%)',
)

figChoroplethLetalidade.update_geos(fitbounds="geojson", visible=False, lataxis_range=[0,500], lonaxis_range=[0, 100])
figChoroplethLetalidade.update_layout(autosize=True, margin={'t': 50, 'r': 0, 'b': 0, 'l': 0}, coloraxis_colorbar_title='')

rowChoropleph = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        dcc.Graph(
                            id='incidencia',
                            figure=figChoroplethIncidencia
                        ),
                    ),
                ],
                className="m-1"
            ),
            md=6,
            className="pr-0"
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        dcc.Graph(
                            id='letalidade',
                            figure=figChoroplethLetalidade
                        ),
                    ),
                ],
                className="m-1"
            ),
            md=6,
            className="pl-0"
        ),
    ]
),