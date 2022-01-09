# -*- coding: utf-8 -*-

import plotly.graph_objects as go
from components.database import DataBase
from components.colors import colors
from datetime import date, timedelta

def _get_df(municipio, bairro):
    df = DataBase.get_df()

    if municipio is not None:
        query = f'Municipio == "{municipio}"'

        if bairro is not None:
            query += f' & Bairro == "{bairro}"'

        return df.query(query)

    return df

def _acumulado(municipio, bairro):
    fig = go.Figure()
    
    df = _get_df(municipio, bairro)[['DataNotificacao', 'ConfirmadosAcumulado', 'ObitosAcumulado', 'CurasAcumulado']]\
        .groupby('DataNotificacao')\
        .sum()\
        .reset_index()
    
    df.columns = ['Data', 'Confirmados', 'Óbitos', 'Recuperados']
    
    scatter = lambda v, color: go.Scatter(
        x = df['Data'],
        y = df[v],
        name = v,
        line = dict(width = 2.5, color = color)
    )
    
    fig.add_trace(scatter('Confirmados', colors['yellow']))
    fig.add_trace(scatter('Óbitos', colors['red']))
    fig.add_trace(scatter('Recuperados', colors['green']))

    fig.update_layout(
        plot_bgcolor="white",
        xaxis=dict(
            rangemode="tozero",
            showline=True,
            showgrid=False,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
        ),
        yaxis=dict(
            rangemode="tozero",
            showline=True,
            showgrid=False,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
        ),
        legend=dict(
            x = 0.5,
            xanchor = 'center',
            orientation = 'h'
        )
    )

    return fig

def _semanal(municipio, bairro, variavel):
    df = _get_df(municipio, bairro)[['DataNotificacao', 'Confirmados', 'Obitos', 'Curas']]\
        .groupby('DataNotificacao')\
        .sum()\
        .reset_index()

    df.columns = ['Data', 'Confirmados', 'Óbitos', 'Recuperados']

    if variavel == 'confirmados':
        variavel = 'Confirmados'
        cor = colors['yellow']
    elif variavel == 'obitos':
        variavel = 'Óbitos'
        cor = colors['red']
    else:
        variavel = 'Recuperados'
        cor = colors['green']

    def get_data_interval(data_inicio):
        data_fim = data_inicio + timedelta(days=6)
        today = date.today()

        if today < data_fim:
            data_fim = today

        pattern = '%d/%m/%Y'

        return f'Consolidado de {data_inicio.strftime(pattern)} a {data_fim.strftime(pattern)}'

    fig = go.Figure(go.Bar(
        x=df['Data'],
        y=df[variavel],
        marker_color=cor,
        name=variavel,
        text=df['Data'].apply(get_data_interval).tolist(),
        hovertemplate=
            "<b>%{text}</b><br>" +
            variavel + ": %{y:,}" +
            "<extra></extra>",
    ))

    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ),
        separators=',.'
    )

    return fig
    

def evolucao(periodo='semanal', variavel='', municipio=None, bairro=None):
    fig = _acumulado(municipio, bairro) if periodo == 'acumulado' else _semanal(municipio, bairro, variavel)

    regiao = 'Espírito Santo'

    if municipio is not None:
        regiao = municipio

        if bairro is not None:
            regiao += f' / {bairro}'

    titulo = f'{regiao} ({variavel})' if periodo != 'acumulado' else regiao

    fig.update_layout(
        title=titulo,
        autosize=True,
        margin=dict(t=50, r=0, b=50, l=50),
        title_x=0.5,
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Arial"
        )
    )

    return fig
