<div align="center">
  <h1>COVID-19 no Espírito Santo</h1>
</div>

<div align="center">
  <!-- Pre-processing Status -->
  <a href="https://github.com/DaniloSI/covid-19_es/actions/workflows/ETL-Covid.yml">
    <img src="https://github.com/DaniloSI/covid-19_es/actions/workflows/ETL-Covid.yml/badge.svg?event=schedule" alt="Pre-processing" />
  </a>
  <br />
  <br />
</div>

O presente projeto foi desenvolvido como parte de um TCC, para a obtenção do grau de Bacharelado em Sistemas de Informação, no Ifes Campus Serra.

- Aluno: Danilo de Oliveira
- Orientador: Moisés Savedra Omena

## Sumário

- [Visão Geral](https://github.com/DaniloSI/covid-19_es#vis%C3%A3o-geral)
- [Estrutura do Projeto](https://github.com/DaniloSI/covid-19_es#estrutura-do-projeto)
- [Baixando o Projeto e Executando o Dash Localmente](https://github.com/DaniloSI/covid-19_es#baixando-o-projeto-e-executando-o-dash-localmente)
  - [Pré-Requisitos](https://github.com/DaniloSI/covid-19_es#pr%C3%A9-requisitos)
  - [Preparando o Ambiente](https://github.com/DaniloSI/covid-19_es#preparando-o-ambiente)
  - [Executando o Dash Localmente](https://github.com/DaniloSI/covid-19_es#executando-o-dash-localmente)

## Visão Geral

O diagrama abaixo apresenta uma visão geral de todo o projeto.

![Imgur](https://i.imgur.com/9cPmLdE.png)

## Diagrama de Componentes do Dashboard

O diagrama abaixo apresenta a organização dos componentes do Dashboard, utilizando o framework Dash.

![Imgur](https://i.imgur.com/jFRgsUk.png)

## Estrutura de Pastas do Projeto

O diagrama abaixo apresenta a organização de pastas do projeto.

```
.
├── dash
│   ├── app.py
│   ├── assets
│   │   ├── img
│   │   │   └── GitHub-Mark-32px.png
│   │   └── page.css
│   └── components
│       ├── dao
│       │   ├── covid_dao.py
│       │   ├── dao.py
│       │   └── municipio_dao.py
│       ├── dashboard.py
│       ├── database.py
│       ├── filtros
│       │   └── Select.py
│       ├── graficos
│       │   ├── Evolucao.py
│       │   ├── Indicator.py
│       │   ├── Scatter.py
│       │   └── Treemap.py
│       ├── mapas
│       │   └── Choropleth.py
│       ├── navbar.py
│       ├── observer.py
│       └── util.py
├── LICENSE
├── notebooks
│   ├── Análise Exploratória de Dados.ipynb
│   ├── Data-visualizations.ipynb
│   ├── ETL-Indicadores-Municipais.ipynb
│   ├── Gráfico de Casos no Brasil e no Espírito Santo.ipynb
│   └── Pre-processing.ipynb
├── preprocessing.py
├── Procfile
├── README.md
├── requirements.txt
└── runtime.txt
```

## Baixando o Projeto e Executando o Dash Localmente

O projeto foi totalmente desenvolvido utilizando o sistema operacional Linux Ubuntu 20.04.1 LTS. Portanto, alguns comandos aplicados ao terminal, devem ser substituídos por seus equivalentes, de acordo com o sistema operacional utilizado.

### Pré-Requisitos

Para executar o projeto localmente, é preciso que os seguintes itens estejam instalados em sua máquina:

- Git
- Python 3.8.5
- Pip

### Preparando o Ambiente

1. Clone o repositório do projeto e entre na pasta, usando os seguintes comandos:

```
git clone https://github.com/DaniloSI/covid-19_es.git
```

```
cd covid-19_es
```

2. Instale o **virtualenv**, caso não o tenha instalado, utilizando os seguintes comandos:

```
sudo apt-get update
```

```
sudo apt-get install python3-virtualenv
```

3. Crie e ative um ambiente virtual com os seguintes comandos:

```
python3 -m venv venv/
```

```
source venv/bin/activate
```

4. Instale as dependências do projeto com o seguinte comando:

```
pip3 install -r requirements.txt
```

### Executando o Dash Localmente

1. Acesse a pasta dash com o seguinte comando:

```
cd dash
```

2. Coloque o dash em execução através do seguinte comando:

```
python3 app.py
```

Após executar localmente, será possível acessar o dashboard através da url **localhost:8050**.

> Obs.: O dash disponibiliza na porta 8050 como padrão, mas pode utilizar outra porta, caso esta esteja em uso.
