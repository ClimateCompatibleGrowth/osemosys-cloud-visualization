import dash_html_components as html
import i18n


class Header:
    def __init__(self, config):
        self.config = config

    def contents(self):
        return [
            html.H1(self.config.title()),
            html.Div([i18n.t(
                'layout.run_info',
                run=self.config.title(),
                version=self.config.version_name(),
                model=self.config.model_name())
            ], className='subtitle'),
            html.Div([self.config.description()], className='subtitle'),
        ]
