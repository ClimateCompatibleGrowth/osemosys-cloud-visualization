import dash_core_components as dcc
import dash_html_components as html


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
                        {'label': id.replace('-', ' ').title(), 'value': id} for id in self.ids
                        ],
                    value=self.ids,
                    id={'type': 'checkboxes', 'index': self.category},
                    persistence=True,
                    className='form-check checkbox-container',
                    inputClassName='form-check-input custom-checkbox',
                    labelClassName='form-check-label'
                ),
            ])
