from dash.dependencies import Input, Output
from plotly.offline import plot, iplot, init_notebook_mode
import cufflinks
import dash
import dash_core_components as dcc
import dash_html_components as html
import os, sys
import pandas as pd
import urllib
cufflinks.go_offline()
cufflinks.set_config_file(world_readable=True, theme='white')

sys.path.append('app/')
from setup import input_path
from figures import fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10

def setup_app(url):
    results_path = input_path(url)

    all_params = {}
    df_y_min = 9999
    df_y_max = 0

    for each_file in os.listdir(results_path):
        df_param = pd.read_csv(os.path.join(results_path, each_file))
        param_name = df_param.columns[-1]
        df_param.rename(columns={param_name:'value'}, inplace=True)
        all_params[param_name] = pd.DataFrame(df_param)
        if 'y' in df_param.columns:
            if df_y_min > df_param.y.min():
                df_y_min = df_param.y.min()
            if df_y_max < df_param.y.max():
                df_y_max = df_param.y.max()

    years = pd.Series(list(range(df_y_min,df_y_max)))

    return [
        fig1(all_params,years),
        fig2(all_params,years),
        fig3(all_params,years),
        fig4(all_params,years),
        fig5(all_params,years),
        fig6(all_params,years),
        fig7(all_params,years),
        fig8(all_params,years),
        fig9(all_params,years),
        fig10(all_params,years),
    ]

##################################################################################################
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

def div_from_figure(figure, number):
    return html.Div(
            children=dcc.Graph(
                id=f'example-graph-{number}',
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
def generate_figures(url):
    all_figures = setup_app(url)
    figure_divs = []
    for number, figure in enumerate(all_figures):
        figure_divs = figure_divs + [div_from_figure(figure, number)]
    return figure_divs

if __name__ == '__main__':
    app.run_server(debug=False)
