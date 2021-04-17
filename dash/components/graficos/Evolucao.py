# -*- coding: utf-8 -*-

import plotly.graph_objects as go
from components.database import DataBase


def get_figAreaAcumulados(tipo='acumulado'):
    df = DataBase.get_df()
    figAreaAcumulados = go.Figure()

    if tipo == 'acumulado':
        columns = ['DataNotificacao', 'ConfirmadosAcumulado',
                   'ObitosAcumulado', 'CurasAcumulado']
        columns_renames = {'ConfirmadosAcumulado': 'Casos',
                           'ObitosAcumulado': 'Óbitos', 'CurasAcumulado': 'Curas'}
    else:
        columns = ['DataNotificacao', 'Confirmados', 'Obitos', 'Curas']
        columns_renames = {'Confirmados': 'Casos',
                           'Obitos': 'Óbitos', 'Curas': 'Curas'}

    df_acumulados = df[columns]\
        .groupby(['DataNotificacao'])\
        .sum()\
        .reset_index()\
        .rename(columns_renames, axis=1)

    figAreaAcumulados.add_trace(
        go.Scatter(
            x=df_acumulados['DataNotificacao'],
            y=df_acumulados['Casos'],
            fill='tozeroy',
            fillcolor=f'rgba{(99, 100, 250, 0.3)}',
            line_color='#636EFA',
            name='Casos',
        )
    )

    figAreaAcumulados.add_trace(
        go.Scatter(
            x=df_acumulados['DataNotificacao'],
            y=df_acumulados['Curas'],
            fill='tozeroy',
            fillcolor=f'rgba{(114, 219, 197, 0.6)}',
            line_color='#00CC96',
            name='Curas',
        )
    )

    figAreaAcumulados.add_trace(
        go.Scatter(
            x=df_acumulados['DataNotificacao'],
            y=df_acumulados['Óbitos'],
            fill='tozeroy',
            fillcolor=f'rgba{(239, 85, 59, 0.6)}',
            line_color='#EF553B',
            name='Óbitos',
        )
    )

    figAreaAcumulados.update_layout(title="Evolução Total do Espírito Santo", autosize=True, margin={
                                    't': 50, 'r': 0, 'b': 50, 'l': 50})

    return figAreaAcumulados
