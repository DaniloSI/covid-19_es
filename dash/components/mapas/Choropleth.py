# -*- coding: utf-8 -*-

import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from ..data import df_municipios, municipios
from components.database import DataBase

from datetime import date


def relative_month(reference_date, current_date):
    # Calcula o mês relativo à data de referência (reference_date)
    return int((current_date - reference_date).days / 30) + 1


def get_label(propriedade):
    if propriedade == 'Incidencia':
        return 'Incidência'
    elif propriedade == 'ConfirmadosAcumulado':
        return 'Confirmados'
    elif propriedade == 'ObitosAcumulado':
        return 'Óbitos'
    else:
        return 'Letalidade'


def get_equivalente(propriedade):
    if propriedade == 'Incidencia':
        return 'ConfirmadosAcumulado'
    elif propriedade == 'ConfirmadosAcumulado':
        return 'Incidencia'
    elif propriedade == 'ObitosAcumulado':
        return 'Letalidade'
    else:
        return 'ObitosAcumulado'


def get_format(propriedade):
    if propriedade == 'Incidencia':
        return ':.1f'
    elif propriedade == 'Letalidade':
        return ':.2%'
    else:
        return ':d'


def get_tickformat(propriedade):
    if propriedade == 'Letalidade':
        return '.0%'

    return 's'


def get_color_scale(propriedade):
    if propriedade == 'Incidencia' or propriedade == 'ConfirmadosAcumulado':
        return px.colors.sequential.Viridis[::-1]

    return px.colors.sequential.Magma[::-1]


def get_figChoropleph(propriedade):
    df = DataBase.get_df()

    df_choropleph = df.groupby(['DataNotificacao', 'Municipio'])\
        .sum()\
        .reset_index()\
        .merge(df_municipios, on='Municipio', how='left')

    df_choropleph['Incidencia'] = round(
        df_choropleph['ConfirmadosAcumulado'] * 10000 / df_choropleph['PopulacaoEstimada'], 1)
    df_choropleph['Letalidade'] = round(
        df_choropleph['ObitosAcumulado'] * 1.0 / df_choropleph['ConfirmadosAcumulado'], 4)

    df_choropleph = df_choropleph[df_choropleph['PopulacaoEstimada'] >= 0]
    df_choropleph['DataNotificacao'] = pd.to_datetime(
        df_choropleph['DataNotificacao'])

    reference_date = df_choropleph['DataNotificacao'].min()
    df_choropleph['Mes'] = df_choropleph['DataNotificacao'].apply(
        lambda d: relative_month(reference_date, d))

    label = get_label(propriedade)
    propriedade_equivalente = get_equivalente(propriedade)
    label_equivalente = get_label(propriedade_equivalente)
    format_value = get_format(propriedade)
    color_scale = get_color_scale(propriedade)
    tickformat = get_tickformat(propriedade)

    figChoropleth = px.choropleth(
        df_choropleph.fillna(0),
        geojson=municipios,
        locations='codarea',
        featureidkey="properties.codarea",
        color=propriedade,
        color_continuous_scale=color_scale,
        hover_name='Municipio',
        hover_data={
            propriedade_equivalente: True,
            propriedade: format_value,
            'codarea': False},
        labels={
            'codarea': 'Código do Município',
            propriedade_equivalente: label_equivalente,
            propriedade: label,
            'Mes': 'Mês Relativo'
        },
        animation_frame='Mes',
        title=label,
    )

    figChoropleth.update_geos(
        fitbounds="geojson", visible=False, lataxis_range=[0, 500], lonaxis_range=[0, 100])
    figChoropleth.update_layout(height=600, autosize=True, margin={
        't': 50, 'r': 0, 'b': 0, 'l': 0}, coloraxis=dict(colorbar=dict(tickformat=tickformat, title='')), title_x=0.5)

    figChoropleth.layout['sliders'][0]['active'] = len(
        figChoropleth.frames) - 1

    return go.Figure(data=figChoropleth['frames'][-1]['data'], frames=figChoropleth['frames'], layout=figChoropleth.layout)
