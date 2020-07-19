from dash.dependencies import Input, Output, State
import cufflinks
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import random
import sys
import urllib
import zipfile
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
    html.Div([
            dcc.Input(id='input-string', type='text', className='input-field'),
            html.Button(id='submit-button', n_clicks=0, children='Submit'),
        ],
        className='source-form'
    ),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            html.Button(children='Upload files'),
        ]),
        className='upload-zone',
    ),

    dcc.Loading(
        [
            html.Div(id='figures-container'),
            html.Div(id='output-data-upload'),
        ],
        fullscreen=True
    ),
])


def div_from_figure(figure):
    return html.Div(dcc.Graph(figure=figure), className='figure')


@app.callback(
    Output(component_id='input-string', component_property='value'),
    [Input(component_id='url', component_property='search')]
    )
def populate_input_string_from_query_string(query_string):
    return parse_query_string(query_string)


@app.callback(
    Output(component_id='figures-container', component_property='children'),
    [
        Input(component_id='submit-button', component_property='n_clicks'),
        Input(component_id='input-string', component_property='n_submit'),
        Input(component_id='url', component_property='search')
    ],
    [State('input-string', 'value')]
    )
def generate_figure_divs(n_clicks, n_submit, raw_query_string, query_string):
    if query_string is None and raw_query_string is None:
        return []
    if query_string is None and raw_query_string is not None:  # First initialization
        query_string = parse_query_string(raw_query_string)
    config = Config(query_string)
    all_figures = generate_figures(config)
    return [div_from_figure(figure) for figure in all_figures]


def parse_query_string(query_string):
    return urllib.parse.parse_qs(
            urllib.parse.unquote(query_string)
           )['?model'][0]


@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    )
def update_output(uploaded_file):
    if uploaded_file is not None:
        return process_uploaded_file(uploaded_file)


def process_uploaded_file(raw_contents):
    random_number = random.randint(1, 99999)
    uploaded_folder_path = os.path.join(os.getcwd(), 'tmp', 'uploaded', str(random_number))
    try:
        os.makedirs(uploaded_folder_path)
    except FileExistsError:
        pass
    content_type, content_string = raw_contents.split(',')

    write_and_extract_zip_file(content_string, uploaded_folder_path)

    config = Config(uploaded_folder_path)
    all_figures = generate_figures(config)
    return [div_from_figure(figure) for figure in all_figures]


def write_and_extract_zip_file(base64_encoded_zip, work_path):
    zip_file_path = os.path.join(work_path, 'uploaded.zip')

    with open(zip_file_path, 'wb') as fh:
        fh.write(base64.b64decode(base64_encoded_zip))

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(work_path)


if __name__ == '__main__':
    if 'DASH_DEBUG' in os.environ:
        app.run_server(debug=True)
    else:
        app.run_server(debug=False)
