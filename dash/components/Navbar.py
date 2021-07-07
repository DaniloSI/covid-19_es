import dash_bootstrap_components as dbc
import dash_html_components as html
from datetime import datetime, timedelta
import urllib
import json

def last_update():
    url = 'https://api.github.com/repos/danilosi/covid-19_es/actions/runs?page=0&per_page=1&status=success'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    datetime_utc = data['workflow_runs'][0]['updated_at']

    data_ultima_atualizacao = (datetime.fromisoformat(
        datetime_utc.replace('Z', '')) - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M')

    return data_ultima_atualizacao

make_nav_item = lambda children: dbc.NavItem(html.Div(
    children,
    style={'display': 'flex', 'height': '100%', 'alignItems': 'center'})
)

def navbar():
    return dbc.NavbarSimple(
        [
            make_nav_item(
                [
                    html.I(
                        '',
                        className="ti ti-info-circle",
                        style={'fontSize': 24, 'paddingRight': '.5rem', 'paddingLeft': '.5rem', 'color': '#7f7f7f'},
                        id="info-last-update",
                    ),
                    dbc.Tooltip(
                        f'Dados atualizados pela última vez em {last_update()}',
                        target='info-last-update',
                        placement='bottom'
                    )
                ]
            ),
            make_nav_item(
                dbc.NavLink(
                    html.I(
                        '',
                        className=f'ti ti-brand-github',
                        style={'fontSize': 24},
                    ),
                    href="https://github.com/DaniloSI/covid-19_es",
                    target="_blank",
                    external_link=True,
                    style={'display': 'flex'}
                )
            )
        ],
        brand="Covid-19 | Espírito Santo, Brasil",
        color="#e5e5e5",
        fluid=True,
        style={'borderRadius': 5, 'marginBottom': 20}
    )