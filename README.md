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
- **data_source**: Contém os dados que foram coletados do IBGE e pré-processados. Esses dados são utilizados para gerar bases de dados enriquecidas, através da integração com a base de dados do [painel da COVID-19](https://coronavirus.es.gov.br/painel-covid-19-es).
- **notebooks**: Contém os notebooks responsáveis por realizar o pré-processamento dos dados e para gerar um "rascunho" das visualizações contidas no Dashboard.
- **notebooks_output**: Contém o resultado do pré-processamento realizado no notebook *Pre-processing.ipynb*.
- **notebooks_source**: Contém os dados obtidos no painel da COVID-19. Ao baixar o arquivo no painel da COVID-19, coloque-o nessa pasta e, em seguida, altere o notebook *Pre-processing.ipynb* para que o notebook aponte para o nome correto do arquivo baixado.
- **Procfile**: Possui o código utilizado pelo Heroku para servir o dashboard.
- **requirements.txt**: Contém as dependências do projeto.

## Baixando e Executando Localmente

O projeto foi totalmente desenvolvido utilizando o sistema operacional Linux Ubuntu 20.04.1 LTS. Portanto, alguns comandos aplicados ao terminal, devem ser substituídos por seus equivalentes, de acordo com o sistema operacional utilizado.

### Pré-Requisitos

- Python 3.8.5
- Pip

### Preparando o Ambiente

Execute o passo-a-passo abaixo, sem utilizar o trecho "$: ". Esse trecho apenas indica que trata-se de um novo comando a ser executado.

1. Clone o repositório do projeto e entre na pasta, usando os seguintes comandos:

```
$: git clone https://github.com/DaniloSI/covid-19_es.git
$: cd covid-19_es
```
2. Instale o **virtualenv**, caso não o tenha instalado, utilizando o seguinte comando:

```
$: apt-get update
$: apt-get install python3-virtualenv
```

3. Crie e ative um ambiente virtual com os seguintes comandos:

```
$: python3 -m venv venv/
$: source venv/bin/activate
```

4. Instale as dependências com o seguinte comando:

```
$: pip3 install -r requirements.txt
```

### Executando Localmente

1. Acesse a pasta dash com o seguinte comando:

```
$: cd dash
```

2. Coloque o dash em execução através do seguinte comando:

```
$: python3 app.py
```

Após executar localmente, será possível acessar o dashboard através do da url **localhost:8050**.
> Obs.: O dash disponibiliza na porta 8050 como padrão, mas pode utilizar outra porta, caso esta esteja em uso.