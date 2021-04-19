# -*- coding: utf-8 -*-

import plotly.graph_objects as go
from components.database import DataBase


def get_figAreaAcumulados(tipo='semanal', municipio=None, bairro=None):
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

    query_municipio = f'Municipio == "{municipio}"'
    query_bairro = f'Bairro == "{bairro}"'

    if municipio != None:
        df = df.query(query_municipio)

        if bairro != None:
            df = df.query(query_bairro)

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

    titulo = "Espírito Santo"

    if municipio != None:
        titulo = municipio
        if bairro != None:
            titulo += f' / {bairro}'

    figAreaAcumulados.update_layout(title=titulo, autosize=True, margin={
                                    't': 50, 'r': 0, 'b': 50, 'l': 50}, title_x=0.5)

    figAreaAcumulados.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    return figAreaAcumulados
