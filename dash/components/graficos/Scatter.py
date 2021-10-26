# -*- coding: utf-8 -*-

import plotly.express as px

from components.database import DataBase


def get_figScatter(tipo='casos-obitos'):
    df = DataBase.get_df()
    df_municipios = DataBase.get_df_municipios()

    df_scatter = df.groupby(['DataNotificacao', 'Municipio'])\
        .sum()\
        .reset_index()\
        .drop_duplicates('Municipio', keep='last')\
        .merge(df_municipios, on='Municipio', how='left')

    df_scatter['Incidencia'] = round(
        df_scatter['ConfirmadosAcumulado'] * 10000 / df_scatter['PopulacaoEstimada'], 1)
    df_scatter['Letalidade'] = round(
        df_scatter['ObitosAcumulado'] * 100.0 / df_scatter['ConfirmadosAcumulado'], 2)

    df_scatter = df_scatter.dropna()\
        .sort_values('Incidencia')

    if tipo == 'casos-obitos':
        df_scatter = df_scatter.sort_values('ConfirmadosAcumulado')
        x = 'ObitosAcumulado'
        y = 'ConfirmadosAcumulado'
        columns_renames = {'ObitosAcumulado': 'Óbitos',
                           'ConfirmadosAcumulado': 'Casos', 'Municipio': ''}
    else:
        x = 'Letalidade'
        y = 'Incidencia'
        columns_renames = {'Incidencia': 'Incidência', 'Municipio': ''}

    figScatter = px.scatter(
        df_scatter,
        x=x,
        y=y,
        color='Municipio',
        size=y,
        hover_name='Municipio',
        hover_data={'Municipio': False},
        size_max=55 if tipo == 'casos-obitos' else 45,
        log_x=tipo == 'casos-obitos',
        labels=columns_renames,
        title='Municípios'
    )

    figScatter.update_layout(
        autosize=True, margin={'t': 50, 'r': 0, 'b': 50, 'l': 50}, showlegend=False, title_x=0.5)

    return figScatter
