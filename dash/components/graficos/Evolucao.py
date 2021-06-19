# -*- coding: utf-8 -*-

import plotly.graph_objects as go
from components.database import DataBase
from components.util import colors
from datetime import date, timedelta


def get_figAreaAcumulados(periodo='semanal', variavel='confirmados', municipio=None, bairro=None):
    df = DataBase.get_df()
    fig = go.Figure()

    if periodo == 'acumulado':
        columns = ['DataNotificacao', 'ConfirmadosAcumulado',
                   'ObitosAcumulado', 'CurasAcumulado']
        columns_renames = {'ConfirmadosAcumulado': 'Confirmados',
                           'ObitosAcumulado': 'Óbitos', 'CurasAcumulado': 'Curas'}
    else:
        columns = ['DataNotificacao', 'Confirmados', 'Obitos', 'Curas']
        columns_renames = {'Confirmados': 'Confirmados',
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

    if variavel == 'confirmados':
        variavel = 'Confirmados'
        cor = colors['red']
    elif variavel == 'obitos':
        variavel = 'Óbitos'
        cor = colors['black']
    else:
        variavel = 'Curas'
        cor = colors['green']

    def get_data_interval(data_inicio):
        data_fim = data_inicio + timedelta(days=6)
        today = date.today()
        
        if today < data_fim:
            data_fim = today

        pattern = '%d/%m/%Y'

        return f'Consolidado de {data_inicio.strftime(pattern)} a {data_fim.strftime(pattern)}'

    if periodo == 'acumulado':
        fig.add_trace(
            go.Scatter(
                x=df_acumulados['DataNotificacao'],
                y=df_acumulados['Confirmados'],
                fill='tozeroy',
                fillcolor=colors['red_transparent'],
                line_color=colors['red'],
                name='Confirmados',
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df_acumulados['DataNotificacao'],
                y=df_acumulados['Curas'],
                fill='tozeroy',
                # fillcolor=f'rgba{(114, 219, 197, 0.6)}',
                fillcolor=colors['green_transparent'],
                line_color=colors['green'],
                name='Curas',
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df_acumulados['DataNotificacao'],
                y=df_acumulados['Óbitos'],
                fill='tozeroy',
                fillcolor=colors['black_transparent'],
                line_color=colors['black'],
                name='Óbitos',
            )
        )
    else:
        fig.add_trace(
            go.Bar(
                x=df_acumulados['DataNotificacao'],
                y=df_acumulados[variavel],
                marker_color=cor,
                name=variavel,
                text=df_acumulados['DataNotificacao'].apply(get_data_interval).tolist(),
                hovertemplate=
                    "<b>%{text}</b><br>" +
                    variavel + ": %{y}" +
                    "<extra></extra>",
            )
        )

    titulo = f'Espírito Santo ({variavel})'

    if municipio != None:
        titulo = municipio
        if bairro != None:
            titulo += f' / {bairro}'

    fig.update_layout(title=titulo, autosize=True, margin={
                                    't': 50, 'r': 0, 'b': 50, 'l': 50}, title_x=0.5)
    
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Arial"
        )
    )

    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    return fig
