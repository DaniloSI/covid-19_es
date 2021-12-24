# -*- coding: utf-8 -*-

import plotly.express as px
from urllib.request import urlopen
import json

from components.database import DataBase
from components.observer import Subscriber

def get_df_choropleph(tipo_visualizacao):
    df_counts = DataBase.get_df()
    df_municipios = DataBase.get_df_municipios()

    df_counts['Periodo'] = df_counts['DataNotificacao'].apply(lambda d: f'{d.year}-{d.month:02d}')

    # Calcula confirmados, obitos e curas por mês
    df_counts_municipios = df_counts[['Periodo', 'Municipio', 'Confirmados', 'Obitos', 'Curas']]\
        .groupby(['Periodo', 'Municipio'])\
        .sum()\
        .reset_index()

    # Calcula os acumulados por mês
    for variavel in ['Confirmados', 'Obitos', 'Curas']:
        df_counts_municipios[f'{variavel}Acumulado'] = df_counts_municipios[['Periodo', 'Municipio', variavel]]\
            .groupby('Municipio')\
            .cumsum()
    
    if (tipo_visualizacao == 'relativo'):
        df_choropleph_relativo = df_counts_municipios[['Periodo', 'Municipio', 'Confirmados', 'Obitos', 'Curas']]\
            .groupby(['Periodo', 'Municipio'])\
            .sum()\
            .reset_index()\
            .merge(df_municipios, on='Municipio', how='left')\
            .fillna(0)
    else:
        df_choropleph_relativo = df_counts_municipios[['Periodo', 'Municipio', 'ConfirmadosAcumulado', 'ObitosAcumulado']]\
            .sort_values(['ConfirmadosAcumulado', 'ObitosAcumulado'])\
            .reset_index()\
            .merge(df_municipios, on='Municipio', how='left')\
            .fillna(0)\
            .sort_values('Periodo')\
            .rename({'ConfirmadosAcumulado': 'Confirmados', 'ObitosAcumulado': 'Obitos'}, axis=1)

    confirmados_relativo = df_choropleph_relativo['Confirmados']
    obitos_relativo = df_choropleph_relativo['Obitos']
    populacao_estimada = df_choropleph_relativo['PopulacaoEstimada']

    df_choropleph_relativo['Incidencia'] = round(confirmados_relativo * 100_000 / populacao_estimada, 1)
    df_choropleph_relativo['Letalidade'] = obitos_relativo / confirmados_relativo

    df_choropleph_relativo['Letalidade'].fillna(0, inplace=True)

    df_choropleph_relativo = df_choropleph_relativo.dropna().sort_values('Periodo')

    df_choropleph_relativo

    return df_choropleph_relativo

def get_fig_choropleph(variavel, tipo_visualizacao):
    # Labels
    labels = {
        'Incidencia': 'Incidência',
        'Letalidade': 'Letalidade',
        'relativo': 'Relativo ao Período',
        'acumulado': 'Acumulado'
    }

    # DataFrame
    df_choropleph = get_df_choropleph(tipo_visualizacao)
    df_choropleph = df_choropleph[df_choropleph['codarea'] != 0]

    # Mapa Coroplético
    color = 'Ice' if variavel.lower() == 'incidencia' else 'Solar'
    
    with urlopen("https://gist.githubusercontent.com/DaniloSI/ec490ce7ef3336c5d7c7c6ea946ae8b4/raw/242984da9784de0d1bbff85e318d46daa1075e04/Malha_Geografica_ES.geojson") as url:
        municipios = json.loads(url.read())

    fig = px.choropleth(
        df_choropleph,
        geojson=municipios,
        locations='codarea',
        featureidkey="properties.codarea",
        color=variavel,
        color_continuous_scale=color,
        animation_frame='Periodo',
        title=f'{labels[variavel]} - {labels[tipo_visualizacao]}',
        custom_data=[
            df_choropleph['Municipio'],
            df_choropleph[variavel],
            df_choropleph['Confirmados'],
            df_choropleph['Obitos'],
            df_choropleph['PopulacaoEstimada'],
            df_choropleph['Periodo'],
        ]
    )

    if variavel.lower() == 'incidencia':
        variavel_hovertemplate = '%{customdata[1]:,} casos a cada 100 mil habitantes'
        colorbar_tickformat = ','
    elif variavel.lower() == 'letalidade':
        variavel_hovertemplate = '%{customdata[1]:.1%}'
        colorbar_tickformat = '.1%'

    CUSTOM_HOVERTEMPLATE = "<br>".join([
        "<b>%{customdata[0]}</b>",
        f"{labels[variavel]}: " + variavel_hovertemplate,
        "Quantidade de Casos: %{customdata[2]:,}",
        "Quantidade de Óbitos: %{customdata[3]:,}",
        "Quantidade Estimada de Habitantes: %{customdata[4]:,}",
    ]) + "<extra>%{customdata[5]}</extra>"

    fig.update_traces(hovertemplate=CUSTOM_HOVERTEMPLATE)

    for frame in fig.frames:
        for data in frame.data:
            data.hovertemplate = CUSTOM_HOVERTEMPLATE

    fig.update_geos(fitbounds="geojson", visible=False, lataxis_range=[0,500], lonaxis_range=[0, 900])

    fig.update_layout(
        height=800,
        autosize=True,
        margin={'t': 50, 'r': 0, 'b': 0, 'l': 0},
        coloraxis=dict(
            colorbar=dict(title='', tickformat=colorbar_tickformat)
        ),
        title_x=0.5,
        separators=",."
    )

    return fig

class Choropleth(Subscriber):
    _choropleths = {}

    @staticmethod
    def update():
        Choropleth._choropleths['Incidencia'] = get_fig_choropleph('Incidencia', 'relativo')
        Choropleth._choropleths['Letalidade'] = get_fig_choropleph('Letalidade', 'relativo')
        Choropleth._choropleths['IncidenciaAcumulado'] = get_fig_choropleph('Incidencia', 'acumulado')
        Choropleth._choropleths['LetalidadeAcumulado'] = get_fig_choropleph('Letalidade', 'acumulado')

    @staticmethod
    def get_figChoropleph(variavel):
        if len(Choropleth._choropleths) == 0:
            Choropleth.update()

        return Choropleth._choropleths[variavel]
