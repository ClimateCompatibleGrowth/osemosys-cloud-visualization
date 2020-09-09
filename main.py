from dash.dependencies import Input, Output, State, ClientsideFunction, ALL
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
from app.cache import cache
from app.config import Config
from app.header import Header
from app.generate_divs import GenerateDivs

cufflinks.go_offline()
cufflinks.set_config_file(world_readable=True, theme='white')

external_scripts = [
        {
            'src': 'https://code.jquery.com/jquery-3.5.1.slim.min.js',
            'integrity': 'sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj',
            'crossorigin': 'anonymous'
        },
        {
            'src': 'https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js',
            'integrity': 'sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo',
            'crossorigin': 'anonymous'
        },
        {
            'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js',
            'integrity': 'sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI',
            'crossorigin': 'anonymous'
        }
    ]

external_stylesheets = [
        {
            'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css',
            'rel': 'stylesheet',
            'integrity': 'sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk',
            'crossorigin': 'anonymous'
        }
    ]

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

server = app.server
cache.init_app(server, config={'CACHE_TYPE': 'filesystem','CACHE_DIR': 'cache'})

app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div([], id='header'),
    html.Div([
            html.Label('Model:', htmlFor='input-string'),
            dcc.Input(id='input-string', type='text', className='input-field mb-3'),
            html.Label('Compare to:', htmlFor='compare-to-1'),
            dcc.Input(id='compare-to-1', type='text', className='input-field mb-1'),
            dcc.Input(id='compare-to-2', type='text', className='input-field mb-1'),
            html.Br(),
            html.Button(id='submit-button', n_clicks=0, children='Submit'),
        ],
        className='source-form'
    ),
    html.Hr(),
    dcc.Upload(
        id='upload-data',
        children=html.Div(html.Button('Or upload zip file')),
        className='upload-zone',
    ),
    html.Nav([
        html.A(
                'All',
                className='nav-item nav-link active',
                id='nav-all-tab',
                href='#nav-all',
                role='tab',
                **{'data-toggle': 'tab'},
                ),
        html.A(
                'Climate',
                className='nav-item nav-link',
                id='nav-climate-tab',
                href='#nav-climate',
                role='tab',
                **{'data-toggle': 'tab'},
            ),
        html.A(
                'Land',
                className='nav-item nav-link',
                id='nav-land-tab',
                href='#nav-land',
                role='tab',
                **{'data-toggle': 'tab'},
                ),
        html.A(
                'Energy',
                className='nav-item nav-link',
                id='nav-energy-tab',
                href='#nav-energy',
                role='tab',
                **{'data-toggle': 'tab'},
                ),
        html.A(
                'Water',
                className='nav-item nav-link',
                id='nav-water-tab',
                href='#nav-water',
                role='tab',
                **{'data-toggle': 'tab'},
                ),
    ], className='nav nav-tabs justify-content-center', id='categoryTab', role='tablist'),
    dcc.Loading(html.Div([
            html.Div([], className='tab-pane show active', id='nav-all', role='tabpanel'),
            html.Div([], className='tab-pane show', id='nav-climate', role='tabpanel'),
            html.Div([], className='tab-pane show', id='nav-land', role='tabpanel'),
            html.Div([], className='tab-pane show', id='nav-energy', role='tabpanel'),
            html.Div([], className='tab-pane show', id='nav-water', role='tabpanel'),
        ], id='categoryTabContent', className='tab-content'), fullscreen=True),
])


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='testFunction'
    ),
    Output(component_id='categoryTabContent', component_property='data-checked-boxes'),
    [Input({'type': 'checkboxes', 'index': ALL}, 'value')],
    [State({'type': 'checkboxes', 'index': ALL}, 'options')],
)


@app.callback(
    Output(component_id='input-string', component_property='value'),
    [Input(component_id='url', component_property='search')]
    )
def populate_input_string_from_query_string(query_string):
    if query_string is not None:
        print(f'populating query_string {query_string}')
        return parse_query_string(query_string)
    else:
        return ''


@app.callback(
    Output(component_id='header', component_property='children'),
    [
        Input(component_id='submit-button', component_property='n_clicks'),
        Input(component_id='input-string', component_property='n_submit'),
        Input(component_id='url', component_property='search'),
        Input(component_id='upload-data', component_property='contents'),
    ],
    [State('input-string', 'value')]
    )
def generate_header(n_clicks, n_submit, raw_query_string, upload_data, input_string):
    triggered_element = dash.callback_context.triggered[0]['prop_id']
    config_input = config_input_from(input_string, raw_query_string, triggered_element)
    config = Config(config_input)
    return Header(config).contents()


@app.callback(
    [
        Output(component_id='nav-all', component_property='children'),
        Output(component_id='nav-climate', component_property='children'),
        Output(component_id='nav-land', component_property='children'),
        Output(component_id='nav-energy', component_property='children'),
        Output(component_id='nav-water', component_property='children'),
    ],
    [
        Input(component_id='submit-button', component_property='n_clicks'),
        Input(component_id='input-string', component_property='n_submit'),
        Input(component_id='url', component_property='search'),
        Input(component_id='upload-data', component_property='contents'),
    ],
    [
        State('input-string', 'value'),
        State('compare-to-1', 'value'),
        State('compare-to-2', 'value'),
    ]
    )
def generate_figure_divs(
        n_clicks, n_submit, raw_query_string, upload_data,
        input_string, compare_to_1, compare_to_2
        ):
    triggered_element = dash.callback_context.triggered[0]['prop_id']
    main_config_input = config_input_from(input_string, raw_query_string, triggered_element)
    configs = [
            Config(config_input) for config_input in [main_config_input, compare_to_1, compare_to_2]
    ]
    valid_configs = [config for config in configs if config.is_valid()]
    if len(valid_configs) > 0:
        return generate_divs(valid_configs)
    else:
        return [f'Invalid models: {[config.input_string for config in configs]}']


# @cache.memoize(timeout=86400)  # 1 Day
def generate_divs(configs):
    return GenerateDivs(configs).generate_divs()


def config_input_from(input_string, raw_query_string, triggered_element=''):
    config_input = input_string

    if input_string is None and raw_query_string is None:
        return ''

    if input_string is None and raw_query_string is not None:  # First initialization
        config_input = parse_query_string(raw_query_string)

    if triggered_element in ['upload-data.contents']:
        config_input = process_uploaded_file(upload_data)

    return config_input


def parse_query_string(query_string):
    parsed_qs = urllib.parse.parse_qs(
        urllib.parse.unquote(query_string)
    )
    return parsed_qs.get('?model', [''])[0]


def process_uploaded_file(raw_contents):
    random_number = random.randint(1, 99999)
    uploaded_folder_path = os.path.join(os.getcwd(), 'tmp', 'uploaded', str(random_number))
    try:
        os.makedirs(uploaded_folder_path)
    except FileExistsError:
        pass
    content_type, content_string = raw_contents.split(',')

    write_and_extract_zip_file(content_string, uploaded_folder_path)

    return uploaded_folder_path


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
