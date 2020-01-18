from dash.dependencies import Input, Output
from plotly.offline import plot, iplot, init_notebook_mode
import cufflinks
import dash
import dash_core_components as dcc
import dash_html_components as html
import sys
import urllib
cufflinks.go_offline()
cufflinks.set_config_file(world_readable=True, theme='white')

sys.path.append('app/')
from generate_figures import generate_figures

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.Div('', **{'id': 'figures-component', 'data-url': ''}),
    dcc.Location(id='url', refresh=False),
    html.H1(
        'CLEWS Dashboard',
        style={
            'textAlign':'center'
        }
    ),

    html.Div(children='An interactive tool to visualise CLEWS model results', style={
        'textAlign':'center'
    }
    ),
    html.Div(children=[], id='figures-container'),
])

def div_from_figure(figure):
    return html.Div(
            children=dcc.Graph(
                figure=figure
                ), 
            style={'width':'50%','display':'inline-block'}
            )

@app.callback(
    Output(component_id='figures-component', component_property='data-url'),
    [Input(component_id='url', component_property='search')]
    )
def setup_url(query_string):
    return urllib.parse.unquote(query_string).split('=')[-1]

@app.callback(
    Output(component_id='figures-container', component_property='children'),
    [Input(component_id='figures-component', component_property='data-url')]
    )
def generate_figure_divs(url):
    all_figures = generate_figures(url)
    return [div_from_figure(figure) for figure in all_figures] 

if __name__ == '__main__':
    app.run_server(debug=False)
