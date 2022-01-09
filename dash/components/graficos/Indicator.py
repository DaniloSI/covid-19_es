# -*- coding: utf-8 -*-

import plotly.graph_objects as go
from components.database import DataBase
from components.colors import colors

def _get_dates(df):
    ultima = df['DataNotificacao'].max()
    penultima = df.query(f'DataNotificacao < "{ultima}"')['DataNotificacao'].max()
    antepenultima = df.query(f'DataNotificacao < "{penultima}"')['DataNotificacao'].max()
    
    return penultima, antepenultima

def _make_indicator(title, value, reference, domain={}, show_delta=True):
    mode = 'number'
    
    if show_delta:
        mode += '+delta'
    
    return go.Indicator(
        mode = mode,
        value = value,
        title = {
            'text': f'<span style="font-size: 18px">{title}</span>'
        },
        number = {
            'font': { 'size': 48 }, 'valueformat':','
        },
        delta = {
            'reference': reference,
            'relative': True,
            'increasing': {'color': colors['red']},
            'decreasing': {'color': colors['green']},
            'font': { 'size': 18 },
            'position': 'right'
        },
        domain=domain
    )

def _indicator(df, first_date, second_date, variavel, domain, show_delta=True):
    calcula_valor = lambda d: int(df.query(f'DataNotificacao == "{d}"')[variavel].sum())

    penultimo_valor = calcula_valor(first_date)
    antepenultimo_valor = calcula_valor(second_date)

    get_label = lambda v: {
        'Confirmados': 'Confirmados',
        'Obitos': 'Óbitos',
        'Curas': 'Recuperados',
    }[v]
    
    return _make_indicator(get_label(variavel), penultimo_valor, antepenultimo_valor, domain, show_delta)

def indicators(municipio=None):
    location = 'Espírito Santo'
    fig = go.Figure()
    df = DataBase.get_df()

    if municipio is not None and municipio != '':
        df = df.query(f'Municipio == "{municipio}"')
        location = municipio

    penultima_data, antepenultima_data = _get_dates(df)

    fig.add_trace(_indicator(df, penultima_data, antepenultima_data, 'Confirmados', {'row': 0, 'column': 0}))
    fig.add_trace(_indicator(df, penultima_data, antepenultima_data, 'Obitos', {'row': 0, 'column': 1}))
    fig.add_trace(_indicator(df, penultima_data, antepenultima_data, 'Curas', {'row': 0, 'column': 2}, False))

    title = f'Comparação entre os últimos consolidados, sendo {antepenultima_data.strftime("%d/%m/%y")} e {penultima_data.strftime("%d/%m/%y")}'
    fig.update_layout(
        height = 200,
        grid = dict(rows=1, columns=3, pattern='independent'),
        title = dict(
            text=f'<span style="color: #2a3f5f">{location}</span><br /><span style="color: #afafaf; font-size: 14px">{title}</span>',
            x=0.5,
            y=0.9,
            font=dict(color='#afafaf')
        ),
        margin = dict(t=90, r=0, b=0, l=0),
        autosize=True,
        separators=',.'
    )

    return fig