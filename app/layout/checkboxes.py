import dash_core_components as dcc
import dash_html_components as html
import i18n
import re


class Checkboxes:
    def __init__(self, ids, category):
        self.ids = ids
        self.category = category

    def to_component(self):
        return html.Div([
            html.A(
                'Select/Deselect all',
                id={'type': 'select-all', 'index': self.category},
                className='btn btn-light d-block btn-lg',
            ),
            dcc.Checklist(
                    options=[
                        {'label': self.id_to_label(id), 'value': id} for id in self.ids
                        ],
                    value=self.ids,
                    id={'type': 'checkboxes', 'index': self.category},
                    persistence=True,
                    className='form-check checkbox-container',
                    inputClassName='form-check-input custom-checkbox',
                    labelClassName='form-check-label'
                ),
            ])

    def id_to_label(self, id):
        region_regex = re.compile('^(.+)_i18n_(.+)$')
        match = region_regex.match(id)
        if match is None:
            return i18n.t(f'figure.{id}')
        else:
            i18n_figure_key = match.group(1)
            region = match.group(2)
            return i18n.t(f'figure.{i18n_figure_key}', region=region)
