import dash_core_components as dcc
import dash_html_components as html
import functools
import traceback


class DashFigure:
    def __init__(self, *, iplots, category, id, name):
        self.iplots = iplots
        self.category = category
        self.id = id
        self.name = name

    @functools.lru_cache(maxsize=128)
    def to_div(self):
        print(f'Generating {self.name}')
        try:
            return html.Div(
                        [
                            html.H4(self.name),
                            html.Div([dcc.Graph(figure=iplot.figure()) for iplot in self.iplots])
                        ],
                        className=f'figure figure-{self.id}',
                    )
        except Exception as e:
            return html.Div([
                    html.Pre(traceback.format_exc(), className='card-body'),
                ],
                className=f'figure-error card figure-{self.id}'
            )
