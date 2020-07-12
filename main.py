from dash.dependencies import Input, Output, State
import cufflinks
import dash
import dash_core_components as dcc
import dash_html_components as html
import sys
import urllib
from app.config import Config
from app.generate_figures import generate_figures  # noqa
cufflinks.go_offline()
cufflinks.set_config_file(world_readable=True, theme='white')

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url'),
    html.H1('CLEWS Dashboard'),
    html.Div('An interactive tool to visualise CLEWS model results', className='subtitle'),
    dcc.Input(id='input-string', type='text'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    dcc.Loading(html.Div(id='figures-container')),
])


def div_from_figure(figure):
    return html.Div(dcc.Graph(figure=figure), className='figure')


@app.callback(
    Output(component_id='input-string', component_property='value'),
    [Input(component_id='url', component_property='search')]
    )
def populate_input_string_from_query_string(query_string):
    return urllib.parse.unquote(query_string).split('=')[-1]


@app.callback(
    Output(component_id='figures-container', component_property='children'),
    [Input(component_id='submit-button', component_property='n_clicks')],
    [State('input-string', 'value')]
    )
def generate_figure_divs(n_clicks, query_string):
    if query_string is None:
        return []
    model_name = urllib.parse.unquote(query_string).split('=')[-1]
    config = Config(model_name)
    all_figures = generate_figures(config)  # We lost the `url` capability
    return [div_from_figure(figure) for figure in all_figures]


if __name__ == '__main__':
    app.run_server(debug=False)
