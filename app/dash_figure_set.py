import dash_core_components as dcc
import dash_html_components as html
import functools
import traceback


class DashFigureSet:
    def __init__(self, *, figures, category, id, name):
        self.figures = figures
        self.category = category
        self.id = id
        self.name = name

    @functools.lru_cache(maxsize=128)
    def to_div(self):
        print(f'Generating {self.name}')
        return html.Div(
                    [
                        html.H4(self.name),
                        self.__content()
                    ],
                    className=f'figure-set figure-set-{self.id}',
                )

    def __content(self):
        try:
            return html.Div(
                [
                    html.Div(dcc.Graph(figure=iplot.figure()), className='figure')
                    for iplot in self.figures
                ],
                className='figures-in-set-container'
            )
        except Exception as e:
            return html.Div([
                    html.Pre(traceback.format_exc(), className='card-body'),
                ],
                className=f'figure figure-error card'
            )
