# -*- coding: utf-8 -*-

import plotly.express as px

from ..data import df, df_municipios

figScatterCasosObitosAcumulado = px.scatter(
    df.groupby(['DataNotificacao', 'Municipio'])
        .sum()
        .reset_index()
        .drop_duplicates('Municipio', keep='last')
        .sort_values('ConfirmadosAcumulado')
        .tail(30),
    x='ObitosAcumulado',
    y='ConfirmadosAcumulado',
    color='Municipio',
    size='ConfirmadosAcumulado',
    hover_name='Municipio',
    hover_data={'Municipio': False},
    labels={
        'ObitosAcumulado': 'Óbitos Acumulados',
        'ConfirmadosAcumulado': 'Casos Acumulados',
        'Municipio': '',
    },
    title='Top 30 Municípios'
)

figScatterCasosObitosAcumulado.update_layout(autosize=True, margin={'t': 50, 'r': 0, 'b': 50, 'l': 50})

df_scatter_inc_let = df.groupby(['DataNotificacao', 'Municipio'])\
    .sum()\
    .reset_index()\
    .drop_duplicates('Municipio', keep='last')\
    .merge(df_municipios, on='Municipio', how='left')

df_scatter_inc_let['Incidencia'] = round(df_scatter_inc_let['ConfirmadosAcumulado'] * 10000 / df_scatter_inc_let['PopulacaoEstimada'], 1)
df_scatter_inc_let['Letalidade'] = round(df_scatter_inc_let['ObitosAcumulado'] * 100.0 / df_scatter_inc_let['ConfirmadosAcumulado'], 2)

df_scatter_inc_let = df_scatter_inc_let.dropna()\
    .sort_values('Incidencia')\
    .tail(30)

figScatterIncidenciaLetalidade = px.scatter(
    df_scatter_inc_let, x='Letalidade',
    y='Incidencia',
    color='Municipio',
    size='Incidencia',
    hover_name='Municipio',
    hover_data={'Municipio': False},
    labels={
        'Incidencia': 'Incidência',
        'Municipio': '',
    },
    title='Top 30 Municípios'
)

figScatterIncidenciaLetalidade.update_layout(autosize=True, margin={'t': 50, 'r': 0, 'b': 50, 'l': 50})
