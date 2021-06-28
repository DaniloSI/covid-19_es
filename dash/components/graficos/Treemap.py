import plotly.express as px
from components.database import DataBase

def treemap_bairros(municipios=[], top_n=20):
    def get_df():
        df = DataBase.get_df()

        if municipios != None and len(municipios) > 0:
            return df[df['Municipio'].isin(municipios)]
        
        return df
    
    bairros = get_df()\
        .sort_values(by=['DataNotificacao', 'ConfirmadosAcumulado'], ascending=False)\
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