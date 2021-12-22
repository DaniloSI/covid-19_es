# -*- coding: utf-8 -*-

import plotly.express as px

from components.database import DataBase

def get_df_scatter(tipo):
    df = DataBase.get_df()
    df_municipios = DataBase.get_df_municipios()

    df['Periodo'] = df['DataNotificacao'].apply(lambda d: f'{d.year}-{d.month:02d}')

    df_counts_municipios = df[['Periodo', 'Municipio', 'Confirmados', 'Obitos', 'Curas']]\
        .groupby(['Periodo', 'Municipio'])\
        .sum()\
        .reset_index()

    for variavel in ['Confirmados', 'Obitos', 'Curas']:
        df_counts_municipios[f'{variavel}Acumulado'] = df_counts_municipios[['Periodo', 'Municipio', variavel]]\
            .groupby('Municipio')\
            .cumsum()

    if (tipo == 'casos-obitos'):
        return df_counts_municipios[['Periodo', 'Municipio', 'ConfirmadosAcumulado', 'ObitosAcumulado', 'CurasAcumulado']]\
            .sort_values(['ConfirmadosAcumulado', 'ObitosAcumulado', 'CurasAcumulado'])\
            .reset_index()\
            .merge(df_municipios, on='Municipio', how='left')\
            .dropna()\
            .sort_values('Periodo')
    
    if (tipo == 'incidencia-letalidade'):
        df_scatter = df_counts_municipios[['Periodo', 'Municipio', 'Confirmados', 'Obitos', 'Curas']]\
            .groupby(['Periodo', 'Municipio'])\
            .sum()\
            .reset_index()\
            .merge(df_municipios, on='Municipio', how='left')
        
        df_scatter['Incidencia'] = round(
            df_scatter['Confirmados'] * 10000 / df_scatter['PopulacaoEstimada'], 1)
        df_scatter['Letalidade'] = round(
            df_scatter['Obitos'] * 100.0 / df_scatter['Confirmados'], 2)
        
        df_scatter['Letalidade'].fillna(0, inplace=True)

        df_scatter = df_scatter.dropna().sort_values('Periodo')
        
        return df_scatter

def get_fig_by_month(tipo):
    df_scatter = get_df_scatter(tipo)

    if tipo == 'casos-obitos':
        x = 'ObitosAcumulado'
        y = 'ConfirmadosAcumulado'
        columns_renames = {'ObitosAcumulado': 'Óbitos', 'ConfirmadosAcumulado': 'Casos', 'Municipio': ''}
        range_x = [1, 10]
        max_x = df_scatter[x].max()
        
        while (range_x[1] < max_x):
            range_x[1] *= 10
    else:
        x = 'Letalidade'
        y = 'Incidencia'
        columns_renames = {'Incidencia': 'Incidência', 'Municipio': ''}
        range_x=[-1.5, 10]

    fig = px.scatter(
        df_scatter,
        x=x,
        y=y,
        size='PopulacaoEstimada',
        color='Municipio',
        size_max=55,
        animation_frame='Periodo',
        animation_group='Municipio',
        log_x=tipo != 'incidencia-letalidade',
        range_x=range_x,
        labels=columns_renames,
        range_y=[0, df_scatter[y].max()],
        custom_data=['Municipio', 'PopulacaoEstimada']
    )

    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 900
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 8000

    fig.update_layout(height=600, autosize=True, margin={'t': 50, 'r': 0, 'b': 50, 'l': 50}, showlegend=False, title_x=0.5)

    return fig

def get_fig_last_two_weeks():
    df = DataBase.get_df()
    df_municipios = DataBase.get_df_municipios()

    # Gera uma lista com as duas últimas datas presentes nos dados
    datas = df['DataNotificacao']\
        .sort_values(ascending=False)\
        .drop_duplicates()\
        .head(2)\
        .tolist()

    # Filtra os dados que contém as duas últimas datas
    df_counts_two_weeks = df.query(f'DataNotificacao in {datas}')

    # Soma os totais de confirmados e óbitos das duas últimas datas
    df_counts_two_weeks = df_counts_two_weeks[['Municipio', 'Confirmados', 'Obitos', 'Curas']]\
        .groupby(['Municipio'])\
        .sum()\
        .reset_index()\
        .merge(df_municipios, on='Municipio', how='left')\
        .dropna()

    # Calcula a incidência e a letalidade
    df_counts_two_weeks['Incidencia'] = round(df_counts_two_weeks['Confirmados'] * 10000 / df_counts_two_weeks['PopulacaoEstimada'], 1)
    df_counts_two_weeks['Letalidade'] = round(df_counts_two_weeks['Obitos'] * 100.0 / df_counts_two_weeks['Confirmados'], 2)

    return px.scatter(
        df_counts_two_weeks,
        x='Letalidade',
        y='Incidencia',
        size='PopulacaoEstimada',
        color='Municipio',
        size_max=55,
        labels={'Incidencia': 'Incidência', 'Municipio': ''},
        custom_data=['Municipio', 'PopulacaoEstimada']
    )

def get_figScatter(tipo='casos-obitos', tipo_visualizacao='time-elapse'):
    if (tipo == 'incidencia-letalidade' and tipo_visualizacao == 'last-two-weeks'):
        fig = get_fig_last_two_weeks()

    fig = get_fig_by_month(tipo)

    if (tipo == 'casos-obitos'):
        label_y = 'Casos'
        label_x = 'Óbitos'
        symbol_x = ''
    else:
        label_y = 'Incidência'
        label_x = 'Letalidade'
        symbol_x = '%'

    CUSTOM_HOVERTEMPLATE = "<br>".join([
        "<b>%{customdata[0]}</b>",
        label_y + " : %{y:,.}",
        label_x + " : %{x:,.}" + symbol_x,
        "População Estimada: %{customdata[1]:,}",
    ]) + "<extra></extra>"

    fig.update_traces(hovertemplate=CUSTOM_HOVERTEMPLATE)
    for frame in fig.frames:
        for data in frame.data:
            data.hovertemplate = CUSTOM_HOVERTEMPLATE

    fig.update_layout(separators=",.")

    return fig
