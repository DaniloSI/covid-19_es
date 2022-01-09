import plotly.express as px
from components.database import DataBase

def get_treemap(regioes_filtro, variavel):
    df = DataBase.get_df_full().drop(['ConfirmadosAcumulado', 'ObitosAcumulado', 'CurasAcumulado'], axis=1)

    regioes = ['Mesorregiao', 'Microrregiao', 'Municipio', 'Bairro']
    columns = regioes + [variavel]
    df_treemap = df.sort_values('DataNotificacao')[columns]\
        .groupby(regioes)\
        .sum()\
        .reset_index()\
        .sort_values(variavel)

    fig = fig = px.treemap(
        df_treemap,
        path=[px.Constant("ESPIRITO SANTO")] + regioes_filtro + ['Municipio', 'Bairro'],
        values=variavel,
        custom_data=regioes,
    )

    fig.update_traces(
        hovertemplate='<br />'.join([
            '<b>' + variavel + ': %{value:,}</b>',
            '',
            'Mesorregião: %{customdata[0]}',
            'Microrregião: %{customdata[1]}',
            'Município: %{customdata[2]}',
            'Bairro: %{customdata[3]}',
        ]),
        texttemplate='%{label} <br /> %{value:,}'
    )
    fig.update_layout(
        margin = dict(t=55, l=0, r=0, b=25),
        height=700,
        separators=',.'
    )
    
    return fig