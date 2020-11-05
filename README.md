# COVID-19 no Espírito Santo

## Estrutura do Projeto

O diagrama abaixo apresenta a organização de pastas do projeto.

```
.
├── dash
│   ├── app.py
│   └── assets
│       └── page.css
├── data_source
│   ├── ES_MALHA_MUNICIPIOS.geojson
│   └── municipios.csv
├── notebooks
│   ├── Data-visualizations.ipynb
│   └── Pre-processing.ipynb
├── notebooks_output
│   └── microdados_pre-processed.csv
├── notebooks_source
│   └── README.txt
├── Procfile
├── README.md
└── requirements.txt
```

Significado de cada pasta e item do projeto:
- **dash**: Possui o código fonte responsável pelo Dashboard e utiliza a ferramenta Dash do Plotly.
  - **app.py**: Contém o código python para gerar os componentes do *Dash Core* e do *Dash Html*. Além disso é utilizado para servir a página HTML do Dashboard.
  - **assets**: Contém as estilizações customizadas para a página HTML do Dashboard.
- **data_source**: Contém os dados que foram coletados do IBGE e pré-processados. Esses dados são utilizados para gerar bases de dados enriquecidas, através da integrção com a base de dados do [painel da COVID-19](https://coronavirus.es.gov.br/painel-covid-19-es).
- **notebooks**: Contém os notebooks responsáveis por realizar o pré-processamento dos dados e para gerar um "rascunho" das visualizações contidas no Dashboard.
- **notebooks_output**: Contém o resultado do pré-processamento realizado no notebook *Pre-processing.ipynb*.
- **notebooks_source**: Contém os dados obtidos no painel da COVID-19. Ao baixar o arquivo no painel da COVID-19, coloque-o nessa pasta e, em seguida, altere o notebook *Pre-processing.ipynb* para que o notebook aponte para o nome correto do arquivo baixado.
- **Procfile**: Possui o código utilizado pelo Heroku para servir o dashboard.
- **requirements.txt**: Contém as dependências do projeto.
