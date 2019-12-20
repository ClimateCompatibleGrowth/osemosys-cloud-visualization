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
from setup import download_files
from utilities import df_plot, df_filter
from calculations import calculate_cap_df, calculate_gen_df, calculate_gen_use_df, calculate_cap_cos_df, calculate_ene_imp_df, calculate_ene_exp_df, calculate_dom_prd_df
from figures import fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10

def setup_app(url):
    all_figures = {}

    results_path = download_files(url)

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

    all_figures['fig1'] = fig1(all_params,years)
    all_figures['fig2'] = fig2(all_params,years)
    all_figures['fig3'] = fig3(all_params,years)
    all_figures['fig4'] = fig4(all_params,years)
    all_figures['fig5'] = fig5(all_params,years)
    all_figures['fig6'] = fig6(all_params,years)
    all_figures['fig7'] = fig7(all_params,years)
    all_figures['fig8'] = fig8(all_params,years)
    all_figures['fig9'] = fig9(all_params,years)
    all_figures['fig10'] = fig10(all_params,years)

    return all_figures

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
    for number, figure in all_figures.items():
        figure_divs = figure_divs + [div_from_figure(figure, number)]
    return figure_divs

if __name__ == '__main__':
    app.run_server(debug=False)
