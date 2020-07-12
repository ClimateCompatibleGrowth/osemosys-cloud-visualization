from dash.dependencies import Input, Output
import cufflinks
import dash
import dash_core_components as dcc
import dash_html_components as html
import sys
import urllib
from app.generate_figures import generate_figures  # noqa
cufflinks.go_offline()
cufflinks.set_config_file(world_readable=True, theme='white')

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url'),
    html.H1('CLEWS Dashboard'),
    html.Div('An interactive tool to visualise CLEWS model results', className='subtitle'),
    dcc.Loading(html.Div(id='figures-container')),
])


def div_from_figure(figure):
    return html.Div(dcc.Graph(figure=figure), className='figure')


@app.callback(
    Output(component_id='figures-container', component_property='children'),
    [Input(component_id='url', component_property='search')]
    )
def generate_figure_divs(query_string):
    model_name = urllib.parse.unquote(query_string).split('=')[-1]
    all_figures = generate_figures(model_name)  # We lost the `url` capability
    return [div_from_figure(figure) for figure in all_figures]


if __name__ == '__main__':
    app.run_server(debug=False)
