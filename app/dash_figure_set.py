from dash import dcc
from dash import html
from app.utilities import df_plot
import functools
import time
import traceback


class DashFigureSet:
    def __init__(self, *, figures, category, id, name):
        self.figures = figures
        self.category = category
        self.id = id
        self.name = name

    @functools.lru_cache()
    def to_div(self):
        start = time.time()
        if self.is_empty():
            return []
        else:
            content = self.__content()
            end = time.time()
            print(f'Generated {self.name} in {round(end - start, 2)}s')
            return(
                    html.Div(
                        [
                            html.H4(self.name),
                            content
                            ],
                        className=f'figure-set figure-set-{self.id}',
                        )
                    )

    def __content(self):
        try:
            return html.Div(
                [
                    html.Div(dcc.Graph(figure=iplot.figure()), className='figure')
                    for iplot in self.figures
                ] + self.__diff(),
                className='figures-in-set-container'
            )
        except Exception as e:
            return html.Div([
                    html.Pre(traceback.format_exc(), className='card-body'),
                ],
                className=f'figure figure-error card'
            )

    def __diff(self):
        if len(self.figures) == 2:
            figure_0 = self.figures[0]
            figure_1 = self.figures[1]

            index_column = figure_0.index_column
            plot = figure_0.plot

            data0 = figure_0.data().set_index(index_column)
            data1 = figure_1.data().set_index(index_column)

            diff = data1 - data0
            diff[index_column] = diff.index
            diff = diff.fillna(0)

            return [
                    html.Div(
                        dcc.Graph(figure=plot(
                            diff,
                            f'Delta ({figure_1.plot_title} - {figure_0.plot_title})'
                        )),
                        className='figure')
                    ]
        else:
            return []

    def is_empty(self):
        try:
            return self.figures[0].data().columns.size == 1
        except Exception as e:  # Surface exceptions occurring during the check
            return False
