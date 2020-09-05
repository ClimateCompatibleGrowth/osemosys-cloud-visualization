import dash_core_components as dcc


class Checkboxes:
    def __init__(self, ids, category):
        self.ids = ids
        self.category = category

    def to_component(self):
        return dcc.Checklist(
                options=[
                    {'label': id.replace('-', ' ').title(), 'value': id} for id in self.ids
                    ],
                value=self.ids,
                id={'type': 'checkboxes', 'index': self.category},
                persistence=True,
                className='form-check checkbox-container',
                inputClassName='form-check-input custom-checkbox',
                labelClassName='form-check-label'
                )
