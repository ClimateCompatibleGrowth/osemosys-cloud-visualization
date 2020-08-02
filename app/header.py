import dash_html_components as html


class Header:
    def __init__(self, config):
        self.config = config

    def contents(self):
        return [
            html.H1(self.config.title()),
            html.Div([self.config.description()], className='subtitle'),
        ]
