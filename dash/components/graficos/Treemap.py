import plotly.express as px
from components.database import DataBase

def treemap_bairros(top_n):
    bairros = DataBase.get_df().sort_values(by=['DataNotificacao', 'ConfirmadosAcumulado'], ascending=False)\
        .drop_duplicates(subset=['Municipio', 'Bairro'])\
        .head(top_n)
    
    bairros['Estado'] = 'Espírito Santo'
    
    fig = px.treemap(
        bairros,
        path=['Estado', 'Municipio', 'Bairro'],
        values='ConfirmadosAcumulado',
    )

    fig.update_layout(autosize=True, margin={'t': 0, 'r': 0, 'b': 0, 'l': 0}, title_x=0.5)

    return fig