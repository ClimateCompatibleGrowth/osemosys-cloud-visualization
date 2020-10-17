import dash_html_components as html


class Header:
    def __init__(self, config):
        self.config = config

    def contents(self):
        return [
            html.H1(self.config.title()),
            html.Div([
                "Run: "
                + self.config.title()
                + ', Version: '
                + self.config.version_name()
                + ', Model: '
                + self.config.model_name()
            ], className='subtitle'),
            html.Div([self.config.description()], className='subtitle'),
        ]
