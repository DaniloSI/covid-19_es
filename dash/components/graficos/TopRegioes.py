import plotly.express as px
from components.database import DataBase

def top_regioes(variavel, top_n):
    df_covid = DataBase.get_df()

    columns = ['Municipio', 'Bairro']
    df_result_regiao = df_covid.sort_values('DataNotificacao')[columns + [variavel]]\
        .groupby(columns)\
        .sum()\
        .reset_index()\
        .sort_values(variavel)\
        .tail(top_n)

    fig = px.bar(
        df_result_regiao,
        x=variavel,
        y="Bairro",
        color='Municipio',
        orientation='h',
        labels=dict(
            Obitos='Óbitos',
            Confirmados='Casos Confirmados',
            Municipio='Município',
            Bairro=''
        ),
    )
    
    fig.update_layout(
        margin=dict(
            t=0,
            b=0,
            l=35,
            r=0
        )
    )
    
    return fig